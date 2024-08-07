#### Schools

from sqlalchemy import create_engine
import pandas as pd
from faker import Faker
import random

fake = Faker('en_US')

# create Schools table
create_schools_table_query = """
CREATE TABLE IF NOT EXISTS schools (
    school_id INT PRIMARY KEY,
    address VARCHAR(255),
    postcode VARCHAR(100),
    type VARCHAR(50)
);
"""
with engine.connect() as connection:
    connection.execute(create_schools_table_query)

print("schools table has been created successfully.")

school_types = ['Kindergarten', 'Primary School', 'Middle School', 'High School']

nyc_postcodes = [
    '10001', '10002', '10003', '10004', '10005', '10006', '10007', '10009', '10010', '10011',
    '10012', '10013', '10014', '10016', '10017', '10018', '10019', '10020', '10021', '10022',
    '10023', '10024', '10025', '10026', '10027', '10028', '10029', '10030', '10031', '10032',
    '10033', '10034', '10035', '10036', '10037', '10038', '10039', '10040', '10044', '10065',
    '10075', '10128', '10280', '10282', '10301', '10302', '10303', '10304', '10305', '10306',
    '10307', '10308', '10309', '10310', '10312', '10314', '10451', '10452', '10453', '10454',
    '10455', '10456', '10457', '10458', '10459', '10460', '10461', '10462', '10463', '10464',
    '10465', '10466', '10467', '10468', '10469', '10470', '10471', '10472', '10473', '10474',
    '10475', '11004', '11005', '11101', '11102', '11103', '11104', '11105', '11106', '11109',
    '11201', '11203', '11204', '11205', '11206', '11207', '11208', '11209', '11210', '11211',
    '11212', '11213', '11214', '11215', '11216', '11217', '11218', '11219', '11220', '11221',
    '11222', '11223', '11224', '11225', '11226', '11228', '11229', '11230', '11231', '11232',
    '11233', '11234', '11235', '11236', '11237', '11238', '11239', '11249', '11354', '11355',
    '11356', '11357', '11358', '11359', '11360', '11361', '11362', '11363', '11364', '11365',
    '11366', '11367', '11368', '11369', '11370', '11371', '11372', '11373', '11374', '11375',
    '11377', '11378', '11379', '11385', '11411', '11412', '11413', '11414', '11415', '11416',
    '11417', '11418', '11419', '11420', '11421', '11422', '11423', '11426', '11427', '11428',
    '11429', '11432', '11433', '11434', '11435', '11436', '11691', '11692', '11693', '11694',
    '11695', '11697'
]

# generate data for 100 schools
schools_data = {
    'school_id': [i for i in range(1, 101)],
    'address': [fake.street_address() + ', New York, NY' for _ in range(100)],
    'postcode': [random.choice(nyc_postcodes) for _ in range(100)],
    'type': [random.choice(school_types) for _ in range(100)]
}

df_schools = pd.DataFrame(schools_data)

# insert data
try:
    df_schools.to_sql('schools', engine, if_exists='append', index=False)
    print("100 rows of school data inserted successfully into the Schools table.")
except Exception as e:
    print(f"An error occurred: {e}")

#### add school_id into homes

from sqlalchemy import create_engine, text

# Add 'school_id' column to the 'homes' table
add_column_query = """
ALTER TABLE homes
ADD COLUMN school_id INT;
"""
with engine.connect() as connection:
    connection.execute(add_column_query)
print("Column 'school_id' has been added to the 'homes' table.")

# Fetch all school_ids from the 'schools' table
school_ids = pd.read_sql_query("SELECT school_id FROM schools", engine)['school_id'].tolist()

# Fetch all homes to update
homes = pd.read_sql_query("SELECT * FROM homes", engine)

# Randomly assign school_ids to homes
homes['school_id'] = [random.choice(school_ids) for _ in range(len(homes))]

# Update the 'homes' table with the assigned school_ids
homes.to_sql('homes', engine, if_exists='replace', index=False)
print("Column 'school_id' has been updated in the 'homes' table.")

#### Clients

import re

# formatting phone numbers to US format
fake = Faker('en_US')

# Function to format phone numbers into a consistent pattern
def format_phone_number(number):
    area_code = ''.join(random.choices('0123456789', k=3))
    prefix = ''.join(random.choices('0123456789', k=3))
    line_number = ''.join(random.choices('0123456789', k=4))

    # Remove all non-digit characters
    digits = re.sub(r'\D', '', number)
    # Ensure the number is exactly 10 digits long
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits.startswith('1'):
        return f"{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    else:
        return f"{area_code}-{prefix}-{line_number}"


