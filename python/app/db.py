import mysql.connector as mysql
from datetime import date

db_dict = {
#    "host"      : "172.16.103.13",
    "host"      : "localhost",
    "database"    : "db",
    "user"      : "user",
    "password"  : "password",
    "port"      : "3306"
}


def test():
    fencer_dicts =[]
    with mysql.connect(**db_dict) as db:
        cursor = db.cursor()
        cursor.execute("""
            select 
                *
            from fencers            
        """)
        fencer_data = cursor.fetchall()

        cursor.execute("""
            select column_name 
            from information_schema.columns 
            where table_schema='db' 
                and table_name = 'fencers';
            """)

        headers = cursor.fetchall()
        headers= [el[0] for el in headers]

        for fencer in fencer_data:
            fencer_dict=dict(zip(headers,fencer))
            day,month,year=fencer_dict["dateofbirth"].split(".")
            birthdate = date(year,month,day)
            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        
            if age >= 18:
                fencer_dict["adult"]=1
            else:
                fencer_dict["adult"]=0



with mysql.connect(**db_dict) as db:
    cursor = db.cursor()
    cursor.execute("""
        select 
            tournamentId,
            name           
        from tournaments;        
        """)
    tournaments=cursor.fetchall()
    ret_dict = dict()
    for tournament in tournaments:
        ret_dict[tournament[0]]=tournament[1]
    print(ret_dict)