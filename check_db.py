from flask import Flask
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'webapp'
app.config['MYSQL_PASSWORD'] = 'motdepassefort'
app.config['MYSQL_DB'] = 'shoptubedb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

try:
    # Try to connect to the MySQL server
    with app.app_context():
        # Get cursor
        cursor = mysql.connection.cursor()

        # Check if the database exists
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()['DATABASE()']
        print(f"You're connected to database: {db_name}")

        # Check if the tables exist
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("Tables in the database:")
        for table in tables:
            print(f"- {table['Tables_in_' + db_name]}")

        # Check if there are products in the database
        cursor.execute("SELECT COUNT(*) as count FROM products;")
        product_count = cursor.fetchone()['count']
        print(f"Number of products in the database: {product_count}")

        # Close the connection
        cursor.close()
        print("MySQL connection check completed")

except Exception as e:
    print(f"Error while connecting to MySQL: {e}")
