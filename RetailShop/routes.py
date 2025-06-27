import builtins
import os
import traceback

import MySQLdb
from flask import render_template, flash, redirect, url_for, session, request, logging, current_app
from passlib.hash import sha256_crypt
import timeit
import datetime
from werkzeug.utils import secure_filename
import hashlib
from RetailShop import mysql
from RetailShop.form import OrderForm, LoginForm, UpdateRegisterForm, DeveloperForm, MessageForm, RegisterForm
from RetailShop import app, not_logged_in, is_logged_in, content_based_filtering, wrappers, photos, is_admin_logged_in, \
    not_admin_logged_in
from math import ceil

@app.route('/')
def index():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'tshirt'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    tshirt = cur.fetchall()
    values = 'wallet'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    wallet = cur.fetchall()
    values = 'belt'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    belt = cur.fetchall()
    values = 'shoes'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    shoes = cur.fetchall()
    # Close Connection
    cur.close()
    return render_template('home.html', tshirt=tshirt, wallet=wallet, belt=belt, shoes=shoes, form=form)


# User Login
@app.route('/login', methods=['GET', 'POST'])
@not_logged_in
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # GEt user form
        username = form.username.data
        # password_candidate = request.form['password']
        password_candidate = form.password.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username=%s", [username])

        if result > 0:
            # Get stored value
            data = cur.fetchone()
            password = data['password']
            uid = data['id']
            name = data['name']

            # Compare password
            if sha256_crypt.verify(password_candidate, password):
                # passed
                session['logged_in'] = True
                session['uid'] = uid
                session['s_name'] = name
                x = '1'
                cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))

                return redirect(url_for('index'))

            else:
                flash('Incorrect password', 'danger')
                return render_template('login.html', form=form)

        else:
            flash('Username not found', 'danger')
            # Close connection
            cur.close()
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/out')
def logout():
    if 'uid' in session:
        # Create cursor
        cur = mysql.connection.cursor()
        uid = session['uid']
        x = '0'
        cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
        session.clear()
        flash('You are logged out', 'success')
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
@not_logged_in
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        mobile = form.mobile.data

        # Create Cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password, mobile) VALUES(%s, %s, %s, %s, %s)",
                    (name, email, username, password, mobile))

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('You are now registered and can login', 'success')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/chatting/<string:id>', methods=['GET', 'POST'])
def chatting(id):
    if 'uid' in session:
        form = MessageForm(request.form)
        # Create cursor
        cur = mysql.connection.cursor()

        # lid name
        get_result = cur.execute("SELECT * FROM users WHERE id=%s", [id])
        l_data = cur.fetchone()
        if get_result > 0:
            session['name'] = l_data['name']
            uid = session['uid']
            session['lid'] = id

            if request.method == 'POST' and form.validate():
                txt_body = form.body.data
                # Create cursor
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO messages(body, msg_by, msg_to) VALUES(%s, %s, %s)",
                            (txt_body, id, uid))
                # Commit cursor
                mysql.connection.commit()

            # Get users
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()

            # Close Connection
            cur.close()
            return render_template('chat_room.html', users=users, form=form)
        else:
            flash('No permission!', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/chats', methods=['GET', 'POST'])
def chats():
    if 'lid' in session:
        id = session['lid']
        uid = session['uid']
        # Create cursor
        cur = mysql.connection.cursor()
        # Get message
        cur.execute("SELECT * FROM messages WHERE (msg_by=%s AND msg_to=%s) OR (msg_by=%s AND msg_to=%s) "
                    "ORDER BY id ASC", (id, uid, uid, id))
        chats = cur.fetchall()
        # Close Connection
        cur.close()
        return render_template('chats.html', chats=chats, )
    return redirect(url_for('login'))

@app.route('/tshirt', methods=['GET', 'POST'])
def tshirt():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'tshirt'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # Create Cursor
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))
        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('Order successful', 'success')
        return render_template('tshirt.html', tshirt=products, form=form)
    if 'view' in request.args:
        product_id = request.args['view']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        wrappered = wrappers(content_based_filtering, product_id)
        execution_time = timeit.timeit(wrappered, number=0)
        # print('Execution time: ' + str(execution_time) + ' usec')
        if 'uid' in session:
            uid = session['uid']
            # Create cursor
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM product_view WHERE user_id=%s AND product_id=%s", (uid, product_id))
            result = cur.fetchall()
            if result:
                now = datetime.datetime.now()
                now_time = now.strftime("%y-%m-%d %H:%M:%S")
                cur.execute("UPDATE product_view SET date=%s WHERE user_id=%s AND product_id=%s",
                            (now_time, uid, product_id))
            else:
                cur.execute("INSERT INTO product_view(user_id, product_id) VALUES(%s, %s)", (uid, product_id))
                mysql.connection.commit()
        return render_template('view_product.html', x=x, tshirts=product)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, tshirts=product, form=form)
    return render_template('tshirt.html', tshirt=products, form=form)

