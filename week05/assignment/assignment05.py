'''
Requirements
1. Using multiple threads, put cars onto a shared queue, with one or more thread consuming
   the items from the queue and one or more thread producing the items.
2. The size of queue should never exceed 10.
3. Do not call queue size to determine if maximum size has been reached. This means
   that you should not do something like this: 
        if q.size() < 10:
   Use the blocking semaphore function 'acquire'.
4. Produce a Plot of car count vs queue size (okay to use q.size since this is not a
   condition statement).
5. The number of cars produced by the manufacturer must equal the number of cars bought by the 
   dealership. Use necessary data objects (e.g., lists) to prove this. There is an assert in 
   main that must be used.
   
Questions:
1. How would you define a barrier in your own words?
   >A barrier is a lock that will not open unless it has the assigned amount of threads are waiting for it.
   >It helps keep threads from dead locking and other errors due to race conditions.
2. Why is a barrier necessary in this assignment?
   >The barrier is important to keep the dealer from taking things off the queue before the manufacturer is ready
   >Keeping the threads from getting tangled.
'''

from datetime import datetime, timedelta
import time
import threading
import random

# Global Constants
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

class Car():
    """ This is the Car class that will be created by the manufacturers """

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

        # Display the car that has was just created in the terminal
        self.display()

    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class QueueTwoFiftyOne():
    """ This is the queue object to use for this assignment. Do not modify!! """

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


class Manufacturer(threading.Thread):
    """ This is a manufacturer.  It will create cars and place them on the car queue """

    def __init__(self,
                manufacturer_index,
                manufacturer_stats,
                sem_manufacturer_full: threading.Semaphore,
                sem_manufacturer_available: threading.Semaphore,
                dealership_queue,
                barrier: threading.Barrier,
                dealership_lock,
                manufacturer_count,
                dealer_count):
        # Call partent class to initiate creating a thread
        threading.Thread.__init__(self)

        # Create the self objects for the arguments
        self.manufacturer_index = manufacturer_index
        self.manufacturer_stats = manufacturer_stats
        self.cars_to_produce = random.randint(200, 300)
        self.sem_manufacturer_full = sem_manufacturer_full
        self.sem_manufacturer_available = sem_manufacturer_available
        self.dealership_queue = dealership_queue
        self.dealership_lock = dealership_lock
        self.barrier = barrier
        self.manufacturer_count = manufacturer_count
        self.dealer_count = dealer_count

    def run(self):
        for i in range(self.cars_to_produce):
            self.sem_manufacturer_full.acquire()
            car = Car()
            # Add a car to the queue from the car class
            with self.dealership_lock:
                self.dealership_queue.put((car))
            
            self.sem_manufacturer_available.release()
            # Add one to the counter of how many cars are made
            self.manufacturer_stats[self.manufacturer_index] += 1
        
        # Wait until all the manufacturer threads are ready
        self.barrier.wait()
        
        # Signal the dealer that there there are no more cars in the queue
        # Make sure the index is zero
        if self.manufacturer_index == 0:
            # Add none to queue for each dealer
            for i in range(self.dealer_count):
                self.sem_manufacturer_full.acquire()

                self.dealership_lock.acquire()
                self.dealership_queue.put(None)
                self.dealership_lock.release()

                self.sem_manufacturer_available.release()


class Dealership(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self,
                dealership_index,
                dealer_stats,
                sem_manufacturer_full: threading.Semaphore,
                sem_manufacturer_available: threading.Semaphore,
                dealership_queue,
                dealership_lock,
                barrier: threading.Barrier
                ):
        # Call partent class to initiate creating a thread
        threading.Thread.__init__(self)

        # Create the self objects for the arguments
        self.dealership_index = dealership_index
        self.dealer_stats = dealer_stats
        self.sem_manufacturer_full = sem_manufacturer_full
        self.sem_manufacturer_available = sem_manufacturer_available
        self.dealership_queue = dealership_queue
        self.dealership_lock = dealership_lock
        self.barrier = barrier

    def run(self):
        while True:
            self.sem_manufacturer_available.acquire()
            
            with self.dealership_lock:
                # Remove a car from the queue
                recieveing_car = self.dealership_queue.get()
            
            # If thread finds None in the queue terminate the thread
            if recieveing_car == None:
                break
            
            # Add one car to the dealer_stats list
            # Where it is added is dependent on how many cars are in the queue
            self.sem_manufacturer_full.release()
            self.dealer_stats[self.dealership_index] += 1
            
            # Sleep a little - don't change.  This is the last line of the loop
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))
        # Wait until all dealer threads are ready
        self.barrier
        


def run_production(manufacturer_count, dealer_count):
    """ This function will do a production run with the number of
        manufacturers and dealerships passed in as arguments.
    """
    # Start a timer
    begin_time = time.perf_counter()

    # Create all objects that will be used in program
    sem_manufacturer_full = threading.Semaphore(MAX_QUEUE_SIZE)
    sem_manufacturer_available = threading.Semaphore(0)
    car_queue = QueueTwoFiftyOne()
    dealership_lock = threading.Lock()
    manufacturer_barrier = threading.Barrier(manufacturer_count)
    dealer_barrier = threading.Barrier(dealer_count)

    # This is used to track the number of cars receives by each dealer
    dealer_stats = list([0] * dealer_count)

    manufacturer_stats = list([0] * manufacturer_count)

    manufacturers = []
    # Create all manufacturer threads and add to list
    for manufacturer_index in range(manufacturer_count):
        manufacturers.append(
            Manufacturer(manufacturer_index, manufacturer_stats, sem_manufacturer_full, sem_manufacturer_available,
            car_queue, manufacturer_barrier, dealership_lock, manufacturer_count, dealer_count)
        )

    dealerships = []
    # Create all dealership threads and add to list
    for dealership_index in range(dealer_count):
        dealerships.append(
            Dealership(dealership_index, dealer_stats, sem_manufacturer_full, sem_manufacturer_available,
            car_queue, dealership_lock, dealer_barrier)
        )

    # Start threads
    for manufacturer in manufacturers:
        manufacturer.start()

    for dealership in dealerships:
        dealership.start()

    # End threads
    for manufacturer in manufacturers:
        manufacturer.join()

    for dealership in dealerships:
        dealership.join()

    run_time = time.perf_counter() - begin_time

    # manufacturer_stats: is a list of the number of cars produced by each manufacturer,
    #                collect this information after the manufacturers are finished.
    return (run_time, car_queue.get_max_size(), dealer_stats, manufacturer_stats)


def main():
    """ Main function """

    # Run the program 7 times changing the number of manufacturs and dealers each time
    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for manufacturers, dealerships in runs:
        run_time, max_queue_size, dealer_stats, manufacturer_stats = run_production(
            manufacturers, dealerships)

        print(f'Manufacturers       : {manufacturers}')
        print(f'Dealerships         : {dealerships}')
        print(f'Run Time            : {run_time:.2f} sec')
        print(f'Max queue size      : {max_queue_size}')
        print(f'Manufacturer Stats  : {manufacturer_stats}')
        print(f'Dealer Stats        : {dealer_stats}')
        print('')

        # The number of cars produces needs to match the cars sold
        assert sum(dealer_stats) == sum(manufacturer_stats)


if __name__ == '__main__':
    main()
