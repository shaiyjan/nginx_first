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

fencerID=1

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
                   a.fencerID,
                case 
                    when a.fencerID = NULL then 0
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
    print(fencer_data)
    cursor.execute("""
        select column_name 
        from information_schema.columns 
        where table_schema='db' 
            and table_name = 'fencers'
        order by ordinal_position;
        """)
    header=[el[0] for el in cursor.fetchall()]
    fencer_dict = dict(zip(header,fencer_data))

    print(header)
    print(fencer_dict)
    fencer_dict["participation"]= participation

print(fencer_dict)