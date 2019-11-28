import time
import uuid
from multiprocessing import Process
from random import randint

from tarantool import Connection
from multiprocessing import current_process


def produce(table: str):
    tnt_connection = Connection("127.0.0.1", 3302)
    trace(table, "Produce start")
    start = time.perf_counter_ns()
    for row in range(0, 100000, 1):
        next_id = tnt_connection.call("box.sequence.test_seq:next")
        tnt_connection.insert(table, (str(uuid.uuid1()), next_id[0], "TestBook_" + str(row), randint(1900, 2000)))
        if row % 1000 == 0:
            trace(table, "Done insert row: {}".format(row))
    end = time.perf_counter_ns()
    table_size = tnt_connection.call("box.space.{}:len".format(table))
    diff = (end - start) / 1000.0
    trace(table, "Completed, table size: {}, time spent: {}"
          .format(table_size[0], diff))
    return diff


def run_requests(table: str, debug: bool = True):
    tnt_connection = Connection("127.0.0.1", 3302)
    trace(table, "Run requests")
    ids = get_ids(tnt_connection, table, 1000)
    start = time.perf_counter_ns()
    row = 0
    for item in ids:
        result = tnt_connection.select(table, [item])
        if row % 100 == 0 and debug:
            trace(table, "Request completed: {}, last result: {}".format(row, result[0]))
        row += 1
    end = time.perf_counter_ns()
    diff = (end - start) / 1000.0
    trace(table, "Completed, request count: {}, time spent: {}"
          .format(row, diff))
    return diff


def show_samples(table: str):
    tnt_connection = Connection("127.0.0.1", 3302)
    trace(table, "Show samples")
    result = tnt_connection.select(space_name=table, offset=0, limit=10)
    for item in result:
        print(item)


def get_ids(tnt_connection: Connection, table: str, count: int):
    trace(table, "Get ids")
    table_size = tnt_connection.call("box.space.{}:len".format(table))
    offset = randint(0, table_size[0] - count)
    trace(table, "Get ids, table size: {}, offset: {}".format(table_size[0], offset))
    result = tnt_connection.select(space_name=table, offset=offset, limit=count)
    ids_data = [] * len(result)
    for item in result:
        ids_data.append(item[0])
    return ids_data


def trace(table: str, data: str):
    print("{} - {} - {}".format(current_process().name, table, data))


if __name__ == '__main__':
    # for i in range(0, 2, 1):
    #     c = Process(target=produce, name="Producer" + str(i), args=["test_tree"])
    #     c.start()
    # for i in range(0, 2, 1):
    #     c = Process(target=produce, name="Producer" + str(i), args=["test_hash"])
    #     c.start()

    # for i in range(0, 2, 1):
    #     c = Process(target=run_requests, name="Requester" + str(i), args=["test_tree"])
    #     c.start()
    # for i in range(0, 2, 1):
    #     c = Process(target=run_requests, name="Requester" + str(i), args=["test_hash"])
    #     c.start()

    avg_hash_time = 0
    avg_tree_time = 0
    try_count = 10
    for i in range(0, try_count, 1):
        avg_hash_time += run_requests("test_hash", False)
        time.sleep(2)
    avg_hash_time /= try_count

    for i in range(0, try_count, 1):
        avg_tree_time += run_requests("test_tree", False)
        time.sleep(2)
    avg_tree_time /= try_count

    print("Average tree get time: {}".format(avg_tree_time))
    print("Average hash get time: {}".format(avg_hash_time))
