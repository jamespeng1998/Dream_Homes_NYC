CREATE TABLE Offices (
    office_id INT PRIMARY KEY,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    phone_number VARCHAR(15)
);

CREATE TABLE Employees (
    employee_id INT PRIMARY KEY,
    role_id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone_number VARCHAR(15),
    employment_type VARCHAR(50),
    FOREIGN KEY (role_id) REFERENCES EmployeeRoles(role_id)
);

CREATE TABLE EmployeeRoles (
    role_id INT PRIMARY KEY,
    role_name VARCHAR(50),
    description TEXT
);

CREATE TABLE EmployeeOfficeAssignments (
    assignment_id INT PRIMARY KEY,
    employee_id INT,
    office_id INT,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
    FOREIGN KEY (office_id) REFERENCES Offices(office_id)
);

CREATE TABLE Expenses (
    expense_id INT PRIMARY KEY,
    description TEXT,
    amount DECIMAL(10, 2),
    date DATE,
    office_id INT,
    FOREIGN KEY (office_id) REFERENCES Offices(office_id)
);

CREATE TABLE Owners (
    owner_id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone_number VARCHAR(15)
);

CREATE TABLE Schools (
    school_id INT PRIMARY KEY,
    address VARCHAR(255),
    postcode VARCHAR(100),
    type VARCHAR(50)
);

CREATE TABLE Homes (
    home_id INT PRIMARY KEY,
	school_id INT,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
	date_recorded DATE,
    assessed_value DECIMAL(10,2),
	sale_amount DECIMAL(10,2),
	sales_ratio DECIMAL(10,4),
    type VARCHAR(50),
    status VARCHAR(50),
	FOREIGN KEY (school_id) REFERENCES Schools(school_id)
);

CREATE TABLE HomeFeatures (
    feature_id INT PRIMARY KEY,
    feature_name VARCHAR(50),
    description TEXT
);

CREATE TABLE HomeFeatureAssignments (
    assignment_id INT PRIMARY KEY,
    home_id INT,
    feature_id INT,
    FOREIGN KEY (home_id) REFERENCES Homes(home_id),
    FOREIGN KEY (feature_id) REFERENCES HomeFeatures(feature_id)
);

CREATE TABLE Clients (
    client_id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone_number VARCHAR(15),
    client_type VARCHAR(50)
);

CREATE TABLE ClientPreferences (
    preference_id INT PRIMARY KEY,
    client_id INT,
    preference_type VARCHAR(50),
    value VARCHAR(255),
    FOREIGN KEY (client_id) REFERENCES Clients(client_id)
);

CREATE TABLE TransactionsTypes (
    transaction_type_id INT PRIMARY KEY,
    transaction_type_name VARCHAR(50),
    description TEXT
);

CREATE TABLE Transactions (
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

CREATE TABLE PaymentMethods (
    payment_method_id INT PRIMARY KEY,
    method_name VARCHAR(50),
    description TEXT
);

CREATE TABLE TransactionPayments (
    payment_id INT PRIMARY KEY,
    transaction_id INT,
    payment_method_id INT,
    amount DECIMAL(10, 2),
    date DATE,
    FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id),
    FOREIGN KEY (payment_method_id) REFERENCES PaymentMethods(payment_method_id)
);

CREATE TABLE OpenHouses (
    open_house_id INT PRIMARY KEY,
    home_id INT,
    date DATE,
    start_time TIME,
    end_time TIME,
    FOREIGN KEY (home_id) REFERENCES Homes(home_id)
);

CREATE TABLE Appointments (
    appointment_id INT PRIMARY KEY,
    client_id INT,
    employee_id INT,
    home_id INT,
    date DATE,
    time TIME,
    FOREIGN KEY (client_id) REFERENCES Clients(client_id),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
    FOREIGN KEY (home_id) REFERENCES Homes(home_id)
);

CREATE TABLE MarketingCampaigns (
    campaign_id INT PRIMARY KEY,
    campaign_name VARCHAR(100),
    description TEXT,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(10, 2)
);

CREATE TABLE CampaignResults (
    result_id INT PRIMARY KEY,
    campaign_id INT,
    result_description TEXT,
    result_date DATE,
    FOREIGN KEY (campaign_id) REFERENCES MarketingCampaigns(campaign_id)
);
