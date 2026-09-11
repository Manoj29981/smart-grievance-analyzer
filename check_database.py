import sqlite3

connection = sqlite3.connect("grievances.db")
cursor = connection.cursor()

cursor.execute("""
    SELECT
        id,
        grievance,
        category,
        priority,
        responsible_department,
        created_at
    FROM grievances
    ORDER BY id DESC
""")

rows = cursor.fetchall()

print("\n--- SAVED GRIEVANCES ---")

for row in rows:
    print(f"""
ID: {row[0]}
Grievance: {row[1]}
Category: {row[2]}
Priority: {row[3]}
Department: {row[4]}
Created: {row[5]}
""")

connection.close()
