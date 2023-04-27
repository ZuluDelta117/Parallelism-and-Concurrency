'''
Requirements
1. Write a multithreaded program that calls a local web server. The web server is 
   provided to you. It will return data about the Star Wars movies.
2. You will make 94 calls to the web server, using 94 threads to get the data.
3. Using a new thread each time, obtain a list of the characters, planets, 
   starships, vehicles, and species of the sixth Star War movie.
3. Use the provided print_film_details function to print out the data 
   (should look exactly like the "sample_output.txt file).
   
Questions:
1. Is this assignment an IO Bound or CPU Bound problem (see https://stackoverflow.com/questions/868568/what-do-the-terms-cpu-bound-and-i-o-bound-mean)?
    >IO Bound issue. The time it takes to get the information from the API is much longer than the time it takes to create and sort the lists
2. Review dictionaries (see https://isaaccomputerscience.org/concepts/dsa_datastruct_dictionary). How could a dictionary be used on this assignment to improve performance?
    >Rather than formating a list you could have a pre-formated dictionary that can take in the data. 
    >Then all you would need to do is display the dictionary. 
    >This would remove the time it takes to create the list, call the list, and format the list when displaying.
'''


from datetime import datetime, timedelta
import time
import requests 
import json
import threading
import multiprocessing as mp


# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'
FILM = "/films/6"

CPU_COUNT = mp.cpu_count()

# Global Variables
call_count = 0


chars_list = []
planets_list = []
starships_list = []
vehicles_list = []
species_list = []


def get_info_from_server(url):
    global call_count
    response = requests.get(url)
    # Check the status code to see if the request succeeded.
    call_count += 1
    if response.status_code == 200:
        response = response.json()
        return response
    else:
        print('RESPONSE = ', response.status_code)


def print_film_details(film, chars, planets, starships, vehicles, species):
    '''
    Print out the film details in a formatted way
    '''
    
    def display_names(title, name_list):
        print('')
        print(f'{title}: {len(name_list)}')
        names = sorted([item["name"] for item in name_list])
        print(str(names)[1:-1].replace("'", ""))


    print('-' * 40)
    print(f'Title   : {film["title"]}')
    print(f'Director: {film["director"]}')
    print(f'Producer: {film["producer"]}')
    print(f'Released: {film["release_date"]}')

    display_names('Characters', chars)
    display_names('Planets', planets)
    display_names('Starships', starships)
    display_names('Vehicles', vehicles)
    display_names('Species', species)



def retrieve_data_multiple(API_data):
    """
    Use multi threading to take data from an API and assign it to a list
    arg: API dictionary
    return: list of data
    """
    server_data = []
    num = len(API_data)
    # Create one thread for each piece of data being requested, add it to a list, and start thread
    for i in range(num):
        t = get_info_from_server(API_data[i])     
        server_data.append(t)
    

    return server_data

# def join_threads(threads):
#     list = []
#     # Join each thread that has been added to the threads list and create list of data retreaved
#     for i in range(len(threads)):
#         threads[i].join()
#         new_data = threads[i].response
#         list.append(new_data)
    
#     return list


def chars_callback(result):
    global chars_list
    # This is called whenever sum_all_values(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    chars_list.append(result)

def planets_callback(result):
    global planets_list
    # This is called whenever sum_all_values(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    planets_list.append(result)

def starships_callback(result):
    global starships_list
    # This is called whenever sum_all_values(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    starships_list.append(result)

def vehicles_callback(result):
    global vehicles_list
    # This is called whenever sum_all_values(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    vehicles_list.append(result)

def species_callback(result):
    global species_list
    # This is called whenever sum_all_values(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    species_list.append(result)

def apply_async_with_callback(film6): # , chars, planets, starships, vehicles, species):
    global call_count
    pool = mp.Pool(CPU_COUNT)

    for url in film6["characters"]:
        pool.apply_async(get_info_from_server, args = (url, ), callback = chars_callback)
        call_count += 1
    
    for url in film6["planets"]:
        pool.apply_async(get_info_from_server, args = (url, ), callback = planets_callback)
        call_count += 1

    for url in film6["starships"]:
        pool.apply_async(get_info_from_server, args = (url, ), callback = starships_callback)
        call_count += 1

    for url in film6["vehicles"]:
        pool.apply_async(get_info_from_server, args = (url, ), callback = vehicles_callback)
        call_count += 1

    for url in film6["species"]:
        pool.apply_async(get_info_from_server, args = (url, ), callback = species_callback)
        call_count += 1


    pool.close()
    pool.join()

    print(chars_list)
    print(planets_list)
    print(starships_list)
    print(vehicles_list)
    print(species_list)


def main():
    global chars_list, planets_list, starships_list, vehicles_list, species_list
    #Start a timer
    begin_time = time.perf_counter()

    print('Starting to retrieve data from the server')

    # Get the data from the API
    data = get_info_from_server(f"{TOP_API_URL}")

    #  Call data from 6th film
    film = get_info_from_server(f"{TOP_API_URL}{FILM}")
    
    # Assign response to a variable
    film6 = film


    # Assign film6 data to a lists variable
    # characters_t = retrieve_data_multiple(film6["characters"])
    # planets_t = retrieve_data_multiple(film6["planets"])
    # starships_t = retrieve_data_multiple(film6["starships"])
    # vehicles_t = retrieve_data_multiple(film6["vehicles"])
    # species_t = retrieve_data_multiple(film6["species"])
    
    apply_async_with_callback(film6) # , characters_t, planets_t, starships_t, vehicles_t, species_t)


    characters = chars_list
    planets = planets_list
    starships = starships_list
    vehicles = vehicles_list
    species = species_list



    # Format the information in the lists and display the results
    print_film_details(film6, characters, planets, starships, vehicles, species)

    # Display the total time it took to run code
    print()
    print(f'There were {call_count} calls to the server')
    total_time = time.perf_counter() - begin_time
    total_time_str = "{:.2f}".format(total_time)
    print(f'Total time = {total_time_str} sec')
    

    # Make sure the program is running properly
    assert total_time < 15, "Unless you have a super slow computer, it should not take more than 15 seconds to get all the data."
    
    assert call_count == 94, "It should take exactly 94 threads to get all the data"
    

if __name__ == "__main__":
    main()
