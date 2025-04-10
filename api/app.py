import sqlite3
import time
from flask import Flask, jsonify, request

app = Flask(__name__)

# Function to create user table
def create_user_table():
    conn = sqlite3.connect('user_login_system.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            last_login INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Function to add user
def add_user(username):
    conn = sqlite3.connect('user_login_system.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, last_login) VALUES (?, ?)", 
                   (username, int(time.time())))
    conn.commit()
    conn.close()

# Function to get all users
def get_users():
    conn = sqlite3.connect('user_login_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# Home route
@app.route("/")
def home():
    users = get_users()
    return jsonify(users)

# Route to add a user
@app.route("/add_user", methods=["POST"])
def add_user_route():
    username = request.json.get("username")
    if username:
        add_user(username)
        return jsonify({"message": f"User {username} added successfully!"}), 200
    return jsonify({"error": "Username is required"}), 400

# Export Flask app for Vercel serverless deployment
def handler(req, res):
    return app(req, res)

if __name__ == "__main__":
    create_user_table()  # Create table if it doesn't exist
    app.run(debug=True)



