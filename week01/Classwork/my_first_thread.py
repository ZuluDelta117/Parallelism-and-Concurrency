import threading

count_global = 0

def count(number):
    global count_global
    for x in range(number):
        count_global += 1
        print(f'{x=}')

class MyThread(threading.Thread):
    
    def __init__(self, number):
        threading.Thread.__init__(self)
        print(f'{self.name} is being created\n', end="")
        self.number = number
        self.sum = 0
    
    def run(self):
        print(f'{self.name} starting\n', end="")
        for x in range(self.number):
            self.sum += 1
        print(f'{self.name} ending\n', end="")
        
def create_threads():
    
    print("-- Process started --")

    threads = []
    for i in range(10):
        threads.append(MyThread(i))
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
        print(f'final count = {t.number}: sum = {t.sum}')

    t1 = threading.Thread(target=count, args=(10,))
    t1.start()
    # do some stuff
    t1.join()
    print(f'using threading.Thread, final count = {count_global}')



if __name__ == '__main__':
    create_threads()
    print("-- End of program --")