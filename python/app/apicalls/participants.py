import mysql.connector as mysql
db_dict = {
    "host"      : "172.16.103.13",
    "database"  : "db",
    "user"      : "user",
    "password"  : "password",
    "port"      : "3306"
}

from datetime import date
from fastapi import APIRouter

router = APIRouter(
    prefix="/participants",
    tags=["participants"]
)
   

@router.post("/updateAttendance")
def change_bool(
    fencerID,
    signupID,
    boolVal):
    """
    Updates to Attendance column in the table fencers of 
    the respective fencer in the respective signuplist to boolval.
    """
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
    
@router.get("/fetchFencers")
def fetchFencers():
    with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute("""
            select 
                *
            from fencers            
        """)
        fencers = cursor.fetchall()

        cursor.execute("""
            select column_name 
            from information_schema.columns 
            where table_schema='db' 
                and table_name = 'fencers'
            order by ordinal_position;
            """)

        headers = cursor.fetchall()
        headers = [header[0] for header in headers]

        fencer_dicts=dict()
        for count,fencer in enumerate(fencers):
            fencer_dict=dict(zip(headers,fencer))
            fencer_dict.pop("dateofbirth")
            fencer_dict.pop("region")
            fencer_dicts[count]=fencer_dict

        return fencer_dicts
    
@router.post("/updateFencer")
def update_Fencer(id,column,value):
    if column in ("paid","attest"):
        value=int(value)
    data_dict= {"id":int(id),
                "column":column,
                "value":value}
    print(data_dict)
    if column in ("paid","attest","note"):
        update_string= """
            update fencers 
                set """ + column + """ = %(value)s
            where fencerID = %(id)s;
            """
    else:
        return {"ok" : False}
    with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute(
            update_string,
            data_dict
        )
        db.commit()
    return{"ok" : True}

@router.get("/unassignedSignups/{fencerID})")
def fetch_unassigned_Signups(fencerID: str):
    with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute("""
            with fencer_signups as (
            select
                *
            from signups where fencerid = %s
            )
            select 
                s.signuplistID, 
                s.name
            from signuplists as s
            left join fencer_signups as su on s.signuplistID = su.signuplistID
            where su.fencerId is NULL;"""
            , (int(fencerID),)
            )
        ret_list = [el[0] for el in cursor.fetchall()]
        return {"unsassigned":ret_list}
    
@router.get("/participant/{fencerID}")
def fetch_participant(fencerID: str):
    with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute("""
            with assignments as (
                select 
                    *
                from signups where fencerID = %s)
                select 
                    su.signuplistID,
                    su.name,
                    case 
                        when a.fencerID IS NULL then 0
                        else 1
                    end as assignd
                from signuplists as su
                left join assignments as a on a.signuplistID = su.signuplistID       
            """,(int(fencerID),))
        participation = cursor.fetchall()

        cursor.execute(
            """
            select * from fencers where fencerID = %s
            """, (int(fencerID),)
        )
        fencer_data = cursor.fetchone()
        cursor.execute("""
            select column_name 
            from information_schema.columns 
            where table_schema='db' 
                and table_name = 'fencers'
            order by ordinal_position;
            """)
        header=[el[0] for el in cursor.fetchall()]
        fencer_dict = dict(zip(header,fencer_data))
        fencer_dict["participation"]= participation

        return fencer_dict

        
@router.post("/update")
def updateParticipant(
    participantID: str,
    lastname: str,
    firstname: str,
    club: str,
    dateofbirth: str,
    gender: str,
    nation: str,
    paid: str,
    note: str):

    data_dict= {
    "participantID": int(participantID),
    "lastname": lastname,
    "firstname": firstname,
    "club": club,
    "dateofbirth": dateofbirth,
    "gender": gender,
    "nation": nation,
    "paid": int(paid),
    "note": note 
    }
    day,month,year=data_dict["dateofbirth"].split(".")
    birthdate = date(int(year),int(month),int(day))
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    if age >= 18:
        data_dict["adult"]=1
    else:
        data_dict["adult"]=0

    with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute("""
        update fencers set
            lastname = %(lastname)s,
            firstname = %(firstname)s,
            club = %(club)s,
            dateofbirth = %(dateofbirth)s,
            gender = %(gender)s,
            nation = %(nation)s,
            paid = %(paid)s,
            adult = %(adult)s,
            note = %(note)s
        where fencerID = %(participantID)s;
        """,data_dict)
        db.commit()
    return {"ok" : True}


@router.post("/insert")
def updateParticipant(
    participantID: str,
    lastname: str,
    firstname: str,
    club: str,
    dateofbirth: str,
    gender: str,
    nation: str,
    paid: str,
    note: str):

    data_dict= {
    "participantID": int(participantID),
    "lastname": lastname,
    "firstname": firstname,
    "club": club,
    "dateofbirth": dateofbirth,
    "gender": gender,
    "nation": nation,
    "paid": int(paid),
    "note": note 
    }
    day,month,year=data_dict["dateofbirth"].split(".")
    birthdate = date(int(year),int(month),int(day))
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    if age >= 18:
        data_dict["adult"]=1
    else:
        data_dict["adult"]=0
    try:
        with mysql.connect(**db_dict) as db:
            cursor = db.cursor()
            cursor.execute("""
            insert int fencers values 
            (   lastname,
                firstname,
                club,
                dateofbirth,
                gender,
                nation,
                paid,
                adult,
                note)
                (%(lastname)s,
                %(firstname)s,
                %(club)s,
                %(dateofbirth)s,
                %(gender)s,
                %(nation)s,
                %(paid)s,
                %(adult)s,
                %(note)s)
            """,data_dict)
            db.commit()
        return {"ok" : True}
    except Exception as e:
        return {"err" : e}