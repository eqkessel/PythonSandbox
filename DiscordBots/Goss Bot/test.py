import os
# import signal
# import time

# class blah:
#     def __init__(self):
#         self.running_flag = True

#     def signalHandler(self,signum, handler):
#         print(f"Signal Handler Triggered via {signum}. Handler was {handler}")
#         print(time.time())
#         running_flag = False

# thing = blah()

# signal.signal(signal.SIGINT, thing.signalHandler)
# signal.signal(signal.SIGTERM, thing.signalHandler)

# print(f"Process ID is {os.getpid()}")

# print(f"Entering loop at {time.time()}")
# while thing.running_flag:
#     time.sleep(1)

# print(f"Exited loop.")

import signal
import time
import PrinTee

class GracefulKiller:
    def __init__(self):
        self.kill_now = False
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self,signum, frame):
        self.kill_now = True

if __name__ == '__main__':
    PrinTee.start_printee_logging()
    
    killer = GracefulKiller()
    print(f"Process ID is {os.getpid()}")
    while not killer.kill_now:
        time.sleep(1)
        print("doing something in a loop ...")

    print("End of the program. I was killed gracefully :)")