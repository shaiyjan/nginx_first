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