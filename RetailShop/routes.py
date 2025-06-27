from flask import render_template, flash, redirect, url_for, session, request, logging, g
from passlib.hash import sha256_crypt
import timeit
import datetime
from RetailShop.db_helper import execute_query, get_db, close_db
from RetailShop.form import OrderForm, LoginForm, UpdateRegisterForm, DeveloperForm, MessageForm, RegisterForm, AddToCartForm, CheckoutForm
from RetailShop import app, not_logged_in, is_logged_in, content_based_filtering, wrappers, photos, is_admin_logged_in, \
    not_admin_logged_in

# Register close_db function to be called when application context ends
app.teardown_appcontext(close_db)


@app.route('/')
def index():
    form = OrderForm(request.form)
    try:
        # Get products for different categories
        tshirt = execute_query("SELECT * FROM products WHERE category=? ORDER BY RANDOM() LIMIT 4", ('tshirt',), fetchall=True)
        wallet = execute_query("SELECT * FROM products WHERE category=? ORDER BY RANDOM() LIMIT 4", ('wallet',), fetchall=True)
        belt = execute_query("SELECT * FROM products WHERE category=? ORDER BY RANDOM() LIMIT 4", ('belt',), fetchall=True)
        shoes = execute_query("SELECT * FROM products WHERE category=? ORDER BY RANDOM() LIMIT 4", ('shoes',), fetchall=True)

        if tshirt is None or wallet is None or belt is None or shoes is None:
            flash('Database error. Please check your database configuration.', 'danger')
            return render_template('modern_home.html', tshirt=[], wallet=[], belt=[], shoes=[], form=form, db_error=True)

        return render_template('modern_home.html', tshirt=tshirt, wallet=wallet, belt=belt, shoes=shoes, form=form, db_error=False)
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
        return render_template('modern_home.html', tshirt=[], wallet=[], belt=[], shoes=[], form=form, db_error=True)


# User Login
@app.route('/login', methods=['GET', 'POST'])
@not_logged_in
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            # Get user form
            username = form.username.data
            password_candidate = form.password.data

            # Get user by username
            data = execute_query("SELECT * FROM users WHERE username=?", (username,), fetchone=True)

            if data:
                # Get stored value
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
                    execute_query("UPDATE users SET online=? WHERE id=?", (x, uid), commit=True)
                    return redirect(url_for('index'))

                else:
                    flash('Incorrect password', 'danger')
                    return render_template('login.html', form=form)

            else:
                flash('Username not found', 'danger')
                return render_template('login.html', form=form)
        except Exception as e:
            flash(f'Database error: {str(e)}', 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/out')
def logout():
    if 'uid' in session:
        try:
            uid = session['uid']
            x = '0'
            execute_query("UPDATE users SET online=? WHERE id=?", (x, uid), commit=True)
        except Exception as e:
            print(f"Error updating user online status: {e}")
            # Continue with logout even if database update fails

        session.clear()
        flash('You are logged out', 'success')
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
@not_logged_in
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            name = form.name.data
            email = form.email.data
            username = form.username.data
            password = sha256_crypt.encrypt(str(form.password.data))
            mobile = form.mobile.data

            # Insert user into database
            execute_query("INSERT INTO users(name, email, username, password, mobile) VALUES(?, ?, ?, ?, ?)",
                        (name, email, username, password, mobile), commit=True)

            flash('You are now registered and can login', 'success')

            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Database error: {str(e)}', 'danger')
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)

@app.route('/chatting/<string:id>', methods=['GET', 'POST'])
def chatting(id):
    if 'uid' in session:
        form = MessageForm(request.form)

        # lid name
        l_data = execute_query("SELECT * FROM users WHERE id=?", [id], fetchone=True)
        if l_data:
            session['name'] = l_data['name']
            uid = session['uid']
            session['lid'] = id

            if request.method == 'POST' and form.validate():
                txt_body = form.body.data
                execute_query("INSERT INTO messages(body, msg_by, msg_to) VALUES(?, ?, ?)",
                            (txt_body, id, uid), commit=True)

            # Get users
            users = execute_query("SELECT * FROM users", fetchall=True)

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
        # Get messages
        chats = execute_query("SELECT * FROM messages WHERE (msg_by=? AND msg_to=?) OR (msg_by=? AND msg_to=?) "
                    "ORDER BY id ASC", (id, uid, uid, id), fetchall=True)
        return render_template('chats.html', chats=chats)
    return redirect(url_for('login'))

