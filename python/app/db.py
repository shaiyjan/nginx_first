import mysql.connector as mysql
from datetime import date

db_dict = {
#    "host"      : "172.16.103.13",
    "host"      : "localhost",
    "database"    : "db",
    "user"      : "user",
    "password"  : "password",
    "port"      : "3306"
}

tournamentID=11

with mysql.connect(**db_dict) as db:
    cursor = db.cursor()
    cursor.execute("""
    select * from matches where tournamentID = %s and type = %s           
    """, (int(tournamentID),type))
    matches = cursor.fetchall()
    print(matches)
