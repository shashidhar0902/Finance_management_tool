import sqlite3
import os
from datetime import datetime, timedelta
import random

def ex():
    # Database file path
    db_path = 'finance_manager.db'

    # Delete the database file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)

    # Connect to the database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    date TEXT,
                    category TEXT,
                    amount REAL,
                    description TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS income (
                    id INTEGER PRIMARY KEY,
                    date TEXT,
                    source TEXT,
                    amount REAL,
                    description TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    amount REAL)''')

    # Generate fake data for expenses
    categories = ['Food', 'Transport', 'Entertainment', 'Utilities', 'Healthcare']
    for _ in range(5):
        date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
        category = random.choice(categories)
        amount = round(random.uniform(10, 100), 2)
        description = f'Sample expense for {category}'
        c.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                  (date, category, amount, description))

    # Generate fake data for income
    sources = ['Salary', 'Freelance', 'Investment', 'Gift']
    for _ in range(5):
        date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
        source = random.choice(sources)
        amount = round(random.uniform(100, 1000), 2)
        description = f'Sample income from {source}'
        c.execute("INSERT INTO income (date, source, amount, description) VALUES (?, ?, ?, ?)",
                  (date, source, amount, description))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Fake data inserted successfully!")