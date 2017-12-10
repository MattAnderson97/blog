import mysql.connector
from mysql.connector import errorcode

from config import mysql_conf


class MySQLDriver:

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.db_open = False

    def open(self):
        try:
            self.conn = mysql.connector.connect(**mysql_conf)
            self.cursor = self.conn.cursor()
            self.db_open = True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Incorrect username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def close(self):
        self.cursor.close()
        self.conn.close()
        self.db_open = False

    def insert(self, query, data):
        if not self.db_open:
            self.open()
        self.cursor.execute(query, (data,))
        self.conn.commit()

    def query(self, query):
        if not self.db_open:
            self.open()
        self.cursor.execute(query)

# names = ["Matthew Anderson", "Tim Barham", "Anthony Badcock", "John Doe", "Jane Doe", "Jack Frost"]


# test connection
if __name__ == "__main__":
    # instantiate MySQL Driver class
    sql = MySQLDriver()
    # open a connection
    sql.open()

    # create a test table
    # sql.query("CREATE TABLE `TestTable` ("
    #             "  `ID` int(11) NOT NULL AUTO_INCREMENT,"
    #             "  `FirstName` varchar(20) NOT NULL, "
    #             "  `SirName` varchar(20) NOT NULL,"
    #             "  PRIMARY KEY (`ID`)"
    #             ") ENGINE=InnoDB;")

    # insert test data from names list into the table
    # query =  "INSERT INTO TestTable (FirstName, SirName) VALUES (%s, %s)"
    # for i in range(len(names)):
    #     person = names[i].split(" ")
    #     sql.insert(query, (person[0], person[1]))

    # display the contents of the test table
    sql.query("SELECT * FROM TestTable")
    print("-------------------------------------------------------")
    print("|{:11}|{:20}|{:20}|".format("ID", "SirName", "FirstName"))
    print("-------------------------------------------------------")
    for (ID, FirstName, SirName) in sql.cursor:
        print("|{:<11}|{:20}|{:20}|".format(ID, SirName, FirstName))
        print("-------------------------------------------------------")

    # close the connection
    sql.close()