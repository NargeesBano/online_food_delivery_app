from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flashing messages

# Database connection
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='',  # Replace with your MySQL password
        database='online_food'  # Replace with your database name
    )

# Home route
@app.route('/')
def index():
    orders = get_all_orders()
    return render_template('index.html', orders=orders)

def get_all_orders():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM orders"
            cursor.execute(sql)
            orders = cursor.fetchall()
    finally:
        connection.close()
    return orders

# Create (Insert new order)
@app.route('/add_order', methods=['POST'])
def add_order():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        insert_order(name, email, phone, message)
        flash("Order added successfully!")
        return redirect(url_for('index'))

def insert_order(name, email, phone, message):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO orders (name, email, phone, message) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, email, phone, message))
            connection.commit()
    finally:
        connection.close()

# Update (Edit existing order)
@app.route('/edit_order/<int:id>', methods=['POST', 'GET'])
def edit_order(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        update_order(id, name, email, phone, message)
        flash("Order updated successfully!")
        return redirect(url_for('index'))

    order = get_order_by_id(id)
    return render_template('edit_order.html', order=order)

def update_order(id, name, email, phone, message):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """UPDATE orders 
                     SET name = %s, email = %s, phone = %s, message = %s 
                     WHERE id = %s"""
            cursor.execute(sql, (name, email, phone, message, id))
            connection.commit()
    finally:
        connection.close()

def get_order_by_id(id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM orders WHERE id = %s"
            cursor.execute(sql, (id,))
            order = cursor.fetchone()
    finally:
        connection.close()
    return order

# Delete (Delete an order)
@app.route('/delete_order/<int:id>', methods=['GET'])
def delete_order(id):
    delete_order_by_id(id)
    flash("Order deleted successfully!")
    return redirect(url_for('index'))

def delete_order_by_id(id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM orders WHERE id = %s"
            cursor.execute(sql, (id,))
            connection.commit()
    finally:
        connection.close()

if __name__ == "__main__":
    app.run(debug=True)
