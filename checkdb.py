import sqlite3

# Connect to the database
conn = sqlite3.connect('C:\\Users\\OSAID$ laptop$\\Desktop\\new\\users.db')
cursor = conn.cursor()

# Query to fetch all data from the users table
cursor.execute("SELECT * FROM users")
all_data = cursor.fetchall()

# Display the data
for row in all_data:
    print(row)

# Close the connection
conn.close()