@app.route('/wallet', methods=['GET', 'POST'])
def wallet():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'wallet'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']

        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # Create Cursor
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))
        # Commit cursor
        mysql.connection.commit()
        # Close Connection
        cur.close()

        flash('Order successful', 'success')
        return render_template('wallet.html', wallet=products, form=form)
    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        products = curso.fetchall()
        return render_template('view_product.html', x=x, tshirts=products)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, tshirts=product, form=form)
    return render_template('wallet.html', wallet=products, form=form)

@app.route('/belt', methods=['GET', 'POST'])
def belt():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'belt'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # Create Cursor
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('Order successful', 'success')
        return render_template('belt.html', belt=products, form=form)
    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        products = curso.fetchall()
        return render_template('view_product.html', x=x, tshirts=products)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, tshirts=product, form=form)
    return render_template('belt.html', belt=products, form=form)

@app.route('/shoes', methods=['GET', 'POST'])
def shoes():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'shoes'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # Create Cursor
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))
        # Commit cursor
        mysql.connection.commit()
        # Close Connection
        cur.close()

        flash('Order successful', 'success')
        return render_template('shoes.html', shoes=products, form=form)
    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        products = curso.fetchall()
        return render_template('view_product.html', x=x, tshirts=products)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, tshirts=product, form=form)
    return render_template('shoes.html', shoes=products, form=form)




PER_PAGE = 10
@app.route('/admin')
@is_admin_logged_in
def admin():

    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * PER_PAGE

    # Connexion à la base de données
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        # Produits (avec pagination)
        # Compte total
        cur.execute("SELECT COUNT(*) as total FROM products")
        total_products = cur.fetchone()['total']
        total_pages = ceil(total_products / PER_PAGE)

        # Données paginées
        cur.execute("SELECT * FROM products ORDER BY id DESC LIMIT %s OFFSET %s", (PER_PAGE, offset))
        products = cur.fetchall()

        # Autres statistiques (sans pagination)
        cur.execute("SELECT COUNT(*) as total FROM users")
        total_users = cur.fetchone()['total']

        cur.execute("SELECT COUNT(*) as total FROM orders")
        total_orders = cur.fetchone()['total']

        return render_template('pages/index.html',
                               result=products,
                               row=total_products,
                               users_rows=total_users,
                               order_rows=total_orders,
                               pagination={
                                   'page': page,
                                   'per_page': PER_PAGE,
                                   'total': total_products,
                                   'total_pages': total_pages
                               }, max=builtins.max,
                                 min=builtins.min)
    finally:
        cur.close()

@app.route('/admin_login', methods=['GET', 'POST'])
@not_admin_logged_in
def admin_login():
    if request.method == 'POST':
        username = request.form['email']
        password_candidate = request.form['password']
        hashed_password = hashlib.sha256(password_candidate.encode()).hexdigest()

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            cur.execute("SELECT * FROM admin WHERE email = %s", [username])
            admin = cur.fetchone()

            if admin:
                if hashed_password == admin['password']:
                    # Mettre à jour les clés de session pour être cohérent
                    session['admin_logged_in'] = True
                    session['admin_id'] = admin['id']  # Utilisez toujours 'admin_id'
                    session['admin_name'] = admin['firstName']

                    flash('Connexion réussie', 'success')
                    return redirect(url_for('admin_profile'))  # Rediriger vers le profil
                else:
                    flash('Mot de passe incorrect', 'danger')
            else:
                flash('Email administrateur introuvable', 'danger')

        except Exception as e:
            flash(f'Erreur: {str(e)}', 'danger')
        finally:
            cur.close()

    return render_template('pages/login.html')


