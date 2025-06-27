from RetailShop import app
from RetailShop.db_helper import execute_query
from passlib.hash import sha256_crypt

def create_admin_user():
    try:
        with app.app_context():
            # Check if role column exists in users table
            cursor = app.mysql.connection.cursor()
            cursor.execute("SHOW COLUMNS FROM users LIKE 'role'")
            role_exists = cursor.fetchone()

            # Add role column if it doesn't exist
            if not role_exists:
                execute_query("ALTER TABLE users ADD COLUMN role INT NOT NULL DEFAULT 1", commit=True)
                # Update existing users to have role=1 (regular users)
                execute_query("UPDATE users SET role=1", commit=True)
                print("Added role column to users table")

            # Check if admin user exists (role=0)
            admin_exists = execute_query("SELECT * FROM users WHERE role=0", fetchall=True)

            if not admin_exists:
                # Create admin user if it doesn't exist
                admin_password = sha256_crypt.encrypt("admin123")
                execute_query("INSERT INTO users(name, email, username, password, mobile, role) VALUES(%s, %s, %s, %s, %s, %s)",
                            ("Admin", "admin@example.com", "admin", admin_password, "", 0), commit=True)
                print("Admin user created with username 'admin' and password 'admin123'")
            else:
                print("Admin user already exists")

            # Verify admin user
            admin_user = execute_query("SELECT * FROM users WHERE username='admin'", fetchone=True)
            if admin_user:
                print(f"Admin user found: {admin_user['username']} (ID: {admin_user['id']})")
            else:
                print("Admin user not found in database")

    except Exception as e:
        print(f"Error creating admin user: {e}")

if __name__ == "__main__":
    create_admin_user()
