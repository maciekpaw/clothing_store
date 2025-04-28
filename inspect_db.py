import sqlite3

# Connect to the store.db SQLite database
conn = sqlite3.connect('store.db')
cursor = conn.cursor()

# List all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:", tables)

# Check the contents of the 'user' table
cursor.execute("SELECT * FROM user;")
users = cursor.fetchall()
print("Users in the database:", users)

conn.close()
