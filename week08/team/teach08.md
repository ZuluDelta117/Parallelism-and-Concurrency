![](../../banner.png)

# 08 Teach: Merge Sort

## Overview

The [merge sort](https://en.wikipedia.org/wiki/Merge_sort) is "an efficient, general-purpose, comparison-based sorting algorithm."

## Assignment

The code found in `team08.py` contains a working merge function that sorts 1,000,000 numbers in a list.  You will be changing the program to;

1. Implement the function `merge_sort_thread()` to use threads in the recursion.  When your merge function makes a recursive call to itself, you will create a new thread to handle that function.
2. Implement the function `merge_sort_process()` to use processes in the recursion.  When your merge function makes a recursive call to itself, you will create a new process to handle that function. **<ins>Don't</ins> create more than 10 processes or you might crash the program.** After creating 10 processes, then use normal sort to sort the rest.

## Sample Solution

No solution provided. A sample solution will be posted on Friday.

