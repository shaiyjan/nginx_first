import mysql.connector as mysql
import csv
from datetime import date

db_dict = {
#    "host"      : "172.16.103.13",
    "host"      : "localhost",
    "database"    : "db",
    "user"      : "user",
    "password"  : "password",
    "port"      : "3306"
}

tournaments=dict()

def insert_cl():
    participants=[]

    with open("participants.csv") as csvfile:
        reader = csv.reader(csvfile,delimiter=";")
        header=next(reader)
        for row in reader:
            row = [ele.strip() for ele in row]
            fencer_dict = dict(zip(header,row))
            if fencer_dict["paid"]=="yes":
                fencer_dict["paid"] = 1
            else:
                fencer_dict["paid"] = 0
            participants.append(fencer_dict)

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
            paid bool default 0,
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
            recipe bool default 0,
            attandence bool defualt 0,
            attest bool default 0,
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
                    competition)
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
            %(competition)s)
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
            SignuplistId int NOT NULL AUTO_INCREMENT,
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


def create_tournaments() -> dict:
    with mysql.connect(**db_dict) as db:
        cursor =db.cursor()
        cursor.execute(
            """
            create table if not exists tournaments(
            TournamentId int NOT NULL AUTO_INCREMENT,
            name varchar(200) NOT NULL,
            group_size int NOT NULL,
            group_count int NOT NULL,
            tournament_mode varchar(20) NOT NULL,
            preliminaries int NOT NULL,
            started bool NOT NULL DEFAULT 0,
            PRIMARY KEY (TournamentID)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tournament_groups (
                GroupId INT NOT NULL AUTO_INCREMENT,
                TournamentId INT NOT NULL,
                group_no INT NOT NULL,
                preliminaries INT NOT NULL,
                fencer_ID INT NOT NULL,
                PRIMARY KEY (GroupId),
                FOREIGN KEY (TournamentId) REFERENCES tournaments(TournamentId) ON DELETE CASCADE
            );
            """
        )
        db.commit()


def setup_db():
    # Setup all tables in the database.
    try:
        mydb =mysql.connect(**db_dict)
        cursor=mydb.cursor()
        cursor.execute(
            """
            create table if not exists tournaments(
                TournamentId int NOT NULL AUTO_INCREMENT,
                name varchar(200) NOT NULL,
                group_size int NOT NULL,
                group_count int NOT NULL,
                tournament_mode varchar(20) NOT NULL,
                preliminaries int NOT NULL,
                started bool NOT NULL DEFAULT 0,
                PRIMARY KEY (TournamentID)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tournament_groups (
                GroupId INT NOT NULL AUTO_INCREMENT,
                TournamentId INT NOT NULL,
                group_no INT NOT NULL,
                preliminaries INT NOT NULL,
                FencerID INT NOT NULL,
                PRIMARY KEY (GroupId),
                FOREIGN KEY (TournamentId) REFERENCES tournaments(TournamentId) ON DELETE CASCADE
            );
            """
        )
        cursor.execute(
            """
            create table if not exists fencers(
                fencerID int NOT NULL AUTO_INCREMENT,
                lastname varchar(100) NOT NULL,
                firstname varchar(100) NOT NULL,
                dateofbirth varchar(10) NOT NULL,
                gender varchar(1) NOT NULL,
                nation varchar(3),
                region varchar(50),
                club varchar(100),
                paid bool default 0,
                attest bool default 0,
                adult bool default 0,
                note varchar(2000) default '',
                PRIMARY KEY(FencerID)
            )
            """
        )
        cursor.execute(
            """
            create table if not exists signuplists(
            SignuplistId int NOT NULL AUTO_INCREMENT,
            name varchar(200),
            in_tournament bool default FALSE,
            PRIMARY KEY (SignuplistId)
            )
            """
        )
        cursor.execute(
            """
            create table if not exists signups(
                SignupID int NOT NULL AUTO_INCREMENT,
                FencerID int NOT NULL,
                SignuplistID int NOT NULL,
                attendance bool NOT NULL DEFAULT 0,
                PRIMARY KEY(SignupID),
                FOREIGN KEY (FencerID) REFERENCES fencers(FencerID) ON DELETE CASCADE,
                FOREIGN KEY (SignuplistID) REFERENCES signuplists(SignuplistID) ON DELETE CASCADE
            )
            """)

    except Exception as e  :
        print(e)

def insert():
    fencer_dict = dict()
    signup_dict = dict()
    fencer_id = dict()

    with open("participants.csv") as csvfile:
        reader = csv.reader(csvfile,delimiter=";")
        header=next(reader)
        for row in reader:
            row = row
            temp_dict= dict(zip(header,row))
            day,month,year=temp_dict["dateofbirth"].split(".")
            birthdate = date(int(year),int(month),int(day))
            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

            if age >= 18:
                adult=1
            else:
                adult=0

            key = tuple([*row[1:8],adult])
            if key not in fencer_dict.keys():
                fencer_dict[key] = [temp_dict["competition"].strip()]
            else:
                fencer_dict[key]=[*fencer_dict[key],temp_dict["competition"].strip()]

            signup_dict[temp_dict["competition"].strip()] = 1

    with mysql.connect(**db_dict) as db:
        cursor=db.cursor()

        for key in signup_dict.keys():   
            cursor.execute("""
                insert into signuplists(name) values (%s)""",
                (key,))
            signup_dict[key]=cursor.lastrowid
            db.commit()

        for key in fencer_dict.keys():
            cursor.execute("""
                           insert into fencers (
                           lastname,
                           firstname,
                           dateofbirth,
                           gender,
                           nation,
                           region,
                           club,
                           adult
                           ) values(%s,%s,%s,%s,%s,%s,%s,%s)
                           """,
                           tuple(key))
            fencer_id[key]=cursor.lastrowid
            db.commit()

        signups_list = list()
        for key in fencer_dict.keys():
            id = fencer_id[key]
            tournament_names = fencer_dict[key]
            for name in tournament_names:
                signups_list.append((id,signup_dict[name]))

        cursor.executemany("""
            INSERT INTO signups (FencerID,SignuplistID) values (%s,%s)             
            """,signups_list)
        db.commit()


setup_db()
insert()
#create_tournaments()

