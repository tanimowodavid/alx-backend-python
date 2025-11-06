import sqlite3 
import functools

#### decorator to manage transactions
"""your code goes here"""
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction failed unfortunately: {e}")
            raise
    return wrapper

#### paste your with_db_decorator here
def with_db_connection(func):
    @functools.wraps(func) 
    def wrapper(*args, **kwargs): 
        conn = sqlite3.connect('users.db')
        try: 
            result = func(conn, *args, **kwargs) 
        finally:
            if conn:
                conn.close() 
        return result 
    return wrapper

@transactional 
@with_db_connection
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')