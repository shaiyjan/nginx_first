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

tournamentID=15

with mysql.connect(**db_dict) as db:
    cursor = db.cursor()
    cursor.execute("""
    select * from tournaments where tournamentID = %s
    """,(tournamentID,))
    tournament_data = cursor.fetchone()
    cursor.execute("""
    select column_name 
    from information_schema.columns 
    where table_schema='db' 
        and table_name = 'tournaments'
    order by ordinal_position;
    """)
    tournament_data = dict(
            zip([el[0] for el in cursor.fetchall()],tournament_data)
            )



    cursor.execute("""
    select * from matches where tournamentID = %s            
    """,(tournamentID,))
    match_data = cursor.fetchall()
    cursor.execute("""
    select column_name 
    from information_schema.columns 
    where table_schema='db' 
        and table_name = 'tournaments'
    order by ordinal_position;
    """)
    header = [el[0] for el in cursor.fetchall()]
    matches = []
    for match in match_data:
        match_dict =dict(zip(header,match))
        matches.append(match_dict)
    

def fetch_Tournaments():
    with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute("""
            select 
                tournamentId,
                name,
                tournament_mode
            from tournaments;        
            """)
        tournaments=cursor.fetchall()
        if tournaments.__len__==0:
            return {"1":"Empty"}
        else:
            return_list = []
            print(tournaments)
            for tournament in tournaments:
                tournament_dict=dict()
                tournament_dict["id"]=tournament[0]
                tournament_dict["name"]=tournament[1]
                tournament_dict["mode"]=tournament[2]
                return_list.append(tournament_dict)
            return return_list

print(fetch_Tournaments())


