from utils import get_db_connection

def drop_existing_tables(cursor):
    """Drops the existing tables if they exist."""
    try:
        cursor.execute("""
            DROP TABLE IF EXISTS opportunities, tasks, interactions, payments,sales_rep, user_sales_rep, products, customers, users CASCADE;
        """)
        print("Existing tables dropped successfully.")
    except Exception as e:
        print(f"Error dropping tables: {e}")
        raise

def create_tables(cursor):
    """Creates the required tables in the database."""
    create_tables_query = """
    -- Creating Sales Reps Table
    CREATE TABLE IF NOT EXISTS sales_rep (
        rep_id SERIAL PRIMARY KEY,
        full_name VARCHAR(100),
        email VARCHAR(100) UNIQUE
    );

    -- Creating Customers Table
    CREATE TABLE IF NOT EXISTS customers (
        customer_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(20),
        industry VARCHAR(100)
    );

    -- Creating Users Table
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,  -- Store hashed passwords
        email VARCHAR(100) UNIQUE NOT NULL,
        role VARCHAR(50) NOT NULL,  -- e.g., 'admin', 'sales_rep', etc.
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Creating Products Table
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        price DECIMAL(10, 2),
        stock_quantity INT DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Creating Opportunities/Deals Table
    CREATE TABLE IF NOT EXISTS opportunities (
        opportunity_id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES customers(customer_id),
        product_id INT REFERENCES products(product_id),
        rep_id INT REFERENCES sales_rep(rep_id),
        status VARCHAR(50) NOT NULL,  -- e.g., 'new', 'closed', 'pending', etc.
        estimated_value DECIMAL(10, 2),
        close_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Creating Tasks/Follow-ups Table
    CREATE TABLE IF NOT EXISTS tasks (
        task_id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES customers(customer_id),
        rep_id INT REFERENCES sales_rep(rep_id),
        task_type VARCHAR(50),  -- e.g., 'call', 'meeting', 'follow-up'
        due_date TIMESTAMP,
        notes TEXT,
        status VARCHAR(50)  -- e.g., 'completed', 'pending'
    );

    -- Updated Interactions Table
    CREATE TABLE IF NOT EXISTS interactions (
        interaction_id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES customers(customer_id),
        rep_id INT REFERENCES sales_rep(rep_id),
        interaction_type VARCHAR(50),  -- e.g., 'call', 'email', 'meeting'
        interaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        notes TEXT,
        follow_up_task_id INT REFERENCES tasks(task_id)
    );

    -- User-Sales Rep Relationship Table
    CREATE TABLE IF NOT EXISTS user_sales_rep (
        user_id INT REFERENCES users(user_id),
        rep_id INT REFERENCES sales_rep(rep_id),
        PRIMARY KEY (user_id, rep_id)
    );

    -- Creating Payments Table
    CREATE TABLE IF NOT EXISTS payments (
        payment_id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES customers(customer_id),
        amount DECIMAL(10, 2) NOT NULL,
        payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        payment_method VARCHAR(50),  -- e.g., 'credit card', 'bank transfer'
        invoice_number VARCHAR(50),
        status VARCHAR(50)  -- e.g., 'paid', 'pending'
    );
    """
    try:
        cursor.execute(create_tables_query)
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise


def main():
    """Main function to manage database setup."""
    try:
        # Establish connection to the database
        with get_db_connection() as conn:
            # Create a cursor object to interact with the database
            with conn.cursor() as cursor:
                # Drop existing tables and create new ones
                drop_existing_tables(cursor)
                create_tables(cursor)

    except Exception as e:
        print(f"An error occurred: {e}")
        # You may want to add more logging or re-raise the exception if needed.

if __name__ == "__main__":
    main()
