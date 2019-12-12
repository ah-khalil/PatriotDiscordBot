import asyncio
import sched
import time

s = sched.scheduler(time.time, time.sleep)

def check_time(func):
    def inner_func(*args, **kwargs):
        begin = time.time()

        func(*args, **kwargs)

        end = time.time()
        print("End time for {} is {}".format(func.__name__, end - begin))

    return inner_func


# def schedule_task_decorator(func):
#     def inner_func(*args, **kwargs):
#         s.enter(10, 1, func, kwargs=kwargs)
#         s.run()
#
#     return inner_func
#
#
# async def print_hello_world():
#     await asyncio.sleep(1)
#     print("Hello World")
#
#
# async def print_goodnight_world():
#     await asyncio.sleep(2)
#     print("Goodnight World")
#
#
# def kick_start(coro):
#     async def inner_func(*args, **kwargs):
#         return await coro(*args, **kwargs)
#
#     loop = asyncio.get_event_loop()
#     future_one = loop.create_task(inner_func())
#     loop.run_until_complete(future_one)
#     s.enter(10, 1, kick_start, (coro,))
#     s.run()
#
