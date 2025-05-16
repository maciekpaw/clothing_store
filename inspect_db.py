import sqlite3

conn = sqlite3.connect('store.db')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:", tables)

# Show users only if table exists
if any("user" in t for t in tables):
    cursor.execute("SELECT * FROM user;")
    print("Users:", cursor.fetchall())
else:
    print("User table does not exist.")

conn.close()
