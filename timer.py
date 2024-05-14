import time
def timer(func):
    def wrapper():
        start = time.time()
        func()
        end = time.time() -start
        print(f'{func.__name__}.py ran {round(end)} seconds')
    return wrapper