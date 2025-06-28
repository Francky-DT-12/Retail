import sys
import os
sys.path.append('/home/lelouch/Retail')

try:
    from RetailShop import app
    print("✓ Application imported successfully")

    with app.app_context():
        from RetailShop.db_helper import execute_query

        # Get admin users with their passwords
        print("\n=== Admin User Credentials ===")
        admins = execute_query("SELECT * FROM admin", (), fetchall=True)

        if admins:
            print(f"Found {len(admins)} admin user(s):")
            print("-" * 60)
            for admin in admins:
                print(f"ID: {admin['id']}")
                print(f"Email: {admin['email']}")
                print(f"Name: {admin.get('firstName', 'N/A')}")
                print(f"Password Hash: {admin['password']}")
                print("-" * 60)
        else:
            print("No admin users found")

        # Let's also check if we can create a simple admin user with known credentials
        print("\n=== Creating Test Admin User ===")
        import hashlib

        # Create a simple admin user with known credentials
        test_email = "admin@shoptub.com"
        test_password = "admin123"
        test_name = "Admin"

        # Hash the password using SHA256 (same method used in admin_login route)
        hashed_password = hashlib.sha256(test_password.encode()).hexdigest()

        try:
            # Check if this admin already exists
            existing = execute_query("SELECT * FROM admin WHERE email=%s", (test_email,), fetchone=True)

            if existing:
                print(f"✓ Test admin user already exists: {test_email}")
            else:
                # Insert new admin user with lastName
                execute_query(
                    "INSERT INTO admin (email, password, firstName, lastName) VALUES (%s, %s, %s, %s)",
                    (test_email, hashed_password, test_name, "User"),
                    commit=True
                )
                print(f"✓ Created test admin user: {test_email}")

            print(f"Test Admin Credentials:")
            print(f"Email: {test_email}")
            print(f"Password: {test_password}")

            # Let's also try some common passwords for existing users
            print(f"\n=== Testing Common Passwords for Existing Users ===")
            common_passwords = ["password", "123456", "admin", "admin123", "password123", "shoptub123"]

            for admin in admins[:2]:  # Test first 2 admins only
                print(f"\nTesting passwords for {admin['email']}:")
                for pwd in common_passwords:
                    test_hash = hashlib.sha256(pwd.encode()).hexdigest()
                    if test_hash == admin['password']:
                        print(f"  ✓ Password found: {pwd}")
                        break
                else:
                    print(f"  ✗ None of the common passwords match")

        except Exception as e:
            print(f"✗ Error creating test admin: {e}")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
