'''
Requirements
1. Create a recursive program that finds the solution path for each of the provided mazes.
'''

import math
from screen import Screen
from maze import Maze
import cv2
import sys

SCREEN_SIZE = 800
COLOR = (0, 0, 255)


def solve(maze, _pos=None):
    """ Solve the maze. The path object should be a list (x, y) of the positions 
        that solves the maze, from the start position to the end position. """
    
    (prow, pcol) = _pos if _pos != None else maze.get_start_pos()
    solution_path = [] 
    moves = maze.get_possible_moves(prow, pcol)
    # Remember that an object is passed by reference, so you can pass in the 
    # solution_path object, modify it, and you won't need to return it from 
    # your recursion function
    if len(moves) == 0:
        if maze.at_end(prow, pcol):
            return [(prow, pcol)]
        else:
            return []
    for (mrow, mcol) in moves:
        maze.move(mrow, mcol, COLOR)
        possible_path = solve(maze, (mrow, mcol))
        # Where there is no more moves go back to where there was a possible move
        if len(possible_path) == 0:
            maze.restore(mrow, mcol)
        else:
            solution_path = [(prow, pcol)]
            solution_path.extend(possible_path)
            return solution_path
    return []



def get_solution_path(filename):
    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    solution_path = solve(maze)

    print(f'Number of drawing commands for = {screen.get_command_count()}')

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

    return solution_path


def find_paths():
    files = ('verysmall.bmp', 'verysmall-loops.bmp',
            'small.bmp', 'small-loops.bmp',
            'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    print('*' * 40)
    print('Part 1')
    for filename in files:
        print()
        print(f'File: {filename}')
        solution_path = get_solution_path(filename)
        print(f'Found path has length          = {len(solution_path)}')
    print('*' * 40)


def main():
    # prevent crashing in case of infinite recursion
    sys.setrecursionlimit(5000)
    find_paths()


if __name__ == "__main__":
    main()
