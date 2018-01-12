import concurrent.futures
import time
from functools import partial
def func1(a):
        return func(*a)
def execute(func, args,threadnum = 10):
    with concurrent.futures.ProcessPoolExecutor(max_workers=threadnum) as pool:
        return [ a for a in pool.map(partial(func, args),args)]

def foo():
    time.sleep(2)
    return i*i+j*j

def f(i,j):
    print i
    print j



k = [(1,1),(2,2)]
print execute(foo,k)