@app.route('/tshirt', methods=['GET', 'POST'])
def tshirt():
    form = OrderForm(request.form)
    # Get products
    values = 'tshirt'
    products = execute_query("SELECT * FROM products WHERE category=? ORDER BY id ASC", (values,), fetchall=True)

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

        if 'uid' in session:
            uid = session['uid']
            execute_query("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(?, ?, ?, ?, ?, ?, ?)",
                         (uid, pid, name, mobile, order_place, quantity, now_time), commit=True)
        else:
            execute_query("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(?, ?, ?, ?, ?, ?)",
                         (pid, name, mobile, order_place, quantity, now_time), commit=True)

        flash('Order successful', 'success')
        return render_template('tshirt.html', tshirt=products, form=form)

    if 'view' in request.args:
        product_id = request.args['view']
        product = execute_query("SELECT * FROM products WHERE id=?", (product_id,), fetchall=True)
        x = content_based_filtering(product_id)
        wrappered = wrappers(content_based_filtering, product_id)
        execution_time = timeit.timeit(wrappered, number=0)
        # print('Execution time: ' + str(execution_time) + ' usec')

        if 'uid' in session:
            uid = session['uid']
            result = execute_query("SELECT * FROM product_view WHERE user_id=? AND product_id=?", (uid, product_id), fetchall=True)

            if result:
                now = datetime.datetime.now()
                now_time = now.strftime("%y-%m-%d %H:%M:%S")
                execute_query("UPDATE product_view SET date=? WHERE user_id=? AND product_id=?",
                            (now_time, uid, product_id), commit=True)
            else:
                execute_query("INSERT INTO product_view(user_id, product_id) VALUES(?, ?)", (uid, product_id), commit=True)

        return render_template('view_product.html', x=x, tshirts=product)

    elif 'order' in request.args:
        product_id = request.args['order']
        product = execute_query("SELECT * FROM products WHERE id=?", (product_id,), fetchall=True)
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, tshirts=product, form=form)

    return render_template('tshirt.html', tshirt=products, form=form)

@app.route('/wallet', methods=['GET', 'POST'])
def wallet():
    form = OrderForm(request.form)
    # Get products
    values = 'wallet'
    products = execute_query("SELECT * FROM products WHERE category=? ORDER BY id ASC", (values,), fetchall=True)

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

        if 'uid' in session:
            uid = session['uid']
            execute_query("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(?, ?, ?, ?, ?, ?, ?)",
                         (uid, pid, name, mobile, order_place, quantity, now_time), commit=True)
        else:
            execute_query("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(?, ?, ?, ?, ?, ?)",
                         (pid, name, mobile, order_place, quantity, now_time), commit=True)

        flash('Order successful', 'success')
        return render_template('wallet.html', wallet=products, form=form)

    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        products = execute_query("SELECT * FROM products WHERE id=?", (q,), fetchall=True)
        return render_template('view_product.html', x=x, tshirts=products)

    elif 'order' in request.args:
        product_id = request.args['order']
        product = execute_query("SELECT * FROM products WHERE id=?", (product_id,), fetchall=True)
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, tshirts=product, form=form)

    return render_template('wallet.html', wallet=products, form=form)

@app.route('/belt', methods=['GET', 'POST'])
def belt():
    form = OrderForm(request.form)
    # Get products
    values = 'belt'
    products = execute_query("SELECT * FROM products WHERE category=? ORDER BY id ASC", (values,), fetchall=True)

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

        if 'uid' in session:
            uid = session['uid']
            execute_query("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(?, ?, ?, ?, ?, ?, ?)",
                         (uid, pid, name, mobile, order_place, quantity, now_time), commit=True)
        else:
            execute_query("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(?, ?, ?, ?, ?, ?)",
                         (pid, name, mobile, order_place, quantity, now_time), commit=True)

        flash('Order successful', 'success')
        return render_template('belt.html', belt=products, form=form)

    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        products = execute_query("SELECT * FROM products WHERE id=?", (q,), fetchall=True)
        return render_template('view_product.html', x=x, tshirts=products)

    elif 'order' in request.args:
        product_id = request.args['order']
        product = execute_query("SELECT * FROM products WHERE id=?", (product_id,), fetchall=True)
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, tshirts=product, form=form)

    return render_template('belt.html', belt=products, form=form)