@app.route('/admin_out')
def admin_logout():
    if 'admin_logged_in' in session:
        session.clear()
        return redirect(url_for('admin_login'))
    return redirect(url_for('admin'))


@app.route('/admin_profile')
@is_admin_logged_in
def admin_profile():
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # 1. Récupérer les infos admin
        cur.execute("SELECT * FROM admin WHERE id = %s", [session['admin_id']])
        admin = cur.fetchone()

        if not admin:
            flash('Profil administrateur introuvable', 'danger')
            return redirect(url_for('admin_login'))


        return render_template('pages/admin_profile.html',
                               admin=admin)

    except Exception as e:
        flash(f'Erreur: {str(e)}', 'danger')
        return redirect(url_for('admin'))
    finally:
        if 'cur' in locals():
            cur.close()

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
UPLOAD_FOLDER = os.path.join('static', 'images', 'admin')  # Changé 'image' en 'images'
MAX_FILE_SIZE = 16 * 1024 * 1024
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/update_admin_profile', methods=['GET', 'POST'])
@is_admin_logged_in
def update_admin_profile():
    # Define UPLOAD_FOLDER dynamically within the route using current_app.root_path
    # This ensures the path is always absolute relative to your application's root directory.
    UPLOAD_FOLDER_ABSOLUTE = os.path.join(current_app.root_path, 'static', 'image', 'admin')

    if request.method == 'GET':
        # ... (your GET logic remains the same)
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            cur.execute("SELECT * FROM admin WHERE id = %s", [session['admin_id']])
            admin = cur.fetchone()
        except Exception as e:
            flash(f"Erreur lors de la récupération du profil: {str(e)}", "danger")
            admin = None
        finally:
            cur.close()

        if not admin:
            flash("Profil administrateur introuvable.", "danger")
            return redirect(url_for('admin_dashboard'))

        return render_template('pages/edit_admin_profile.html', admin=admin)

    if request.method == 'POST':
        cur = None
        try:
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            email = request.form['email']
            mobile = request.form.get('mobile', '')
            address = request.form.get('address', '')
            current_password = request.form['current_password']
            image_file = request.files.get('image')

            if not all([firstName, lastName, email, current_password]):
                flash('Tous les champs obligatoires doivent être remplis.', 'danger')
                return redirect(url_for('update_admin_profile'))

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Fetch only password and image_profile to avoid issues if other columns are missing during initial setup
            cur.execute("SELECT password, image_profile FROM admin WHERE id = %s", [session['admin_id']])
            admin_data = cur.fetchone()

            if not admin_data:
                flash('Administrateur introuvable ou non connecté.', 'danger')
                return redirect(url_for('update_admin_profile'))

            # Vérification du mot de passe (adaptez selon votre méthode de hachage)
            hashed_password = hashlib.sha256(current_password.encode()).hexdigest()
            if hashed_password != admin_data['password']: # Using admin_data here
                flash('Mot de passe actuel incorrect.', 'danger')
                return redirect(url_for('update_admin_profile'))

            image_profile = admin_data.get('image_profile') # Use .get() for safety

            if image_file and image_file.filename != '':
                if not allowed_file(image_file.filename):
                    flash("Format de fichier non autorisé. Formats acceptés : jpg, jpeg, png, gif.", "danger")
                    return redirect(url_for('update_admin_profile'))

                file_ext = os.path.splitext(image_file.filename)[1].lower()
                new_filename = f"admin_{session['admin_id']}{file_ext}"

                # Use the absolute path defined above
                os.makedirs(UPLOAD_FOLDER_ABSOLUTE, exist_ok=True)
                upload_path = os.path.join(UPLOAD_FOLDER_ABSOLUTE, new_filename)

                # --- Debugging Print Statements ---
                print(f"DEBUG: Tentative d'enregistrement de l'image.")
                print(f"DEBUG: Fichier: {image_file.filename}")
                print(f"DEBUG: Chemin absolu du dossier: {UPLOAD_FOLDER_ABSOLUTE}")
                print(f"DEBUG: Chemin complet de sauvegarde: {upload_path}")
                # --- End Debugging Print Statements ---

                try:
                    image_file.save(upload_path)
                    print(f"DEBUG: Image enregistrée avec succès: {upload_path}")

                    # Delete old image if it's not the default one and different from new
                    if image_profile and image_profile != 'default_admin.png' and image_profile != new_filename:
                        old_image_path = os.path.join(UPLOAD_FOLDER_ABSOLUTE, image_profile)
                        if os.path.exists(old_image_path):
                            try:
                                os.remove(old_image_path)
                                print(f"DEBUG: Ancienne image supprimée: {old_image_path}")
                            except OSError as remove_err: # Catch specific OSError for file ops
                                print(f"WARNING: Impossible de supprimer l'ancienne image {old_image_path}: {remove_err}")

                    image_profile = new_filename # Update the filename to store in DB

                except Exception as save_error:
                    print(f"ERREUR CRITIQUE: Erreur lors de l'enregistrement du fichier: {save_error}")
                    print(f"TRACEBACK: {traceback.format_exc()}")
                    flash(f"Impossible d'enregistrer l'image. Vérifiez les permissions du dossier: {str(save_error)}", "danger")
                    return redirect(url_for('update_admin_profile'))
            else:
                print("DEBUG: Pas de fichier image soumis ou fichier vide.")


            # Mise à jour en base de données
            cur.execute("""
                UPDATE admin SET
                    firstName = %s,
                    lastName = %s,
                    email = %s,
                    mobile = %s,
                    address = %s,
                    image_profile = %s
                WHERE id = %s
            """, (firstName, lastName, email, mobile, address, image_profile, session['admin_id']))

            mysql.connection.commit()

            session['admin_name'] = firstName
            session['admin_image'] = image_profile

            flash('Profil mis à jour avec succès.', 'success')

        except Exception as e:
            if cur:
                mysql.connection.rollback()
            flash(f'Une erreur est survenue lors de la mise à jour du profil : {str(e)}', 'danger')
            print(f"Erreur générale de mise à jour: {traceback.format_exc()}")
        finally:
            if cur:
                cur.close()

        return redirect(url_for('admin_profile'))


