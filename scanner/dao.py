import sqlite3


class SimpleDao(object):

    def __init__(self, database):
        self.con = sqlite3.connect(database)

    @staticmethod
    def iter_result(cursor, n=100):
        while True:
            chunk = cursor.fetchmany(n)
            if not chunk:
                break
            for c in chunk:
                yield c

    def process_all_uids(self, callback):
        stm = "SELECT uid FROM movies"
        cur = self.con.cursor()
        cur.execute(stm)
        for res in SimpleDao.iter_result(cur):
            callback(res[0])
