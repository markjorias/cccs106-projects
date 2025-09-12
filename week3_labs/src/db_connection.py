import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin123",
            database="fletapp"
        )

        if connection.is_connected():
            print("Successfully connected to the database")
            return connection

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

if __name__ == '__main__':
    db_connection = connect_db()
    if db_connection:
        db_connection.close()
        print("Database connection closed.")