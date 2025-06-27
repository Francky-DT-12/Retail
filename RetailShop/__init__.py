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
        from RetailShop.db_helper import get_db, execute_query

        # Get product details
        product = execute_query("SELECT * FROM products WHERE id=%s", (product_id,), fetchone=True)
        if not product:
            print(f"No product found with ID: {product_id}")
            return ''

        data_cat = product['category']  # get id category ex shirt
        print('Showing result for Product Id: ' + product_id)

        # Get all products in the same category
        cat_products = execute_query("SELECT * FROM products WHERE category=%s", (data_cat,), fetchall=True)
        if not cat_products:
            print(f"No products found in category: {data_cat}")
            return ''

        category_matched = len(cat_products)
        print('Total product matched: ' + str(category_matched))

        # Get product level info
        id_level = execute_query("SELECT * FROM product_level WHERE product_id=%s", (product_id,), fetchone=True)
        if not id_level:
            print(f"No product level found for ID: {product_id}")
            return ''

        recommend_id = []
        cate_level = ['v_shape', 'polo', 'clean_text', 'design', 'leather', 'color', 'formal', 'converse', 'loafer', 'hook',
                      'chain']

        for product_f in cat_products:
            f_level = execute_query("SELECT * FROM product_level WHERE product_id=%s", (product_f['id'],), fetchone=True)
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
            placeholders = ','.join(['%s'] * len(recommend_id))
            query = f'SELECT * FROM products WHERE id IN ({placeholders})'
            recommend_list = execute_query(query, recommend_id, fetchall=True)
            return recommend_list, recommend_id, category_matched, product_id
        else:
            return ''
    except Exception as e:
        print(f"Error in content_based_filtering: {e}")
        return ''

from RetailShop import routes
