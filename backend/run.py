import os
import sys
from flask import Flask
from werkzeug.security import generate_password_hash  # נשתמש ב-generate_password_hash עבור סיסמאות ראשוניות

# הוסף את תיקיית src לנתיב הפייתון
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from app import app, db, login_manager  # ייבוא האפליקציה, ה-db וה-login_manager
from models.tenant import Tenant
from models.user import User
from models.warehouse import Warehouse
from models.product import Product
from models.warehouse_permission import WarehousePermission


def create_initial_data():
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created/checked.")

        # יצירת מנהל מערכת ראשי אם לא קיים
        system_admin_user = User.query.filter_by(email='admin@system.com').first()
        if not system_admin_user:
            print("Creating system admin user...")
            new_sys_admin = User(
                data={
                    'email': 'admin@system.com',
                    'role': 'system_admin',
                    'first_name': 'System',
                    'last_name': 'Admin'
                }
            )
            new_sys_admin.set_password('adminpassword')  # הגדרת סיסמה באמצעות המתודה במודל
            db.session.add(new_sys_admin)
            db.session.commit()
            print("System admin created: admin@system.com / adminpassword")
        else:
            print("System admin user already exists.")

        # דוגמה ליצירת טננט ומשתמשים (אם לא קיימים)
        acme_tenant = Tenant.query.filter_by(name='Acme Corp').first()
        if not acme_tenant:
            print("Creating Acme Corp tenant...")
            acme_tenant = Tenant(data={'name': 'Acme Corp', 'contact_email': 'contact@acmecorp.com'})
            acme_tenant.create()
            print(f"Acme Corp tenant created with ID: {acme_tenant.id}")

            print("Creating Acme Corp tenant admin user...")
            acme_admin = User(
                data={
                    'tenant_id': acme_tenant.id,
                    'email': 'admin@acmecorp.com',
                    'role': 'tenant_admin',
                    'first_name': 'Acme',
                    'last_name': 'Admin'
                }
            )
            acme_admin.set_password('acmeadminpass')
            acme_admin.create()
            print(f"Acme Corp admin created: admin@acmecorp.com / acmeadminpass (ID: {acme_admin.id})")

            print("Creating Acme Corp regular user...")
            acme_user = User(
                data={
                    'tenant_id': acme_tenant.id,
                    'email': 'john.doe@acmecorp.com',
                    'role': 'regular_user',
                    'first_name': 'John',
                    'last_name': 'Doe'
                }
            )
            acme_user.set_password('johnpass')
            acme_user.create()
            print(f"Acme Corp regular user created: john.doe@acmecorp.com / johnpass (ID: {acme_user.id})")

            print("Creating Acme Corp warehouse...")
            acme_warehouse = Warehouse(
                data={
                    'tenant_id': acme_tenant.id,
                    'name': 'Main Acme Warehouse',
                    'location': '123 Acme St',
                    'capacity_sqm': 1000
                }
            )
            acme_warehouse.create()
            print(f"Acme Corp warehouse created with ID: {acme_warehouse.id}")

            print("Granting John Doe permission to Main Acme Warehouse...")
            permission = WarehousePermission(
                data={
                    'user_id': acme_user.id,
                    'warehouse_id': acme_warehouse.id,
                    'tenant_id': acme_tenant.id,
                    'access_level': 'edit'
                }
            )
            permission.create()
            print("Permission granted.")

            print("Creating a product in Main Acme Warehouse...")
            product1 = Product(
                data={
                    'warehouse_id': acme_warehouse.id,
                    'tenant_id': acme_tenant.id,
                    'name': 'Widget A',
                    'sku': 'WGT-A-001',
                    'quantity': 100,
                    'unit_price': 10.50
                }
            )
            product1.create()
            print(f"Product '{product1.name}' created (ID: {product1.id})")

        else:
            print("Acme Corp tenant and associated data already exists.")


if __name__ == '__main__':
    create_initial_data()
    app.run(debug=True, port=8080)
