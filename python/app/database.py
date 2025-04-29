import mysql.connector as mysql

try:
    mydb = mysql.connect(
        host="localhost:1433",
        user="root",
        password="P@ssw0rd",
        
    )
except Exception as e:
    print(e)