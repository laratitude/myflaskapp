import sqlite3
import time

def track_failed_login(username, ip_address):
    try:
        conn = sqlite3.connect('user_login_system.db')
        cursor = conn.cursor()

        # Get current failed attempts and last login location for the user
        cursor.execute("SELECT failed_attempts, last_login_location FROM users WHERE username=?", (username,))
        user_data = cursor.fetchone()

        if user_data:
            current_failed_attempts = user_data[0]
            last_location = user_data[1]

            # Check if the location (IP address) is different from the last location
            if last_location != ip_address:
                print(f"Login attempt from new location: {ip_address} for user {username}")

            # Increment failed attempts
            cursor.execute("UPDATE users SET failed_attempts = ?, last_login_location = ? WHERE username=?", 
                           (current_failed_attempts + 1, ip_address, username))
            conn.commit()

            # If failed attempts exceed 5, trigger an alert
            if current_failed_attempts + 1 >= 5:
                generate_alert(username, ip_address)

            print(f"Failed login for {username}, total failed attempts: {current_failed_attempts + 1}")
        else:
            print(f"User {username} does not exist.")
        
    except Exception as e:
        print(f"Error tracking failed login: {e}")
    finally:
        conn.close()

def generate_alert(username, ip_address):
    # Generate an alert for investigation
    print(f"ALERT: Multiple failed login attempts detected for user {username} from IP {ip_address}. A ticket has been created.")
    create_ticket(username, ip_address, "Failed login attempts")

def create_ticket(username, ip_address, issue_type):
    try:
        conn = sqlite3.connect('user_login_system.db')
        cursor = conn.cursor()

        # Create ticket in the tickets table
        cursor.execute("INSERT INTO tickets (username, ip_address, issue_type) VALUES (?, ?, ?)", 
                       (username, ip_address, issue_type))
        conn.commit()
        print(f"Ticket created for {username} with issue {issue_type} from IP {ip_address}")
    except Exception as e:
        print(f"Error creating ticket: {e}")
    finally:
        conn.close()
