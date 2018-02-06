import psycopg2
import psycopg2.extras
import Creds

class ocelliDb():
    def __init__(self):
        self.username = Creds.username
        self.password = Creds.password
        self.db_name = Creds.db_name

    def connect(self):
        conn_string = "dbname = '%s' user= '%s' host = '10.1.10.131' password = '%s'" % (self.db_name, self.username, self.password)
        self.connection = psycopg2.connect(conn_string)
        # use DictCursor so we can access columns by their name
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def query(self, query, *args):
        self.connect()
        rows = []
        try:
            #print self.cursor.mogrify(query, args)
            self.cursor.execute(query, args)
            rows = self.cursor.fetchall()

        except psycopg2.Error, e:
            pass

        self.connection.commit()
        self.connection.close()
        return rows

