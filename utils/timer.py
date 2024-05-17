import time
def timer(func):
    async def wrapper():
        start = time.time()
        await func()
        end = time.time() -start
        print(f'{func.__name__}.py ran {end:.2f} seconds'.upper())
    return wrapper