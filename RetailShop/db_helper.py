from flask import current_app
from RetailShop import mysql

def get_db():
    """Get MySQL database connection"""
    try:
        conn = mysql.connection
        if conn is None:
            print("MySQL connection is None. Please check your database configuration.")
            return None
        return conn
    except Exception as e:
        print(f"Error getting MySQL connection: {e}")
        return None

def execute_query(query, args=(), commit=False, fetchone=False, fetchall=False):
    """Execute a MySQL query and return results"""
    try:
        connection = get_db()
        if connection is None:
            print("Database connection error. Please check your MySQL configuration.")
            print("This could be due to:")
            print("1. MySQL server is not running")
            print("2. Database 'shoptub' does not exist")
            print("3. User 'webapp' does not have access to the database")
            print("4. Password is incorrect")
            return None

        try:
            cur = connection.cursor()
            cur.execute(query, args)

            if commit:
                connection.commit()
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
            # Try to rollback if it was a commit operation
            if commit:
                try:
                    connection.rollback()
                    print("Transaction rolled back")
                except:
                    pass
            return None
    except Exception as e:
        print(f"Error with database connection: {e}")
        return None

def close_db(e=None):
    """Close MySQL database connection (handled automatically by Flask-PyMySQL)"""
    # Flask-PyMySQL handles connection closing automatically
    pass