PER_PAGE = 10  # Nombre de commandes par page
@app.route('/orders')
@is_admin_logged_in
def orders():
    # Pagination
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * PER_PAGE

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        # Comptage total des commandes
        cur.execute("SELECT COUNT(*) as total FROM orders")
        total_orders = cur.fetchone()['total']
        total_pages = ceil(total_orders / PER_PAGE)

        # Commandes paginées
        cur.execute("SELECT * FROM orders ORDER BY odate DESC LIMIT %s OFFSET %s", (PER_PAGE, offset))
        orders = cur.fetchall()

        # Autres statistiques (optionnel)
        cur.execute("SELECT COUNT(*) as total FROM products")
        num_rows = cur.fetchone()['total']

        cur.execute("SELECT COUNT(*) as total FROM users")
        users_rows = cur.fetchone()['total']

        return render_template('pages/all_orders.html',
                               result=orders,
                               row=num_rows,
                               order_rows=total_orders,
                               users_rows=users_rows,
                               pagination={
                                   'page': page,
                                   'per_page': PER_PAGE,
                                   'total': total_orders,
                                   'total_pages': total_pages
                               })
    finally:
        cur.close()

@app.route('/order/<int:order_id>/manage', methods=['GET', 'POST'])
def manage_order(order_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
                SELECT o.*,
                       u.name as user_name,
                       u.email as user_email,
                       p.pName as product_name,  
                       p.price as product_price
                FROM orders o
                LEFT JOIN users u ON o.uid = u.id  
                JOIN products p ON o.pid = p.id   
                WHERE o.id = %s
            """, (order_id,))
    order = cursor.fetchone()

    if not order:
        flash("Commande introuvable.", "danger")
        return redirect(url_for('orders'))

    if request.method == 'POST':
        action = request.form.get("action")
        if action == "complete":
            cursor.execute("UPDATE orders SET dstatus = %s WHERE id = %s", ('Traité', order_id))
            mysql.connection.commit()
            flash('Commande marquée comme traitée.', 'success')
        elif action == "cancel":
            cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
            mysql.connection.commit()
            flash('Commande annulée.', 'warning')
        return redirect(url_for('orders'))

    return render_template('pages/manage_order.html', order=order)



@app.route('/users')
@is_admin_logged_in
def users():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM products")
    order_rows = curso.execute("SELECT * FROM orders")
    users_rows = curso.execute("SELECT * FROM users")
    result = curso.fetchall()
    return render_template('pages/all_users.html', result=result, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)


@app.route('/statistiques')
@is_admin_logged_in
def statistiques():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  # Important pour avoir des dictionnaires
    stats_data = {}

    try:
        # 1. Total Number of Users
        cur.execute("SELECT COUNT(id) FROM users")
        stats_data['total_users'] = cur.fetchone()['COUNT(id)']

        # 2. Total Number of Products
        cur.execute("SELECT COUNT(id) FROM products")
        stats_data['total_products'] = cur.fetchone()['COUNT(id)']

        # 3. Total Number of Orders
        cur.execute("SELECT COUNT(id) FROM orders")
        stats_data['total_orders'] = cur.fetchone()['COUNT(id)']

        # 4. Number of Online Users
        cur.execute("SELECT COUNT(id) FROM users WHERE online = '1'")
        stats_data['online_users'] = cur.fetchone()['COUNT(id)']

        # 5. Orders by Category (for a chart)
        # Assuming products table has 'category' and orders table links to products via 'pid'
        cur.execute("""
            SELECT p.category as label, COUNT(o.id) as value
            FROM orders o
            JOIN products p ON o.pid = p.id
            GROUP BY p.category
            ORDER BY value DESC
        """)
        stats_data['orders_by_category'] = cur.fetchall()

        # 6. Product Distribution - Format adapté pour Morris Donut
        cur.execute("""
            SELECT category as label, COUNT(id) as value
            FROM products
            GROUP BY category
            ORDER BY value DESC
        """)
        stats_data['products_by_category'] = cur.fetchall()

    except Exception as e:
        flash(f'Erreur lors de la récupération des statistiques: {str(e)}', 'danger')
        stats_data = {
            'orders_by_category': [],
            'products_by_category': []
        }
    finally:
        cur.close()

    return render_template('pages/statistics.html', stats=stats_data)

@app.route('/admin_add_product', methods=['POST', 'GET'])
@is_admin_logged_in
def admin_add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form['price']
        description = request.form['description']
        available = request.form['available']
        category = request.form['category']
        item = request.form['item']
        code = request.form['code']
        file = request.files['picture']
        if name and price and description and available and category and item and code and file:
            pic = file.filename
            photo = pic.replace("'", "")
            picture = photo.replace(" ", "_")
            if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                save_photo = photos.save(file, folder=category)
                if save_photo:
                    # Create Cursor
                    curs = mysql.connection.cursor()
                    curs.execute("INSERT INTO products(pName,price,description,available,category,item,pCode,picture)"
                                 "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                                 (name, price, description, available, category, item, code, picture))
                    mysql.connection.commit()
                    product_id = curs.lastrowid
                    curs.execute("INSERT INTO product_level(product_id)" "VALUES(%s)", [product_id])
                    if category == 'tshirt':
                        level = request.form.getlist('tshirt')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # Commit cursor
                            mysql.connection.commit()
                    elif category == 'wallet':
                        level = request.form.getlist('wallet')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # Commit cursor
                            mysql.connection.commit()
                    elif category == 'belt':
                        level = request.form.getlist('belt')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # Commit cursor
                            mysql.connection.commit()
                    elif category == 'shoes':
                        level = request.form.getlist('shoes')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # Commit cursor
                            mysql.connection.commit()
                    else:
                        flash('Product level not fund', 'danger')
                        return redirect(url_for('admin_add_product'))
                    # Close Connection
                    curs.close()

                    flash('Product added successful', 'success')
                    return redirect(url_for('admin_add_product'))
                else:
                    flash('Picture not save', 'danger')
                    return redirect(url_for('admin_add_product'))
            else:
                flash('File not supported', 'danger')
                return redirect(url_for('admin_add_product'))
        else:
            flash('Please fill up all form', 'danger')
            return redirect(url_for('admin_add_product'))
    else:
        return render_template('pages/add_product.html')


@app.route('/edit_product', methods=['POST', 'GET'])
@is_admin_logged_in
def edit_product():
    if 'id' in request.args:
        product_id = request.args['id']
        curso = mysql.connection.cursor()
        res = curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        curso.execute("SELECT * FROM product_level WHERE product_id=%s", (product_id,))
        product_level = curso.fetchall()
        if res:
            if request.method == 'POST':
                name = request.form.get('name')
                price = request.form['price']
                description = request.form['description']
                available = request.form['available']
                category = request.form['category']
                item = request.form['item']
                code = request.form['code']
                file = request.files['picture']
                # Create Cursor
                if name and price and description and available and category and item and code and file:
                    pic = file.filename
                    photo = pic.replace("'", "")
                    picture = photo.replace(" ", "")
                    if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                        file.filename = picture
                        save_photo = photos.save(file, folder=category)
                        if save_photo:
                            # Create Cursor
                            cur = mysql.connection.cursor()
                            exe = curso.execute(
                                "UPDATE products SET pName=%s, price=%s, description=%s, available=%s, category=%s, item=%s, pCode=%s, picture=%s WHERE id=%s",
                                (name, price, description, available, category, item, code, picture, product_id))
                            if exe:
                                if category == 'tshirt':
                                    level = request.form.getlist('tshirt')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        mysql.connection.commit()
                                elif category == 'wallet':
                                    level = request.form.getlist('wallet')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        mysql.connection.commit()
                                elif category == 'belt':
                                    level = request.form.getlist('belt')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        mysql.connection.commit()
                                elif category == 'shoes':
                                    level = request.form.getlist('shoes')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        mysql.connection.commit()
                                else:
                                    flash('Product level not fund', 'danger')
                                    return redirect(url_for('admin_add_product'))
                                flash('Product updated', 'success')
                                return redirect(url_for('edit_product'))
                            else:
                                flash('Data updated', 'success')
                                return redirect(url_for('edit_product'))
                        else:
                            flash('Pic not upload', 'danger')
                            return render_template('pages/edit_product.html', product=product,
                                                   product_level=product_level)
                    else:
                        flash('File not support', 'danger')
                        return render_template('pages/edit_product.html', product=product,
                                               product_level=product_level)
                else:
                    flash('Fill all field', 'danger')
                    return render_template('pages/edit_product.html', product=product,
                                           product_level=product_level)
            else:
                return render_template('pages/edit_product.html', product=product, product_level=product_level)
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/search', methods=['POST', 'GET'])
def search():
    form = OrderForm(request.form)
    if 'q' in request.args:
        q = request.args['q']
        # Create cursor
        cur = mysql.connection.cursor()
        # Get message
        query_string = "SELECT * FROM products WHERE pName LIKE %s ORDER BY id ASC"
        cur.execute(query_string, ('%' + q + '%',))
        products = cur.fetchall()
        # Close Connection
        cur.close()
        flash('Showing result for: ' + q, 'success')
        return render_template('search.html', products=products, form=form)
    else:
        flash('Search again', 'danger')
        return render_template('search.html')



@app.route('/profile')
@is_logged_in
def profile():
    if 'user' in request.args:
        q = request.args['user']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM users WHERE id=%s", (q,))
        result = curso.fetchone()
        if result:
            if result['id'] == session['uid']:
                curso.execute("SELECT * FROM orders WHERE uid=%s ORDER BY id ASC", (session['uid'],))
                res = curso.fetchall()
                return render_template('profile.html', result=res)
            else:
                flash('Unauthorised', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


@app.route('/settings', methods=['POST', 'GET'])
@is_logged_in
def settings():
    form = UpdateRegisterForm(request.form)
    if 'user' in request.args:
        q = request.args['user']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM users WHERE id=%s", (q,))
        result = curso.fetchone()
        if result:
            if result['id'] == session['uid']:
                if request.method == 'POST' and form.validate():
                    name = form.name.data
                    email = form.email.data
                    password = sha256_crypt.encrypt(str(form.password.data))
                    mobile = form.mobile.data

                    # Create Cursor
                    cur = mysql.connection.cursor()
                    exe = cur.execute("UPDATE users SET name=%s, email=%s, password=%s, mobile=%s WHERE id=%s",
                                      (name, email, password, mobile, q))
                    if exe:
                        flash('Profile updated', 'success')
                        return render_template('user_settings.html', result=result, form=form)
                    else:
                        flash('Profile not updated', 'danger')
                return render_template('user_settings.html', result=result, form=form)
            else:
                flash('Unauthorised', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


@app.route('/developer', methods=['POST', 'GET'])
def developer():
    form = DeveloperForm(request.form)
    if request.method == 'POST' and form.validate():
        q = form.id.data
        curso = mysql.connection.cursor()
        result = curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        if result > 0:
            x = content_based_filtering(q)
            wrappered = wrappers(content_based_filtering, q)
            execution_time = timeit.timeit(wrappered, number=0)
            seconds = ((execution_time / 1000) % 60)
            return render_template('developer.html', form=form, x=x, execution_time=seconds)
        else:
            nothing = 'Nothing found'
            return render_template('developer.html', form=form, nothing=nothing)
    else:
        return render_template('developer.html', form=form)


@app.route('/admin_search', methods=['GET'])
@is_admin_logged_in  # Assurez-vous que seul l'admin peut accéder
def admin_search():
    search_term = request.args.get('q', '').strip()

    if not search_term:
        flash('Veuillez entrer un terme de recherche', 'warning')
        return redirect(url_for('admin'))  # Retour au dashboard admin

    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Recherche dans les produits (nom, description, catégorie, code)
        query = """
            SELECT id, pName as name, price, category, available, pCode as code 
            FROM products 
            WHERE pName LIKE %s 
               OR description LIKE %s 
               OR category LIKE %s
               OR pCode LIKE %s
            ORDER BY id DESC
            LIMIT 20
        """
        search_pattern = f"%{search_term}%"
        cur.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
        products = cur.fetchall()

        # Recherche dans les utilisateurs si besoin
        user_query = "SELECT id, name, email FROM users WHERE name LIKE %s OR email LIKE %s LIMIT 5"
        cur.execute(user_query, (search_pattern, search_pattern))
        users = cur.fetchall()

        # Recherche dans les commandes si besoin
        order_query = """
            SELECT o.id, o.ofname as customer, o.oplace as address, o.dstatus as status, 
                   p.pName as product_name 
            FROM orders o
            LEFT JOIN products p ON o.pid = p.id
            WHERE o.ofname LIKE %s OR o.oplace LIKE %s OR p.pName LIKE %s
            LIMIT 5
        """
        cur.execute(order_query, (search_pattern, search_pattern, search_pattern))
        orders = cur.fetchall()

        return render_template('pages/search_results.html',
                               products=products,
                               users=users,
                               orders=orders,
                               search_term=search_term)

    except Exception as e:
        flash(f'Erreur lors de la recherche: {str(e)}', 'danger')
        return redirect(url_for('admin'))
    finally:
        if cur:
            cur.close()