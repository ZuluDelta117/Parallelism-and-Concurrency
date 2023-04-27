![](../../banner.png)

# 04 Teach: Feed Me Seymour!

## Overview

[Feed Me Seymour!](https://www.youtube.com/watch?v=L7SkrYF8lCU). You will be implementing a program that has two threads: one eater and one feeder. You will be using a shared, custom queue to pass food from the feeder to the eater. You will be using semaphores to ensure that the queue size is not exceeded and ensure that you don't pop from an empty custom queue.

## Assignment

Download the file [team04.py](team04.py) to your computer. 

### Instructions:

The main function is already implemented for you. You and your team need to implement the Eater and Feeder thread classes. The classes will utilize semaphores in order to synchronize the feeder putting food into the queue for the eater to consume. 

Work on this for the remaining class time. If you can't complete it by the end of class, try to:
   a. Stay after class until you have it done.
   b. Get together with your team at another time.
   c. Finish it on your own.

### Core Requirements

1. Use a semaphore to prevent errors from reading an empty queue (table).
2. Use a semaphore to prevent too many items being added to the queue (table).
3. Use a lock to prevent items (food) from being added/removed to/from the queue (table) at the same time by two threads (feeder/eater).
4. The number of food made must equal the number of food eaten.

## Sample Solution

No solution provided. A sample solution will be posted on Friday.
