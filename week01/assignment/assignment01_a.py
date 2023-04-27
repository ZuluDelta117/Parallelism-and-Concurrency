'''
Requirements:
1. Write a function that takes a number and computes the sum of all numbers between
   one and that number (exclusive). This will be the target of your thread.
2. Create a thread to run this function.
3. Assert that your sums are correct for the given number.
   
Psuedocode:
1. Create either a global SUM or create a list object in main.
2a. If using a global, then inside of your function, set the global equal to the sum.
2b. If using a list object, set the appropriate index position equal to the sum.
3. In main, create a thread to call the sum function using 10.
4. Using assert, check the expected result (see main)
5. Repeat steps 3 and 4, but use 13.
6. Repeat steps 3 and 4, but use 17.

Things to consider:
a. If using a global, what is the correct syntax for creating a thread with one argument?
   (see https://stackoverflow.com/questions/3221655/python-threading-string-arguments)
b. How do you start a thread? (see this week's reading) 
c. How will you wait until the thread is done? (see this week's reading)
d. Do threads (including the main thread) share global variables? (see https://superfastpython.com/thread-share-variables/)
e. If you use a global, how will you ensure that one thread doesn't change the value of
   your global while another thread is using it too? (We haven't learned about locks yet, so you
   won't be able to run your threads simultaneously)
f. How do you modify the value of a global variable (see https://stackoverflow.com/questions/10588317/python-function-global-variables)
g. If using a list object, how to you instantiate it with the correct number of indexes? (see https://stackoverflow.com/questions/8528178/list-of-zeros-in-python)
'''
import threading

# create global variable
SUM = 0

def count_sum(number):
   """
   This function will count all numbers 0-numer and add them together not including the given number
   Arg: number you would like the sum of
   """
   # Allow global variable to be accessed within the count_sum function
   global SUM
   number_list = []
   # Had to set global SUM to -1 instead of 0 because when I inputed 10 rather then counting 0-9 
   # like it should it would count 0-10 making each of my SUM's being 10, 13, or 17 off respectivly.
   SUM -= 1
   for x in range(number):
      SUM += 1
      number_list.append(SUM)
   SUM = sum(number_list)
   number_list.clear()
   

def main():
   """
   Create three threads to take in the argument 10, 13, and 17 and test to see if the count_sum function
   is working properly. 
   """
   # Allow global variable to be accessed within the main function
   global SUM
   print("-- Process Started --")

   t1 = threading.Thread(target=count_sum, args=(10,))
   t1.start()
   print("Thread-1 is running")
   t1.join()

   print(f'Using threading.Thread for Thread-1, final count = {SUM}')
   assert SUM == 45, f'The sum should equal 45 but instead was {SUM}'
   
   # Reset global SUM before starting next thread
   SUM = 0
   
   
   t2 = threading.Thread(target=count_sum, args=(13,))
   t2.start()
   print("Thread-2 is running")
   t2.join()

   print(f'Using threading.Thread for Thread-2, final count = {SUM}')
   assert SUM == 78, f'The sum should equal 78 but instead was {SUM}'
   
   # Reset global SUM before starting next thread
   SUM = 0


   t3 = threading.Thread(target=count_sum, args=(17,))
   t3.start()
   print("Thread-3 is running")
   t3.join()

   print(f'Using threading.Thread for Thread-3, final count = {SUM}')
   assert SUM == 136, print(f'The sum should equal 136 but instead was {SUM}')
   

if __name__ == '__main__':
   main()
   print("DONE")
