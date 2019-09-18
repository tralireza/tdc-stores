import threading
import queue
import lib.rwlock


def test_multiple_reads():
    rwl = lib.rwlock.ReadWriteLock()
    data_queue = queue.Queue()

    def reader():
        rwl.acquire_read()
        data_queue.put(True)
        rwl.release_read()

    readers = [threading.Thread(target=reader) for _ in range(5)]
    [e.start() for e in readers]

    for _ in range(len(readers)):
        assert data_queue.get()


def test_wait_for_write():
    rwl = lib.rwlock.ReadWriteLock()
    data_queue = queue.Queue()

    rwl.acquire_write()

    def reader():
        rwl.acquire_read()
        data_queue.put(True)
        rwl.release_read()

    reader_thread = threading.Thread(target=reader)
    reader_thread.start()

    try:
        data_queue.get(timeout=3)
        assert False
    except queue.Empty:
        assert True

    rwl.release_write()
    assert data_queue.get()
