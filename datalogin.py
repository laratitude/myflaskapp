import sqlite3
import hashlib
import time

# Function to create the users table in SQLite
def create_user_table():
    try:
        conn = sqlite3.connect('user_security.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                email TEXT,
                password TEXT,
                failed_attempts INTEGER DEFAULT 0,
                last_login INTEGER,
                last_login_location TEXT  -- Track last login location (e.g., IP address)
            )
        ''')

        conn.commit()
        print("User table created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()

# Function to check if the user exists and their password is correct
def check_login(username, password, ip_address):
    try:
        conn = sqlite3.connect('user_security.db')
        cursor = conn.cursor()

        cursor.execute("SELECT username, password, failed_attempts, last_login_location FROM users WHERE username=?", (username,))
        user_data = cursor.fetchone()

        if user_data:
            db_password = user_data[1]
            failed_attempts = user_data[2]
            last_login_location = user_data[3]

            # Compare entered password with stored password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == db_password:
                print("Login successful!")
                reset_failed_attempts(username)  # Reset failed attempts on successful login
                return True
            else:
                print("Incorrect password!")
                track_failed_login(username, failed_attempts, ip_address)  # Track failed login attempt
                return False
        else:
            print("User not found.")
            return False
    except Exception as e:
        print(f"Error checking login: {e}")
    finally:
        conn.close()

# Function to track failed login attempts
def track_failed_login(username, failed_attempts, ip_address):
    try:
        conn = sqlite3.connect('user_security.db')
        cursor = conn.cursor()

        # Increment failed attempts
        cursor.execute("UPDATE users SET failed_attempts = ? WHERE username=?", (failed_attempts + 1, username))
        conn.commit()

        print(f"Failed login for {username}, total failed attempts: {failed_attempts + 1}")

        # If failed attempts exceed 5, create a ticket
        if failed_attempts + 1 >= 5:
            print(f"ALERT: Multiple failed login attempts detected for {username}. Generating a ticket.")
            create_ticket(username, ip_address, "Failed login attempts")

    except Exception as e:
        print(f"Error tracking failed login: {e}")
    finally:
        conn.close()

# Function to reset failed attempts after a successful login
def reset_failed_attempts(username):
    try:
        conn = sqlite3.connect('user_security.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET failed_attempts = 0 WHERE username=?", (username,))
        conn.commit()
        print(f"Failed attempts for {username} have been reset.")
    except Exception as e:
        print(f"Error resetting failed attempts: {e}")
    finally:
        conn.close()

# Function to create tickets for suspicious activity
def create_ticket(username, ip_address, issue_type):
    try:
        conn = sqlite3.connect('user_security.db')
        cursor = conn.cursor()

        # Get the current timestamp
        timestamp = int(time.time())

        cursor.execute("INSERT INTO tickets (username, ip_address, issue_type, timestamp) VALUES (?, ?, ?, ?)", 
                       (username, ip_address, issue_type, timestamp))
        conn.commit()
        print(f"Ticket created for {username} with issue {issue_type} from IP {ip_address}")

    except Exception as e:
        print(f"Error creating ticket: {e}")
    finally:
        conn.close()

