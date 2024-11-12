import re
import pickle
from typing import Optional

import win32api

from Database import Database
from Logger import Logger  # Import the Logger class
import win32event
import win32file
import win32con
import pywintypes

BUF_SIZE = 2048


class DataBase(Database):
    def __init__(self, filepath: str) -> None:
        """
        Initializes the database with the provided file path.

        :param filepath: Path to the database file.
        """
        super().__init__()
        self.__filepath = filepath
        self.change = True
        if re.search(r"\w+\.pickle$", filepath) is None:
            raise Exception("db file is not valid!")

        # if not os.path.exists(filepath):
        #     # Create the file if it doesn't exist
        #     with open(filepath, 'wb') as f:
        #         # Optionally write an initial value or leave it empty
        #         pickle.dump(self.db, f)
        #     Logger.info(f"Database file created at: {filepath}")
        # else:
        #     Logger.info(f"Database initialized from file: {filepath}")
        try:
            win32api.GetFileAttributes(filepath)
            Logger.info(f"Database initialized from file: {filepath}")
        except Exception as exc:
            han = win32file.CreateFile(filepath, win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                                       win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE, None,
                                       win32con.OPEN_ALWAYS, win32con.FILE_ATTRIBUTE_NORMAL, None)
            win32file.WriteFile(han, pickle.dumps(self.db), None)
            win32api.CloseHandle(han)
            Logger.info(f"Database file created at: {filepath}")

    def __read_data(self, file_handle):
        data = b''

        try:
            while True:
                code, buf = win32file.ReadFile(file_handle, BUF_SIZE, None)
                if not buf:
                    break

                data += buf
        except Exception as exc:
            Logger.error(f"exception has occurred when reading file: {exc}")
        finally:
            return data

    def __load_dict(self) -> None:
        """
        Loads the dictionary from the file if changes have been made.

        This method will only load the data if it hasn't been loaded already (i.e., `self.change` is `True`).
        """
        if self.change:
            # with open(self.__filepath, "rb") as f:
            f = win32file.CreateFile(self.__filepath, win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                                     win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE, None,
                                     win32con.OPEN_EXISTING, win32con.FILE_ATTRIBUTE_NORMAL, None)
            data = self.__read_data(f)
            self.db = pickle.loads(data)

            self.change = False
            Logger.info(f"Database loaded from file: {self.__filepath}")

            win32api.CloseHandle(f)

    def __write_to_file(self) -> None:
        """
        Writes the current database dictionary to the file.

        This method updates the file with the current state of `self.db`.
        """
        f = win32file.CreateFile(self.__filepath, win32con.GENERIC_WRITE | win32con.GENERIC_WRITE,
                                 win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE, None,
                                 win32con.OPEN_EXISTING, win32con.FILE_ATTRIBUTE_NORMAL, None)
        dumped = pickle.dumps(self.db)
        try:
            win32file.WriteFile(f, dumped, None)
        except Exception as exc:
            Logger.error(f"error while writing {exc}")
        finally:
            win32api.CloseHandle(f)
            self.change = True
            Logger.info(f"Database written to file: {self.__filepath}")

    def get_value(self, key: str) -> Optional[object]:
        """
        Retrieves a value associated with the given key.

        :param key: The key whose associated value is to be retrieved.
        :return: The value associated with the key or None if the key doesn't exist.
        """
        self.__load_dict()
        value = super().get_value(key)
        if value is not None:
            Logger.info(f"Retrieved value for key: {key} - {value}")
        else:
            Logger.warning(f"Key not found for get_value: {key}")
        return value

    def set_value(self, key: str, val: object) -> bool:
        """
        Sets the value associated with the given key.

        :param key: The key to set the value for.
        :param val: The value to associate with the key.
        :return: True if the value was set successfully, False otherwise.
        """
        self.__load_dict()
        success = super().set_value(key, val)
        if success:
            self.__write_to_file()
            Logger.info(f"Set value for key: {key} to {val}")
        else:
            Logger.warning(f"Failed to set value for key: {key}")
        return success

    def delete_value(self, key: str) -> None:
        """
        Deletes the value associated with the given key.

        :param key: The key whose associated value is to be deleted.
        """
        self.__load_dict()
        super().delete_value(key)
        self.__write_to_file()
        Logger.info(f"Deleted value for key: {key}")
