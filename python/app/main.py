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
                f.FencerID,
                f.lastname,
                f.firstname,
                f.club,
                s.attendance
            from fencers as f
            left join signups as s on s.fencerId = f.fencerID
            where s.signuplistID =
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
            with total as(
                select 
                    COUNT(distinct case when s.attendance = 1 then s.fencerID else NULL end) as sum,
                    s.signuplistID
                from signups as s
                where attendance = 1 
                group by signuplistID)
            select 
                s.signuplistID,
                s.name,
                coalesce(t.sum,0)
            from signuplists as s
            left join total as t on t.signuplistID = s.signuplistid;"""
            )
        ret_dict = dict(enumerate(cursor.fetchall()))
        return ret_dict
    
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
                count(distinct fencerID)
            from signups 
            where signuplistID in (""" + ",".join(item_list) + ")"
            " and attendance = 1;"
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
            with total as(
                select
                    distinct(s.fencerID)
                from signups as s
                where attendance = 1 and
                s.signuplistID in (""" + ",".join(item_list) + """)
                )
            select 
                f.fencerid,
                f.lastname,
                f.firstname,
                f.club
            from total as t 
            left join fencers as f on t.fencerId = f.fencerid;"""
            )
        ret_dict = dict(enumerate(cursor.fetchall()))
        print(ret_dict)
        return ret_dict


@app.post("/submitTournament")
def submit_tournament(
    tournament: str,
    gsize: int,
    gcount: int,
    tmode: str,
    precount: int,
    grp: str):

    groups = grp.split("#")[1:]
    groups = [inner.strip(",").split(",") for inner in groups]

    with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute("""
           INSERT INTO tournaments (
                       name,
                       group_size,
                       group_count,
                       tournament_mode,
                       preliminaries
                       ) VALUES 
                    (%s,%s,%s,%s,%s);"""
                    ,(tournament,int(gsize),int(gcount),tmode,int(precount)))
        db.commit()
        tournament_id = cursor.lastrowid
        for count,group in enumerate(groups):
            for fencer in group:
                cursor.execute("""
                                INSERT INTO tournament_groups (
                                tournamentID,
                                group_no,
                                preliminaries,
                                fencerID
                                ) VALUES
                                (%s,%s,%s,%s) """,
                                (int(tournament_id),
                                 int(count),
                                 int(precount),
                                 int(fencer))
                                )
        db.commit()

    return {"ok": True}


@app.post("/updateAttendance")
def change_bool(
    fencerID,
    signupID,
    boolVal):
      boolInt = 1 if boolVal == "true" else 0
      with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute("""
        update signups        
        set attendance = %s
        where fencerid = %s and signuplistID = %s
        """,
        (boolInt,int(fencerID),int(signupID)))
        db.commit()
        return {"ok": True}
