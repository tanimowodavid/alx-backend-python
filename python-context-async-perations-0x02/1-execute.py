import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params

    def __enter__(self):
        # Connect to the database
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Execute the query
        self.cursor.execute(self.query, self.params)
        # Fetch results
        self.results = self.cursor.fetchall()

        # Return the query result to the 'as' variable
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Always close the connection when done
        self.conn.close()

# --- Usage ---
with ExecuteQuery('users.db', "SELECT * FROM users WHERE age > ?", (25,)) as results:
    for row in results:
        print(row)

