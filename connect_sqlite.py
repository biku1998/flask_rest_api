# provide sqlite cursor

import sqlite3

DB_PATH = "data.db"

def get_connection():
    return sqlite3.connect(DB_PATH)



# this file will also be used to create tables

if __name__ == "__main__":
    connection = get_connection()
    
    cursor = connection.cursor()

    queries = [
    "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,username text,password text)",
    "CREATE TABLE IF NOT EXISTS items(name text PRIMARY KEY,price real)"
    ]

    _ = [cursor.execute(query) for query in queries]

    connection.commit()
    connection.close()

