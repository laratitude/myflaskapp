import sqlite3

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('user_login_system.db')  # This will create 'user_login_system.db' in the current directory
cursor = conn.cursor()

# Create tables for users and login attempts
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    last_login INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS login_attempts (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    ip TEXT,
                    timestamp INTEGER,
                    success INTEGER)''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database created successfully!")