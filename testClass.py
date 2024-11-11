import os
import threading
from DatabaseRead import DataBase
from SyncDb import SyncDatabase  # Assuming SyncDatabase extends functionality of Sync
from Logger import Logger


# Helper function to print test results
def assert_equal(actual, expected, test_name):
    if actual == expected:
        print(f"{test_name}: Pass")
    else:
        print(f"{test_name}: Fail (Expected: {expected}, Got: {actual})")


def read_task(db, key):
    result_t = db.get_value(key)
    print(f"Read Task: {result_t}")


def write_task(db, key):
    db.set_value(key, "concurrentValue")
    print("Write Task: completed")


def main():
    Logger.setup_logger()
    # Set up a filepath, semaphore, and SyncDatabase instance
    filepath = "test_database.pickle"  # Sample filepath

    sync_db = SyncDatabase(filepath, True, 2)

    # Test 1: Setting and getting a single value
    key, value = "testKey", "testValue"
    sync_db.set_value(key, value)
    result = sync_db.get_value(key)
    print(result)
    assert_equal(result, value, "Test 1: Set and Get Single Value")

    # Test 2: Updating an existing value
    updated_value = "updatedValue"
    sync_db.set_value(key, updated_value)
    result = sync_db.get_value(key)
    assert_equal(result, updated_value, "Test 2: Update Value")

    # Test 3: Deleting a value
    sync_db.delete_value(key)
    result = sync_db.get_value(key)
    assert_equal(result, None, "Test 3: Delete Value")

    # Test 4: Invalid key type handling
    assert not sync_db.set_value(123, "value")
    assert not sync_db.get_value(123)
    assert not sync_db.delete_value(123)

    # Launch multiple threads for reading and writing
    # Test 5: Concurrent access (Simulating multiple reads and writes)

    # Set initial value
    sync_db.set_value(key, "initialValue")

    # Launch multiple threads for reading and writing
    threads = []
    for _ in range(5):  # Creating 5 read and 5 write tasks
        t_read = threading.Thread(target=read_task, args=(sync_db, key))
        t_write = threading.Thread(target=write_task, args=(sync_db, key))
        threads.append(t_read)
        threads.append(t_write)
        t_read.start()
        t_write.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Verify final state after concurrency
    final_result = sync_db.get_value(key)
    expected_final_value = "concurrentValue"
    assert_equal(final_result, expected_final_value, "Test 5: Concurrent Access Final Value")

    os.remove(filepath)


if __name__ == '__main__':
    main()
