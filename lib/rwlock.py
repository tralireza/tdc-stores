import threading


class ReadWriteLock:
    def __init__(self):
        self.read_ready = threading.Condition(threading.Lock())
        self.readers = 0

    def acquire_read(self):
        self.read_ready.acquire()
        try:
            self.readers += 1
        finally:
            self.read_ready.release()

    def release_read(self):
        self.read_ready.acquire()
        try:
            self.readers -= 1
            if self.readers == 0:
                self.read_ready.notify_all()
        finally:
            self.read_ready.release()

    def acquire_write(self):
        self.read_ready.acquire()
        while self.readers > 0:
            self.read_ready.wait()

    def release_write(self):
        self.read_ready.release()
