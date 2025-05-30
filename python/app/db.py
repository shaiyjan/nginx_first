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

def read_total_participants_per_signup(item_strlist : str) -> dict:
    if item_strlist== "": return {"0":0}
    with mysql.connect(**db_dict) as db:
        item_list= item_strlist.split("%")[0:-1]
        cursor = db.cursor()
        cursor.execute(
            """
            with total as (
                select 
                    r.firstname,
                    r.lastname,
                    r.Fencerid,
                    r.club,
                    s.TournamentID
                from registrations as r 
                left join signuplists as s on s.name = r.competition
                where s.TournamentID in ("""
                + ",".join([str(ind) for ind in item_list]) + """)
                ),
                min_tournament as (
                select 
                    FencerID,
                    min(tournamentId) as min_tID
                from total group by FencerId
                )
            select 
                total.*
            from min_tournament as mt
            left join total
                on total.FencerID = mt.FencerId 
                and total.tournamentID = mt.min_tID
            """
            )

        return dict(enumerate(cursor.fetchall()))

print(read_total_participants_per_signup("1%2%3%4%5%"))
print(read_total_participants_per_signup("2%3%"))

#  