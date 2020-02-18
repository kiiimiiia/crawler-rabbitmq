import pika
from threading import Thread as thread
import time


from classes.myThread import myThread
def printing():
    print("hi hi hi")


def thread_for_getting_new_url():
    # reader_thread = myThread(1, "file_reader_thread", 1)
    # reader_thread.start()
    # try:
    #     thread.start(printing, ('reader-thread', 1 ,))
    # except:
    #     print("unable to run thread :" + 'reader-thread')
    try:
        reader_thread = myThread(1, "Thread-1", 1)
        reader_thread.run()
    except:
        print("unable to run " + myThread.name.__str__())


def main():
    thread_for_getting_new_url()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='htmlResponse')

    # print(" [x] Sent 'Hello World!'")
    channel.basic_publish(exchange='', routing_key='htmlResponse', body='geeksforgeeks.org')
    connection.close()


if __name__ == '__main__':
    main()
