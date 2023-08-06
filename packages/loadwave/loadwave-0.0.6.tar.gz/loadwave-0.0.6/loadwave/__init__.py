import sys
import threading
import time
from colorama import Fore, Style

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
            progress_bar = self.progress_bar()
            sys.stdout.write(f"\r{self.message} [{progress_bar}]")
            sys.stdout.flush()
            time.sleep(0.1)
            self.progress += 1

    def progress_bar(self, bar_length=60):
        percent = int((self.progress / bar_length) * 100)
        bar = '=' * int(self.progress / bar_length * bar_length)
        bar = Fore.GREEN + bar.ljust(bar_length, '-') + Style.RESET_ALL
        return f"{bar}"
