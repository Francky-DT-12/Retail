from flask import Flask, redirect, url_for, session
from flask_mysqldb import MySQL
from functools import wraps
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os


app = Flask(__name__)

app.secret_key = os.urandom(24)

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'image', 'product')

upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'image', 'product')

os.makedirs(upload_path, exist_ok=True)

photos = UploadSet('photos', IMAGES)

configure_uploads(app, photos)

mysql = MySQL()

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'webapp'
app.config['MYSQL_PASSWORD'] = 'motdepassefort'
app.config['MYSQL_DB'] = 'shoptubedb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

try:
    mysql.init_app(app)
    # Test connection
    with app.app_context():
        mysql.connection.cursor().close()
    print("MySQL connection successful!")
except Exception as e:
    print(f"Error connecting to MySQL: {e}")
    print("Please check if MySQL server is running and the credentials are correct.")
    print("Database: shoptubedb, User: webapp, Password: motdepassefort")


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('login'))

    return wrap


def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return redirect(url_for('index'))
        else:
            return f(*args, *kwargs)

    return wrap


def is_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('admin_login'))

    return wrap


def not_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return redirect(url_for('admin'))
        else:
            return f(*args, *kwargs)

    return wrap


def wrappers(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped


def content_based_filtering(product_id):
    try:
        # Check if MySQL connection is available
        if not hasattr(mysql, 'connection') or mysql.connection is None:
            print("Database connection error. Please check your MySQL configuration.")
            return ''

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))  # getting id row
        data = cur.fetchone()  # get row info
        if not data:
            print(f"No product found with ID: {product_id}")
            cur.close()
            return ''

        data_cat = data['category']  # get id category ex shirt
        print('Showing result for Product Id: ' + product_id)
        category_matched = cur.execute("SELECT * FROM products WHERE category=%s", (data_cat,))  # get all shirt category
        print('Total product matched: ' + str(category_matched))
        cat_product = cur.fetchall()  # get all row
        cur.execute("SELECT * FROM product_level WHERE product_id=%s", (product_id,))  # id level info
        id_level = cur.fetchone()
        if not id_level:
            print(f"No product level found for ID: {product_id}")
            cur.close()
            return ''

        recommend_id = []
        cate_level = ['v_shape', 'polo', 'clean_text', 'design', 'leather', 'color', 'formal', 'converse', 'loafer', 'hook',
                      'chain']
        for product_f in cat_product:
            cur.execute("SELECT * FROM product_level WHERE product_id=%s", (product_f['id'],))
            f_level = cur.fetchone()
            if not f_level:
                continue

            match_score = 0
            if f_level['product_id'] != int(product_id):
                for cat_level in cate_level:
                    if f_level[cat_level] == id_level[cat_level]:
                        match_score += 1
                if match_score == 11:
                    recommend_id.append(f_level['product_id'])
        print('Total recommendation found: ' + str(recommend_id))
        if recommend_id:
            cur = mysql.connection.cursor()
            placeholders = ','.join((str(n) for n in recommend_id))
            query = 'SELECT * FROM products WHERE id IN (%s)' % placeholders
            cur.execute(query)
            recommend_list = cur.fetchall()
            cur.close()
            return recommend_list, recommend_id, category_matched, product_id
        else:
            cur.close()
            return ''
    except Exception as e:
        print(f"Error in content_based_filtering: {e}")
        return ''

from RetailShop import routes