# Generate data for 1000 clients
client_data = {
    'client_id': [i for i in range(1, 1001)],
    'first_name': [fake.first_name() for _ in range(1000)],
    'last_name': [fake.last_name() for _ in range(1000)],
    'email': [fake.email() for _ in range(1000)],
    'phone_number': [format_phone_number(fake.phone_number()) for _ in range(1000)],
    'client_type': [fake.random_element(elements=('Individual', 'Company')) for _ in range(1000)]
}

# Create a DataFrame
df_clients = pd.DataFrame(client_data)

# Create the Clients table
create_clients_table_query = """
CREATE TABLE IF NOT EXISTS clients (
    client_id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone_number VARCHAR(15),
    client_type VARCHAR(50)
);
"""
with engine.connect() as connection:
    connection.execute(create_clients_table_query)

# Insert data into the Clients table
try:
    df_clients.to_sql('clients', engine, if_exists='append', index=False)
    print("1000 rows of client data inserted successfully into the clients table.")
except Exception as e:
    print(f"An error occurred: {e}")

#### ClientPreferences

db_url = "postgresql+psycopg2://postgres:123@localhost:5432/Dream_Homes_NYC"
engine = create_engine(db_url)
conn = engine.connect()

# Create the ClientPreferences table
create_preferences_table_query = """
CREATE TABLE IF NOT EXISTS clientpreferences (
    preference_id INT PRIMARY KEY,
    client_id INT,
    preference_type VARCHAR(50),
    value VARCHAR(255),
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
);
"""
with engine.connect() as connection:
    connection.execute(create_preferences_table_query)


# Define preference-related words for each type
preference_values = {
    'Color': ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange', 'Black', 'White', 'Pink', 'Gray'],
    'Size': ['Single Family', 'Two Family', 'Three Family', 'Four Family', 'Condo'],
    'Brand': ['Ikea', 'Raymour&Flanigan', 'Ethan Ellen', 'Rove', 'West Elm', 'Castlery', 'Samsung', 'LG'],
    'Category': ['Modern Design', 'Brick Structure', 'Wood Structure', 'Fire Place', 'Old School Design']
}

# get existing client_id
existing_client_ids_query = "SELECT client_id FROM clients"
with engine.connect() as connection:
    existing_client_ids = [row['client_id'] for row in connection.execute(existing_client_ids_query)]

# Generate data for 5000 client preferences
preference_data = {
    'preference_id': [i for i in range(1, 5001)],
    'client_id': [random.choice(existing_client_ids) for _ in range(5000)],
    'preference_type': [fake.random_element(elements=('Color', 'Size', 'Brand', 'Category')) for _ in range(5000)]
}

#Generate value based on type
preference_data['value'] = [random.choice(preference_values[preference_type])
                            for preference_type in preference_data['preference_type']]

# Create a DataFrame
df_preferences = pd.DataFrame(preference_data)
# Insert data into the ClientPreferences table
try:
    df_preferences.to_sql('clientpreferences', engine, if_exists='append', index=False)
    print("5000 rows of client preference data inserted successfully into the clientpreferences table.")
except Exception as e:
    print(f"An error occurred: {e}")

#  Emolyee role:

create_employee_roles_table_query = """
CREATE TABLE IF NOT EXISTS employeeroles (
    role_id INT PRIMARY KEY,
    role_name VARCHAR(50),
    description TEXT
);
"""

with engine.connect() as connection:
    connection.execute(create_employee_roles_table_query)

# create fixed roles
role_data = {
    'role_id': [1, 2, 3],
    'role_name': ['Associate', 'Senior', 'Manager'],
    'description': ['Entry level position', 'Experienced professional', 'Management position']
}

df_roles = pd.DataFrame(role_data)

# insert into EmployeeRoles table
try:
    df_roles.to_sql('employeeroles', engine, if_exists='append', index=False)
    print("3 rows of role data inserted successfully into the employeeroles table.")
except Exception as e:
    print(f"An error occurred: {e}")

#### Employees

# Create the Employees table
create_employees_table_query = """
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    role_id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone_number VARCHAR(15),
    employment_type VARCHAR(50),
    FOREIGN KEY (role_id) REFERENCES employeeroles(role_id)
);
"""
with engine.connect() as connection:
    connection.execute(create_employees_table_query)

# Get existing role_id
existing_role_ids_query = "SELECT role_id FROM employeeroles"
with engine.connect() as connection:
    existing_role_ids = [row['role_id'] for row in connection.execute(existing_role_ids_query)]

