import threading
'''
Requirements:
1. Create a class that extends the 'threading.Thread' class (see https://stackoverflow.com/questions/15526858/how-to-extend-a-class-in-python). This means that the class IS a thread. 
   Any objects instantiated using this class ARE threads.
2. Instantiate this thread class that computes the sum of all numbers 
   between one and that number (exclusive)

Psuedocode:
1. In your class, write a constructor (in python a constructor is __init__) and allow a number
   to be passed in as a parameter.
2. The constructor should call the parent class's constructor:
   threading.Thread.__init__(self)
3. Create a local sum variable in your constructor.
4. A thread must have a run function, so create a run function that sums from one to the 
   passed in number (inclusive).
5. In the run function, set the sum on self.
6. In main, instantiate your thread class with the a value of 10.
7. Start the thread.
8. Wait for the thread to finish.
9. Assert that thread object's sum attribute is equal to the appropriate value (see main).
10. Repeat steps 7 through 10 using a value of 13.
11. Repeat steps 7 through 10 using a value of 17.

Things to consider:
a. How do you instantiate a class and pass in arguments (see https://realpython.com/lessons/instantiating-classes/)?
b. How do you start a thread object (see this week's reading)?
c. How will you wait until the thread is done (see this week's reading)?
d. How do you get the value an object's attribute (see https://datagy.io/python-print-objects-attributes/)?
'''

class MyThread(threading.Thread):
   """
   Create a class that when called upon it will create a thread that will add all numbers up to 
   a given number.
   """

   def __init__(self, number):
      """
      Initiates the thread and calles the threading.Thread parent class
      Arg: number you would like the sum of
      """
      threading.Thread.__init__(self)
      
      print(f"{self.name} is being created\n", end="")

      self.number = number
      self.sum = 0
   
   def run(self):

      number_list = []
      # The number was including the given number rather then stopping the count at the given number so I had to
      # sebtract 1 from the given number so the intended value was not 10, 13, or 17 off respectivly. .
      numbers = -1
      print(f"{self.name} starting\n", end="")
      for x in range(self.number):
         numbers += 1
         number_list.append(numbers)
         self.sum = sum(number_list)

      print(f"{self.name} ending\n", end="")


def main():

   print("-- Process Started --")

   # Instantiate your thread class and pass in 10.
   t1 = MyThread(10)
   t1.start()
   t1.join()
   
      
   print(f"final count = {t1.number} sum = {t1.sum}")

   # Test (assert) if its sum attribute is equal to 45.
   assert t1.sum == 45, f'The sum should equal 45 but instead was {t1.sum}'
   
   # Repeat, passing in 13
   t2 = MyThread(13)
   t2.start()
   t2.join()
   
      
   print(f"final count = {t2.number} sum = {t2.sum}")


   # Check to see if the number is adding the thread correctly
   assert t2.sum == 78, f'The sum should equal 78 but instead was {t2.sum}'
   
   # Repeat, passing in 17
   t3 = MyThread(17)
   t3.start()
   t3.join()

      
   print(f"final count = {t3.number} sum = {t3.sum}")


   # Check to see if the number is adding the thread correctly
   assert t3.sum == 136, f'The sum should equal 136 but instead was {t3.sum}'

if __name__ == '__main__':
   main()
   assert threading.active_count() == 1
   print("DONE")
