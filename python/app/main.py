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

def insert():
    try:
        mydb =mysql.connect(**db_dict)
        cursor=mydb.cursor()
        cursor.execute("""
                create table if not exists students(
                StudentID int not null AUTO_INCREMENT,
                FirstName varchar(100) not null,
                LastName varchar(100) not null,
                primary key(StudentID)
                );
                """)
        mydb.commit()
        cursor.execute("""
                INSERT INTO students(FirstName,LastName)
                VALUES ("Ada","Abel"),("Cane","Chenning");
                """)
        mydb.commit()
        mydb.close()
    except Exception as e:
        print(e)





insert()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

@app.get("/")
def read_root():
    return {"Hello": "World", "bla": test()}

@app.get("/tournaments")
def read_tournaments() -> dict:
    with mysql.connect(**db_dict) as db:
        cursor=db.cursor()
        cursor.execute(
            """
            select * from tournaments;
            """
        )
        tournaments=cursor.fetchall()
        ret_dict = dict()
        for tournament in tournaments:
            ret_dict[tournament[0]]=tournament[1]
        return ret_dict


dummy_dict={1:"A",2:"B",3:"C"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "q": dummy_dict[item_id]}

#@app.get("/tournaments")
#def read_names() -> list:
#    names_list=database.tournament_names()
#    return {"data" : [{"id": count, "name": names_list[count]} for count in range(names_list.__len__())]}

@app.get("/insert")
def db_insertion() -> dict:
    try:
        insert()
    except Exception as e:
        ret_dict = {"Success" : "Failed"}
    else: 
        ret_dict = {"Success" : "Succesfull"}
    return ret_dict

# if __name__=="__main__":
#     insert()
#     test()
#     database=db.dbcon()
#     print(read_names())