from flask import Flask, render_template, request, redirect, url_for
import sqlite3

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

@app.route('/')
def index():
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
    return redirect(url_for('index'))

@app.route('/delete_income/<int:id>', methods=['POST'])
def delete_income(id):
    conn = sqlite3.connect('finance_manager.db')
    c = conn.cursor()
    c.execute("DELETE FROM income WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)