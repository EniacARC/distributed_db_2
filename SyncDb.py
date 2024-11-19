import threading
import multiprocessing

import win32api

from SynClass import Sync
from Logger import Logger
import win32event


class SyncDatabase(Sync):
    SEMAPHORE_NAME = 'SemReadWrite'
    WRITE_LOCK_NAME = 'WriteLock'

    def __init__(self, filepath: str, mode: bool, amount: int) -> None:
        """
        Initialize SyncDatabase with either threading or multiprocessing.

        :param filepath: Path to the database file.
        :param mode: If True, use threading; if False, use multiprocessing.
        :param amount: The number of concurrent readers allowed.
        """
        # Log initialization details
        if mode:
            Logger.info(f"Initializing SyncDatabase with threading. Concurrent readers allowed: {amount}")
            # semaphore: threading.Semaphore = threading.Semaphore(amount)
            # lock: threading.Lock = threading.Lock()
        else:
            Logger.info(f"Initializing SyncDatabase with multiprocessing. Concurrent readers allowed: {amount}")
            # semaphore: multiprocessing.Semaphore = multiprocessing.Semaphore(amount)
            # lock: multiprocessing.Lock = multiprocessing.Lock()
        semaphore = win32event.CreateSemaphore(None, amount, amount, self.SEMAPHORE_NAME)
        lock = win32event.CreateMutex(None, False, self.WRITE_LOCK_NAME)

        super().__init__(filepath, semaphore, lock, amount)

        # Log successful initialization
        Logger.info(f"SyncDatabase initialized for {'threading' if mode else 'multiprocessing'} mode.")

    def __del__(self):
        win32api.CloseHandle(self.semaphore)
        win32api.CloseHandle(self.lock_write)
        Logger.info("Closed lock logic handles")
