from Queue import Queue
from threading import Thread
import datetime

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print(e)
            finally:
                self.tasks.task_done()

class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()


def test():
    from time import sleep

    delays = [10 for i in range(100)]

    def wait_delay(i, d):
        print('Task'+str(i)+' => Sleeping for sec: '+str(d))
        sleep(d)

    pool = ThreadPool(50)

    for i, d in enumerate(delays):
        pool.add_task(wait_delay, i+1, d)

    pool.wait_completion()


a = datetime.datetime.now()
test()
b = datetime.datetime.now()
c = b-a
print("Time spent:"+str(c.seconds)+" sec.")
