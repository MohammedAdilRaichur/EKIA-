import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(base_dir, "database")
os.makedirs(db_dir, exist_ok=True)

db_path = os.path.join(db_dir, "enterprise.db")

# Connect to SQLite (this creates the file if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create Tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS departments (
    dept_id TEXT PRIMARY KEY,
    dept_name TEXT NOT NULL,
    manager_id TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    emp_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    dept_id TEXT,
    title TEXT,
    email TEXT,
    FOREIGN KEY (dept_id) REFERENCES departments (dept_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS projects (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    status TEXT,
    budget REAL,
    dept_id TEXT,
    FOREIGN KEY (dept_id) REFERENCES departments (dept_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    expense_id TEXT PRIMARY KEY,
    emp_id TEXT,
    amount REAL,
    category TEXT,
    date TEXT,
    status TEXT,
    FOREIGN KEY (emp_id) REFERENCES employees (emp_id)
)
''')

# Clear existing data if script is re-run
cursor.execute("DELETE FROM expenses")
cursor.execute("DELETE FROM projects")
cursor.execute("DELETE FROM employees")
cursor.execute("DELETE FROM departments")

# Insert Data
departments = [
    ('D101', 'Engineering', 'E101'),
    ('D102', 'HR', 'E104'),
    ('D103', 'Finance', 'E105'),
    ('D104', 'IT', 'E106')
]
cursor.executemany("INSERT INTO departments VALUES (?, ?, ?)", departments)

employees = [
    ('E101', 'Jane Doe', 'D101', 'VP Engineering', 'jane.doe@novatech.com'),
    ('E102', 'John Smith', 'D101', 'Senior Engineer', 'john.smith@novatech.com'),
    ('E103', 'Alice Johnson', 'D101', 'Software Engineer', 'alice.johnson@novatech.com'),
    ('E104', 'Bob Williams', 'D102', 'HR Director', 'bob.williams@novatech.com'),
    ('E105', 'Charlie Brown', 'D103', 'Finance Manager', 'charlie.brown@novatech.com'),
    ('E106', 'Diana Prince', 'D104', 'IT Lead', 'diana.prince@novatech.com'),
    ('E107', 'Eve Adams', 'D101', 'DevOps Engineer', 'eve.adams@novatech.com')
]
cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?)", employees)

projects = [
    ('P1001', 'Payment Service V2', 'Active', 150000.00, 'D101'),
    ('P1002', 'HR Portal Upgrade', 'Active', 50000.00, 'D102'),
    ('P1003', 'Cloud Migration', 'Completed', 250000.00, 'D104'),
    ('P1004', 'Q3 Financial Audit', 'Planned', 20000.00, 'D103')
]
cursor.executemany("INSERT INTO projects VALUES (?, ?, ?, ?, ?)", projects)

expenses = [
    ('EXP001', 'E102', 12000.00, 'Travel', '2023-10-01', 'Approved'),
    ('EXP002', 'E103', 450.00, 'Meals', '2023-10-02', 'Pending'),
    ('EXP003', 'E106', 2500.00, 'Software License', '2023-09-15', 'Approved')
]
cursor.executemany("INSERT INTO expenses VALUES (?, ?, ?, ?, ?, ?)", expenses)

# Commit and close
conn.commit()
conn.close()

print(f"Database initialized successfully at {db_path}")
