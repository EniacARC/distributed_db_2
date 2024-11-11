from abc import ABC
from typing import Optional
from Logger import Logger  # Import the Logger class


class Database(ABC):
    def __init__(self) -> None:
        """
        Initializes an empty database dictionary.
        """
        self.db: dict[str, object] = {}
        Logger.info("Database initialized.")

    def set_value(self, key: str, val: object) -> bool:
        """
        Sets a value in the database for the specified key.

        :param key: The key associated with the value.
        :param val: The value to associate with the key.
        :return: True if the value was set successfully, otherwise False.
        """
        if not isinstance(key, str):
            Logger.warning(f"Invalid key type for set_value: {type(key)}. Expected string.")
            return False

        self.db[key] = val
        Logger.info(f"Set value for key: {key} to {val}")
        return True

    def get_value(self, key: str) -> Optional[object]:
        """
        Retrieves the value associated with the given key.

        :param key: The key whose associated value is to be retrieved.
        :return: The value associated with the key or None if the key doesn't exist.
        """
        if not isinstance(key, str):
            Logger.warning(f"Invalid key type for get_value: {type(key)}. Expected string.")
            return None

        value = self.db.get(key)
        if value is not None:
            Logger.info(f"Retrieved value for key: {key} - {value}")
        else:
            Logger.warning(f"Key not found for get_value: {key}")
        return value

    def delete_value(self, key: str) -> None:
        """
        Deletes the value associated with the given key.

        :param key: The key whose associated value is to be deleted.
        """
        if not isinstance(key, str):
            Logger.warning(f"Invalid key type for delete_value: {type(key)}. Expected string.")
            return

        if key in self.db:
            del self.db[key]
            Logger.info(f"Deleted value for key: {key}")
        else:
            Logger.warning(f"Key not found for delete_value: {key}")
