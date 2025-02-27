import random
from datetime import datetime, timedelta
from utils import get_db_connection

# Helper function to generate random dates within a specified range
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Function to generate random customer data
def generate_customers(num):
    customers = []
    industries = ['Retail', 'Finance', 'Healthcare', 'Education', 'Technology']
    for _ in range(num):
        name = f"Customer {_ + 1}"
        email = f"customer{_ + 1}@example.com"
        phone = f"+1234567890"
        industry = random.choice(industries)
        customers.append((name, email, phone, industry))
    return customers

# Function to generate random sales rep data
def generate_sales_reps(num):
    sales_reps = []
    for _ in range(num):
        full_name = f"Sales Rep {_ + 1}"
        email = f"salesrep{_ + 1}@example.com"
        sales_reps.append((full_name, email))
    return sales_reps

# Function to generate random product data
def generate_products(num):
    products = []
    for _ in range(num):
        name = f"Product {_ + 1}"
        description = f"Description of Product {_ + 1}"
        price = round(random.uniform(10, 500), 2)
        stock_quantity = random.randint(1, 100)
        products.append((name, description, price, stock_quantity))
    return products

# Function to generate random user data
def generate_users(num):
    users = []
    roles = ['admin', 'sales_rep', 'manager']
    for _ in range(num):
        username = f"user{_ + 1}"
        password_hash = f"hash{_ + 1}"
        email = f"user{_ + 1}@example.com"
        role = random.choice(roles)
        users.append((username, password_hash, email, role))
    return users

# Function to generate random tasks
def generate_tasks(num, customer_ids, sales_rep_ids):
    task_types = ['call', 'meeting', 'follow-up']
    statuses = ['completed', 'pending']
    tasks = []
    for _ in range(num):
        customer_id = random.choice(customer_ids)
        rep_id = random.choice(sales_rep_ids)
        task_type = random.choice(task_types)
        due_date = random_date(start_date, end_date)
        status = random.choice(statuses)
        notes = f'Task notes for {task_type} on {due_date}'
        tasks.append((customer_id, rep_id, task_type, due_date, notes, status))
    return tasks

# Function to generate random opportunities (deals)
def generate_opportunities(num, customer_ids, product_ids, sales_rep_ids):
    statuses = ['new', 'closed', 'pending']
    opportunities = []
    for _ in range(num):
        customer_id = random.choice(customer_ids)
        product_id = random.choice(product_ids)
        rep_id = random.choice(sales_rep_ids)
        status = random.choice(statuses)
        estimated_value = round(random.uniform(1000, 10000), 2)
        close_date = random_date(start_date, end_date)
        opportunities.append((customer_id, product_id, rep_id, status, estimated_value, close_date))
    return opportunities

# Function to generate random interactions
def generate_interactions(num, customer_ids, sales_rep_ids, task_ids):
    interaction_types = ['call', 'email', 'meeting']
    interactions = []
    for _ in range(num):
        customer_id = random.choice(customer_ids)
        rep_id = random.choice(sales_rep_ids)
        interaction_type = random.choice(interaction_types)
        interaction_date = random_date(start_date, end_date)
        follow_up_task_id = random.choice([None, random.choice(task_ids)])  # Can be None or a valid task_id
        notes = f'Interaction notes for {interaction_type} on {interaction_date}'
        interactions.append((customer_id, rep_id, interaction_type, interaction_date, notes, follow_up_task_id))
    return interactions

# Function to generate random payments
def generate_payments(num, customer_ids):
    payments = []
    for _ in range(num):
        customer_id = random.choice(customer_ids)
        amount = round(random.uniform(100, 5000), 2)
        payment_date = random_date(start_date, end_date)
        payment_method = random.choice(['credit card', 'bank transfer'])
        status = random.choice(['paid', 'pending'])
        payments.append((customer_id, amount, payment_date, payment_method, status))
    return payments

# Function to generate random user-sales rep relationships
def generate_user_sales_rep(num_users, sales_rep_ids):
    user_sales_rep = []
    for user_id in range(1, num_users + 1):
        rep_id = random.choice(sales_rep_ids)
        user_sales_rep.append((user_id, rep_id))
    return user_sales_rep

# Initialize start and end date for random date generation
start_date = datetime(2020, 1, 1)
end_date = datetime(2025, 1, 1)

# Number of rows to insert into each table
num_rows = 1000

# Generate random data
customers = generate_customers(num_rows)
sales_reps = generate_sales_reps(num_rows)
products = generate_products(num_rows)
users = generate_users(num_rows)

# Establish connection to the database
conn = get_db_connection()
cursor = conn.cursor()

# Step 1: Insert users
cursor.executemany("""
    INSERT INTO users (username, password_hash, email, role) 
    VALUES (%s, %s, %s, %s);
""", users)

# Insert customers
cursor.executemany("""
    INSERT INTO customers (name, email, phone, industry) 
    VALUES (%s, %s, %s, %s);
""", customers)

# Insert sales reps
cursor.executemany("""
    INSERT INTO sales_rep (full_name, email) 
    VALUES (%s, %s);
""", sales_reps)

# Insert products
cursor.executemany("""
    INSERT INTO products (name, description, price, stock_quantity) 
    VALUES (%s, %s, %s, %s);
""", products)

# Commit to ensure data is inserted and IDs are available
conn.commit()

# Fetch valid IDs for customers, sales reps, products, and users
cursor.execute("SELECT customer_id FROM customers;")
customer_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT rep_id FROM sales_rep;")
sales_rep_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT product_id FROM products;")
product_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT user_id FROM users;")
user_ids = [row[0] for row in cursor.fetchall()]

# Step 2: Generate and insert tasks
tasks = generate_tasks(num_rows, customer_ids, sales_rep_ids)
cursor.executemany("""
    INSERT INTO tasks (customer_id, rep_id, task_type, due_date, notes, status) 
    VALUES (%s, %s, %s, %s, %s, %s);
""", tasks)

# Commit changes so task IDs are available
conn.commit()

# Fetch valid task IDs
cursor.execute("SELECT task_id FROM tasks;")
task_ids = [row[0] for row in cursor.fetchall()]

# Step 3: Generate and insert opportunities, interactions, payments, and user-sales rep relationships
opportunities = generate_opportunities(num_rows, customer_ids, product_ids, sales_rep_ids)
interactions = generate_interactions(num_rows, customer_ids, sales_rep_ids, task_ids)
payments = generate_payments(num_rows, customer_ids)
user_sales_rep = generate_user_sales_rep(len(user_ids), sales_rep_ids)

# Insert generated data
cursor.executemany("""
    INSERT INTO opportunities (customer_id, product_id, rep_id, status, estimated_value, close_date) 
    VALUES (%s, %s, %s, %s, %s, %s);
""", opportunities)

cursor.executemany("""
    INSERT INTO interactions (customer_id, rep_id, interaction_type, interaction_date, notes, follow_up_task_id) 
    VALUES (%s, %s, %s, %s, %s, %s);
""", interactions)

cursor.executemany("""
    INSERT INTO payments (customer_id, amount, payment_date, payment_method, status) 
    VALUES (%s, %s, %s, %s, %s);
""", payments)

cursor.executemany("""
    INSERT INTO user_sales_rep (user_id, rep_id) 
    VALUES (%s, %s);
""", user_sales_rep)

# Commit the final changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("All tables filled with random data successfully!")
