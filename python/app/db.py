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

fencer_dict = dict()
signup_dict = dict()

with open("participants.csv") as csvfile:
    reader = csv.reader(csvfile,delimiter=";")
    header=next(reader)
    for row in reader:
        row = row
        temp_dict= dict(zip(header,row))
        key = tuple(row[1:8])
        if key not in fencer_dict.keys():
            fencer_dict[key] = [temp_dict["competition"].strip()]
        else:
            fencer_dict[key]=[*fencer_dict[key],temp_dict["competition"].strip()]

        signup_dict[temp_dict["competition"]] = 1

for key in fencer_dict.keys():
    print(key,fencer_dict[key],sep="\n",end="\n")