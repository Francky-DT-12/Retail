"""
Database manager to handle both SQLite and MySQL connections
"""
from flask import g, current_app
import sqlite3
import os
from RetailShop.config import DATABASE

def dict_factory(cursor, row):
    """Convert SQLite row to dictionary to mimic MySQL's DictCursor"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    """Get database connection (SQLite primary, MySQL fallback)"""
    db = getattr(g, '_database', None)
    if db is None:
        # Use SQLite as primary database
        if os.path.exists(DATABASE):
            db = g._database = sqlite3.connect(DATABASE)
            db.row_factory = dict_factory
            print("Connected to SQLite database")
        else:
            print(f"SQLite database not found at: {DATABASE}")
            return None
    return db

def init_db():
    """Initialize the database if it doesn't exist"""
    if not os.path.exists(DATABASE):
        print(f"Creating new SQLite database at: {DATABASE}")
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
        
        # Create empty database
        conn = sqlite3.connect(DATABASE)
        conn.close()
        print("Empty SQLite database created")
    return True

def execute_query(query, args=(), commit=False, fetchone=False, fetchall=False):
    """Execute a query and return results"""
    conn = get_db()
    if conn is None:
        print("Database connection failed")
        return None
        
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, args)
        
        if commit:
            conn.commit()
            return cursor.lastrowid
        
        if fetchone:
            return cursor.fetchone()
        
        if fetchall:
            return cursor.fetchall()
        
        return cursor
    except Exception as e:
        print(f"Database error: {e}")
        if commit:
            conn.rollback()
        return None
    finally:
        cursor.close()

def close_db(e=None):
    """Close database connection"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Initialize database on import
init_db()
