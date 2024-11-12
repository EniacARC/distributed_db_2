from typing import Union
import threading
import multiprocessing
from DatabaseRead import DataBase
from Logger import Logger  # Import the Logger class
from ctypes.wintypes import HANDLE
import win32event


class Sync:
    def __init__(self, filepath: str, sem_read: HANDLE,
                 lock_write: HANDLE, read_amount: int) -> None:
        """
        Initializes the Sync class for controlling concurrent read/write operations.

        :param filepath: Path to the database file.
        :param sem_read: Semaphore to control read access (allows a limited number of concurrent readers).
        :param lock_write: Lock for write operations to ensure exclusive write access.
        :param read_amount: The maximum number of concurrent readers allowed.
        """
        self.semaphore = sem_read
        self.lock_write = lock_write
        self.read_amount = read_amount
        self.writer = False
        self.db = DataBase(filepath)

        # Log initialization
        Logger.info(f"Sync initialized for file: {filepath}, read_amount: {read_amount}")

    def __get_read(self, func, *args) -> object:
        """
        Handles the read operation with semaphore locking.

        :param func: The function to execute (e.g., `db.get_value`).
        :param args: Arguments to pass to the function.
        :return: The result of the function call (object).
        """
        r_value = None
        try:
            win32event.WaitForSingleObject(self.semaphore, win32event.INFINITE)
            r_value = func(*args)
        except Exception as ex:
            Logger.error(f"Read operation failed for key: {args[0]} - {ex}")
        finally:
            win32event.ReleaseSemaphore(self.semaphore, 1)
        return r_value

    def __get_write(self, func, *args) -> bool:
        """
        Handles the write operation with both semaphore and lock.

        :param func: The function to execute (e.g., `db.set_value` or `db.delete_value`).
        :param args: Arguments to pass to the function.
        :return: The result of the function call (bool).
        """
        r_value = False
        try:
            win32event.WaitForSingleObject(self.lock_write, win32event.INFINITE)  # make inf
            for _ in range(self.read_amount):
                win32event.WaitForSingleObject(self.semaphore, win32event.INFINITE)

            r_value = func(*args)
        except Exception as ex:
            Logger.error(f"Write operation failed for key: {args[0]} - {ex}")
        finally:
            win32event.ReleaseSemaphore(self.semaphore, self.read_amount)
            win32event.ReleaseMutex(self.lock_write)
        return r_value

    def get_value(self, key: str) -> object:
        """
        Retrieves a value associated with the given key.

        :param key: The key whose associated value is to be retrieved.
        :return: The value associated with the key.
        """
        result = self.__get_read(self.db.get_value, key)
        if result is not None:
            Logger.info(f"Read value for key: {key} - {result}")
        return result

    def set_value(self, key: str, val: object) -> bool:
        """
        Sets the value associated with the given key.

        :param key: The key to set the value for.
        :param val: The value to associate with the key.
        :return: True if the value was set successfully, False otherwise.
        """
        success = self.__get_write(self.db.set_value, key, val)
        if success:
            Logger.info(f"Set value for key: {key} to {val}")
        return success

    def delete_value(self, key: str) -> bool:
        """
        Deletes the value associated with the given key.

        :param key: The key whose associated value is to be deleted.
        """
        success = self.__get_write(self.db.delete_value, key)
        if success:
            Logger.info(f"Deleted value for key: {key}")
        return success
