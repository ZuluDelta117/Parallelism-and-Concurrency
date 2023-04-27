![](../../banner.png)

# 06 Prove: Video Frame Processing

## Overview

You will be finishing [Team06](../team/team06.md), if your team did not finish it. Then you will be modifying it to run using a range of processes and plotting the results.

Download the [assignment06.py](assignment06.py) file and read the requirements.

## Project Description

Your program will need to process all 300 frames using starting with 1 CPU core. You will need to keep track of the time it took to process all of the frames.  (See the main code for the variables that will be used.)

Then, you will process all of the frames using 2 CPU cores and record the time it took.  Then 3 CPU cores, 4 CPU cores, etc... until you reach `CPU_COUNT` CPU cores.

On my computer, I have 8 CPU cores.  The const variable `CPU_COUNT` is set to 4 more the number of CPU cores on your computer.  So for me CPU_COUNT equals 12.  Here is a example of the plot that is created for 12 CPU cores. While your results might look slightly different, the general relationship should hold.

![](seconds_vs_cpus_300_frames.png)

## Assignment

1. Download the [assignment05.py](assignment05.py) file.
2. Review the instructions found in the Python file as well as the global constants.
4. The function `run_production()` will be passed different number of manufacturers and dealerships that are to be created for a production run.
5. You must not use the Python queue object for this assignment.  Use the provided queue class.

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

Assignments are individual and not team based.  Any assignments found to be  plagiarised will be graded according to the `ACADEMIC HONESTY` section in the syllabus. The Assignment will be graded in broad categories as outlined in the syllabus:

## Submission

When finished, upload your Python file to Canvas.

