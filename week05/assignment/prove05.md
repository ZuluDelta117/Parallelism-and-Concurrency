![](../../banner.png)

# 06 Prove: Factories and Dealerships Part 2

## Overview

You will be using queue(s) and thread semaphore(s) to synchronize many threads in the production and selling of cars.

## Project Description

This is a continuation of the previous assignment.  Instead of one manufacturer and one dealership, will have multiple of each.  The restriction of only producing `MAX_QUEUE_SIZE` is still in place for all of the dealerships.

## Assignment

1. Download the [assignment05.py](assignment05.py) file.
2. Review the instructions found in the Python file as well as the global constants.
4. The function `run_production()` will be passed different number of manufacturers and dealerships that are to be created for a production run.
5. You must not use the Python queue object for this assignment.  Use the provided queue class.

Here is a sample run of the completed assignment.  The number of cars each manufacturer produces is random:

```
Manufacturers       : 1
Dealerships         : 1
Run Time            : 4.99 sec
Max queue size      : 2
Manufacturer Stats  : [233]
Dealer Stats        : [233]

Manufacturers       : 1
Dealerships         : 2
Run Time            : 6.32 sec
Max queue size      : 2
Manufacturer Stats  : [295]
Dealer Stats        : [147, 148]

Manufacturers       : 2
Dealerships         : 1
Run Time            : 6.87 sec
Max queue size      : 10
Manufacturer Stats  : [251, 222]
Dealer Stats        : [473]

Manufacturers       : 2
Dealerships         : 2
Run Time            : 7.27 sec
Max queue size      : 6
Manufacturer Stats  : [293, 281]
Dealer Stats        : [292, 282]

Manufacturers       : 2
Dealerships         : 5
Run Time            : 7.00 sec
Max queue size      : 5
Manufacturer Stats  : [283, 211]
Dealer Stats        : [99, 99, 100, 98, 98]

Manufacturers       : 5
Dealerships         : 2
Run Time            : 14.15 sec
Max queue size      : 10
Manufacturer Stats  : [208, 294, 259, 282, 272]
Dealer Stats        : [649, 666]

Manufacturers       : 10
Dealerships         : 10
Run Time            : 26.36 sec
Max queue size      : 10
Manufacturer Stats  : [280, 234, 286, 272, 223, 241, 238, 232, 211, 232]
Dealer Stats        : [246, 244, 245, 242, 248, 246, 244, 244, 240, 250]
```


## Rubric

Item | Proficient | Emerging | Beginning | Missing
--- | --- | --- | --- | ---
Runs without errors | 20 | 0 | 0 | 0
[Style](../../style.md) | 15 | 10 | 5 | 0
Semaphore used to control queue size | 10 | 7 | 3 | 0
Semaphore used to control reading empty queue | 10 | 7 | 3 | 0
Queue size not used in IF statement | 5 | 5 | 5 | 0
Cars produced equals cars bought (assert passes) | 20 | 15 | 10 | 0
Sentinel correctly sent from manufacturer to dealership | 10 | 7 | 3 | 0
Barrier correctly used to ensure sentinel not placed prematurely on queue | 10 | 7 | 3 | 0

Assignments are not accepted late. Instead, you should submit what you have completed by the due date for partial credit.

Assignments are individual and not team based.  Any assignments found to be  plagiarized will be graded according to the `ACADEMIC HONESTY` section in the syllabus. The Assignment will be graded in broad categories as outlined in the syllabus:

## Submission

When finished, upload your Python file to Canvas.