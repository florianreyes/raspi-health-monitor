import sqlite3


def establish_connection(nombre_cliente):
    connection = sqlite3.connect(f"{nombre_cliente}-favaloro.db")
    cursor = connection.cursor()
    return connection, cursor


def close_connection(connection, cursor):
    cursor.close()
    connection.close()


def create_table(nombre_cliente):
    connection, cursor = establish_connection(nombre_cliente)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS mediciones (fecha INTEGER primary key, BPM INTEGER)"
    )
    connection.commit()
    close_connection(connection, cursor)


def insert_medicion(fecha, BPM, nombre_cliente):
    connection, cursor = establish_connection(nombre_cliente)
    cursor.execute("INSERT INTO mediciones VALUES (?, ?)", (fecha, BPM))
    connection.commit()
    close_connection(connection, cursor)


def query_data():
    connection, cursor = establish_connection("gonzo-floro")
    cursor.execute("SELECT * FROM mediciones")
    rows = cursor.fetchall()
    close_connection(connection, cursor)
    return rows


if __name__ == "__main__":
    # create_table("gonzo-floro")
    print(query_data())
