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


# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'
FILM = "/films/6"

# Global Variables
call_count = 0


class Request_Thread(threading.Thread):

    def __init__(self, url):
        """
        Initiates the thread and calles the threading.Thread parent class
        Arg: API URL
        """
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        global call_count
        response = requests.get(self.url)
        call_count += 1
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.response = response.json()
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
    threads = []
    num = len(API_data)
    # Create one thread for each piece of data being requested, add it to a list, and start thread
    for i in range(num):
        t = Request_Thread(API_data[i])     
        threads.append(t)
        threads[i].start()
    

    return threads

def join_threads(threads):
    list = []
    # Join each thread that has been added to the threads list and create list of data retreaved
    for i in range(len(threads)):
        threads[i].join()
        new_data = threads[i].response
        list.append(new_data)
    
    return list



def main():
    #Start a timer
    begin_time = time.perf_counter()

    print('Starting to retrieve data from the server')

    # Get the data from the API
    data = Request_Thread(f"{TOP_API_URL}")
    data.start()

    data.join()

    #  Call data from 6th film
    film = Request_Thread(f"{TOP_API_URL}{FILM}")
    film.start()
    
    film.join()
    # Assign response to a variable
    film6 = film.response


    # Assign film6 data to a lists variable
    characters_t = retrieve_data_multiple(film6["characters"])
    planets_t = retrieve_data_multiple(film6["planets"])
    starships_t = retrieve_data_multiple(film6["starships"])
    vehicles_t = retrieve_data_multiple(film6["vehicles"])
    species_t = retrieve_data_multiple(film6["species"])

    characters = join_threads(characters_t)
    planets = join_threads(planets_t)
    starships = join_threads(starships_t)
    vehicles = join_threads(vehicles_t)
    species = join_threads(species_t)



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
