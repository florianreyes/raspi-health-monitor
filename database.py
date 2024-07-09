import sqlite3

class Schema:
    def __init__(self, nombre_cliente):
        self.nombre_cliente = nombre_cliente
        self.create_table()

    def establish_connection(self):
        connection = sqlite3.connect(f"{self.nombre_cliente}-favaloro.db")
        cursor = connection.cursor()
        return connection, cursor


    def close_connection(self, connection, cursor):
        cursor.close()
        connection.close()


    def create_table(self):
        connection, cursor = self.establish_connection()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS mediciones (fecha INTEGER primary key, BPM INTEGER)"
        )
        connection.commit()
        self.close_connection(connection, cursor)


    def insert_medicion(self, fecha, BPM):
        connection, cursor = self.establish_connection()
        cursor.execute("INSERT INTO mediciones VALUES (?, ?)", (fecha, BPM))
        connection.commit()
        self.close_connection(connection, cursor)


    def query_data(self):
        connection, cursor = self.establish_connection()
        cursor.execute("SELECT * FROM mediciones ORDER BY fecha DESC LIMIT 10")
        rows = cursor.fetchall()
        self.close_connection(connection, cursor)
        return rows

