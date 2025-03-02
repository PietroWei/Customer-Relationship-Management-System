import random
import numpy as np
from datetime import datetime, timedelta
from utils import get_db_connection

# Helper function to generate random dates within a specified range
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Function to introduce random errors (NaN, negative values, typos, etc.)

def add_random_error(value, nan_probability=0.05, is_unique=False):
    # Avoid NaN for unique fields (like email)
    if is_unique and isinstance(value, str) and "@" in value:  # Check if it's an email-like field
        while random.random() < nan_probability:  # Retry to avoid NaN
            value = f"customer{random.randint(1000, 9999)}@example.com"  # Generate a new email if NaN is introduced
    
    # Introduce NaN or None (ensure this doesn't apply to unique fields)
    if random.random() < nan_probability and not is_unique:
        return None  # Return None for optional fields instead of NaN
    
    return value

# Function to generate random customer data with errors

def generate_customers(num):
    customers = []
    industries = ['Retail', 'Finance', 'Healthcare', 'Education', 'Technology']
    
    # List of European countries and their approximate populations
    countries_with_population = [
        ('Albania', 2877797), ('Andorra', 77265), ('Armenia', 2963243), ('Austria', 8917205),
        ('Azerbaijan', 10139177), ('Belarus', 9449323), ('Belgium', 11589623), ('Bosnia and Herzegovina', 3280819),
        ('Bulgaria', 6951482), ('Croatia', 4095267), ('Cyprus', 1207359), ('Czech Republic', 10649800),
        ('Denmark', 5818553), ('Estonia', 1326535), ('Finland', 5523146), ('France', 67413000),
        ('Georgia', 3989167), ('Germany', 83166711), ('Greece', 10423054), ('Hungary', 9660351),
        ('Iceland', 376248), ('Ireland', 4937786), ('Italy', 60262770), ('Kazakhstan', 18776707),
        ('Kosovo', 1831000), ('Latvia', 1886198), ('Liechtenstein', 38128), ('Lithuania', 2722289),
        ('Luxembourg', 634814), ('Malta', 51464), ('Moldova', 2657637), ('Monaco', 39242),
        ('Montenegro', 622359), ('Netherlands', 17134872), ('North Macedonia', 2083459), ('Norway', 5421241),
        ('Poland', 38386000), ('Portugal', 10276617), ('Romania', 19237691), ('Russia', 145805947),
        ('San Marino', 33931), ('Serbia', 8772235), ('Slovakia', 5456362), ('Slovenia', 2078654),
        ('Spain', 46719142), ('Sweden', 10423054), ('Switzerland', 8610000), ('Turkey', 85862215),
        ('Ukraine', 41401830), ('United Kingdom', 68497907), ('Vatican City', 800)
    ]
    
    # Create a weighted list of countries based on their population
    countries, populations = zip(*countries_with_population)
    total_population = sum(populations)
    weights = [population / total_population for population in populations]

    existing_emails = set()  # Set to track unique emails

    for i in range(num):
        name = f"Customer {i + 1}"

        # Ensure email is always unique
        email = None
        while email is None or email in existing_emails:
            email = f"customer{i + 1}_{random.randint(1000, 9999)}@example.com"
        
        existing_emails.add(email)  # Add the newly generated email to the set

        phone = f"+123456{random.randint(10000, 99999)}"  # More varied phone numbers
        industry = random.choice(industries)
        
        # Select a country with weighted probability
        country = random.choices(countries, weights=weights, k=1)[0]
        
        customers.append((name, email, phone, industry, country))

    return customers


# Function to generate random user data with errors
def generate_users(num):
    users = []
    roles = ['admin', 'sales_rep', 'manager']
    existing_emails = set()  # Track generated emails to ensure uniqueness

    for _ in range(num):
        username = f"user{_ + 1}"
        password_hash = f"hash{_ + 1}"
        
        # Generate email and ensure it's unique
        email = None
        while email is None or email in existing_emails:
            email = f"user{_ + 1}@example.com"  # Generate email
            email = add_random_error(email, is_unique=True)  # Add error to email if needed

        # Add the email to the set to prevent duplicates
        existing_emails.add(email)
        
        # Ensure role is valid and add random errors
        role = random.choice(roles)
        role = add_random_error(role)
        if role is None:  # Default to 'sales_rep' if no valid role
            role = 'sales_rep'

        users.append((username, password_hash, email, role))

    return users

