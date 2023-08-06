import sys
import time
import threading

class Loader:
    def __init__(self, message):
        self.message = message

    def start(self):
        self.stop_flag = False
        self.loader_thread = threading.Thread(target=self.loader)
        self.loader_thread.start()

    def stop(self):
        self.stop_flag = True
        self.loader_thread.join()

    def loader(self):
        while not self.stop_flag:
            sys.stdout.write('\r' + self.message + ' [' + self.animate() + ']')
            sys.stdout.flush()
            time.sleep(0.1)

    def animate(self):
        animation = '|/-\\'
        self.i = (self.i + 1) % 4
        return animation[self.i]

