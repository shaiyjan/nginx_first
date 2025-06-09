import mysql.connector as mysql
db_dict = {
    "host"      : "172.16.103.13",
    "database"  : "db",
    "user"      : "user",
    "password"  : "password",
    "port"      : "3306"
}


from fastapi import APIRouter

router = APIRouter(
    prefix="/signups",
    tags=["signups"]
)

# Get the signuplists to fetch id and name
@router.get("/signuplists")
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
    

    
# Get all indiviuals signed up the the competition with id = list_id
@router.get("/signuplist/{list_id}")
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
    
# Get all signuplists which are not already selected into a tournament
# Additionally fetch all participants in the respective signuplist
@router.get("/signup_attendance")
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
@router.get("/signup_overlap/{item_strlist}")
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
    
@router.get("/signup_overlap_particpants/{item_strlist}")
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