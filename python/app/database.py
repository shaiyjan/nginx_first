import mysql.connector as mysql
import csv

db_dict = {
#    "host"      : "172.16.103.13",
    "host"      : "localhost",
    "database"    : "db",
    "user"      : "user",
    "password"  : "password",
    "port"      : "3306"
}

tournaments=dict()

def insert():
    try:
        mydb =mysql.connect(**db_dict)
        cursor=mydb.cursor()
        cursor.execute(
            """
            create table if not exists registrations(
            RegistrationID int NOT NULL AUTO_INCREMENT,
            FencerID int,
            lastname varchar(100) NOT NULL,
            firstname varchar(100) NOT NULL,
            dateofbirth varchar(10) NOT NULL,
            gender varchar(1) NOT NULL,
            nation varchar(3),
            region varchar(50),
            club varchar(100),
            paid varchar(10),
            paymentmethod varchar(100),
            paymentid  varchar(50),
            partner varchar(100),
            date varchar(20),
            user varchar(100),
            user_email varchar(100),
            ranking  varchar(50),
            points  varchar(50),
            state varchar(100),
            orderid varchar(50),
            natid varchar(50),
            competition varchar(200),
            recipe varchar(3),
            attandence varchar(3),
            attest varchar(3),
            PRIMARY KEY(RegistrationID)
            )
            """
        )

        cursor.executemany(
            """
            INSERT INTO registrations 
                    (FencerID,
                    lastname,
                    firstname,
                    dateofbirth,
                    gender,
                    nation,
                    region,
                    club,
                    paid,
                    paymentmethod,
                    paymentid,
                    partner,
                    date,
                    user,
                    user_email,
                    ranking,
                    points,
                    state,
                    orderid,
                    natid,
                    competition,
                    recipe,
                    attandence ,
                    attest)
            values 
            (%(id)s,
            %(lastname)s,
            %(firstname)s,
            %(dateofbirth)s,
            %(gender)s,
            %(nation)s,
            %(region)s,
            %(club)s,
            %(paid)s,
            %(paymentmethod)s,
            %(payment-id)s,
            %(partner)s,
            %(date)s,
            %(user)s,
            %(user_email)s,
            %(ranking)s,
            %(points)s,
            %(state)s,
            %(order)s,
            %(natid)s,
            %(competition)s,
            %(recipe)s,
            %(attandence)s,
            %(attest)s)
            """,
            participants)
        mydb.commit()

        cursor.execute(
            """
            select distinct(competition) from registrations;
            """
        )
        tournaments = [{"name" :  fetch[0]} for fetch in cursor.fetchall()]
        cursor.execute(
            """
            create table if not exists signuplists(
            TournamentId int NOT NULL AUTO_INCREMENT,
            name varchar(200),
            in_tournament bool default FALSE,
            PRIMARY KEY (TournamentID)
            )
            """
        )
        cursor.executemany(
        """
        INSERT INTO signuplists (name) VALUES
        (%(name)s)
        """,
        tournaments
        )
        mydb.commit()
        mydb.close()
    except Exception as e:
        print(e)



participants=[]

with open("participants.csv") as csvfile:
    reader = csv.reader(csvfile,delimiter=";")
    header=next(reader)
    for row in reader:
        row = [ele.strip() for ele in row]
        participants.append(
            dict(zip(header,row))
        )

insert()

def copy_tournaments() -> dict:
    with mysql.connect(**db_dict) as db:
        cursor =db.cursor()
        cursor.execute(
            """
            select * from signuplists;
            """
        )
        tournaments =cursor.fetchall()
        ret_dict = dict()
        for tournament in tournaments:
            ret_dict[tournament[0]]=tournament[1]
        
        print(tournaments)
        cursor.execute(
            """
            create table if not exists tournaments(
            TournamentId int NOT NULL AUTO_INCREMENT,
            name varchar(200),
            PRIMARY KEY (TournamentID)
            )
            """
        )

        cursor.executemany(
        """
        INSERT INTO tournaments (name) VALUES
        (%(name)s)
        """,
            [{"name": "Tournament " + tup[1]} for tup in tournaments ]
        )
        db.commit()

copy_tournaments()
