'''
Requirements
1. Create a recursive, multithreaded program that finds the exit of each maze.
   
Questions:
1. It is not required to save the solution path of each maze, but what would
   be your strategy if you needed to do so?
   >I would make another function to keep track of when the maze is not hitting a dead end. 
   >When it back tracks I would remove the from the solution path those moves.
   >I am not sure how that would all work, but with enough time I think I could figure it out.
2. Is using threads to solve the maze a depth-first search (DFS) or breadth-first search (BFS)?
   Which search is "better" in your opinion? You might need to define better. 
   (see https://stackoverflow.com/questions/20192445/which-procedure-we-can-use-for-maze-exploration-bfs-or-dfs)
   >I think it is a DFS. It does not find the shortest path, but just any path that makes it to the end.
   >I think DFS is more practical with this kind of thing, due to wanting to compleate the program quickly,
   >but if we wanted to find the shortest path than BFS would be better. If we were keeping track of the solution 
   >path I think that BFS would be easier also. 
'''

import math
import threading
from screen import Screen
from maze import Maze
import sys
import cv2

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
COLORS = (
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (128, 0, 0),
    (128, 128, 0),
    (0, 128, 0),
    (128, 0, 128),
    (0, 128, 128),
    (0, 0, 128),
    (72, 61, 139),
    (143, 143, 188),
    (226, 138, 43),
    (128, 114, 250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False


def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color

def maze_can_move(lock, maze, row, col):
    # Keep track of when the maze can move
    with lock:
        return maze.can_move_here(row, col)

def solve_path(maze, start, color, path_found, lock):
    """Find a path to the next dead end.
    When a fork is reached, spawn a new thread for every path except 1,
    and go down the remaining path.
    Push all created threads to threads.
    When a dead end is reached or path_found is True, die.
    When the end is reached, set path_found to True."""
    # Call global thread so I can add 1 to the count when I make a new thread
    global thread_count
    threads = []
    (row, col) = start
    # Keep searching for the end of the maze until you find it
    while True:
        if path_found[0] or not maze_can_move(lock, maze, row, col):
            [thread.join() for thread in threads]
            return
        with lock:
            maze.move(row, col, color)
        moves = maze.get_possible_moves(row, col)
        # When there are no possible moves end the thread
        if len(moves) == 0:
            # If a thread finds the end then return path_found as True
            if maze.at_end(row, col):
                path_found[0] = True
            [thread.join() for thread in threads]
            return
        # When there is more than one option to move create a new thread
        elif len(moves) > 1:
            # Use recurssion to add a new thread
            new_threads = [threading.Thread(target = solve_path, args =
                (maze, moves[i], get_color(), path_found, lock)) for i in range(len(moves) - 1)]
            threads.extend(new_threads)
            thread_count += 1
            [thread.start() for thread in new_threads]
            (row, col) = moves[-1]
        else:
            (row, col) = moves[0]


def solve_find_end(maze):
    """ finds the end position using threads.  Nothing is returned """
    # When one of the threads finds the end position, stop all of them
    path_found = [False]
    start_pos = maze.get_start_pos()
    color = get_color()
    lock = threading.Lock()
    threads = []
    start_thread = threading.Thread(target = solve_path,
        args = (maze, start_pos, color, path_found, lock))
    threads.append(start_thread)
    start_thread.start()
    start_thread.join()



def find_end(filename, delay):

    global thread_count

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    print(f'Number of drawing commands = {screen.get_command_count()}')
    print(f'Number of threads created  = {thread_count}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed):
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True


def find_ends():
    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    print('*' * 40)
    print('Part 2')
    for filename, delay in files:
        print()
        print(f'File: {filename}')
        find_end(filename, delay)
    print('*' * 40)


def main():
    # prevent crashing in case of infinite recursion
    sys.setrecursionlimit(5000)
    find_ends()


if __name__ == "__main__":
    main()