# Generate data for 100 employees
employee_data = {
    'employee_id': [i for i in range(1, 101)],
    'role_id': [random.choice(existing_role_ids) for _ in range(100)],
    'first_name': [fake.first_name() for _ in range(100)],
    'last_name': [fake.last_name() for _ in range(100)],
    'email': [fake.email() for _ in range(100)],
    'phone_number': [format_phone_number(fake.phone_number()) for _ in range(100)],
    'employment_type': [fake.random_element(elements=('Full-Time', 'Part-Time', 'Contract', 'Temporary')) for _ in range(100)]
}

# Create a DataFrame
df_employees = pd.DataFrame(employee_data)

# Insert data into the Employees table
try:
    df_employees.to_sql('employees', engine, if_exists='append', index=False)
    print("100 rows of employee data inserted successfully into the employees table.")
except Exception as e:
    print(f"An error occurred: {e}")

#### Owners

# Generate data for 1000 owners
owners_data = {
    'owner_id': [i for i in range(1, 1001)],
    'first_name': [fake.first_name() for _ in range(1000)],
    'last_name': [fake.last_name() for _ in range(1000)],
    'email': [fake.email() for _ in range(1000)],
    'phone_number': [fake.phone_number() for _ in range(1000)]
}

# Create a DataFrame
df_owners = pd.DataFrame(owners_data)

# Create the Owners table
create_owners_table_query = """
CREATE TABLE IF NOT EXISTS owners (
    owner_id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone_number VARCHAR(15)
);
"""
with engine.connect() as connection:
    connection.execute(create_owners_table_query)

# Insert data into the Owners table
try:
    df_owners.to_sql('owners', engine, if_exists='append', index=False)
    print("1000 rows of owners data inserted successfully into the owners table.")
except Exception as e:
    print(f"An error occurred: {e}")

#### TransactionTypes

# Data for TransactionsTypes
transaction_types_data = {
    'transaction_type_id': [i for i in range(1, 6)],
    'transaction_type_name': ['Purchase', 'Lease', 'Sale', 'Rent', 'Mortgage'],
    'description': [fake.text(max_nb_chars=200) for _ in range(5)]
}

# Create a DataFrame
df_transaction_types = pd.DataFrame(transaction_types_data)

# Create the TransactionsTypes table
create_transaction_types_table_query = """
CREATE TABLE IF NOT EXISTS TransactionsTypes (
    transaction_type_id INT PRIMARY KEY,
    transaction_type_name VARCHAR(50),
    description TEXT
);
"""
with engine.connect() as connection:
    connection.execute(create_transaction_types_table_query)

# Insert data into the TransactionsTypes table
try:
    df_transaction_types.to_sql('TransactionsTypes', engine, if_exists='append', index=False)
    print("5 rows of transaction types data inserted successfully into the TransactionsTypes table.")
except Exception as e:
    print(f"An error occurred: {e}")

#### Transactions

# Generate data for 400 transactions
transaction_data = {
    'transaction_id': [i for i in range(1, 401)],
    'home_id': [fake.random_int(min=1, max=500) for _ in range(400)],
    'buyer_id': [fake.random_int(min=1, max=1000) for _ in range(400)],
    'owner_id': [fake.random_int(min=1, max=1000) for _ in range(400)],
    'agent_id': [fake.random_int(min=1, max=100) for _ in range(400)],
    'transaction_type_id': [fake.random_int(min=1, max=5) for _ in range(400)],
    'date': [fake.date_between(start_date='-2y', end_date='today') for _ in range(400)],
    'amount': [round(random.uniform(10000, 1000000), 2) for _ in range(400)]
}

# Create a DataFrame
df_transactions = pd.DataFrame(transaction_data)

# Create the Transactions table
create_transactions_table_query = """
CREATE TABLE IF NOT EXISTS Transactions (
    transaction_id INT PRIMARY KEY,
    home_id INT,
    buyer_id INT,
    owner_id INT,
    agent_id INT,
    transaction_type_id INT,
    date DATE,
    amount DECIMAL(10, 2),
    FOREIGN KEY (home_id) REFERENCES Homes(home_id),
    FOREIGN KEY (buyer_id) REFERENCES Clients(client_id),
    FOREIGN KEY (owner_id) REFERENCES Owners(owner_id),
    FOREIGN KEY (agent_id) REFERENCES Employees(employee_id),
    FOREIGN KEY (transaction_type_id) REFERENCES TransactionsTypes(transaction_type_id)
);
"""
with engine.connect() as connection:
    connection.execute(create_transactions_table_query)

# Insert data into the Transactions table
try:
    df_transactions.to_sql('Transactions', engine, if_exists='append', index=False)
    print("400 rows of transaction data inserted successfully into the Transactions table.")
except Exception as e:
    print(f"An error occurred: {e}")

