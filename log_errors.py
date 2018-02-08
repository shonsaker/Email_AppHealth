import ocelliDB

class error_handling:
    def __init__(self):
        self.db = ocelliDB.ocelliDb()

    def log_error(self, module, client_id, traceback_message):
        query = "insert into e1n_error_log (e1n_module, client_id, error_msg)" \
                "values(%s, %s, %s);"

        self.db.error_query(query, (module, client_id, traceback_message))

