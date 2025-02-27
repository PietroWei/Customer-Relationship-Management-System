import random
from datetime import datetime, timedelta

# Function to generate random dates
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Set date range for interactions and sales
start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 2, 27)

# Function to generate random customer data
def generate_customers(num):
    industries = ['Technology', 'Finance', 'Retail', 'Healthcare', 'Education', 'E-commerce', 'Manufacturing', 'Real Estate', 'Hospitality', 'Automotive']
    customers = []
    for i in range(1, num + 1):
        name = f'Customer{i}'
        email = f'customer{i}@example.com'
        phone = f'{i:03}-{i:03}-{i:04}'
        industry = random.choice(industries)
        customers.append((name, email, phone, industry))
    return customers

# Function to generate random lead data
def generate_leads(num):
    lead_sources = ['Website', 'Referral', 'Social Media', 'Advertisement', 'Cold Call', 'Email Campaign', 'Trade Show']
    statuses = ['New', 'Qualified', 'Converted', 'Contacted', 'Lost']
    leads = [(random.randint(1, num), random.choice(lead_sources), random.choice(statuses)) for _ in range(num)]
    return leads

# Function to generate multiple random interactions per customer
def generate_interactions(num, max_per_customer=5):
    interaction_types = ['Email', 'Call', 'Meeting']
    interactions = []
    for _ in range(num * max_per_customer):
        customer_id = random.randint(1, num)
        interaction_type = random.choice(interaction_types)
        interaction_date = random_date(start_date, end_date).strftime('%Y-%m-%d %H:%M:%S')
        notes = f'Interaction note for customer {customer_id}'.replace("'", "''")  # Escape quotes
        interactions.append((customer_id, interaction_type, interaction_date, notes))
    return interactions

# Function to generate random sales history data
def generate_sales_history(num):
    products = ['CRM Software Subscription', 'Financial Consulting Package', 'Retail Analytics Report', 'Healthcare Data Management', 
                'Online Learning Platform License', 'E-commerce Growth Strategy', 'Manufacturing Process Optimization', 
                'Real Estate Investment Analysis', 'Hospitality Revenue Forecasting', 'Automotive Supply Chain Software']
    sales_history = []
    for _ in range(num):
        customer_id = random.randint(1, num)
        amount = round(random.uniform(500, 5000), 2)
        product = random.choice(products)
        sale_date = random_date(start_date, end_date).strftime('%Y-%m-%d')
        sales_history.append((customer_id, amount, product, sale_date))
    return sales_history

# Number of rows
num_rows = 1000

# Generate data
customers = generate_customers(num_rows)
leads = generate_leads(num_rows)
interactions = generate_interactions(num_rows)
sales_history = generate_sales_history(num_rows)

# Write SQL insert statements to a file
with open('insert_statements.sql', 'w') as f:
    lines = ["-- Insert customers\n"]
    lines += [f"INSERT INTO customers (name, email, phone, industry) VALUES ('{c[0]}', '{c[1]}', '{c[2]}', '{c[3]}');\n" for c in customers]
    
    lines.append("\n-- Insert leads\n")
    lines += [f"INSERT INTO leads (customer_id, lead_source, status) VALUES ({l[0]}, '{l[1]}', '{l[2]}');\n" for l in leads]
    
    lines.append("\n-- Insert interactions\n")
    lines += [f"INSERT INTO interactions (customer_id, interaction_type, interaction_date, notes) VALUES ({i[0]}, '{i[1]}', '{i[2]}', '{i[3]}');\n" for i in interactions]
    
    lines.append("\n-- Insert sales history\n")
    lines += [f"INSERT INTO sales_history (customer_id, amount, product, sale_date) VALUES ({s[0]}, {s[1]}, '{s[2]}', '{s[3]}');\n" for s in sales_history]
    
    f.writelines(lines)

print("SQL insert statements have been written to insert_statements.sql")