@app.route('/shoes', methods=['GET', 'POST'])
def shoes():
    form = OrderForm(request.form)
    # Get products
    values = 'shoes'
    products = execute_query("SELECT * FROM products WHERE category=? ORDER BY id ASC", (values,), fetchall=True)

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

        if 'uid' in session:
            uid = session['uid']
            execute_query("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(?, ?, ?, ?, ?, ?, ?)",
                         (uid, pid, name, mobile, order_place, quantity, now_time), commit=True)
        else:
            execute_query("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(?, ?, ?, ?, ?, ?)",
                         (pid, name, mobile, order_place, quantity, now_time), commit=True)

        flash('Order successful', 'success')
        return render_template('shoes.html', shoes=products, form=form)

    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        products = execute_query("SELECT * FROM products WHERE id=?", (q,), fetchall=True)
        return render_template('view_product.html', x=x, tshirts=products)

    elif 'order' in request.args:
        product_id = request.args['order']
        product = execute_query("SELECT * FROM products WHERE id=?", (product_id,), fetchall=True)
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, tshirts=product, form=form)

    return render_template('shoes.html', shoes=products, form=form)


import hashlib # You'll need to import hashlib

@app.route('/admin_login', methods=['GET', 'POST'])
@not_admin_logged_in
def admin_login():
    if request.method == 'POST':
        # Get user form
        username = request.form['email']
        password_candidate = request.form['password']

        hashed_password_candidate = hashlib.sha256(password_candidate.encode()).hexdigest()

        try:
            # Get user by username
            data = execute_query("SELECT * FROM admin WHERE email=?", [username], fetchone=True)

            if data:
                # Get stored value
                stored_password_hash = data['password']
                uid = data['id']
                name = data['firstName']

                if hashed_password_candidate == stored_password_hash:
                    session['admin_logged_in'] = True
                    session['admin_uid'] = uid
                    session['admin_name'] = name

                    return redirect(url_for('admin'))

                else:
                    flash('Incorrect password', 'danger')
                    return render_template('pages/login.html')

            else:
                flash('Username not found', 'danger')
                return render_template('pages/login.html')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
            return render_template('pages/login.html')
    return render_template('pages/login.html')


@app.route('/admin_out')
def admin_logout():
    if 'admin_logged_in' in session:
        session.clear()
        return redirect(url_for('admin_login'))
    return redirect(url_for('admin'))


@app.route('/admin')
@is_admin_logged_in
def admin():
    result = execute_query("SELECT * FROM products", fetchall=True)
    num_rows = len(result) if result else 0
    orders = execute_query("SELECT * FROM orders", fetchall=True)
    order_rows = len(orders) if orders else 0
    users = execute_query("SELECT * FROM users", fetchall=True)
    users_rows = len(users) if users else 0
    return render_template('pages/index.html', result=result, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)


@app.route('/orders')
@is_admin_logged_in
def orders():
    products = execute_query("SELECT * FROM products", fetchall=True)
    num_rows = len(products) if products else 0
    result = execute_query("SELECT * FROM orders", fetchall=True)
    order_rows = len(result) if result else 0
    users = execute_query("SELECT * FROM users", fetchall=True)
    users_rows = len(users) if users else 0
    return render_template('pages/all_orders.html', result=result, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)


