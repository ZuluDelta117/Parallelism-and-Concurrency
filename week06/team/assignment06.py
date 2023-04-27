'''
Requirements
1. Finish the team06 assignment (if necessary).
2. Change your program to process all 300 images using 1 CPU, then 2 CPUs, all the way up to the
   number of CPUs on your computer plus 4.
3. Keep track of the time it takes to process all 300 images per CPU.
4. Plot the time to process vs the number of CPUs.
   
Questions:
1. What is the relationship between the time to process versus the number of CPUs?
   Does there appear to be an asymptote? If so, what do you think the asymptote is?
   >The number on CPU and the time it takes in directly linked. The greater the CPU count the less time it takes proportionately.
   >For my computer the asymptote is about 30 seconds, but I think if I had 300 or more CPUs then the asymptote would cap at how long it
   >takes to run one image. So less than a second.  
2. Is this a CPU bound or IO bound problem? Why?
   >This is a CPU bound issue. I know this because when we increase the number of CPU the time it takes
   >to compleat the task is reduced proportionately.
3. Would threads work on this assignment? Why or why not? (guess if you need to) 
   >I tihnk threads would work, but the code would be more complex and would take longer to run.
   >This is because it would only be running on one CPU but switching between them quickly rather
   >rather than runnin on all CPU simultaneously. 
'''

from matplotlib.pylab import plt  # load plot library
from PIL import Image
import numpy as np
import timeit
import multiprocessing as mp

# 4 more than the number of cpu's on your computer
CPU_COUNT = mp.cpu_count() + 4  

FRAME_COUNT = 300

RED   = 0
GREEN = 1
BLUE  = 2


def create_new_frame(image_file, green_file, process_file):
   """ Creates a new image file from image_file and green_file """

   # this print() statement is there to help see which frame is being processed
   print(f'{process_file[-7:-4]}', end=',', flush=True)

   image_img = Image.open(image_file)
   green_img = Image.open(green_file)

   # Make Numpy array
   np_img = np.array(green_img)

   # Mask pixels 
   mask = (np_img[:, :, BLUE] < 120) & (np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)

   # Create mask image
   mask_img = Image.fromarray((mask*255).astype(np.uint8))

   image_new = Image.composite(image_img, green_img, mask_img)
   image_new.save(process_file)


if __name__ == '__main__':
   all_process_time = timeit.default_timer()

   # Use two lists: one to track the number of CPUs and the other to track
   # the time it takes to process the images given this number of CPUs.
   xaxis_cpus = []
   yaxis_times = []

   image_number = 300

   # Loop through each cpu starting at 1
   for cpu in range(1, CPU_COUNT + 1):
      start_time = timeit.default_timer()
      
      image_list = []
      # Make each processed image by combining one of each of the other images
      for i in range(1, image_number + 1):

         image_file = rf'elephant/image{i:03d}.png'
         green_file = rf'green/image{i:03d}.png'
         process_file = rf'processed/image{i:03d}.png'

         one_image = [image_file, green_file, process_file]
         image_list.append(one_image)
      
      # Using multi-processing make a new frame
      with mp.Pool(cpu) as p:
         p.starmap(create_new_frame, image_list)

      # Add the numebr of CPU's dedicated to the program to the x-axis list
      xaxis_cpus.append(cpu)

      # Display how long it takes to run program with CPU
      time = timeit.default_timer() - start_time
      print(time)

      # Add the the time to the y-axis time list
      yaxis_times.append(time)

      print(f'\nTime To Process all images with {cpu} CPU = {timeit.default_timer() - start_time}')

   print(f'Total Time for ALL processing: {timeit.default_timer() - all_process_time}')

   # create plot of results and also save it to a PNG file
   plt.plot(xaxis_cpus, yaxis_times, label=f'{FRAME_COUNT}')
   
   plt.title('CPU Core yaxis_times VS CPUs')
   plt.xlabel('CPU Cores')
   plt.ylabel('Seconds')
   plt.legend(loc='best')

   plt.tight_layout()
   plt.savefig(f'Plot for {FRAME_COUNT} frames.png')
   plt.show()
