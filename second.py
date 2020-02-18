import pika
import requests
from bs4 import BeautifulSoup
import sys
import dpath.util


def Add_to_main_tree(new_dict, keylist, splited, depth):
    global tree
    x = ''
    if len(keylist) == 0:
        if '\'' not in splited[0]:
            dpath.util.new(tree, splited[0], new_dict[splited[0]])


    else:
        for n in range(len(keylist)):
            x = keylist[n] + "/"
        dpath.util.new(tree, x + splited[depth], new_dict[splited[depth]])
    print(tree)


def is_in_tree(url):
    url.replace(" ", "")
    splited = url.split('/')
    global tree
    temp_dict = tree
    for i in range(len(splited)):
        if (splited[i] in temp_dict.keys()):
            if (i == len(splited) - 1):
                return 1
            temp_dict = temp_dict[splited[i]]
            continue

        else:
            depth = i
            new_dict = {}
            for j in range(len(splited) - 1, i - 1, -1):
                temp = new_dict
                new_dict = {}
                new_dict[splited[j]] = temp
            Add_to_main_tree(new_dict, splited[:depth], splited, depth)
            return 0


def callback(ch, method, properties, body):
    print(tree.keys())
    global count
    response = session.get('http://www.' + body.decode("utf-8"))
    global requests
    requests += 1
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)
    for el in links:
        try:
            url = el['href'].__str__()
        except:
            return
            sys.exit()
        if ((url == '') or ('#' not in url)):
            continue
        url = url.replace(' ', '')
        url = url.replace('www.', '')
        url = url.replace('https:', '')
        url = url.replace('http:', '')
        url = url.replace('//', '')
        if (('#' in url) and ('/' not in url)):
            url = body.decode('utf-8') + '/' + url
        in_tree = is_in_tree(url)
        if (in_tree == 0):
            count += 1
            channel.basic_publish(exchange='', routing_key='htmlResponse', body=url)
            print(count.__str__() + '\' th unique url')
        print(requests.__str__() + '\' th request')


session = requests.Session()
session.headers.update({
                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'})
count = 1
requests = 0
tree = {}

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='htmlResponse')
channel.basic_consume(
    queue='htmlResponse', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
