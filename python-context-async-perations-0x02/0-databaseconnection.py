import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection when entering the 'with' block."""
        self.conn = sqlite3.connect(self.db_name)
        print("Database connection opened.")
        return self.conn  # makes the connection available inside the with block

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the database connection automatically."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

# --- Usage ---
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("Query results:", results)
