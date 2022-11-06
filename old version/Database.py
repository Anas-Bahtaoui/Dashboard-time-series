import sqlite3

class Database:
    """A DataBase object holds information about a database,
    makes a connection, controls flow of information in and
    of the Database.
    """

    def __init__(self, location):
        self.location = location

    def get(self, query):
        try:
            db = sqlite3.connect(self.location)
            cursor = conn.cursor()
            cursor.execute(query)

            return cursor.fetchall()

        except Exception as e:
            raise e

        finally:
            db.close()

def exampledb():
    return 0

if __name__ == '__main__':
    db = Database("/Users/mo159/OneDrive/Desktop/proj inno/data.db")