@app.route('/users')
@is_admin_logged_in
def users():
    products = execute_query("SELECT * FROM products", fetchall=True)
    num_rows = len(products) if products else 0
    orders = execute_query("SELECT * FROM orders", fetchall=True)
    order_rows = len(orders) if orders else 0
    result = execute_query("SELECT * FROM users", fetchall=True)
    users_rows = len(result) if result else 0
    return render_template('pages/all_users.html', result=result, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)


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
                    # Insert product into database
                    product_id = execute_query("INSERT INTO products(pName,price,description,available,category,item,pCode,picture)"
                                 "VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                 (name, price, description, available, category, item, code, picture), commit=True)

                    execute_query("INSERT INTO product_level(product_id) VALUES(?)", [product_id], commit=True)

                    if category == 'tshirt':
                        level = request.form.getlist('tshirt')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=? WHERE product_id=?'.format(field=lev)
                            execute_query(query, (yes, product_id), commit=True)

                    elif category == 'wallet':
                        level = request.form.getlist('wallet')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=? WHERE product_id=?'.format(field=lev)
                            execute_query(query, (yes, product_id), commit=True)

                    elif category == 'belt':
                        level = request.form.getlist('belt')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=? WHERE product_id=?'.format(field=lev)
                            execute_query(query, (yes, product_id), commit=True)

                    elif category == 'shoes':
                        level = request.form.getlist('shoes')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=? WHERE product_id=?'.format(field=lev)
                            execute_query(query, (yes, product_id), commit=True)

                    else:
                        flash('Product level not fund', 'danger')
                        return redirect(url_for('admin_add_product'))

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
        product = execute_query("SELECT * FROM products WHERE id=?", (product_id,), fetchall=True)
        product_level = execute_query("SELECT * FROM product_level WHERE product_id=?", (product_id,), fetchall=True)

        if product:
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
                    picture = photo.replace(" ", "")
                    if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                        file.filename = picture
                        save_photo = photos.save(file, folder=category)
                        if save_photo:
                            # Update product in database
                            exe = execute_query(
                                "UPDATE products SET pName=?, price=?, description=?, available=?, category=?, item=?, pCode=?, picture=? WHERE id=?",
                                (name, price, description, available, category, item, code, picture, product_id), commit=True)

                            if exe is not None:
                                if category == 'tshirt':
                                    level = request.form.getlist('tshirt')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=? WHERE product_id=?'.format(field=lev)
                                        execute_query(query, (yes, product_id), commit=True)

                                elif category == 'wallet':
                                    level = request.form.getlist('wallet')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=? WHERE product_id=?'.format(field=lev)
                                        execute_query(query, (yes, product_id), commit=True)

                                elif category == 'belt':
                                    level = request.form.getlist('belt')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=? WHERE product_id=?'.format(field=lev)
                                        execute_query(query, (yes, product_id), commit=True)

                                elif category == 'shoes':
                                    level = request.form.getlist('shoes')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=? WHERE product_id=?'.format(field=lev)
                                        execute_query(query, (yes, product_id), commit=True)

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
        # Get products matching search query
        query_string = "SELECT * FROM products WHERE pName LIKE ? ORDER BY id ASC"
        products = execute_query(query_string, ('%' + q + '%',), fetchall=True)
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
        result = execute_query("SELECT * FROM users WHERE id=?", (q,), fetchone=True)
        if result:
            if result['id'] == session['uid']:
                res = execute_query("SELECT * FROM orders WHERE uid=? ORDER BY id ASC", (session['uid'],), fetchall=True)
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
        result = execute_query("SELECT * FROM users WHERE id=?", (q,), fetchone=True)
        if result:
            if result['id'] == session['uid']:
                if request.method == 'POST' and form.validate():
                    name = form.name.data
                    email = form.email.data
                    password = sha256_crypt.encrypt(str(form.password.data))
                    mobile = form.mobile.data

                    # Update user in database
                    exe = execute_query("UPDATE users SET name=?, email=?, password=?, mobile=? WHERE id=?",
                                      (name, email, password, mobile, q), commit=True)
                    if exe is not None:
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
        product = execute_query("SELECT * FROM products WHERE id=?", (q,), fetchone=True)
        if product:
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

# Modern interface route
@app.route('/modern')
def modern_index():
    form = OrderForm(request.form)
    try:
        # Get products for different categories
        tshirt = execute_query("SELECT * FROM products WHERE category=? ORDER BY RANDOM() LIMIT 4", ('tshirt',), fetchall=True)
        wallet = execute_query("SELECT * FROM products WHERE category=? ORDER BY RANDOM() LIMIT 4", ('wallet',), fetchall=True)
        belt = execute_query("SELECT * FROM products WHERE category=? ORDER BY RANDOM() LIMIT 4", ('belt',), fetchall=True)
        shoes = execute_query("SELECT * FROM products WHERE category=? ORDER BY RANDOM() LIMIT 4", ('shoes',), fetchall=True)

        if tshirt is None or wallet is None or belt is None or shoes is None:
            flash('Database error. Please check your database configuration.', 'danger')
            return render_template('modern_home.html', tshirt=[], wallet=[], belt=[], shoes=[], form=form, db_error=True)

        return render_template('modern_home.html', tshirt=tshirt, wallet=wallet, belt=belt, shoes=shoes, form=form, db_error=False)
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
        return render_template('modern_home.html', tshirt=[], wallet=[], belt=[], shoes=[], form=form, db_error=True)

# Old interface route for comparison
@app.route('/old')
def old_index():
    form = OrderForm(request.form)
    try:
        # Get products for different categories
        tshirt = execute_query("SELECT * FROM products WHERE category=? ORDER BY RANDOM() LIMIT 4", ('tshirt',), fetchall=True)
        wallet = execute_query("SELECT * FROM products WHERE category=? ORDER BY RANDOM() LIMIT 4", ('wallet',), fetchall=True)
        belt = execute_query("SELECT * FROM products WHERE category=? ORDER BY RANDOM() LIMIT 4", ('belt',), fetchall=True)
        shoes = execute_query("SELECT * FROM products WHERE category=? ORDER BY RANDOM() LIMIT 4", ('shoes',), fetchall=True)

        if tshirt is None or wallet is None or belt is None or shoes is None:
            flash('Database error. Please check your database configuration.', 'danger')
            return render_template('home.html', tshirt=[], wallet=[], belt=[], shoes=[], form=form, db_error=True)

        return render_template('home.html', tshirt=tshirt, wallet=wallet, belt=belt, shoes=shoes, form=form, db_error=False)
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
        return render_template('home.html', tshirt=[], wallet=[], belt=[], shoes=[], form=form, db_error=True)


# Cart routes
@app.route('/cart')
@is_logged_in
def cart():
    # Get all items in the user's cart
    cart_items = execute_query("""
        SELECT c.id, c.quantity, p.id as product_id, p.pName, p.price, p.picture, p.available
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    """, (session['uid'],), fetchall=True)

    # Calculate total price
    total = 0
    for item in cart_items:
        total += item['price'] * item['quantity']

    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart', methods=['POST'])
@is_logged_in
def add_to_cart():
    form = AddToCartForm(request.form)
    if form.validate():
        product_id = form.product_id.data
        quantity = form.quantity.data

        # Check if product exists and is available
        product = execute_query("SELECT * FROM products WHERE id = ?", (product_id,), fetchone=True)
        if not product:
            flash("Produit non trouvé", "danger")
            return redirect(request.referrer or url_for('index'))

        if product['available'] < int(quantity):
            flash("Quantité non disponible", "danger")
            return redirect(request.referrer or url_for('index'))

        # Check if product is already in cart
        existing_item = execute_query(
            "SELECT * FROM cart WHERE user_id = ? AND product_id = ?", 
            (session['uid'], product_id), 
            fetchone=True
        )

        if existing_item:
            # Update quantity
            new_quantity = existing_item['quantity'] + int(quantity)
            if new_quantity > product['available']:
                flash("Quantité non disponible", "danger")
                return redirect(request.referrer or url_for('index'))

            execute_query(
                "UPDATE cart SET quantity = ? WHERE id = ?",
                (new_quantity, existing_item['id']),
                commit=True
            )
            flash("Quantité mise à jour dans le panier", "success")
        else:
            # Add new item to cart
            execute_query(
                "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
                (session['uid'], product_id, quantity),
                commit=True
            )
            flash("Produit ajouté au panier", "success")

        return redirect(request.referrer or url_for('index'))

    flash("Erreur lors de l'ajout au panier", "danger")
    return redirect(request.referrer or url_for('index'))

@app.route('/remove_from_cart/<int:cart_id>')
@is_logged_in
def remove_from_cart(cart_id):
    # Check if cart item belongs to user
    cart_item = execute_query(
        "SELECT * FROM cart WHERE id = ? AND user_id = ?", 
        (cart_id, session['uid']), 
        fetchone=True
    )

    if not cart_item:
        flash("Article non trouvé dans votre panier", "danger")
        return redirect(url_for('cart'))

    # Remove item from cart
    execute_query("DELETE FROM cart WHERE id = ?", (cart_id,), commit=True)
    flash("Article supprimé du panier", "success")
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@is_logged_in
def checkout():
    form = CheckoutForm(request.form)

    # Get cart items
    cart_items = execute_query("""
        SELECT c.id, c.quantity, p.id as product_id, p.pName, p.price, p.picture, p.available
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    """, (session['uid'],), fetchall=True)

    if not cart_items:
        flash("Votre panier est vide", "danger")
        return redirect(url_for('cart'))

    # Calculate total price
    total = 0
    for item in cart_items:
        total += item['price'] * item['quantity']

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile.data
        address = form.address.data

        # Create orders for each cart item
        for item in cart_items:
            # Check if product is still available
            product = execute_query("SELECT * FROM products WHERE id = ?", (item['product_id'],), fetchone=True)
            if not product or product['available'] < item['quantity']:
                flash(f"Le produit {item['pName']} n'est plus disponible en quantité suffisante", "danger")
                return redirect(url_for('cart'))

            # Create order
            execute_query("""
                INSERT INTO orders (uid, ofname, pid, quantity, oplace, mobile, dstatus)
                VALUES (?, ?, ?, ?, ?, ?, 'no')
            """, (session['uid'], name, item['product_id'], item['quantity'], address, mobile), commit=True)

            # Update product availability
            new_available = product['available'] - item['quantity']
            execute_query(
                "UPDATE products SET available = ? WHERE id = ?",
                (new_available, item['product_id']),
                commit=True
            )

        # Clear cart
        execute_query("DELETE FROM cart WHERE user_id = ?", (session['uid'],), commit=True)

        flash("Commande passée avec succès", "success")
        return redirect(url_for('orders'))

    return render_template('checkout.html', form=form, cart_items=cart_items, total=total)

# Category routes
@app.route('/mens')
def mens():
    form = OrderForm(request.form)
    products = execute_query("SELECT * FROM products WHERE category IN ('tshirt', 'wallet', 'belt', 'shoes') AND item='mens'", fetchall=True)
    return render_template('category.html', products=products, form=form, category="Hommes")

@app.route('/womens')
def womens():
    form = OrderForm(request.form)
    products = execute_query("SELECT * FROM products WHERE category IN ('tshirt', 'wallet', 'belt', 'shoes') AND item='womens'", fetchall=True)
    return render_template('category.html', products=products, form=form, category="Femmes")

@app.route('/arrivals')
def arrivals():
    form = OrderForm(request.form)
    products = execute_query("SELECT * FROM products ORDER BY date DESC LIMIT 8", fetchall=True)
    return render_template('category.html', products=products, form=form, category="Nouveautés")

@app.route('/new-arrivals')
def new_arrivals():
    # Redirect to the new route for backward compatibility
    return redirect(url_for('arrivals'))

@app.route('/sales')
def sales():
    form = OrderForm(request.form)
    # Get best-selling products based on order quantity
    products = execute_query("""
        SELECT p.*, COUNT(o.id) as order_count 
        FROM products p
        JOIN orders o ON p.id = o.pid
        GROUP BY p.id
        ORDER BY order_count DESC
        LIMIT 8
    """, fetchall=True)

    # Fallback if no orders exist
    if not products:
        products = execute_query("SELECT * FROM products ORDER BY RANDOM() LIMIT 8", fetchall=True)

    return render_template('category.html', products=products, form=form, category="Meilleures Ventes")

@app.route('/view_product/<int:product_id>')
def view_product(product_id):
    # Get product details
    product = execute_query("SELECT * FROM products WHERE id=?", (product_id,), fetchone=True)

    if not product:
        flash('Produit non trouvé', 'danger')
        return redirect(url_for('index'))

    # Get similar products using content-based filtering
    similar_products = content_based_filtering(product_id)

    # Record view if user is logged in
    if 'uid' in session:
        uid = session['uid']
        result = execute_query("SELECT * FROM product_view WHERE user_id=? AND product_id=?", 
                             (uid, product_id), fetchall=True)

        if result:
            now = datetime.datetime.now()
            now_time = now.strftime("%y-%m-%d %H:%M:%S")
            execute_query("UPDATE product_view SET date=? WHERE user_id=? AND product_id=?",
                        (now_time, uid, product_id), commit=True)
        else:
            execute_query("INSERT INTO product_view(user_id, product_id) VALUES(?, ?)", 
                        (uid, product_id), commit=True)

    form = OrderForm(request.form)
    return render_template('view_product.html', product=product, similar_products=similar_products, form=form)

@app.route('/all-products')
def all_products():
    form = OrderForm(request.form)
    category = request.args.get('category', None)

    if category:
        products = execute_query("SELECT * FROM products WHERE category=? ORDER BY id ASC", 
                               (category,), fetchall=True)
        category_title = category.capitalize()
    else:
        products = execute_query("SELECT * FROM products ORDER BY id ASC", fetchall=True)
        category_title = "Tous les produits"

    return render_template('category.html', products=products, form=form, category=category_title)

@app.route('/brands')
def brands():
    form = OrderForm(request.form)
    # This is a placeholder - in a real app, you'd have brand information in the database
    products = execute_query("SELECT * FROM products ORDER BY RANDOM() LIMIT 8", fetchall=True)
    return render_template('category.html', products=products, form=form, category="Marques")
