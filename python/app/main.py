import mysql.connector as mysql
import csv


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


db_dict = {
    "host"      : "172.16.103.13",
#    "host"      : "localhost",
    "database"    : "db",
    "user"      : "user",
    "password"  : "password",
    "port"      : "3306"
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

# Get the signuplists to fetch id and name
@app.get("/signuplists")
def read_signuplists() -> dict:
    with mysql.connect(**db_dict) as db:
        cursor=db.cursor()
        cursor.execute(
            """
            select * from signuplists;
            """
        )
        tournaments=cursor.fetchall()
        ret_dict = dict()
        for tournament in tournaments:
            ret_dict[tournament[0]]=tournament[1]
        return ret_dict
    
# Get the tournaments to fetch id and name
@app.get("/registrations")
def read_tournaments() -> dict:
    with mysql.connect(**db_dict) as db:
        cursor =db.cursor()
        cursor.execute(
            """
            select * from signuplists;
            """
        )
        lists =cursor.fetchall()
        ret = dict()
        for lis in lists:
            ret[lis[0]]=lis[1]
        print(ret)
        return ret


# Get all indiviuals signed up the the competition with id = list_id
@app.get("/signuplist/{list_id}")
def read_participants(list_id : int) -> dict:
    with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute(
            """
            select 
                r.registrationID,
                r.lastname,
                r.firstname,
                r.club,
                r.paid,
                r.recipe,
                r.attandence,
                r.attest
            from registrations as r
            left join signuplists as s on s.name = r.competition
            where s.tournamentid =
            """  + str(list_id) + ";"
                       )
        ret = cursor.fetchall()
        print(ret)
        return dict(enumerate(ret))


# Get all signuplists which are not already selected in to a tournament
# Additionally fetch all participants in the respective signuplist
@app.get("/signup_extra")
def read_signuplist_extend() -> dict:
    with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute(
            """
            select 
                s.TournamentID,
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
        return (dict(enumerate(cursor.fetchall())))
    
# get all registrations with tournament id in item_strlist, seperated by %
# there is an additional trailing %!
@app.get("/signup_overlap/{item_strlist}")
def read_total_participants(item_strlist : str) -> dict:
    if item_strlist == "": return {"0":0}
    with mysql.connect(**db_dict) as db:
        item_list= item_strlist.split("_")[0:-1]
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
    
@app.get("/signup_overlap_particpants/{item_strlist}")
def read_total_participants_per_signup(item_strlist : str) -> dict:
    if item_strlist== "": return {"0":0}
    with mysql.connect(**db_dict) as db:
        item_list= item_strlist.split("_")[0:-1]
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
    
@app.post("/submitTournament")
def submit_tournament(
    tournament: str,
    gsize: int,
    gcount: int,
    tmode: str,
    precount: int,
    grp: str):

    print(grp)
    groups = grp.split("#")[1:]
    print(groups)
    groups = [inner.strip(",").split(",") for inner in groups]
    print(groups)

    return {"ok": True}


@app.post("/changeBool")
def change_bool(
    registrationId,
    fieldName,
    boolVal):
      boolInt = 1 if boolVal == "true" else 0
      with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute("""
        update registrations 
            set """ + fieldName + "=" +  boolVal + """
        where registrationId = """ + registrationId +";") 
        db.commit()
        print("""
        update registrations 
            set """ + fieldName + "=" +  str(boolInt) + """
        where registrationId = """ + registrationId +";"
        )
        return {"ok": True}
