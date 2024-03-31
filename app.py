import psycopg2

def connect():
    conn = psycopg2.connect(
        dbname="",
        user="",
        password="",
        host="",
        port=""
    )
    return conn

def create_clients_table():
    connection = connect()
    cursor = connection.cursor()
    create_table_query = '''CREATE TABLE IF NOT EXISTS clients (
                                id SERIAL PRIMARY KEY,
                                first_name TEXT,
                                last_name TEXT,
                                email TEXT,
                                phones TEXT[]
                            )'''
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()

def add_client(first_name, last_name, email, phones=None):
    connection = connect()
    cursor = connection.cursor()
    insert_query = '''INSERT INTO clients (first_name, last_name, email, phones)
                      VALUES (%s, %s, %s, %s)'''
    cursor.execute(insert_query, (first_name, last_name, email, phones))
    connection.commit()
    cursor.close()
    connection.close()

def add_phone(client_id, phone_number):
    connection = connect()
    cursor = connection.cursor()
    update_query = '''UPDATE clients
                      SET phones = array_append(phones, %s)
                      WHERE id = %s'''
    cursor.execute(update_query, (phone_number, client_id))
    connection.commit()
    cursor.close()
    connection.close()

def update_client_info(client_id, first_name=None, last_name=None, email=None, phones=None):
    connection = connect()
    cursor = connection.cursor()
    update_query = '''UPDATE clients
                      SET first_name = COALESCE(%s, first_name),
                          last_name = COALESCE(%s, last_name),
                          email = COALESCE(%s, email),
                          phones = COALESCE(%s, phones)
                      WHERE id = %s'''
    cursor.execute(update_query, (first_name, last_name, email, phones, client_id))
    connection.commit()
    cursor.close()
    connection.close()

def delete_phone(client_id, phone_number):
    connection = connect()
    cursor = connection.cursor()
    update_query = '''UPDATE clients
                      SET phones = array_remove(phones, %s)
                      WHERE id = %s'''
    cursor.execute(update_query, (phone_number, client_id))
    connection.commit()
    cursor.close()
    connection.close()

def delete_client(client_id):
    connection = connect()
    cursor = connection.cursor()
    delete_query = '''DELETE FROM clients
                      WHERE id = %s'''
    cursor.execute(delete_query, (client_id,))
    connection.commit()
    cursor.close()
    connection.close()

def search_client(search_term):
    connection = connect()
    cursor = connection.cursor()
    search_query = '''SELECT * FROM clients
                      WHERE first_name ILIKE %s
                      OR last_name ILIKE %s
                      OR email ILIKE %s
                      OR phones @> ARRAY[%s]::varchar[]'''
    search_term = '%' + search_term + '%'  # Добавляем символы подстановки для поиска по частичным совпадениям
    cursor.execute(search_query, (search_term, search_term, search_term, search_term))
    clients = cursor.fetchall()
    cursor.close()
    connection.close()
    return clients
