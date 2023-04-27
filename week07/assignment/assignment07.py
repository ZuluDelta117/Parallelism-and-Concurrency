'''
Requirements
1.  Create a multiprocessing program that connects the processes using Pipes.
2.  Create a process from each of the following custom process classes, 
    Marble_Creator, Bagger, Assembler, and Wrapper.
3.  The Marble_Creator process will send a marble to the Bagger process using
    a Pipe.
4.  The Bagger process will create a Bag object with the required number of
    marbles. 
5.  The Bagger process will send the Bag object to the Assembler using a Pipe.
6.  The Assembler process will create a Gift object and send it to the Wrapper
    process using a Pipe.
7.  The Wrapper process will write to a file the current time followed by the 
    gift string.
8.  The program should not hard-code the number of marbles, the various delays,
    nor the bag count. These should be obtained from the settings.txt file.

Questions:
1.  Why can you not use the same pipe object for all the processes (i.e., why 
    do you need to create three different pipes)?
    >Because a pipe can only have one start location and one end location.
    >If you tried to use one pipe the data would get all mixed up and I think you would deadlock.
2.  Compare and contrast pipes with queues (i.e., how are the similar or different)?
    >Queues are able to send and recieve to multiple location where pipes cannot.
    >They are both used to send and recieve data though. I think pipes are faster and
    >more simple to use when doing things that are a step by step process and each 
    >piece of data builds on top of each other. 
'''

from datetime import datetime
import json
import multiprocessing as mp
import os
import random
import time

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME = 'boxes.txt'

# Settings constants
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'


class Bag():
    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver',
            'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda',
            'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green',
            'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', "Big Dip O’ruby",
            'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink',
            'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple',
            'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango',
            'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink',
            'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green',
            'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple',
            'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue',
            'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue',
            'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow',
            'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink',
            'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink',
            'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
            'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue',
            'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, pipeout, marble_count, creator_delay):
        mp.Process.__init__(self)
        self.pipeout = pipeout
        self.marble_count = marble_count
        self.creator_delay = creator_delay

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
            - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        # Create and send each marble to te bagger
        for _ in range(self.marble_count):
            self.pipeout.send(random.choice(Marble_Creator.colors))
            time.sleep(self.creator_delay)
        self.pipeout.send(None)

        self.pipeout.close()



class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """

    def __init__(self, pipein, pipeout, bag_count, bagger_delay):
        mp.Process.__init__(self)
        self.pipeout = pipeout
        self.pipein = pipein
        self.bag_count = bag_count
        self.bagger_delay = bagger_delay

    def make_bag(self):
        # Create the bag to put marbles in
        bag = Bag()
        for _ in range(self.bag_count):
            marble = self.pipein.recv()
            
            if marble == None:
                break

            bag.add(marble)
        return bag

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        # Add all the marbles to a bag
        while True:
            bag = self.make_bag()
            if bag.get_size() == self.bag_count:
                pass
                self.pipeout.send(bag)
            else:
                self.pipeout.send(None)
                break
            time.sleep(self.bagger_delay)
        
        self.pipein.close()
        self.pipeout.close()



class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss',
                    'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, pipein, pipeout, assembler_delay):
        mp.Process.__init__(self)
        self.pipeout = pipeout
        self.pipein = pipein
        self.assembler_delay = assembler_delay

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        # Adds a name to each bag of marbles
        while True:
            bag = self.pipein.recv()
            if bag == None:
                self.pipeout.send(None)
                break
            gift = Gift(random.choice(Assembler.marble_names), bag)
            self.pipeout.send(gift)
            time.sleep(self.assembler_delay)


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """

    def __init__(self, pipein, wrapper_delay, gift_count):
        mp.Process.__init__(self)
        self.pipein = pipein
        self.wrapper_delay = wrapper_delay
        self.gift_count = gift_count

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        (see prepare00.md for helpful file operations)
        '''
        # Wrappes the bags into a box and sends marbles to the text file
        with open("boxes.txt", mode='w') as box:
            while True:
                gift = self.pipein.recv()
                if gift == None:
                    break
                current_time = datetime.now().time()
                box.write(f"Created - {current_time} {str(gift)}\n")
                self.gift_count.value += 1
                time.sleep(self.wrapper_delay)


def display_final_boxes(filename):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        print(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                print(line.strip())
    else:
        print(
            f'ERROR: The file {filename} doesn\'t exist.  No boxes were created.')


def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return data
    else:
        return {}


def main():
    """ Main function """

    # Start a timer
    begin_time = time.perf_counter()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        print(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    print(f'Marble count                = {settings[MARBLE_COUNT]}')
    print(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    print(f'settings["bag-count"]       = {settings[BAG_COUNT]}')
    print(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    print(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    print(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    # Create each of the pipes used to send the marbles
    creator_out, bagger_in = mp.Pipe()
    bagger_out, assembler_in = mp.Pipe()
    assembler_out, wrapper_in = mp.Pipe()

    # Keep track of how many gifts were created
    gift_count = mp.Manager().Value('i', 0)

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    print('Create the processes')

    # Create a list of all the processes
    processes = [
            Marble_Creator(creator_out, settings[MARBLE_COUNT], settings[CREATOR_DELAY]),
            Bagger(bagger_in, bagger_out,settings[BAG_COUNT], settings[BAGGER_DELAY]), 
            Assembler(assembler_in, assembler_out, settings[ASSEMBLER_DELAY]),
            Wrapper(wrapper_in, settings[WRAPPER_DELAY], gift_count)
            ]


    print('Starting the processes')
    # Start each process in the list
    for process in processes:
        process.start()


    print('Waiting for processes to finish')
    # End each process in the list
    for process in processes:
        process.join()

    display_final_boxes(BOXES_FILENAME)

    # Display the number of gifts created
    print(f"{gift_count.value} gifts were created.")


if __name__ == '__main__':
    main()
