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
                name,
                tournament_mode
            from tournaments;        
            """)
        tournaments=cursor.fetchall()
        if tournaments.__len__==0:
            return {"1":"Empty"}
        else:
            return_list = []
            for tournament in tournaments:
                tournament_dict=dict()
                tournament_dict["id"]=tournament[0]
                tournament_dict["name"]=tournament[1]
                tournament_dict["mode"]=tournament[2]
                return_list.append(tournament_dict)
            return return_list

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
        grp = [[int(e) for e in el] for el in grp]

    data = {
        "name" : tournament,
        "gsize" : int(gsize),
        "gcount" : int(gcount),
        "precount" : int(precount),
        "groups" : grp
    }

    print(tmode)
    print(tmode=="ko")
    if tmode == "ko":
        response = create_ko_tournament(data)
    elif tmode == "rr":
        response = create_rr_tournament(data)

    if response == 1:
        return {"ok": True}
    else:
        return {"err": response}

def create_ko_tournament(data : dict):
    try:
        with mysql.connect(**db_dict) as db:
            grps = data.pop("groups")
            cursor = db.cursor()
            # Writes tournament into database and fetches id 
            # of respective tournament
            cursor.execute("""
            INSERT INTO tournaments (
                        name,
                        group_size,
                        group_count,
                        tournament_mode,
                        preliminaries
                        ) VALUES 
                        (%(name)s,%(gsize)s,%(gcount)s,'ko',1);"""
                        ,data)
            db.commit()
            tournament_id = cursor.lastrowid
            # Create tournament status as preliminary 1, this will later
            # need to be updated to depend on the selected preliminary 
            # counter.
            cursor.execute("""
            INSERT INTO tournament_status (
            tournamentID,
            status  
            ) VALUES (%s,%s)""",
            (tournament_id,"preliminary 1"))
            db.commit()
            tournament_status_id = cursor.lastrowid
            for count,group in enumerate(grps):
                while len(group)>0:
                    fencer=group.pop()
                    # For each participant, create an entry with the 
                    # respectuve group in the tournament_groups table.
                    cursor.execute("""
                                    INSERT INTO tournament_groups (
                                    tournamentID,
                                    group_no,
                                    preliminaries,
                                    fencerID,
                                   tournamentStatusID
                                    ) VALUES
                                    (%s,%s,%s,%s) """,
                                    (int(tournament_id),
                                    int(count),
                                    data["precount"],
                                    int(fencer),
                                    tournament_status_id)
                                    )
                    # For each pair of participants in the respective group
                    # add a match to the matches table.
                    for fencerB in group:
                        if fencer == fencerB: continue
                        match_dict={
                        "tournamentID" : tournament_id,
                        "type" : "preliminary 1",
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
            db.commit()
            return 1
    except Exception as e:
        print(e)
        return e


def create_rr_tournament(data):
    try:
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
                            "type" : "roundrobin",
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
                return 1
    except Exception as e:
        return e
    
@router.get("/fetchTournament/{tournamentID}")
def fetch_tournament(tournamentID):
    with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute("""
        select * from tournaments where tournamentID = %s
        """,(tournamentID,))
        tournament_data = cursor.fetchall()


def fetch_ko_tournament(tournamentID):
    with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute("""
        select distinct type from matches
        tournamentID = %s;""",
        (tournamentID,)
        )
        types = [el[0] for el in cursor.fetchall()]
        return {"types" : types}
    
def fetch_ko_type(tournamentID,matchtype):
    with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute("""
        select * from matches where tournamentID = %s and type = %s           
        """, (int(tournamentID),matchtype))
        matches = []