#### PaymentMethods

# Data for PaymentMethods with realistic descriptions
payment_methods_data = {
    'payment_method_id': [i for i in range(1, 6)],
    'method_name': ['Credit Card', 'Bank Transfer', 'Cash', 'Check', 'Cryptocurrency'],
    'description': [
        'Payments made using credit cards are processed through merchant services and typically involve fees. Suitable for smaller transactions.',
        'Bank transfers are direct transfers of funds from one bank account to another. Common for large transactions due to security and traceability.',
        'Cash transactions are immediate and often used for smaller, informal payments. Not common for large real estate transactions due to risk and lack of traceability.',
        'Checks are written orders directing a bank to pay a specified amount from the drawer’s account. Commonly used for deposits and larger payments.',
        'Cryptocurrencies offer a digital payment method with decentralized control. Used occasionally in real estate for its security and global reach, though not widely accepted.'
    ]
}

# Create a DataFrame
df_payment_methods = pd.DataFrame(payment_methods_data)

# Create the PaymentMethods table
create_payment_methods_table_query = """
CREATE TABLE IF NOT EXISTS paymentmethods (
    payment_method_id INT PRIMARY KEY,
    method_name VARCHAR(50),
    description TEXT
);
"""
with engine.connect() as connection:
    connection.execute(create_payment_methods_table_query)

# Insert data into the PaymentMethods table
try:
    df_payment_methods.to_sql('paymentmethods', engine, if_exists='append', index=False)
    print("5 rows of payment methods data inserted successfully into the paymentmethods table.")
except Exception as e:
    print(f"An error occurred: {e}")

#### TransactionPayments

# Generate data for 400 transaction payments
transaction_payments_data = {
    'payment_id': [i for i in range(1, 401)],
    'transaction_id': [fake.random_int(min=1, max=400) for _ in range(400)],
    'payment_method_id': [fake.random_int(min=1, max=5) for _ in range(400)],
    'amount': [round(random.uniform(10000, 1000000), 2) for _ in range(400)],
    'date': [fake.date_between(start_date='-2y', end_date='today') for _ in range(400)]
}

# Create a DataFrame
df_transaction_payments = pd.DataFrame(transaction_payments_data)

# Create the TransactionPayments table
create_transaction_payments_table_query = """
CREATE TABLE IF NOT EXISTS TransactionPayments (
    payment_id INT PRIMARY KEY,
    transaction_id INT,
    payment_method_id INT,
    amount DECIMAL(10, 2),
    date DATE,
    FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id),
    FOREIGN KEY (payment_method_id) REFERENCES PaymentMethods(payment_method_id)
);
"""
with engine.connect() as connection:
    connection.execute(create_transaction_payments_table_query)

# Insert data into the TransactionPayments table
try:
    df_transaction_payments.to_sql('TransactionPayments', engine, if_exists='append', index=False)
    print("400 rows of transaction payments data inserted successfully into the TransactionPayments table.")
except Exception as e:
    print(f"An error occurred: {e}")

# Office:

# generate office data
office_data = {
    'office_id': [1, 2, 3],
    'address': ['123 Broadway', '101 Park Ave', '202 Madison Ave'],
    'city': ['New York'] * 3,
    'state': ['NY'] * 3,
    'zip_code': ['10001', '10178', '10016'],
    'phone_number': ['212-555-0101', '212-555-0134', '212-555-0145']
}

df_offices = pd.DataFrame(office_data)

# create offices table
create_offices_table_query = """
CREATE TABLE IF NOT EXISTS offices (
    office_id INT PRIMARY KEY,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    phone_number VARCHAR(15)
);
"""

with engine.connect() as connection:
    connection.execute(create_offices_table_query)

# insert data
try:
    df_offices.to_sql('offices', engine, if_exists='append', index=False)
    print("3 rows of office data inserted successfully into the offices table.")
except Exception as e:
    print(f"An error occurred: {e}")

# Expenses:

# Define SQL query to create Expenses table
create_expenses_table_query = """
CREATE TABLE IF NOT EXISTS expenses (
    expense_id INT PRIMARY KEY,
    description TEXT,
    amount DECIMAL(10, 2),
    date DATE,
    office_id INT,
    FOREIGN KEY (office_id) REFERENCES offices(office_id)
);
"""

with engine.connect() as connection:
    connection.execute(create_expenses_table_query)

print("Expenses table created successfully.")

