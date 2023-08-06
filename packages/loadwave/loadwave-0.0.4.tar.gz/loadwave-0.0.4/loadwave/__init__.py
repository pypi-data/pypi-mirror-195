import sys
import threading
import time

class Loader:
    def __init__(self, message):
        self.message = message
        self.stop_flag = None
        self.loader_thread = None
        self.progress = 0

    def start(self):
        self.stop_flag = False
        self.loader_thread = threading.Thread(target=self.loader)
        self.loader_thread.start()

    def stop(self):
        self.stop_flag = True
        self.loader_thread.join()

    def loader(self):
        while not self.stop_flag:
            sys.stdout.write('\r' + self.message + ' [' + self.progress_bar() + ']')
            sys.stdout.flush()
            time.sleep(0.1)
            self.progress += 1

    def progress_bar(self, bar_length=20):
        percent = int((self.progress / bar_length) * 100)
        bar = '=' * int(self.progress / bar_length * bar_length)
        bar = bar.ljust(bar_length, '-')
        return f"{percent}% [{bar}]"
