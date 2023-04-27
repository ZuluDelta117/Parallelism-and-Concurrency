import queue
import threading
import time

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


def create_family(family_id, q: queue.Queue, pandemic: Pandemic):

    # base case
    if family_id == None:
        return

    # CREATE FAMILY THREAD
    t_thread = Request_thread(
        f'http://{hostName}:{serverPort}/family/{family_id}')
    t_thread.start()
    t_thread.join()

    if ("id" not in t_thread.response):
        return

    # ADD FAMILY
    family = Family.fromResponse(t_thread.response)
    # print(f'###\n{family}\n###')
    pandemic.add_family(family)

    # Flag to indicate if there are no more parents to check
    any_more_parents = False

    virus1 = None
    virus2 = None
    virus_thread1 = None
    virus_thread2 = None

    # Get VIRUS1
    if family.virus1 != None:
        # Get virus via thread so it can run concurrently to other threads
        virus_thread1 = Request_thread(
            f'http://{hostName}:{serverPort}/virus/{family.virus1}')
        virus_thread1.start()

    # Get VIRUS2
    if family.virus2 != None:
        # Get virus via thread so it can run concurrently to other threads
        virus_thread2 = Request_thread(
            f'http://{hostName}:{serverPort}/virus/{family.virus2}')
        virus_thread2.start()

    # Get OFFSPRING
    offspring = []
    offspring_thread_list = []
    for id in family.offspring:
        # Get offspring via thread so it can run concurent to other threads
        offspring_thread = Request_thread(f'http://{hostName}:{serverPort}/virus/{id}')
        offspring_thread.start()
        offspring_thread_list.append(offspring_thread)

    # ADD VIRUS1 to Pandemic
    if virus_thread1 != None:
        # Join virus thread to get server response
        virus_thread1.join()
        virus1 = virus_thread1.response

    if virus1 != None:
        v = Virus.createVirus(virus1)
        pandemic.add_virus(v)

        if v.parents != None:
            q.put(v.parents)
            any_more_parents = True


    # ADD VIRUS2 to Pandemic
    if virus_thread2 != None:
        # Join virus thread to get server response
        virus_thread2.join()
        virus2 = virus_thread2.response
        
    if virus2 != None:
        v = Virus.createVirus(virus2)
        pandemic.add_virus(v)

        if v.parents != None:
            q.put(v.parents)
            any_more_parents = True



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

    # Exit the WHILE loop
    if not any_more_parents:
        q.put("DONE")
    


def bfs_recursion(start_id, pandemic):
    global NUMBER_THREADS

    # create a queue to store family ids
    q = queue.Queue()
    t_fam_list = []
    # put on the first family id
    q.put(start_id)

    while True:
        family_id = q.get()

        if family_id == "DONE":
            break

        if family_id != None:
            # Call all family threads available
            t_fam = threading.Thread(target= create_family, args= (family_id, q, pandemic))
            t_fam_list.append(t_fam)
            t_fam.start()
            NUMBER_THREADS += 1
    
    # Join all family threads
    for t in t_fam_list:
        t.join()


def bfs(start_id, generations):
    pandemic = Pandemic(start_id)
    
    # tell server we are starting a new generation of viruses
    req = Request_thread(f'{TOP_API_URL}/start/{generations}')
    req.start()
    req.join()

    # get all the viruses in the pandemic recursively
    bfs_recursion(start_id, pandemic)
    

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

    virus_count = bfs(start_id, NUMBER_GENERATIONS)

    total_time = time.perf_counter() - begin_time
    total_time_str = "{:.2f}".format(total_time)

    print(f'\nTotal time = {total_time_str} sec')
    print(f'Number of threads: {NUMBER_THREADS}')
    print(f'Performance: {round(virus_count / total_time, 2)} viruses/sec')


if __name__ == '__main__':
    main()
