from time import time

def operating_time(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        stuff = func(*args, **kwargs)
        t2 = time()-t1
        print(f'{func.__name__} ran in\n{t2} seconds')
        return stuff
    return wrapper