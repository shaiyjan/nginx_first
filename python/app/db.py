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
            count(distinct r.fencerID)
        from registrations as r 
        left join signuplists as s on s.name = r.competition
        where s.TournamentID in (1,2,3,4,5)
        """
    )
    print(cursor.fetchall())

def read_total_participants(item_strlist : str) -> dict:
    if item_strlist== "": return {"0":0}
    with mysql.connect(**db_dict) as db:
        item_list= item_strlist.split("%")[0:-1]
        cursor = db.cursor()
        cursor.execute(
            """
            select 
                count(distinct r.fencerID)
            from registrations as r 
            left join signuplists as s on s.name = r.competition
            where s.TournamentID in (
            """+ ",".join([str(ind) for ind in item_list]) +")"
        )
        return {"0":cursor.fetchall()[0][0]}

print(read_total_participants("1%2%"))
print(read_total_participants(""))