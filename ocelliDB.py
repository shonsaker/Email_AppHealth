import psycopg2
import psycopg2.extras
import traceback
import Creds

class ocelliDb():
    def __init__(self):
        self.module = "PDF-OcelliDB"
        self.client_id = 0
        self.username = Creds.username
        self.password = Creds.password
        self.db_name = Creds.db_name

    def connect(self):
        conn_string = f"dbname = '{self.db_name}' user= '{self.username}' host = '10.1.10.131' password = '{self.password}'"
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

        except Exception:
            traceback_message = traceback.format_exc()
            self.log_error(self.module, self.client_id, traceback_message)

        self.connection.commit()
        self.connection.close()
        return rows

    def error_query(self, query, args):
        self.connect()
        try:
            self.cursor.execute(query, args)
            self.connection.commit()
            self.connection.close()
            return 0
        except Exception:
            return 1


    def log_error(self, module, client_id, traceback_message):
        query = "insert into e1n_error_log (e1n_module, client_id, error_msg)" \
                "values(%s, %s, %s);"

        self.error_query(query, (module, client_id, traceback_message))