# Predefined descriptions for expenses relevant to a real estate company in NYC
expense_descriptions = [
    "Office Rent", "Utilities", "Property Maintenance", "Marketing Campaign",
    "Employee Salaries", "Office Supplies", "Legal Fees", "Insurance Premiums",
    "Travel Expenses", "Client Entertainment", "Professional Development",
    "Website Maintenance", "IT Services", "Furniture Purchase", "Cleaning Services",
    "Security Services", "Software Subscriptions", "Advertising Costs", "Commission Payments",
    "Event Sponsorship", "Training Workshops", "Networking Events", "Property Taxes",
    "Renovation Costs", "Consultant Fees", "Public Relations", "Office Equipment",
    "Internet Services", "Telephone Services", "Courier Services"
]

# Get existing office_id
existing_office_ids_query = "SELECT office_id FROM offices"
with engine.connect() as connection:
    existing_office_ids = [row['office_id'] for row in connection.execute(existing_office_ids_query)]

# Generate 1000 rows of data for Expenses table
fake = Faker()
expense_data = {
    'expense_id': [i for i in range(1, 1001)],
    'description': [random.choice(expense_descriptions) for _ in range(1000)],
    'amount': [round(random.uniform(100.0, 5000.0), 2) for _ in range(1000)],
    'date': [fake.date_this_year() for _ in range(1000)],
    'office_id': [random.choice(existing_office_ids) for _ in range(1000)]
}

df_expenses = pd.DataFrame(expense_data)

# Insert data into Expenses table
try:
    df_expenses.to_sql('expenses', engine, if_exists='append', index=False)
    print("1000 rows of expense data inserted successfully into the expenses table.")
except Exception as e:
    print(f"An error occurred: {e}")

# EmployeeOfficeAssignment

# use Faker to generate 125 EmployeeOfficeAssignments data
fake = Faker()
assignment_data = {
    'assignment_id': [i for i in range(1, 126)],
    'employee_id': [random.randint(1, 100) for _ in range(125)],
    'office_id': [random.choice([1, 2, 3]) for _ in range(125)],
    'start_date': [fake.date_between(start_date='-2y', end_date='today') for _ in range(125)],
    'end_date': [fake.date_between(start_date='today', end_date='+1y') for _ in range(125)]
}

df_assignments = pd.DataFrame(assignment_data)

# create EmployeeOfficeAssignments table
create_assignments_table_query = """
CREATE TABLE IF NOT EXISTS employeeofficeassignments (
    assignment_id INT PRIMARY KEY,
    employee_id INT,
    office_id INT,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (office_id) REFERENCES offices(office_id)
);
"""

with engine.connect() as connection:
    connection.execute(create_assignments_table_query)

# insert into EmployeeOfficeAssignments table
try:
    df_assignments.to_sql('employeeofficeassignments', engine, if_exists='append', index=False)
    print("125 rows of assignment data inserted successfully into the employeeofficeassignments table.")
except Exception as e:
    print(f"An error occurred: {e}")

# Marketingcampagin&campaign results
# Define SQL query to create marketingcampaigns table
create_marketing_campaigns_table_query = """
CREATE TABLE IF NOT EXISTS marketingcampaigns (
    campaign_id INT PRIMARY KEY,
    campaign_name VARCHAR(100),
    description TEXT,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(10, 2)
);
"""

# Define SQL query to create campaignresults table with CHECK constraint
create_campaign_results_table_query = """
CREATE TABLE IF NOT EXISTS campaignresults (
    result_id INT PRIMARY KEY,
    campaign_id INT,
    result_description TEXT CHECK (result_description IN ('High', 'Medium', 'Low')),
    result_date DATE,
    FOREIGN KEY (campaign_id) REFERENCES marketingcampaigns(campaign_id)
);
"""

# Create tables
with engine.connect() as connection:
    connection.execute(create_marketing_campaigns_table_query)
    connection.execute(create_campaign_results_table_query)

print("Tables created successfully.")

# Generate data using Faker
fake = Faker()

# Predefined campaign names and descriptions for a real estate company
campaign_names = [
    "Spring Property Showcase",
    "Luxury Homes Expo",
    "First-Time Buyer Seminar",
    "Investor Opportunities Event",
    "Holiday Open House Tour",
    "New Development Unveiling",
    "Real Estate Investment Webinar",
    "Community Homes Fair",
    "Exclusive Property Auction",
    "Virtual Home Tour Week"
]

campaign_descriptions = [
    "Join us for a showcase of the best properties this spring. Exclusive deals available for attendees.",
    "Explore luxury homes in your area. Meet with top real estate agents and get special offers.",
    "A seminar for first-time homebuyers. Learn everything you need to know about buying your first home.",
    "Discover investment opportunities in the real estate market. Network with other investors.",
    "Tour homes decorated for the holidays. Find your dream home before the end of the year.",
    "Be the first to see our new development. Exclusive pre-sale prices for early buyers.",
    "Join our webinar on real estate investment. Learn from experts and ask your questions.",
    "A fair showcasing homes in the community. Connect with local real estate agents and get great deals.",
    "Attend our exclusive property auction. Bid on prime real estate at unbeatable prices.",
    "Experience our virtual home tour week. View properties from the comfort of your home."
]

