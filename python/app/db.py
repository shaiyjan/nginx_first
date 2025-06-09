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

        print(headers)

        fencer_dicts=dict()
        for count,fencer in enumerate(fencers):
            fencer_dict=dict(zip(headers,fencer))
            fencer_dict.pop("dateofbirth")
            fencer_dict.pop("region")
            fencer_dicts[count]=fencer_dict
            print(fencer_dict)

        return fencer_dicts
    
fetchFencers()