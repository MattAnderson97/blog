import sqlite3


class DatabaseController:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.conn_open = False

    def open_conn(self):
        if !self.conn_open:
            self.conn = sqlite3.connect(self.db_name)
            self.conn_open = True
    
    def close_conn(self):
        if self.conn_open and self.conn is not None:
            self.conn.close()
            self.conn_open = False

    def create_table(self, name, *args):
        rows = args.join(", ")
        query = f"create table {name} ({args})"


    def execute_query(self, query, data):
        cur = self.conn.cursor()
        cur.execute(query, data)
        self.conn.commit()
        return cur.fetchall()