# Generate data for marketingcampaigns table
campaign_data = {
    'campaign_id': [i for i in range(1, 21)],
    'campaign_name': [random.choice(campaign_names) for _ in range(20)],
    'description': [random.choice(campaign_descriptions) for _ in range(20)],
    'start_date': [fake.date_between(start_date='-2y', end_date='-1y') for _ in range(20)],
    'end_date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(20)],
    'budget': [round(random.uniform(1000, 100000), 2) for _ in range(20)]
}

df_campaigns = pd.DataFrame(campaign_data)

# Insert data into marketingcampaigns table
try:
    df_campaigns.to_sql('marketingcampaigns', engine, if_exists='append', index=False)
    print("20 rows of campaign data inserted successfully into the marketingcampaigns table.")
except Exception as e:
    print(f"An error occurred: {e}")

# Generate data for campaignresults table with limited descriptions
result_descriptions = ['High', 'Medium', 'Low']
result_data = {
    'result_id': [i for i in range(1, 21)],
    'campaign_id': [random.choice([i for i in range(1, 21)]) for _ in range(20)],
    'result_description': [random.choice(result_descriptions) for _ in range(20)],
    'result_date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(20)]
}

df_results = pd.DataFrame(result_data)

# Insert data into campaignresults table
try:
    df_results.to_sql('campaignresults', engine, if_exists='append', index=False)
    print("20 rows of result data inserted successfully into the campaignresults table.")
except Exception as e:
    print(f"An error occurred: {e}")

# Payment method:
import pandas as pd
from sqlalchemy import create_engine
from faker import Faker
import random

fake = Faker()

engine = create_engine('sqlite:///realestate.db', echo=True)


create_payment_methods_table_query = """
CREATE TABLE IF NOT EXISTS PaymentMethods (
    payment_method_id INT PRIMARY KEY,
    method_name VARCHAR(50),
    description TEXT
);
"""

with engine.connect() as connection:
    connection.execute(create_payment_methods_table_query)

print("PaymentMethods table created successfully.")

# fixed payment method types
payment_methods_data = {
    'payment_method_id': [1, 2, 3, 4, 5],
    'method_name': ['Credit Card', 'Debit Card', 'Bank Transfer', 'Cash', 'PayPal'],
    'description': [
        'Payment made using credit card',
        'Payment made using debit card',
        'Payment made through bank transfer',
        'Payment made in cash',
        'Payment made using PayPal'
    ]
}

df_payment_methods = pd.DataFrame(payment_methods_data)

# insert into PaymentMethods
try:
    df_payment_methods.to_sql('PaymentMethods', engine, if_exists='append', index=False)
    print("5 rows of payment methods data inserted successfully into the PaymentMethods table.")
except Exception as e:
    print(f"An error occurred: {e}")

# randomly generate 400 TransactionPayments sample data
transaction_payments_data = {
    'payment_id': [i for i in range(1, 401)],
    'transaction_id': [fake.random_int(min=1, max=400) for _ in range(400)],
    'payment_method_id': [fake.random_int(min=1, max=5) for _ in range(400)],
    'amount': [round(random.uniform(10000, 1000000), 2) for _ in range(400)],
    'date': [fake.date_between(start_date='-2y', end_date='today') for _ in range(400)]
}

df_transaction_payments = pd.DataFrame(transaction_payments_data)

# insert into TransactionPayments
try:
    df_transaction_payments.to_sql('TransactionPayments', engine, if_exists='append', index=False)
    print("400 rows of transaction payments data inserted successfully into the TransactionPayments table.")
except Exception as e:
    print(f"An error occurred: {e}")

# HomefeatureAssignments& HomeFeatures:
# Define SQL query to create HomeFeatures table
create_home_features_table_query = """
CREATE TABLE IF NOT EXISTS homefeatures (
    feature_id INT PRIMARY KEY,
    feature_name VARCHAR(50),
    description TEXT
);
"""

with engine.connect() as connection:
    connection.execute(create_home_features_table_query)

print("homefeatures table created successfully.")

