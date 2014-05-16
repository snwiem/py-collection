import os
import sqlite3


class SimpleDao(object):

    def __init__(self, database):
        self.con = sqlite3.connect(database)
        self.create_schema()

    def create_schema(self):
        cur = self.con.cursor()
        schema = os.path.join(os.path.dirname(__file__), 'schema.sql')
        script = open(schema, 'r').read()
        cur.executescript(script)
        self.con.commit()
        cur.close()

    def select_value_id(self, table, value):
        stmt = "SELECT id FROM " + table + " WHERE name = ?"
        cur = self.con.cursor()
        cur.execute(stmt, (value,))
        row = cur.fetchone()
        return row[0] if row else None

    def insert_value(self, table, value):
        stmt = "INSERT INTO " + table + " (name) VALUES (?)"
        cur = self.con.cursor()
        cur.execute(stmt, (value,))
        id = cur.lastrowid
        cur.close()
        return id

    def map_value_id(self, table, value_column, movie_id, value_id):
        stmt = "INSERT INTO movie_" + table + " (movie_id, " + value_column + ") VALUES (?, ?)"
        cur = self.con.cursor()
        cur.execute(stmt, (movie_id, value_id))
        self.con.commit()
        cur.close()

    def insert_movie(self, obj):
        stmt = "INSERT INTO movies (uid, upc, title, original_title, sort_title, overview, rating, length, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cur = self.con.cursor()
        cur.execute(stmt,
                    (obj['id'], obj['upc'], obj['title'], obj['original_title'], obj['sort_title'], obj['overview'], obj['rating'], obj['length'], obj['year'],))
        self.con.commit()
        id = cur.lastrowid
        cur.close()
        return id

    def select_person(self, obj):
        stmt = "SELECT id FROM persons WHERE first_name = ? AND middle_name = ? AND last_name = ? AND birth_year = ?"
        cur = self.con.cursor()
        cur.execute(stmt,
                    (obj['firstname'], obj['middlename'], obj['lastname'], obj['birthyear'],))
        row = cur.fetchone()
        return row[0] if row else None

    def insert_person(self, obj):
        stmt = "INSERT INTO persons (first_name, middle_name, last_name, birth_year) VALUES (?, ?, ?, ?)"
        cur = self.con.cursor()
        cur.execute(stmt,
                    (obj['firstname'], obj['middlename'], obj['lastname'], obj['birthyear'],))
        self.con.commit()
        id = cur.lastrowid
        cur.close()
        return id

    def map_role(self, movie_id, person_id, role):
        stmt = "INSERT INTO roles (movie_id, person_id, role) VALUES (?, ?, ?)"
        cur = self.con.cursor()
        cur.execute(stmt, (movie_id, person_id, role,))
        self.con.commit()
        id = cur.lastrowid
        cur.close()
        return id

    def map_credit(self, movie_id, person_id, credit_type, credit_subtype):
        stmt = "INSERT INTO credits (movie_id, person_id, credit_type, credit_subtype) VALUES (?, ?, ?, ?)"
        cur = self.con.cursor()
        cur.execute(stmt, (movie_id, person_id, credit_type, credit_subtype,))
        self.con.commit()
        id = cur.lastrowid
        cur.close()
        return id

    def close(self):
        self.con.close()