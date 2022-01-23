import mysql.connector
from mysql.connector import Error
import re


def clean_res(result):
    result = re.sub("[(,)']", '', result)
    return result


# connect to the server
def sql_connect(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            # passwd = user_password
        )
    except Error as e:
        print(f"The error '{e}' occured")
    return connection

# connect to a database
def database_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            # passwd = user_password,
            database=db_name
        )
    except Error as e:
        print(f"The error '{e}' occured")
    return connection

def database_create(connection, database_name):
    query = 'CREATE DATABASE ' + str(database_name)
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except Error as e:
        print(f"The error '{e}' occured")

def database_exists(connection , database_name):
    query = "SHOW DATABASES LIKE '" + database_name + "'"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False


#header: e.g. Product VARCHAR(255), Subproduct VARCHAR(255) ...
def table_create(connection, table_name, query):
    cursor = connection.cursor()
    command = "CREATE TABLE " + table_name + " ( " + query + ")"
    cursor.execute(command)


def table_exists(connection, table_name):
    query = "SHOW TABLES LIKE '" + table_name + "'"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False

# data: List of Tuples
def table_insert_many(connection, query, data, table_name):
    try:
        with connection.cursor() as cursor:
            cursor.executemany(query, data)
            connection.commit()
            return cursor.rowcount
    except Error as e:
        print(f"Failed to insert data into the table {e}")
        return False

# delete table
def table_delete(connection, table_name):
    drop_table_query = "DROP TABLE " + str(table_name)
    with connection.cursor() as cursor:
        cursor.execute(drop_table_query)

# check active policies
def check_policies(connection, table_name):
    query = "SELECT count(policy_status) FROM " + table_name + " WHERE policy_status = 'Active'"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
        result = int(clean_res(str(result)))
        return result

def check_s2(connection, table_name):
    query = "SELECT sum(s2_res) FROM " + table_name
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
        if clean_res(str(result)) == 'None':
            return 0
        result = round(float(clean_res(str(result))),2)
        return result

def check_statres(connection, table_name):
    query = "SELECT sum(statutory_res) FROM " + table_name
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
        if clean_res(str(result)) == 'None':
            return 0
        result = round(float(clean_res(str(result))),2)
        return result

def union(connection, quarter):
    query = "SHOW TABLES"
    union_query = f'CREATE TABLE {quarter} '
    tables = []
    with connection.cursor() as cursor:
        cursor.execute(query)
        for table in cursor:
            tables.append(clean_res(str(table)))
    for table in tables:
        union_query += f'SELECT * FROM {table} UNION '
    with connection.cursor() as cursor:
        cursor.execute(union_query[:-7])