# Predefined home feature names and descriptions for NYC house sales
feature_names = [
    "Central Air Conditioning", "Hardwood Floors", "Granite Countertops",
    "Stainless Steel Appliances", "Walk-In Closet", "In-Unit Laundry",
    "Private Balcony", "Rooftop Access", "Gym Access", "Pet-Friendly",
    "Doorman Service", "Swimming Pool", "Garage Parking", "High Ceilings",
    "Fireplace", "Home Office", "Renovated Kitchen", "Smart Home System",
    "Energy Efficient Windows", "Soundproof Walls", "Heated Floors",
    "Wine Cellar", "Home Theater", "Jacuzzi", "Private Garden",
    "Security System", "Guest Suite", "Library", "Sauna", "Billiard Room",
    "Yoga Studio", "Tennis Court", "Basketball Court", "Private Elevator",
    "Media Room", "Pantry", "Breakfast Nook", "Sunroom", "Mudroom",
    "Workshop", "Storage Room", "Attic", "Basement", "En Suite Bathroom",
    "Butler's Pantry", "Formal Dining Room", "Outdoor Kitchen",
    "Spa Bathroom", "Greenhouse", "Corner Unit"
]

# Descriptions for the predefined features
feature_descriptions = [
    "Provides cool air throughout the home for ultimate comfort.",
    "Elegant and durable floors made from high-quality wood.",
    "Durable and attractive countertops made from granite.",
    "Modern and sleek kitchen appliances made from stainless steel.",
    "Spacious closet with ample room for clothing and storage.",
    "Convenient and private laundry facilities within the unit.",
    "Private outdoor space with great views and fresh air.",
    "Access to rooftop amenities and entertainment areas.",
    "State-of-the-art fitness center available to residents.",
    "Allows pets with certain conditions and amenities for them.",
    "Professional doorman service for added security and convenience.",
    "Outdoor pool available for residents to enjoy.",
    "Secure and convenient parking space within the building.",
    "Tall ceilings that enhance the sense of space and light.",
    "Cozy fireplace for warmth and ambiance.",
    "Dedicated space for a home office setup.",
    "Recently updated kitchen with modern amenities.",
    "Integrated smart home features for enhanced living.",
    "Windows designed to reduce energy consumption.",
    "Walls designed to minimize noise from outside or neighbors.",
    "Luxuriously heated floors for added comfort.",
    "Specialized storage for wine collections.",
    "Home theater setup for an immersive viewing experience.",
    "Luxurious jacuzzi for relaxation and wellness.",
    "Private garden space for outdoor enjoyment.",
    "Advanced security system for peace of mind.",
    "Separate suite for guests or extended family.",
    "A quiet space for reading and study.",
    "Relaxing sauna available for residents.",
    "Room equipped with a pool table and entertainment.",
    "Dedicated space for yoga and meditation.",
    "Private tennis court available for residents.",
    "Basketball court available for recreational use.",
    "Private elevator for direct access to the unit.",
    "Room designed for media consumption and entertainment.",
    "Additional kitchen space for storage and prep.",
    "Cozy nook for breakfast and casual dining.",
    "Bright sunroom with plenty of natural light.",
    "Entryway space designed for shoes and coats.",
    "Space dedicated to hobbies and DIY projects.",
    "Room for additional storage needs.",
    "Additional attic space for storage or conversion.",
    "Basement space for storage or additional rooms.",
    "Private bathroom connected to the bedroom.",
    "Additional pantry space for food storage.",
    "Formal space for dining with guests.",
    "Outdoor kitchen setup for cooking and entertaining.",
    "Luxurious bathroom with spa-like features.",
    "Greenhouse space for plants and gardening.",
    "Unit located on the corner for additional light and views."
]

# Generate data for HomeFeatures table
home_features_data = {
    'feature_id': [i for i in range(1, 51)],
    'feature_name': [feature_names[i % len(feature_names)] for i in range(50)],
    'description': [feature_descriptions[i % len(feature_descriptions)] for i in range(50)]
}

df_home_features = pd.DataFrame(home_features_data)

# Insert data into HomeFeatures table
try:
    df_home_features.to_sql('homefeatures', engine, if_exists='append', index=False)
    print("50 rows of home features data inserted successfully into the homefeatures table.")
except Exception as e:
    print(f"An error occurred: {e}")

# Define SQL query to create HomeFeatureAssignments table
create_home_feature_assignments_table_query = """
CREATE TABLE IF NOT EXISTS homefeatureassignments (
    assignment_id INT PRIMARY KEY,
    home_id INT,
    feature_id INT,
    FOREIGN KEY (home_id) REFERENCES homes(home_id),
    FOREIGN KEY (feature_id) REFERENCES homefeatures(feature_id)
);
"""

with engine.connect() as connection:
    connection.execute(create_home_feature_assignments_table_query)

print("homefeatureassignments table created successfully.")

