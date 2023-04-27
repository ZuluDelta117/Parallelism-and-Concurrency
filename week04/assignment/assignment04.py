'''
Requirements
1. Using two threads, put cars onto a shared queue, with one thread consuming
   the items from the queue and the other producing the items.
2. The size of queue should never exceed 10.
3. Do not call queue size to determine if maximum size has been reached. This means
   that you should not do something like this: 
        if q.size() < 10:
   Use the blocking semaphore function 'acquire'.
4. Produce a Plot of car count vs queue size (okay to use q.size since this is not a
   condition statement).
   
Questions:
1. Do you need to use locks around accessing the queue object when using multiple threads? 
   Why or why not?
   >Yes, because each thread has access to the queue object and if it is not protected by a lock
   >more than one thread may access it at one time and you will have a data discrepency.
2. How would you define a semaphore in your own words?
   >A semaphore is a list of locks that will subtract or add to the number of locks depending on if
   >you acquire or release the lock.
3. Read https://stackoverflow.com/questions/2407589/what-does-the-term-blocking-mean-in-programming.
   What does it mean that the "join" function is a blocking function? Why do we want to block?
   >The join function acts as a blocking function by preventing a thread from finishing until
   >another thread has finished exicuting.
   >We want to block so that the data does not get tangled up and it keeps the data consistant.
'''

from datetime import datetime
import time
import threading
import random

from plots import Plots

# Global Constants
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru',
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus',
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE', 'Super', 'Tall', 'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has just be created in the terminal
        self.display()

    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class QueueTwoFiftyOne():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Manufacturer(threading.Thread):
    """ This is a manufacturer.  It will create cars and place them on the car queue """

    def __init__(self,
                manufacturer_index,
                cars_to_produce,
                sem_manufacturer_full: threading.Semaphore,
                sem_manufacturer_available: threading.Semaphore,
                dealership_queue,
                dealership_lock):

        threading.Thread.__init__(self)

        # Create the self objects for the arguments
        self.manufacturer_index = manufacturer_index
        self.car_count = cars_to_produce
        self.sem_manufacturer_full = sem_manufacturer_full
        self.sem_manufacturer_available = sem_manufacturer_available
        self.dealership_queue = dealership_queue
        self.dealership_lock = dealership_lock
        self.cars_made = 0

    def run(self):
        """
        create a car
        place the car on the queue
        signal the dealer that there is a car on the queue
        """
        for i in range(self.car_count):
            self.sem_manufacturer_full.acquire()
            car = Car()
            # Add a car to the queue from the car class
            with self.dealership_lock:
                self.dealership_queue.put((car))
            
            # Add one to the counter of how many cars are made
            self.cars_made += 1
            self.sem_manufacturer_available.release()

        # signal the dealer that there there are no more cars
        self.sem_manufacturer_full.acquire()
        self.dealership_queue.put(None)
        self.sem_manufacturer_available.release()


class Dealership(threading.Thread):
    """ This is a dealership that receives cars """

    def __init__(self,
                dealership_index,
                queue_stats,
                sem_manufacturer_full: threading.Semaphore,
                sem_manufacturer_available: threading.Semaphore,
                dealership_queue,
                dealership_lock):

        threading.Thread.__init__(self)

        self.dealership_index = dealership_index
        self.queue_stats = queue_stats
        self.sem_manufacturer_full = sem_manufacturer_full
        self.sem_manufacturer_available = sem_manufacturer_available
        self.dealership_queue = dealership_queue
        self.dealership_lock = dealership_lock
        
    def run(self):
        while True:
            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """
            self.sem_manufacturer_available.acquire()
            
            with self.dealership_lock:
                recieveing_car = self.dealership_queue.get()
            
            if recieveing_car == None:
                break
            
            # Add one car to the queue_stats list
            # Where it is added is dependent on how many cars are in the queue
            index = self.dealership_queue.size()
            self.queue_stats[index] += 1

            self.sem_manufacturer_full.release()
            
            # Sleep a little after selling a car
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))


def main(number_of_manufacturers, number_of_dealerships):
    # Start a timer
    begin_time = time.perf_counter()

    # random amount of cars to produce
    CARS_TO_PRODUCE = random.randint(500, 600)

    sem_manufacturer_full = threading.Semaphore(MAX_QUEUE_SIZE)
    sem_manufacturer_available = threading.Semaphore(0)
    dealership_queue = QueueTwoFiftyOne()
    dealership_lock = threading.Lock()

    # This tracks the length of the car queue during receiving cars by the dealership,
    # the index of the list is the size of the queue. Update this list each time the
    # dealership receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    # Call the manufacturer thread(s) to produce the cars
    manufacturers = []
    for manufacturer_index in range(number_of_manufacturers):
        manufacturers.append(
            Manufacturer(manufacturer_index, CARS_TO_PRODUCE, sem_manufacturer_full, sem_manufacturer_available,
            dealership_queue, dealership_lock)
        )

    # Call the dealership thread(s) to sell the cars
    dealerships = []
    for dealership_index in range(number_of_dealerships):
        dealerships.append(
            Dealership(dealership_index, queue_stats, sem_manufacturer_full, sem_manufacturer_available,
            dealership_queue, dealership_lock)
        )

    # Start and join the threads
    for manufacturer in manufacturers:
        manufacturer.start()

    for dealership in dealerships:
        dealership.start()

    for manufacturer in manufacturers:
        manufacturer.join()

    for dealership in dealerships:
        dealership.join()

    

    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time = {total_time} sec')

    # Plot car count vs queue size
    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats,
            title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')


if __name__ == '__main__':
    main(1, 1)
