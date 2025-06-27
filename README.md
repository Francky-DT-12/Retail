Prérequis : Python 3.8.x
# E-Commerce-Website-Using-Python

## Get In Touch
Have any problem? Don't hesitate to connect... <br>
(i) Facebook: https://www.facebook.com/mohsingram <br>
(ii) Youtube: https://www.youtube.com/mohsingram <br>

## Web View
Go to this link to view website <br>
https://menshut.pythonanywhere.com

## Summary
Hello friends, This is my first full e-commerce project with Python-Flask. This is free. Anybody can use and moderate this project.

## Platform Used
### Front-End
  (i) HTML5 <br>
  (ii) CSS3 <br>
  (iii) JavaScript <br>
  (iv) Bootstrap <br>

### Back-End
  (i) Python - Flask <br>
  (ii) MySQL <br>

## Database Setup

The application requires a MySQL database to function properly. Follow these steps to set up the database:

1. Make sure MySQL server is installed and running on your system.

2. Create the database and user by running the setup_db.sql script:
   ```bash
   mysql -u root -p < setup_db.sql
   ```
   This will:
   - Create a database named 'shoptub'
   - Create a user 'webapp' with password 'motdepassefort'
   - Grant all privileges on the 'shoptub' database to the 'webapp' user
   - Create the necessary tables and insert sample data

3. Verify that the database was created successfully:
   ```bash
   mysql -u webapp -pmotdepassefort -e "SHOW DATABASES;"
   ```
   You should see 'shoptub' in the list of databases.

## Running the Application

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Set the Flask application environment variable:
   ```bash
   export FLASK_APP=app.py
   ```

3. Run the application:
   ```bash
   flask run
   ```

4. Access the application in your web browser at http://127.0.0.1:5000/

## Troubleshooting Database Connection Issues

If you encounter database connection issues, check the following:

1. Make sure the MySQL server is running:
   ```bash
   sudo service mysql status
   ```
   or
   ```bash
   sudo systemctl status mysql
   ```

2. Verify that the 'shoptub' database exists:
   ```bash
   mysql -u root -p -e "SHOW DATABASES;"
   ```

3. Verify that the 'webapp' user has access to the 'shoptub' database:
   ```bash
   mysql -u webapp -pmotdepassefort -e "SHOW DATABASES;"
   ```

4. Run the test_db_connection.py script to check the database connection:
   ```bash
   python test_db_connection.py
   ```

5. If all else fails, you can recreate the database by running the setup_db.sql script again:
   ```bash
   mysql -u root -p < setup_db.sql
   ```

## Key Features
### Public User
(i) Search Product <br>
(ii) View Product <br>
(iii) Create User Account <br>

### Signin User
(i) Search Product <br>
(ii) View Product <br>
(iii) Create Order <br>
(iv) Change Email & Password <br>
(v) Can View Previous Order with UPDATE and DELETE <br>

### Admin
(i) Add New Product <br>
(ii) Update Product <br>
(iii) See all Orders <br>
(iv) Manage all Users <br>

## Conclusion
There are also many more feature which are not in the list. Feel free to use this project
