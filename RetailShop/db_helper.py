from flask import current_app
from RetailShop import mysql

def get_db():
    """Get MySQL database connection"""
    try:
        return mysql.connection
    except Exception as e:
        print(f"Error getting MySQL connection: {e}")
        return None

def execute_query(query, args=(), commit=False, fetchone=False, fetchall=False):
    """Execute a MySQL query and return results"""
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, args)
        
        if commit:
            mysql.connection.commit()
            result = cur.rowcount
        elif fetchone:
            result = cur.fetchone()
        elif fetchall:
            result = cur.fetchall()
        else:
            result = cur.rowcount
            
        cur.close()
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        print(f"Query: {query}")
        print(f"Args: {args}")
        return None

def close_db(e=None):
    """Close MySQL database connection (handled automatically by Flask-MySQLdb)"""
    # Flask-MySQLdb handles connection closing automatically
    pass