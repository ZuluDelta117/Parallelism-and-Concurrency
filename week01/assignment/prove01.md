![](../../../banner.png)

# 01 Prove: Creating Threads 

## Overview

Your first assignment is to create two programs that will compute the sum of numbers from 1 to a given number (not counting the number). The first program will need to perform this function using the threading module and either a global variable or a list object that gets passed in. The second program will perform this function by extending the Thread class and creating an object using this thread class.

## Instructions

Read the `assignment01_a.py` and `assignment01-b.py` from the `week01/assignment` folder you cloned from Github. 


## Rubric

**Rubric for Assignment01-a.py**
Item | Proficient | Emerging | Beginning | Missing
--- | --- | --- | --- | ---
Runs without errors | 10 | 0 | 0 | 0
[Style](../../style.md)* | 10 | 7 | 3 | 0
Creates a new thread | 5 | 0 | 0 | 0
Starts thread (does not call run) | 5 | 0 | 0 | 0
Joins threads | 5 | 0 | 0 | 0
Sets global SUM in sum function | 5 | 0 | 0 | 0
Asserts pass | 10 | 7 | 3 | 0


**Rubric for Assignment01-b.py**
Item | Proficient | Emerging | Beginning | Missing
--- | --- | --- | --- | ---
Runs without errors | 10 | 0 | 0 | 0
[Style](../../style.md)* | 10 | 7 | 3 | 0
Class extends threading.Thread | 5 | 0 | 0 | 0
Calls super constructor | 5 | 0 | 0 | 0
Constructor takes the number to sum | 5 | 0 | 0 | 0
Constructor creates class sum variable | 5 | 0 | 0 | 0
Asserts pass | 10 | 7 | 3 | 0

*For the first few assignments, more feedback will be given on style issues, rather than point deductions, to help you figure out the expectations.

Assignments are not accepted late. Instead, you should submit what you have completed by the due date for partial credit.

Assignments are individual and not team based.  Any assignments found to be plagiarized will be graded according to the `ACADEMIC HONESTY` section in the syllabus. Personalize your code by adding comments explaining how your code works. This provides evidence that you wrote it yourself. You are allowed to work with other students, but your comments need to be in your own words.

## Submission

When finished, upload your Python file to Canvas (please no ZIP files).
