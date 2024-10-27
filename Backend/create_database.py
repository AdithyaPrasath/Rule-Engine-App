import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('rules_database.db')

# Create a cursor object
cursor = conn.cursor()

# Create the rules table
cursor.execute('''
CREATE TABLE IF NOT EXISTS rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_id TEXT NOT NULL,
    rule_expression TEXT NOT NULL,
    ast TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")




