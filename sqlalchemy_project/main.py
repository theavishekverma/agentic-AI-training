from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import User, Product

# Create all tables in the database
def init_db():
    """Initialize database and create tables"""
    # Drop all existing tables first
    Base.metadata.drop_all(bind=engine)
    # Create all tables fresh
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

# ==================== USER CRUD OPERATIONS ====================

def create_user(name: str, email: str, age: int = None) -> User:
    """Create a new user"""
    db = SessionLocal()
    try:
        user = User(name=name, email=email, age=age)
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"User created: {user}")
        return user
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
    finally:
        db.close()

def get_user(user_id: int) -> User:
    """Get a user by ID"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            print(f"User found: {user}")
        else:
            print(f"User with id {user_id} not found")
        return user
    finally:
        db.close()

def get_all_users() -> list:
    """Get all users"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"Total users: {len(users)}")
        for user in users:
            print(f"  - {user}")
        return users
    finally:
        db.close()

def update_user(user_id: int, name: str = None, email: str = None, age: int = None) -> User:
    """Update a user"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            if name:
                user.name = name
            if email:
                user.email = email
            if age is not None:
                user.age = age
            db.commit()
            db.refresh(user)
            print(f"User updated: {user}")
            return user
        else:
            print(f"User with id {user_id} not found")
            return None
    except Exception as e:
        db.rollback()
        print(f"Error updating user: {e}")
    finally:
        db.close()

def delete_user(user_id: int) -> bool:
    """Delete a user"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            print(f"User with id {user_id} deleted")
            return True
        else:
            print(f"User with id {user_id} not found")
            return False
    except Exception as e:
        db.rollback()
        print(f"Error deleting user: {e}")
    finally:
        db.close()

# ==================== PRODUCT CRUD OPERATIONS ====================

def create_product(name: str, price: float, description: str = None, quantity: int = 0) -> Product:
    """Create a new product"""
    db = SessionLocal()
    try:
        product = Product(name=name, description=description, price=price, quantity=quantity)
        db.add(product)
        db.commit()
        db.refresh(product)
        print(f"Product created: {product}")
        return product
    except Exception as e:
        db.rollback()
        print(f"Error creating product: {e}")
    finally:
        db.close()

def get_product(product_id: int) -> Product:
    """Get a product by ID"""
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            print(f"Product found: {product}")
        else:
            print(f"Product with id {product_id} not found")
        return product
    finally:
        db.close()

def get_all_products() -> list:
    """Get all products"""
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        print(f"Total products: {len(products)}")
        for product in products:
            print(f"  - {product}")
        return products
    finally:
        db.close()

def update_product(product_id: int, name: str = None, price: float = None, quantity: int = None) -> Product:
    """Update a product"""
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            if name:
                product.name = name
            if price is not None:
                product.price = price
            if quantity is not None:
                product.quantity = quantity
            db.commit()
            db.refresh(product)
            print(f"Product updated: {product}")
            return product
        else:
            print(f"Product with id {product_id} not found")
            return None
    except Exception as e:
        db.rollback()
        print(f"Error updating product: {e}")
    finally:
        db.close()

def delete_product(product_id: int) -> bool:
    """Delete a product"""
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            db.delete(product)
            db.commit()
            print(f"Product with id {product_id} deleted")
            return True
        else:
            print(f"Product with id {product_id} not found")
            return False
    except Exception as e:
        db.rollback()
        print(f"Error deleting product: {e}")
    finally:
        db.close()

# ==================== MAIN FUNCTION ====================

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    print("\n" + "="*50)
    print("USER OPERATIONS")
    print("="*50)
    
    # Create users
    create_user("John Doe", "john@example.com", 30)
    create_user("Jane Smith", "jane@example.com", 25)
    create_user("Bob Johnson", "bob@example.com", 35)
    
    # Get all users
    print("\n--- All Users ---")
    get_all_users()
    
    # Get specific user
    print("\n--- Get User 1 ---")
    get_user(1)
    
    # Update user
    print("\n--- Update User 1 ---")
    update_user(1, age=31)
    
    print("\n" + "="*50)
    print("PRODUCT OPERATIONS")
    print("="*50)
    
    # Create products
    create_product("Laptop", 999.99, "High-performance laptop", 5)
    create_product("Mouse", 29.99, "Wireless mouse", 50)
    create_product("Keyboard", 79.99, "Mechanical keyboard", 20)
    
    # Get all products
    print("\n--- All Products ---")
    get_all_products()
    
    # Get specific product
    print("\n--- Get Product 1 ---")
    get_product(1)
    
    # Update product
    print("\n--- Update Product 1 ---")
    update_product(1, price=1099.99, quantity=3)
    
    # Delete product
    print("\n--- Delete Product 2 ---")
    delete_product(2)
    
    print("\n" + "="*50)
    print("FINAL STATE")
    print("="*50)
    print("\n--- Final Users ---")
    get_all_users()
    
    print("\n--- Final Products ---")
    get_all_products()
