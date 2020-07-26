import asyncio
import time

def f():
    while True:
        print("Hello World")
        time.sleep(1)
        # loop.run_until_complete(asyncio.sleep(1))

loop = asyncio.get_event_loop()

try:
    exe = loop.run_in_executor(None, f)
    print("Started blocking function in executor")
except KeyboardInterrupt:
    print("Stopping...")
finally:
    loop.stop()


# import asyncio

# async def greet_every_two_seconds():
#     while True:
#         print('Hello World')
#         await asyncio.sleep(2)



# # run in background
# asyncio.create_task(greet_every_two_seconds())