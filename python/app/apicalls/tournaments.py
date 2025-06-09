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

@router.post("/submitTournament")
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
            
                for fencerB in group:
                    match_dict={
                    "tournamentID" : tournament_id,
                    "type" : ""
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
                    
                    )
        db.commit()
    return {"ok": True}


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