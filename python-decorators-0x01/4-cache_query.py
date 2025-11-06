import time
import sqlite3 
import functools


#### paste your with_db_decorator here
def with_db_connection(func):
    """ your code goes here""" 
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

query_cache = {}
#### decorator to cache query results
"""your code goes here"""
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Using cached result for query.")
            return query_cache[query]
        
        ### If no result then Execute the query and cache the result
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@cache_query
@with_db_connection
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")