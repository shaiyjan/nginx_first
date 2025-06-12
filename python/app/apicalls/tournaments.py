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
    prefix="/tournaments",
    tags=["tournaments"]
)

@router.get("/fetchTournaments")
def fetch_Tournaments():
    with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute("""
            select 
                tournamentId,
                name           
            from tournaments;        
            """)
        tournaments=cursor.fetchall()
        if tournaments.__len__==0:
            return {"1":"Empty"}
        else:
            ret_dict = dict()
            for tournament in tournaments:
                ret_dict[tournament[0]]=tournament[1]
            return ret_dict

@router.post("/submitTournament")
def submit_tournament(
    tournament: str,
    gsize: int,
    gcount: int,
    tmode: str,
    precount: int,
    grp: str):

    if tmode != "rr":
        grp = grp.split("#")[1:]
        grp = [inner.strip(",").split(",") for inner in grp]
        grp = [int(el) for el in grp]

    data = {
        "name" : tournament,
        "gsize" : int(gsize),
        "gcount" : int(gcount),
        "precount" : int(precount),
        "groups" : grp
    }

    if tmode == "ko":
        response = create_ko_tournament(data)
    elif tmode == "rr":
        response = create_rr_tournament(data)

    if response == 1:
        return {"ok": True}
    else:
        return {"ok": False}

def create_ko_tournament(data):
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
                    (%(name)s,%(gsize)s,%(gcount)s,ko,%(precount)s);"""
                    ,data)
        db.commit()
        tournament_id = cursor.lastrowid
        for count,group in enumerate(data["groups"]):
            while len(group)>0:
                fencer=group.pop()
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
                                 data["precount"],
                                 int(fencer))
                                )
            
                for fencerB in group:
                    if fencer == fencerB: continue
                    match_dict={
                    "tournamentID" : tournament_id,
                    "type" : "roundrobin",
                    "idA" : fencer,
                    "idB" : fencerB
                    }
                    cursor.execute("""
                    INSERT INTO matches (
                    tournamentID,
                    type,
                    idA,
                    idB) VALUES
                    (%(tournamentID)s,
                    %(type)s,
                    %(idA)s,
                    %(idB)s)                    
                    """,
                    match_dict
                    )
        db.commit()


def create_rr_tournament(data):
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
                    (%(name)s,0,1,'rr',0);"""
                    ,data)
        db.commit()
        tournament_id = cursor.lastrowid
        item_list= data["groups"].split("_")[0:-1]
        cursor.execute(
            """
            select
                distinct(fencerID)
            from signups where
            signuplistID in (""" + ",".join(item_list) + ");"
                )
        groups=[el[0] for el in cursor.fetchall()]

        
        while len(groups)> 0:
            fencer=groups.pop()
            cursor.execute("""
                            INSERT INTO tournament_groups (
                            tournamentID,
                            group_no,
                            preliminaries,
                            fencerID
                            ) VALUES
                            (%s,%s,%s,%s) """,
                            (int(tournament_id),
                            1,
                            0,
                            int(fencer))
                            )
            
            for fencerB in groups:
                try:
                    if fencer == fencerB: continue
                    match_dict={
                    "tournamentID" : tournament_id,
                    "type" : "preliminaries",
                    "idA" : fencer,
                    "idB" : fencerB
                    }
                    cursor.execute("""
                    INSERT INTO matches (
                    tournamentID,
                    type,
                    fencerAID,
                    fencerBID) VALUES
                    (%(tournamentID)s,
                    %(type)s,
                    %(idA)s,
                    %(idB)s)                    
                    """,
                    match_dict
                    )  
                except:
                    print(match_dict)
        db.commit() 

