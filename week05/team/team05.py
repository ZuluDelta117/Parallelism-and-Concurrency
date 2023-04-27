"""
Course: CSE 251
Lesson Week: 05
File: team05.py
Author: Brother Comeau (modified by Brother Foushee)

Purpose: Team Activity

Instructions:

- See in Canvas

"""

import threading
import queue
import time
import requests
import json

RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

class Queue251():

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)

class url_putter(threading.Thread):
    def __init__(self,
                grabber_index,
                sem_queue_full: threading.Semaphore,
                sem_can_pull: threading.Semaphore,
                url_queue,
                queue_lock,
                url_list):

        threading.Thread.__init__(self)
        self.grabber_index = grabber_index
        self.sem_queue_full = sem_queue_full
        self.sem_can_pull = sem_can_pull
        self.url_queue = url_queue
        self.queue_lock = queue_lock
        self.url_list = url_list


    def run(self):
        for url in self.url_list:
            self.sem_queue_full.acquire()

            with self.queue_lock:
                self.url_queue.put(url)
                self.sem_can_pull.release()
            self.sem_can_pull.release()

            self.sem_queue_full.acquire()
            # for _ in range(RETRIEVE_THREADS):
            self.url_queue.put(NO_MORE_VALUES)
            self.sem_can_pull.release()

class url_taker(threading.Thread):
    def __init__(self,
                taker_index,
                sem_queue_full: threading.Semaphore,
                sem_can_pull: threading.Semaphore,
                url_queue,
                queue_lock,
                barrier: threading.Barrier):

        threading.Thread.__init__(self)
        self.taker_index = taker_index
        self.sem_queue_full = sem_queue_full
        self.sem_can_pull = sem_can_pull
        self.url_queue = url_queue
        self.queue_lock = queue_lock
        self.barrier = barrier


    def run(self):
        while True:
            self.sem_can_pull.acquire()

            with self.queue_lock:
                url = self.url_queue.get()

            if url == NO_MORE_VALUES:
                break

            rq = requests.get(url)
            json_request = rq.json()
            with self.queue_lock:
                print(f"{json_request['name']}\n")
            self.sem_queue_full.release()

        self.barrier.wait()







    



# def retrieve_thread():  # TODO add arguments
#     """ Process values from the data_queue """

#     while True:
#         # TODO check to see if anything is in the queue

#         # TODO process the value retrieved from the queue

#         # TODO make Internet call to get characters name and print it out
#         pass



# def file_reader(file, data_queue): # TODO add arguments
#     """ This thread reading the data file and places the values in the data_queue """

#     # TODO Open the data file "urls.txt" and place items into a queue


#     # TODO signal the retrieve threads one more time that there are "no more values"



def main():
    """ Main function """

    # Start a timer
    begin_time = time.perf_counter()

    url_list = []
    with open('urls.txt', 'r') as f:
        for line in f:
            url_list.append(line.strip())
    
    # TODO create queue (if you use the queue module, then you won't need semaphores/locks)
    sem_queue_full = threading.Semaphore(len(url_list))
    sem_can_pull = threading.Semaphore(0)

    url_queue = Queue251()

    queue_lock = threading.Lock()
    barrier = threading.Barrier(RETRIEVE_THREADS)

    feeder_thread = url_putter(1, sem_queue_full, sem_can_pull, url_queue, queue_lock, url_list)

    takers = []

    for taker_index in range(RETRIEVE_THREADS):
        takers.append(url_taker(taker_index, sem_queue_full, sem_can_pull, url_queue, queue_lock, barrier))
    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread needed to do their jobs

    # TODO Get them going

    feeder_thread.start()
    
    for thread in takers:
        thread.start()
        
    feeder_thread.join()
    
    for thread in takers:
        thread.join()

    # TODO Wait for them to finish

    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time to process all URLS = {total_time} sec')


if __name__ == '__main__':
    main()




