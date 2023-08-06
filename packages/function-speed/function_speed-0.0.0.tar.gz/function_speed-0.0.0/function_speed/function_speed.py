from time import time

def operating_time(func):
    def wrapper(*args):
        t1 = time()
        stuff = func(*args)
        t2 = time()-t1
        print(f'{func.__name__} ran in\n{t2} seconds')
        return stuff
    return wrapper
