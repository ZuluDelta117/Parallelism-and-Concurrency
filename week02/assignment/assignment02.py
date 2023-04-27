'''
Requirements
1. Write a multithreaded program that counts the number of prime numbers 
   between 10,000,000,000 and 10,000,110,003.
2. The program should be able to use a variable amount of threads.
3. Each thread should look over an approximately equal number of numbers.
   This means that you need to divise an algorithm that can divide up the
   110,003 numbers "fairly" based on a variable number of threads. 
   
Psuedocode: 
1. Create variable for the start number (10_000_000_000)
2. Create variable for range of numbers to examine (110_003)
3. Create variable for number of threads (start with 1 to get your program running,
   then increase to 5, then 10).
4. Determine an algorithm to partition the 110,003 numbers based on 
    the number of threads. Each thread should have approx. the same amount
    of numbers to examine. For example, if the number of threads is
    5, then the first 4 threads will examine 22,003 numbers, and the
    last thread will examine 22,003 numbers. Determine the start and
    end values of each partition.
5. Use these start and end values as arguments to a function.
6. Use a thread to call this function.
7. Create a function that loops from a start and end value, and checks
   if the value is prime using the isPrime function. Use the globals
   to keep track of the total numbers examined and the number of primes
   found. 

Questions:
1. Time to run using 1 thread = 15.50 sec
2. Time to run using 5 threads = 18.11 sec
3. Time to run using 10 threads = 16.84 sec
4. Based on your study of the GIL (see https://realpython.com/python-gil), 
   what conclusions can you draw about the similarity of the times (short answer)?
   > Due to the GIL multi-threading this program is not faster. It is actually a bit slower
   >
5. Is this assignment an IO Bound or CPU Bound problem (see https://stackoverflow.com/questions/868568/what-do-the-terms-cpu-bound-and-i-o-bound-mean)?
   > This is a CPU bound issue. Most of the time spent in the program is calculating is all the numbers are prime.
'''

from datetime import datetime, timedelta
import math
import threading
import time

# Global count of the number of primes found
prime_count = 0

# Global count of the numbers examined
numbers_processed = 0


def is_prime(n: int):
    """
    Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test

    Parameters
    ----------
    ``n`` : int
        Number to determine if prime

    Returns
    -------
    bool
        True if ``n`` is prime.
    """

    # Check to see if a number is prime
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def process_range(start, end):
    """
    Process how many numbers you would like to check for prime numbers
    """
    global prime_count
    global numbers_processed
    for i in range(start, end):
        numbers_processed += 1
        if is_prime(i):
            prime_count += 1
            

if __name__ == '__main__':
    # Start a timer
    begin_time = time.perf_counter()
    # adjust how many thread you would like to split the task between 
    thread_number = 13
    start_number = 10000000000
    range_count = 110003

    numbers = []

    # Divide the rangew of numbers you want to check by number of threads you would like to 
    # split the work between 
    for i in range(thread_number):
        thread_range = range_count // thread_number
        numbers.append(thread_range)
    remainder = range_count % thread_number

    if thread_number == 1:
        pass
    else:
        numbers.append(numbers[thread_number-1] + remainder)
        numbers.remove(numbers[thread_number-1])

    threads = []
    # create the thread(s) to run process_range function
    for i in range(thread_number):
        thread_start = start_number + (thread_range * i)
        thread_end = thread_start + numbers[i]
        print(thread_end)
        t = threading.Thread(target=process_range, args=(thread_start, thread_end))
        threads.append(t)

    for t in threads:
        print(f"{t} begins")
        t.start()
            
    for t in threads:
        t.join()
        print(f"{t} ends")

    # Use the below code to check and print your results
    assert numbers_processed == 110_003, f"Should check exactly 110,003 numbers but checked {numbers_processed}"
    assert prime_count == 4764, f"Should find exactly 4764 primes but found {prime_count}"

    print(f'Numbers processed = {numbers_processed}')
    print(f'Primes found = {prime_count}')
    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time = {total_time} sec')
