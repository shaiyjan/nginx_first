
import mysql.connector as mysql


db_dict = {
    "host"      : "172.16.103.13",
#    "host"      : "localhost",
    "database"    : "db",
    "user"      : "user",
    "password"  : "password",
    "port"      : "3306"
}

class dbcon:
    def __init__(self):
        self.db_dict = {
            "host"      : "172.16.103.13",
        #    "host"      : "localhost",
            "database"    : "db",
            "user"      : "user",
            "password"  : "password",
            "port"      : "3306"
                }
        self.connect()
    
    def connect(self):
        self.db = mysql.connect(**self.db_dict)
        self.cursor = self.db.cursor()
    
    def cancelcon(self):
        self.db.close()

    def commit(self):
        self.db.commit()

    def tournament_names(self):
        try:
            self.connect()
            self.cursor.execute(
                """
                show tables;
                """
            )
            names = [name[0] for name in self.cursor.fetchall()]
            self.cancelcon()
            return names
        except Exception as e:
            print(e)

 if __name__=="__main__":
     db=dbcon()
     print(db.tournament_names())