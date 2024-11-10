import pymysql

def get_db_connection():
    # Estabslish a connection to databse
    return( pymysql.connect(
        host='localhost',
        user='root',  # replace with your MySQL username
        password='abcd',  # replace with your MySQL password
        database='my_food_app'  # replace with your database name
    ))

def get_db_records():
    try:
        # create a cursor object using connection.cursor() 
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Execute a Sql Query
            sql = "select * from food_table"
            cursor.execute(sql)

            # fetch all results
            results = cursor.fetchall()
            if len(results) ==0:
                print("The Table has no records")
            else:
                for row in results:
                    print(row)

    finally:
        # close the connection 
        connection.close()

def add_data():
    try:
         # create a cursor object using connection.cursor() 
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Execute a Sql results
            sql = "Insert into food_table (name ,email,phone,message) values('Nargees','nargees@gmail.com',86756,'Your order is on the way...')"
            cursor.execute(sql)
            connection.commit()
    finally:
        #close the connection
        connection.close()

def delete_table():
    try:
        # create a cursor object using connection.cursor()
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Execute a Sql results
            sql="drop table food_table"
            cursor.execute(sql)
            connection.commit()
            print("Table Deleteed..!!!")

    finally:
        # close the connection
        connection.close()

add_data()
get_db_records()
# delete_table()
