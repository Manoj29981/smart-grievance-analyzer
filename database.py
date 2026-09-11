import sqlite3

DATABASE = "grievances.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():

    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS grievances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grievance TEXT NOT NULL,
            category TEXT,
            issue TEXT,
            location TEXT,
            duration TEXT,
            priority TEXT,
            responsible_department TEXT,
            sustainability_impact TEXT,
            recommended_action TEXT,
            summary TEXT,
            recurring_issue INTEGER DEFAULT 0,
            matched_grievance_id INTEGER,
            similarity_score REAL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Add recurring-detection columns if the table already existed
    columns = [
        row["name"]
        for row in connection.execute("PRAGMA table_info(grievances)").fetchall()
    ]

    if "recurring_issue" not in columns:
        connection.execute(
            "ALTER TABLE grievances ADD COLUMN recurring_issue INTEGER DEFAULT 0"
        )

    if "matched_grievance_id" not in columns:
        connection.execute(
            "ALTER TABLE grievances ADD COLUMN matched_grievance_id INTEGER"
        )

    if "similarity_score" not in columns:
        connection.execute("ALTER TABLE grievances ADD COLUMN similarity_score REAL")

    if "status" not in columns:
        connection.execute(
            "ALTER TABLE grievances ADD COLUMN status TEXT DEFAULT 'Pending'"
        )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully!")
