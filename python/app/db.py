import mysql.connector as mysql
import csv

db_dict = {
#    "host"      : "172.16.103.13",
    "host"      : "localhost",
    "database"    : "db",
    "user"      : "user",
    "password"  : "password",
    "port"      : "3306"
}


with mysql.connect(**db_dict) as db:
    cursor = db.cursor()
    cursor.execute(
        """
        select 
            f.*,
            s.in_tournament
            from signuplists as s
            left join (
            select 
                r.competition,
                count(distinct r.FencerId)
            from registrations as r 
            group by r.competition
            ) as f  on s.name = f.competition
        """
    )
    print(dict(enumerate(cursor.fetchall())))