# Get existing home_id
existing_home_ids_query = "SELECT home_id FROM homes"
with engine.connect() as connection:
    existing_home_ids = [row['home_id'] for row in connection.execute(existing_home_ids_query)]

# Randomly generate 5000 HomeFeatureAssignments sample data
home_feature_assignments_data = {
    'assignment_id': [i for i in range(1, 5001)],
    'home_id': [random.choice(existing_home_ids) for _ in range(5000)],
    'feature_id': [random.randint(1, 50) for _ in range(5000)]
}

df_home_feature_assignments = pd.DataFrame(home_feature_assignments_data)

# Insert data into HomeFeatureAssignments
try:
    df_home_feature_assignments.to_sql('homefeatureassignments', engine, if_exists='append', index=False)
    print("5000 rows of home feature assignments data inserted successfully into the homefeatureassignments table.")
except Exception as e:
    print(f"An error occurred: {e}")

# Openhouses:
import pandas as pd
from sqlalchemy import create_engine
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

db_url = "postgresql+psycopg2://postgres:123@localhost:5432/Dream_Homes_NYC"
engine = create_engine(db_url)
conn = engine.connect()

create_open_houses_table_query = """
CREATE TABLE IF NOT EXISTS openhouses (
    open_house_id INT PRIMARY KEY,
    home_id INT,
    date DATE,
    start_time TIME,
    end_time TIME,
    FOREIGN KEY (home_id) REFERENCES Homes(home_id)
);
"""

with engine.connect() as connection:
    connection.execute(create_open_houses_table_query)

print("openhouses table created successfully.")

# get existing home_id
existing_home_ids_query = "SELECT home_id FROM homes"
with engine.connect() as connection:
    existing_home_ids = [row['home_id'] for row in connection.execute(existing_home_ids_query)]


def random_time():
    """Randomly generate time"""
    return (datetime.min + timedelta(seconds=random.randint(0, 24 * 3600))).time()

open_houses_data = {
    'open_house_id': [i for i in range(1, 101)],
    'home_id': [random.choice(existing_home_ids) for _ in range(100)],
    'date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(100)],
    'start_time': [random_time() for _ in range(100)],
    'end_time': [random_time() for _ in range(100)]
}

# ensure end_time is later than start_time
df_open_houses = pd.DataFrame(open_houses_data)
df_open_houses['end_time'] = df_open_houses.apply(
    lambda row: row['end_time'] if row['end_time'] > row['start_time'] else (datetime.combine(datetime.min, row['start_time']) + timedelta(hours=1)).time(),
    axis=1
)

try:
    df_open_houses.to_sql('openhouses', engine, if_exists='append', index=False)
    print("100 rows of open houses data inserted successfully into the openhouses table.")
except Exception as e:
    print(f"An error occurred: {e}")

# Appointments:
db_url = "postgresql+psycopg2://postgres:123@localhost:5432/Dream_Homes_NYC"
engine = create_engine(db_url)
conn = engine.connect()

create_appointments_table_query = """
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INT PRIMARY KEY,
    client_id INT,
    employee_id INT,
    home_id INT,
    date DATE,
    time TIME,
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (home_id) REFERENCES homes(home_id)
);
"""

with engine.connect() as connection:
    connection.execute(create_appointments_table_query)

print("Appointments table created successfully.")

# get existing client_id, employee_id, and home_id
existing_client_ids_query = "SELECT client_id FROM clients"
existing_employee_ids_query = "SELECT employee_id FROM employees"
existing_home_ids_query = "SELECT home_id FROM homes"

with engine.connect() as connection:
    existing_client_ids = [row['client_id'] for row in connection.execute(existing_client_ids_query)]
    existing_employee_ids = [row['employee_id'] for row in connection.execute(existing_employee_ids_query)]
    existing_home_ids = [row['home_id'] for row in connection.execute(existing_home_ids_query)]

def random_time():
    """Randomly generate time"""
    return (datetime.min + timedelta(seconds=random.randint(0, 24 * 3600))).time()

appointments_data = {
    'appointment_id': [i for i in range(1, 5001)],
    'client_id': [random.choice(existing_client_ids) for _ in range(5000)],
    'employee_id': [random.choice(existing_employee_ids) for _ in range(5000)],
    'home_id': [random.choice(existing_home_ids) for _ in range(5000)],
    'date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(5000)],
    'time': [random_time() for _ in range(5000)]
}


df_appointments = pd.DataFrame(appointments_data)


try:
    df_appointments.to_sql('appointments', engine, if_exists='append', index=False)
    print("5000 rows of appointments data inserted successfully into the appointments table.")
except Exception as e:
    print(f"An error occurred: {e}")

