# http://localhost:5000/ 

from flask import Flask , render_template , url_for ,request,redirect
import pymysql

app = Flask(__name__)

# database connection 


def get_db_connection():
    # Estabslish a connection to databse
    return( pymysql.connect(
        host='localhost',
        user='root',  # replace with your MySQL username
        password='1106@MySql',  # replace with your MySQL password
        database='my_food_app'  # replace with your database name
    ))

# Home route
@app.route('/')
def index():    
    return render_template('index.html')        

# route to handle form submission
@app.route('/submit-form' , methods=['POST'])
def subit_from():
    # get form data
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    # insert data into database
    connection = get_db_connection()
    cursor = connection.cursor()
    
    sql = 'insert into food_table (name , email , phone, message) values (%s, %s, %s, %s)'
    cursor.execute(sql,(name , email , phone,message))
    connection.commit()

    # close the connection
    cursor.close()
    connection.close()

    # Redirect to a thank-you page or back to the home page
    return redirect(url_for('index'))

@app.route('/fetch-records' ,methods=['GET'])
def get_database_records():
    connection = get_db_connection()
    cursor = connection.cursor()

    sql = 'select * from food_table'
    cursor.execute(sql)
    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('records.html' , records=records)

if __name__ == "__main__":
    app.run(debug=True)

# http://localhost:5000/ 