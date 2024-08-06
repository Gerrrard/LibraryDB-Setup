import mysql.connector
import csv
from mysql.connector import Error

db_name = "librarydb"
books_csv_name = "Books_Data.csv"
users_csv_name = "Users_Data.csv"
transactions_csv_name = "Transactions_Data.csv"

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def read_csv_and_insert_books_to_db(connection, cursor):
    try:
        with open(books_csv_name, mode='r') as file:
            csv_reader = csv.reader(file)
            
            headers = cursor.execute(f"SHOW COLUMNS FROM books")
            columns = [row[0] for row in cursor.fetchall()]
            
            columns_str = ", ".join(columns)

            placeholders = "%s, %s, %s, %s, %s"

            sql_insert_query = f"INSERT INTO `librarydb`.`books` ({columns_str}) VALUES ({placeholders});"

            for row in csv_reader:
                cursor.execute(sql_insert_query, tuple(row[0].split(',')))

            connection.commit()
    
    except Error as e:
        print(f"Error: {e}")
        if connection.is_connected():
            connection.rollback()
    except Exception as e:
        print(f"Error: {e}")

def read_csv_and_insert_users_to_db(connection, cursor):
    try:
        with open(users_csv_name, mode='r') as file:
            csv_reader = csv.reader(file)
            
            headers = cursor.execute(f"SHOW COLUMNS FROM users")
            columns = [row[0] for row in cursor.fetchall()]
            
            columns_str = ", ".join(columns)

            placeholders = "%s, %s, %s, %s"

            sql_insert_query = f"INSERT INTO `librarydb`.`users` ({columns_str}) VALUES ({placeholders});"

            try:
                while True:
                    pair_string_concat = str(next(csv_reader)[0]) + str(next(csv_reader)[0])
                    splitting_info = pair_string_concat.split(',')
                    ready_line = (splitting_info[0], splitting_info[1], ",".join(splitting_info[2:-1])[1:-1], splitting_info[-1])

                    cursor.execute(sql_insert_query, ready_line)
            except Exception as e:
                pass

            connection.commit()
    
    except Error as e:
        print(f"Error: {e}")
        if connection.is_connected():
            connection.rollback()
    except Exception as e:
        print(f"Error: {e}")

def read_csv_and_insert_transactions_to_db(connection, cursor):
    try:
        with open(transactions_csv_name, mode='r') as file:
            csv_reader = csv.reader(file)
            
            headers = cursor.execute(f"SHOW COLUMNS FROM transactions")
            columns = [row[0] for row in cursor.fetchall()]
            
            columns_str = ", ".join(columns)

            placeholders = "%s, %s, %s, %s, %s"

            sql_insert_query = f"INSERT INTO `librarydb`.`transactions` ({columns_str}) VALUES ({placeholders});"

            for row in csv_reader:
                lineReadTuple = tuple(row[0].split(','))
                if lineReadTuple[-1] == "":
                    lst = list(lineReadTuple)
                    lst[-1] = None
                    lineReadTuple = tuple(lst)
                cursor.execute(sql_insert_query, lineReadTuple)

            connection.commit()
    
    except Error as e:
        print(f"Error: {e}")
        if connection.is_connected():
            connection.rollback()
    except Exception as e:
        print(f"Error: {e}")

def execute_sql_file(cursor, sql_file_path):
    sql_queries = read_file(sql_file_path)
    queries = sql_queries.split(';')
    for query in queries:
        query = query.strip()
        if query:
            try:
                cursor.execute(query)
                print(f"Executed query: {query}")
            except Error as e:
                print(f"Error executing query '{query}': {e}")

def initialize_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',      # Replace with your MySQL username
            password='rootpassword',  # Replace with your MySQL password
        )

        if connection.is_connected():
            print("Connected to MySQL server.")
            cursor = connection.cursor()

            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"Database '{db_name}' checked/created successfully.")

            cursor.execute(f"USE {db_name}")

            execute_sql_file(cursor, 'create-tables.sql')
            connection.commit()

        read_csv_and_insert_books_to_db(connection, cursor)
        read_csv_and_insert_users_to_db(connection, cursor)
        read_csv_and_insert_transactions_to_db(connection, cursor)

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    initialize_db()