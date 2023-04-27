![](../../banner.png)

# 13 Teach: Word Search

## Overview

[Word Search](https://thewordsearch.com/) puzzles are fun to play.  You will be speeding up a word search program.

## Assignment

Download the file [team13.py](team13.py) to your computer.  Place it based on the suggested directory structure of the course.  This program creates a word search puzzle, then it solves it.  However, the searching for the words isn't fast and needs to be improved.

### Instructions:

- Try to speed up this program
- you can change the Board class
- talk with your team before making changes
- make backups if you try something that doesn't work

### Core Requirements

1. Download the `team13.py` file and make sure it runs on your computer.  The program will display the board before and after finding the words in it.  Read the header in the program for any other instructions.
2. Discuss with your team members ideas on how to improve this program with regards to speed.
3. Make the program faster - use any technique (ie, threads, processes, algorithm analysis, etc...) 
4. Time your changes. What worked and what didn't?  Was it worth the effort?

### Things to consider
What is the [space and time complexity](https://towardsdatascience.com/space-and-time-complexity-in-computer-algorithms-a7fffe9e4683) of the "find_word" function? To find each word we call this function which loops over the row, then the column, then the eight letters around the this location. Worse yet, it calls "_word_at_this_location" function to check if the target word is found at this location. This helper function contains a loop that loops over every letter in the word.

**There is a solution that can solve this problem in around 1/100th of second on most computers. See if you can find it!**

## Sample Solution

Since we will not be meeting again, a sample solution will be posted for you to look at.
