import mysql.connector

# Establishing the connection
try:
    mydb = mysql.connector.connect(
        host='localhost',
        user='',
        password='',  # Replace with your password
        database=''
    )

    # Checking if the connection was successful
    if mydb.is_connected():
        print('Connection successful')
    else:
        print('Connection failed')
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'mydb' in locals() and mydb.is_connected():
        mydb.close()
