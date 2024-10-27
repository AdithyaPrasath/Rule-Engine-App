from werkzeug.security import generate_password_hash
import sqlite3

def create_user_credentials_table():
    conn = sqlite3.connect('rules_database.db')
    cursor = conn.cursor()

    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS user_credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    conn.commit()
    conn.close()

def insert_user_credentials(username, password, email):
    try:
        conn = sqlite3.connect('rules_database.db')
        cursor = conn.cursor()

        # Hash the password before inserting
        hashed_password = generate_password_hash(password)

        cursor.execute(''' 
        INSERT INTO user_credentials (username, password, email)
        VALUES (?, ?, ?)
        ''', (username, hashed_password, email))

        conn.commit()
        print(f"User '{username}' inserted successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: User '{username}' or email '{email}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Create the user_credentials table
create_user_credentials_table()

# Insert user credentials with email
insert_user_credentials('Adithya', 'Adithya01', 'adithya@example.com')
insert_user_credentials('Thanu', 'Thanu02', 'thanu@example.com')
