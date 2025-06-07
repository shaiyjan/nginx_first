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
        fencer_dict = dict(zip(header,row))
        if fencer_dict["paid"]=="yes":
            fencer_dict["paid"] = 1
        else:
            fencer_dict["paid"] = 0
        participants.append(fencer_dict)
        


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




#insert()
create_tournaments()
