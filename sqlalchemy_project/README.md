# Simple SQLAlchemy Project

A simple project demonstrating SQLAlchemy ORM with database models and CRUD operations.

## Project Structure

```
sqlalchemy_project/
├── database.py      # Database configuration and session setup
├── models.py        # Database models (User, Product)
├── main.py          # CRUD operations and main application
├── requirements.txt # Project dependencies
└── README.md        # This file
```

## Features

- **Database Configuration**: SQLite database with SQLAlchemy ORM
- **Models**: Two sample models (User and Product)
- **CRUD Operations**: Create, Read, Update, Delete functionality for both models
- **Session Management**: Proper database session handling

## Setup Instructions

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

## Models

### User Model
- `id`: Primary key
- `name`: User's name (required)
- `email`: User's email (unique, required)
- `age`: User's age (optional)
- `created_at`: Timestamp of creation

### Product Model
- `id`: Primary key
- `name`: Product name (required)
- `description`: Product description (optional)
- `price`: Product price (required)
- `quantity`: Stock quantity (default: 0)
- `created_at`: Timestamp of creation

## CRUD Operations

### User Operations
- `create_user(name, email, age)`: Create a new user
- `get_user(user_id)`: Get a user by ID
- `get_all_users()`: Get all users
- `update_user(user_id, name, email, age)`: Update user details
- `delete_user(user_id)`: Delete a user

### Product Operations
- `create_product(name, price, description, quantity)`: Create a new product
- `get_product(product_id)`: Get a product by ID
- `get_all_products()`: Get all products
- `update_product(product_id, name, price, quantity)`: Update product details
- `delete_product(product_id)`: Delete a product

## Database File

The SQLite database is automatically created as `test.db` when you run the application for the first time.

## Example Usage

```python
from main import create_user, get_all_users, create_product, init_db

# Initialize database
init_db()

# Create a user
create_user("Alice", "alice@example.com", 28)

# Get all users
get_all_users()

# Create a product
create_product("Phone", 799.99, "Smartphone", 10)
```

## Extending the Project

To add more models:

1. Define the model in `models.py` (inheriting from `Base`)
2. Create CRUD functions in `main.py`
3. Run `init_db()` to create the new tables

## Notes

- Uses SQLite for simplicity (can be switched to MySQL, PostgreSQL, etc.)
- The database file is created in the project directory
- Each CRUD operation opens and closes its own session
- Includes error handling with proper rollback on failures
