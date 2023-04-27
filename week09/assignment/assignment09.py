'''
Requirements
1. Create a multiprocessing program that reads in files with defined tasks to perform.
2. The program should use a process pool per task type and use apply_async calls with callback functions.
3. The callback functions will store the results in global lists based on the task to perform.
4. Once all 4034 tasks are done, the code should print out each list and a breakdown of 
   the number of each task performed.
   
Questions:
1. How many processes did you specify for each pool:
   >Finding primes: 4
   >Finding words in a file: 8
   >Changing text to uppercase: 1
   >Finding the sum of numbers: 6
   >Web request to get names of Star Wars people: 12
   
   >How do you determine these numbers: I tested each task indavidulay and found the minimum pool size for it to
   >run optimally. I then did it all together and adjusted it a bit from there. 
   
2. Specify whether each of the tasks is IO Bound or CPU Bound?
   >Finding primes: CPU Bound
   >Finding words in a file: I/O Bound
   >Changing text to uppercase: CPU Bound
   >Finding the sum of numbers: CPU Bound
   >Web request to get names of Star Wars people: I/O Bound
   
3. What was your overall time, with:
   >one process in each of your five pools:  63 seconds
   >with the number of processes you show in question one:  19 seconds
'''

import glob
import json
import math
import multiprocessing as mp
import os
import time
from datetime import datetime, timedelta

import numpy as np
import requests

TYPE_PRIME = 'prime'
TYPE_WORD = 'word'
TYPE_UPPER = 'upper'
TYPE_SUM = 'sum'
TYPE_NAME = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []


def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
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


def prime_cb(results):
    global result_primes
    result_primes.append(results)



def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    return f"{value} is prime" if is_prime(value) else f"{value} is not prime"


def word_cb(results):
    global result_words
    result_words.append(results)



def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open('words.txt') as f:
            found = word in map(lambda x:x[:-1],f.readlines())
            return f"{word} Found" if found else f"{word} not found *****"
    

def upper_cb(results):
    global result_upper
    result_upper.append(results)



def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    return f"{text} ==> {text.upper()}"


def sum_cb(results):
    global result_sums
    result_sums.append(results)



def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    total = sum(range(start_value, end_value + 1))
    return f"sum of {start_value:,} to {end_value:,} = {total:,}"


def name_cb(results):
    global result_names
    result_names.append(results)


def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "name" in data:
            name = data['name']
            return f"{url} has name {name}"
    return f"{url} had an error receiving the information"



def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return data
    else:
        return {}


def main():
    begin_time = time.time()
    # Call all global lists so we can append to them
    global result_primes, result_words, result_upper, result_sums, result_names

    # Create all the process pools for each task type
    prime_pool = mp.Pool(4)
    word_pool = mp.Pool(8)
    upper_pool = mp.Pool(1)
    sum_pool = mp.Pool(6)
    name_pool = mp.Pool(12)

    # List to take the value from the tasks
    prime_params = []
    word_params = []
    upper_params = []
    sum_params = []
    name_params  = []


    count = 0
    print("Starting to retrieve tasks from file")
    # Open each task file and add the task to a list
    task_files = glob.glob("tasks/*.task")
    for filename in task_files:
        task = load_json_file(filename)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            prime_params.append((task['value'],))
        elif task_type == TYPE_WORD:
            word_params.append((task['word'],))
        elif task_type == TYPE_UPPER:
            upper_params.append((task['text'],))
        elif task_type == TYPE_SUM:
            sum_params.append((task['start'], task['end']))
        elif task_type == TYPE_NAME:
            name_params.append((task['url'],))
        else:
            print(f'Error: unknown task type {task_type}')


    # start each task asynchronously using a call back function to 
    # add results to a global list
    print("Running tasks")
    for args in prime_params:
        prime_pool.apply_async(task_prime, args, callback = prime_cb)

    for args in word_params: 
        word_pool.apply_async(task_word, args, callback= word_cb)

    for args in upper_params:
        upper_pool.apply_async(task_upper, args, callback= upper_cb)

    for args in sum_params:
        sum_pool.apply_async(task_sum, args, callback= sum_cb)

    for args in name_params:
        name_pool.apply_async(task_name, args, callback= name_cb)


    # Close and end each pool
    prime_pool.close()
    word_pool.close()
    upper_pool.close()
    sum_pool.close()
    name_pool.close()

    prime_pool.join()
    word_pool.join()
    upper_pool.join()
    sum_pool.join()
    name_pool.join()

    # Display all the results
    def print_list(lst):
        for item in lst:
            print(item)
        print(' ')

    print('-' * 80)
    print(f'Primes: {len(result_primes)}')
    print_list(result_primes)

    print('-' * 80)
    print(f'Words: {len(result_words)}')
    print_list(result_words)

    print('-' * 80)
    print(f'Uppercase: {len(result_upper)}')
    print_list(result_upper)

    print('-' * 80)
    print(f'Sums: {len(result_sums)}')
    print_list(result_sums)

    print('-' * 80)
    print(f'Names: {len(result_names)}')
    print_list(result_names)

    print(f'Number of Primes tasks: {len(result_primes)}')
    print(f'Number of Words tasks: {len(result_words)}')
    print(f'Number of Uppercase tasks: {len(result_upper)}')
    print(f'Number of Sums tasks: {len(result_sums)}')
    print(f'Number of Names tasks: {len(result_names)}')
    print(f'Finished processes {count} tasks = {time.time() - begin_time}')


if __name__ == '__main__':
    main()
