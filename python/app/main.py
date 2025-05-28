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

def test():
    try:
        mydb = mysql.connect(
            host="172.16.103.13",
            port="3306",
            user="user",
            password="password",
            database="db"
        )

        cursor = mydb.cursor()

        cursor.execute(
            """
            select * from students;
            """)
        data = cursor.fetchall()
        mydb.close()

        print(data)

        x=str(data)
        
    except Exception as e:
        x=str(e)
        print(x)
    
    return x

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

@app.get("/")
def read_root():
    return {"Hello": "World", "bla": test()}

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
    
@app.get("/tournaments")
def read_tournaments() -> dict:
    with mysql.connect(**db_dict) as db:
        cursor =db.cursor()
        cursor.execute(
            """
            select * from tournaments;
            """
        )
        tournaments =cursor.fetchall()
        return dict(tournaments)

@app.get("/signuplist/{list_id}")
def read_participants(list_id : int) -> dict:
    with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute(
            """
            select 
                r.lastname,
                r.firstname,
                r.club
            from registrations as r
            left join signuplists as s on s.name = r.competition
            where s.tournamentid =
            """  + str(list_id) + ";"
                       )
        ret = cursor.fetchall()
        return dict(enumerate(ret))



@app.get("/insert")
def db_insertion() -> dict:
    try:
        insert()
    except Exception as e:
        ret_dict = {"Success" : "Failed"}
    else: 
        ret_dict = {"Success" : "Succesfull"}
    return ret_dict
