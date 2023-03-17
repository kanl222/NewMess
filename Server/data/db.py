import logging
try:
    import queue as Queue # module re-named in Python 3
except ImportError:
    import Queue
import sqlite3
import threading
import time
import uuid
db__ = None

class Sqlite3Worker(threading.Thread):
    def __init__(self, file_name, max_queue_size=100):
        threading.Thread.__init__(self)
        self.daemon = True
        self.sqlite3_conn = sqlite3.connect(
            file_name, check_same_thread=False,
            detect_types=sqlite3.PARSE_DECLTYPES)
        self.sqlite3_cursor = self.sqlite3_conn.cursor()
        self.sql_queue = Queue.Queue(maxsize=max_queue_size)
        self.results = {}
        self.max_queue_size = max_queue_size
        self.exit_set = False
        # Token that is put into queue when close() is called.
        self.exit_token = str(uuid.uuid4())
        self.start()
        self.thread_running = True
        

    def run(self):
        execute_count = 0
        for token, query, values in iter(self.sql_queue.get, None):
            if token != self.exit_token:
                self.run_query(token, query, values)
                execute_count += 1
                # Let the executes build up a little before committing to disk
                # to speed things up.
                if (
                        self.sql_queue.empty() or
                        execute_count == self.max_queue_size):
                    self.sqlite3_conn.commit()
                    execute_count = 0
            # Only exit if the queue is empty. Otherwise keep getting
            # through the queue until it's empty.
            if self.exit_set and self.sql_queue.empty():
                self.sqlite3_conn.commit()
                self.sqlite3_conn.close()
                self.thread_running = False
                return

    def run_query(self, token, query, values):
        if query.lower().strip().startswith("select"):
            try:
                self.sqlite3_cursor.execute(query, values)
                self.results[token] = self.sqlite3_cursor.fetchall()
            except sqlite3.Error as err:
                self.results[token] = (
                    "Query returned error: %s: %s: %s" % (query, values, err))
                logging.error("Query returned error: %s: %s: %s" % (query, values, err))
        else:
            try:
                print(values)
                self.sqlite3_cursor.execute(query, values)
            except sqlite3.Error as err:
                print(err)
                logging.error(err)

    def close(self):
        """Close down the thread and close the sqlite3 database file."""
        self.exit_set = True
        self.sql_queue.put((self.exit_token, "", ""), timeout=5)
        # Sleep and check that the thread is done before returning.
        while self.thread_running:
            time.sleep(.01)  # Don't kill the CPU waiting.

    @property
    def queue_size(self):
        """Return the queue size."""
        return self.sql_queue.qsize()

    def query_results(self, token):
        delay = .001
        while True:
            if token in self.results:
                return_val = self.results[token]
                del self.results[token]
                return return_val
            time.sleep(delay)
            if delay < 8:
                delay += delay

    def execute(self, query, values=None,return_id=False):
        if self.exit_set:
            return "Exit Called"
        values = values or []
        token = str(uuid.uuid4())
        if query.lower().strip().startswith("select"):
            self.sql_queue.put((token, query, values), timeout=5)
            return self.query_results(token)
        else:
            self.sql_queue.put((token, query, values), timeout=5)


def db_session():
    global db__
    return db__



