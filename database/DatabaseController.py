import sqlite3


class DatabaseController:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.conn_open = False
        self.open_conn()
        # enable foreign keys
        cur = self.conn.cursor()
        cur.execute('PRAGMA foreign_keys = ON;')

    def open_conn(self):
        if not self.conn_open:
            # create database connection
            self.conn = sqlite3.connect(self.db_name)
            self.conn_open = True
    
    def close_conn(self):
        if self.conn_open and self.conn is not None:
            # close database connection
            self.conn.close()
            self.conn_open = False

    def create_table(self, name, *args):
        rows = ', '.join(args)
        query = f"create table if not exists {name} ({rows});"
        # make sure a database connection is active
        if not self.conn_open:
            self.open_conn()
        # get database cursor
        cur = self.conn.cursor()
        cur.execute(query)
        # save changes to database
        self.conn.commit()

    def execute_query(self, query, data):
        # make sure a database connection is active
        if not self.conn_open:
            self.open_conn()
        # get database cursor
        cur = self.conn.cursor()
        cur.execute(query, data)
        # save changes to database
        self.conn.commit()
        return cur.fetchall()