# Function to generate random sales rep data with errors
def generate_sales_reps(num):
    sales_reps = []
    for _ in range(num):
        full_name = f"Sales Rep {_ + 1}"
        full_name = add_random_error(full_name)  # Add error to sales rep name
        email = f"salesrep{_ + 1}@example.com"
        email = add_random_error(email)  # Add error to email
        sales_reps.append((full_name, email))
    return sales_reps

# Function to generate random product data with errors
def generate_products(num):
    products = []
    for i in range(num):
        name = f"Product {i + 1}"  # Ensure each product has a unique name
        description = f"Description of Product {i + 1}"
        price = round(random.uniform(10, 500), 2)
        stock_quantity = random.randint(1, 100)
        
        # Add error to product name if needed (if you want to randomly introduce errors)
        name = add_random_error(name)
        
        # Ensure the product name is not None or empty
        if not name:
            name = f"Product {i + 1}"

        products.append((name, description, price, stock_quantity))
    return products

# Function to generate random tasks with errors
def generate_tasks(num, customer_ids, sales_rep_ids):
    task_types = ['call', 'meeting', 'follow-up']
    statuses = ['completed', 'pending']
    tasks = []
    for _ in range(num):
        customer_id = random.choice(customer_ids)
        rep_id = random.choice(sales_rep_ids)
        task_type = random.choice(task_types)
        due_date = random_date(start_date, end_date)
        due_date = add_random_error(due_date)  # Add error to due date
        status = random.choice(statuses)
        status = add_random_error(status)  # Add error to status
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
        
        # Ensure status is randomly chosen from the valid statuses
        status = random.choice(statuses)
        
        estimated_value = round(random.uniform(1000, 10000), 2)
        close_date = random_date(start_date, end_date)
        
        # Ensure the opportunity has a valid status
        if status is None:
            status = random.choice(statuses)  # Default to a valid status if None is returned
        
        opportunities.append((customer_id, product_id, rep_id, status, estimated_value, close_date))

    return opportunities



# Function to generate random interactions with errors
def generate_interactions(num, customer_ids, sales_rep_ids, task_ids):
    interaction_types = ['call', 'email', 'meeting']
    interactions = []
    for _ in range(num):
        customer_id = random.choice(customer_ids)
        rep_id = random.choice(sales_rep_ids)
        interaction_type = random.choice(interaction_types)
        interaction_date = random_date(start_date, end_date)
        interaction_date = add_random_error(interaction_date)  # Add error to interaction date
        follow_up_task_id = random.choice([None, random.choice(task_ids)])  # Can be None or a valid task_id
        notes = f'Interaction notes for {interaction_type} on {interaction_date}'
        interactions.append((customer_id, rep_id, interaction_type, interaction_date, notes, follow_up_task_id))
    return interactions

# Function to generate random payments
def generate_payments(num, customer_ids):
    payments = []
    for _ in range(num):
        customer_id = random.choice(customer_ids)
        
        # Ensure 'amount' is always a valid positive float
        amount = round(random.uniform(100, 5000), 2)
        
        # Ensure 'payment_date' is always a valid date
        payment_date = random_date(start_date, end_date)
        
        # Ensure 'payment_method' is always one of the valid methods
        payment_method = random.choice(['credit card', 'bank transfer'])
        
        # Ensure 'status' is always one of the valid statuses
        status = random.choice(['paid', 'pending'])
        
        payments.append((customer_id, amount, payment_date, payment_method, status))
    
    return payments

