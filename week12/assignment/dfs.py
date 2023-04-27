"""
Course: CSE 251
Lesson Week: 12
File: assignment.py
Author: Zack Doxey
Purpose: Assignment 12 - Family Search
"""
import json
import threading
import time

import requests
from virusApi import *

TOP_API_URL = 'http://127.0.0.1:8129'
NUMBER_GENERATIONS = 6
NUMBER_THREADS = 0  

# -----------------------------------------------------------------------------
class Request_thread(threading.Thread):

    def __init__(self, url):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        global NUMBER_THREADS
        response = requests.get(self.url)
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            NUMBER_THREADS += 1
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)

def dfs_recursion(family_id, pandemic: Pandemic):
    global NUMBER_THREADS
    t_fam_list = []

    # base case
    if family_id == None:
        return

    # print(f'{family_id=} Retrieving Family: {family_id}\n', end="")

    # add family to pandemic
    family_response = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    family_response.start()
    family_response.join()
    if ("id" not in family_response.response):
        return

    family = Family.fromResponse(family_response.response)
    # print(f'{family_id=} family.response={family_t.response}\n', end="")
    pandemic.add_family(family)

    virus1 = None
    virus2 = None
    virus1_thread = None
    virus2_thread = None

    # Get VIRUS1
    if family.virus1 != None:
        # Get virus via thread so it can run concurrently to other threads
        virus1_thread = Request_thread(
            f'http://{hostName}:{serverPort}/virus/{family.virus1}')
        virus1_thread.start()

    # Get VIRUS2
    if family.virus2 != None:
        # Get virus via thread so it can run concurrently to other threads
        virus2_thread = Request_thread(
            f'http://{hostName}:{serverPort}/virus/{family.virus2}')
        virus2_thread.start()

    # Get OFFSPRING
    offspring = []
    offspring_thread_list = []
    for id in family.offspring:
        # Get offspring via thread so it can run concurent to other threads
        offspring_thread = Request_thread(f'http://{hostName}:{serverPort}/virus/{id}')
        offspring_thread.start()
        offspring_thread_list.append(offspring_thread)

    # ADD VIRUS1 to Pandemic
    if virus1_thread != None:
        # Join virus thread to get server response
        virus1_thread.join()
        virus1 = virus1_thread.response

    if virus1 != None:
        v = Virus.createVirus(virus1)
        pandemic.add_virus(v)
        if v.parents != None:
            # Call recursion function via thread to run concurent to other threads
            t_fam1 = threading.Thread(target= dfs_recursion, args= (v.parents, pandemic))
            NUMBER_THREADS += 1
            t_fam_list.append(t_fam1)
            t_fam1.start()

    # ADD VIRUS2 to Pandemic
    if virus2_thread != None:
        # Join virus thread to get server response
        virus2_thread.join()
        virus2 = virus2_thread.response

    if virus2 != None:
        v = Virus.createVirus(virus2)
        pandemic.add_virus(v)
        if v.parents != None:
            # Call recursion function via thread to run concurent to other threads
            t_fam2 = threading.Thread(dfs_recursion(v.parents, pandemic))
            NUMBER_THREADS += 1
            t_fam_list.append(t_fam2)
            t_fam2.start()

    # ADD offspring to Pandemic
    for t in offspring_thread_list:
        # Join offspring threads to get server response
        t.join()
        offspring.append(t.response)

    for o in offspring:
        v = Virus.createVirus(o)
        # don't try and add virus that we have already added
        # (happens when we add a virus and then loop over the
        # virus parent's offspring)
        if not pandemic.does_virus_exist(v.id):
            pandemic.add_virus(v)
    
    for t in t_fam_list:
        # Join recursion threads so they all run at the same time
        t.join()


def dfs(start_id, generations):
    pandemic = Pandemic(start_id)

    # tell server we are starting a new generation of viruses
    req = Request_thread(f'{TOP_API_URL}/start/{generations}')
    req.start()
    req.join()
    
    
    # get all the viruses in the pandemic recursively
    dfs_recursion(start_id, pandemic)

    req = Request_thread(f'{TOP_API_URL}/end')
    req.start()
    req.join()
    
    
    print('')
    print(f'Total Viruses  : {pandemic.get_virus_count()}')
    print(f'Total Families : {pandemic.get_family_count()}')
    print(f'Generations    : {generations}')
    
    return pandemic.get_virus_count()


def main():
    # Start a timer
    begin_time = time.perf_counter()

    print(f'Pandemic starting...')
    print('#' * 60)
    
    t_json = Request_thread(f'{TOP_API_URL}')
    t_json.start()
    t_json.join()
    jsonResponse = t_json.response
    
    print(f'First Virus Family id: {jsonResponse["start_family_id"]}')
    start_id = jsonResponse['start_family_id']

    virus_count = dfs(start_id, NUMBER_GENERATIONS)

    total_time = time.perf_counter() - begin_time
    total_time_str = "{:.2f}".format(total_time)

    print(f'\nTotal time = {total_time_str} sec')
    print(f'Number of threads: {NUMBER_THREADS}')
    print(f'Performance: {round(virus_count / total_time, 2)} viruses/sec')
    
if __name__ == '__main__':
    main()