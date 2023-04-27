"""
Course: CSE 251
Lesson Week: 10
File: Assignment.py
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5


# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'


def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id):
    print(f'Guest {id}')
    time.sleep(random.uniform(0, 1))

def cleaner(lock_guest, lock_cleaner, clean_count):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    while True:
        with lock_guest:
            cleaner = []
            id = list(range(1, CLEANING_STAFF + 1))
            for i in id:
                lock_cleaner.acquire()
                print(STARTING_CLEANING_MESSAGE)
                # Add to total number of cleaners
                clean_count.value += 1
                cleaner_cleaning(i)
                print(STOPPING_CLEANING_MESSAGE)
                lock_cleaner.release()
                cleaner.append(i)

            if len(cleaner) == CLEANING_STAFF:
                # Clear cleaning list
                cleaner.clear()
                break
            # Have cleaners wait so a party can start
            cleaner_waiting()

def guest(lock_guest, lock_cleaner, party_count):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    partying = True
    while partying:
        with lock_guest:
            guest = []
            id = list(range(1, HOTEL_GUESTS + 1))
            lock_cleaner.acquire()
            print(STARTING_PARTY_MESSAGE)
            
            for i in id:
                guest_partying(i)
                guest.append(i)

            if len(guest) == HOTEL_GUESTS:
                guest.clear()
                print(STOPPING_PARTY_MESSAGE)
                lock_cleaner.release()
                partying = False
            party_count.value += 1
    
            guest_waiting()

def main():
    # Start time of the running of the program. 
    start_time = time.time()


    # Lock for the guests
    lock_guest = mp.Manager().Lock()
    
    # Lock for the cleaners
    lock_cleaner = mp.Manager().Lock()

    # Number of cleanings and parties
    party_count = mp.Manager().Value('i', 0)
    clean_count = mp.Manager().Value('i', 0)

    while time.time() - start_time <= TIME:
        
        cleaner_process = (mp.Process(target=cleaner, args=(lock_guest, lock_cleaner, clean_count)))

        guests_process = (mp.Process(target=guest, args=(lock_guest, lock_cleaner, party_count)))

        # Start both
        guests_process.start()
        cleaner_process.start()

        # join both
        guests_process.join()
        cleaner_process.join()


    # Results
    print(f'Room was clean {clean_count} times, there were {party_count} parties')



if __name__ == '__main__':
    main()

