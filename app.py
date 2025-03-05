from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3, os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend
import matplotlib.pyplot as plt

app = Flask(__name__)

def get_expenses():
    conn = sqlite3.connect('finance_manager.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    rows = c.fetchall()
    conn.close()
    return rows

def get_income():
    conn = sqlite3.connect('finance_manager.db')
    c = conn.cursor()
    c.execute("SELECT * FROM income")
    rows = c.fetchall()
    conn.close()
    return rows

def generate_expense_chart():
    expenses = get_expenses()
    if not expenses:
        print("No expense data available to plot.")
        if os.path.exists('static/expense_chart.png'):
            os.remove('static/expense_chart.png')
        return
    df = pd.DataFrame(expenses, columns=['ID', 'Date', 'Category', 'Amount', 'Description'])
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df.groupby('Category')['Amount'].sum().plot(kind='bar')
    plt.title('Expenses by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.savefig('static/expense_chart.png')
    plt.close()

def generate_income_chart():
    income = get_income()
    if not income:
        print("No income data available to plot.")
        if os.path.exists('static/income_chart.png'):
            os.remove('static/income_chart.png')
        return
    df = pd.DataFrame(income, columns=['ID', 'Date', 'Source', 'Amount', 'Description'])
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df.groupby('Source')['Amount'].sum().plot(kind='bar')
    plt.title('Income by Source')
    plt.xlabel('Source')
    plt.ylabel('Amount')
    plt.savefig('static/income_chart.png')
    plt.close()

@app.route('/')
def index():
    generate_expense_chart()
    generate_income_chart()
    expenses = get_expenses()
    income = get_income()
    return render_template('index.html', expenses=expenses, income=income)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    date = request.form['date']
    category = request.form['category']
    amount = request.form['amount']
    description = request.form['description']
    conn = sqlite3.connect('finance_manager.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
              (date, category, amount, description))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/generate_expense_chart', methods=['POST'])
def generate_expense_chart_route():
    generate_expense_chart()
    return jsonify({'result': 'success'})

@app.route('/generate_income_chart', methods=['POST'])
def generate_income_chart_route():
    generate_income_chart()
    return jsonify({'result': 'success'})

@app.route('/add_income', methods=['POST'])
def add_income():
    date = request.form['date']
    source = request.form['source']
    amount = request.form['amount']
    description = request.form['description']
    conn = sqlite3.connect('finance_manager.db')
    c = conn.cursor()
    c.execute("INSERT INTO income (date, source, amount, description) VALUES (?, ?, ?, ?)",
              (date, source, amount, description))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete_expense/<int:id>', methods=['POST'])
def delete_expense(id):
    conn = sqlite3.connect('finance_manager.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'result': 'success'})

@app.route('/delete_income/<int:id>', methods=['POST'])
def delete_income(id):
    conn = sqlite3.connect('finance_manager.db')
    c = conn.cursor()
    c.execute("DELETE FROM income WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(debug=True)