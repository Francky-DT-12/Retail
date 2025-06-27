import sys
import os
sys.path.append('/home/lelouch/Retail')

try:
    from RetailShop import app
    print("✓ Application imported successfully")

    with app.app_context():
        from RetailShop.db_helper import execute_query
        import hashlib
        
        # Create a complete admin user
        print("\n=== Creating Complete Admin User ===")
        
        test_email = "admin@shoptub.com"
        test_password = "admin123"
        hashed_password = hashlib.sha256(test_password.encode()).hexdigest()
        
        try:
            # Check if admin already exists
            existing = execute_query("SELECT * FROM admin WHERE email=%s", (test_email,), fetchone=True)
            
            if existing:
                print(f"✓ Admin user already exists: {test_email}")
            else:
                # Insert with ALL required fields
                execute_query(
                    "INSERT INTO admin (email, password, firstName, lastName, mobile, address, type, confirmCode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (test_email, hashed_password, "Admin", "User", "1234567890", "Admin Address", "admin", "123456"),
                    commit=True
                )
                print(f"✓ Created complete admin user: {test_email}")
                
            print(f"\n=== ADMIN CREDENTIALS ===")
            print(f"Email: {test_email}")
            print(f"Password: {test_password}")
            print(f"=========================")
                
        except Exception as e:
            print(f"✗ Error creating admin user: {e}")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()