# Function to generate random user-sales rep relationships with errors
def generate_user_sales_rep(num_users, sales_rep_ids):
    user_sales_rep = []
    for user_id in range(1, num_users + 1):
        rep_id = random.choice(sales_rep_ids)
        user_sales_rep.append((user_id, rep_id))
    return user_sales_rep

# Initialize start and end date for random date generation
start_date = datetime(2000, 1, 1)
end_date = datetime(2025, 1, 1)

# Number of rows to insert into each table
num_rows = 10000

# Generate random data
customers = generate_customers(num_rows)
sales_reps = generate_sales_reps(num_rows)
products = generate_products(num_rows)
users = generate_users(num_rows)

# Establish connection to the database
conn = get_db_connection()
cursor = conn.cursor()

# Reset all present data in the tables
tables_to_reset = ["opportunities", "tasks", "interactions", "payments", "sales_rep", "user_sales_rep", "products", "customers", "users"]
for table in tables_to_reset:
    cursor.execute(f"DELETE FROM {table};")
conn.commit()

# Step 1: Insert users
cursor.executemany("""
    INSERT INTO users (username, password_hash, email, role) 
    VALUES (%s, %s, %s, %s);
""", users)

# Insert customers
cursor.executemany("""
    INSERT INTO customers (name, email, phone, industry,country) 
    VALUES (%s, %s, %s, %s, %s);
""", customers)

# Insert sales reps
cursor.executemany("""
    INSERT INTO sales_rep (full_name, email) VALUES (%s, %s);
""", sales_reps)

# Insert products
cursor.executemany("""
    INSERT INTO products (name, description, price, stock_quantity) 
    VALUES (%s, %s, %s, %s);
""", products)

# Insert tasks (assuming you have customer and sales rep IDs available)
task_ids = [1, 2, 3]  # Example task_ids
tasks = generate_tasks(num_rows, [random.randint(1, num_rows) for _ in range(num_rows)], [random.randint(1, num_rows) for _ in range(num_rows)])

cursor.executemany("""
    INSERT INTO tasks (customer_id, rep_id, task_type, due_date, notes, status)
    VALUES (%s, %s, %s, %s, %s, %s);
""", tasks)

# Insert opportunities (assuming you have customer_id, product_id, and rep_id)
#opportunities = [
#    (random.randint(1, num_rows), random.randint(1, num_rows), random.randint(1, num_rows), 'new', round(random.uniform(1000, 10000), 2), '2025-12-31')
#    for _ in range(num_rows)
#]
customer_ids = list(range(1, num_rows + 1))
opportunities = generate_opportunities(num_rows, customer_ids,customer_ids,customer_ids)
cursor.executemany("""
    INSERT INTO opportunities (customer_id, product_id, rep_id, status, estimated_value, close_date)
    VALUES (%s, %s, %s, %s, %s, %s);
""", opportunities)

# Commit changes to the database
conn.commit()
# Assuming `generate_payments` and `generate_user_sales_rep` functions are already defined

# Step 1: Generate data for payments and user-sales rep relationships
# Generate random data for payments and user-sales rep relationships

payments = generate_payments(num_rows, customer_ids)   # Use customer IDs from `customers` list
user_sales_rep = generate_user_sales_rep(num_rows, customer_ids)  # Use sales rep IDs from `sales_reps` list
interactions = generate_interactions(num_rows, customer_ids,customer_ids,customer_ids)

cursor.executemany("""
    INSERT INTO payments (customer_id, amount, payment_date, payment_method, status)
    VALUES (%s, %s, %s, %s, %s);
""", payments)

# Insert data into user_sales_rep table
cursor.executemany("""
    INSERT INTO user_sales_rep (user_id, rep_id)
    VALUES (%s, %s);
""", user_sales_rep)

cursor.executemany("""
    INSERT INTO interactions (customer_id, rep_id, interaction_type, interaction_date, notes, follow_up_task_id)
    VALUES (%s, %s, %s, %s, %s, %s);
""", interactions)

# Step 4: Commit changes to both tables
conn.commit()
# Close connection
cursor.close()
conn.close()
