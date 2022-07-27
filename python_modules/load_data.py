import csv
import os
import mysql.connector
import yaml
from datetime import datetime
from bs4 import BeautifulSoup

class LoadKey:

    global db_today_date
    db_today_date = datetime.today().strftime('%Y-%m-%d')

    global user, mysql_password, host, database
    user, mysql_password, host, database = None, None, None, "E_MilhoesDB"

    global full_key 
    full_key = None

    global table_names
    table_names = []

    global landing_zone
    landing_zone = os.path.dirname(os.path.abspath(__file__ + "../../"))

    def __init__(self, file_name, config_file):
        self.file_name = file_name
        self.config_file = config_file


    def get_key(self):
        with open((landing_zone + self.file_name), 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            global full_key
            full_key = (soup.find("div", {"class": "betMiddle twocol regPad"}).find("li").get_text()).split(" ")
            del full_key[5]
        print("key obtained")

    def read_config(self):
        global user, mysql_password, host
        with open((landing_zone + self.config_file), 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            user = data['user']
            mysql_password = data['password']
            host = data['host']

    def connect_to_db(self):
        return mysql.connector.connect(
            host=host,
            user=user,
            password=mysql_password,
            database=database)
   
    def save_to_db(self):
        db = self.connect_to_db()
        sql_statement = "INSERT INTO `{}` (date, n1, n2, n3, n4, n5, e1, e2) VALUES (%s,\
        %s, %s, %s, %s, %s, %s, %s)".format(datetime.today().strftime('%Y'))
        cursor = db.cursor()
        cursor.execute(sql_statement, [db_today_date, full_key[0],
        full_key[1], full_key[2], full_key[3],
        full_key[4], full_key[5], full_key[6]])
        db.commit()
        db.close()
        print("Key Saved In DB")

    def get_tables_names(self):
        db = self.connect_to_db()
        all_tables_statement = "SHOW TABLES"
        cursor = db.cursor()
        cursor.execute(all_tables_statement)
        for table_name in cursor:
            detuppled_table = list(table_name[0:5])
            for item in detuppled_table:
                add_pelic_to_item ="`" + item[0:5] + "`"
                table_names.append(add_pelic_to_item)
        db.close()
        return table_names
    
    def write_csv(self, keys):
        with open((landing_zone + "/csv/keys.csv"), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["id","date", "n1", "n2", "n3", "n4", "n5", "e1", "e2"])
            writer.writerows(keys)
            print("CSV Saved")

    def save_to_csv(self):
        db = self.connect_to_db()  
        cursor = db.cursor()
        n_tables = table_names.__len__()
        if n_tables > 1: 
            template_statement = "SELECT * FROM {} "
            sql_statement = template_statement.format(" UNION ALL SELECT * FROM ".join(map(str,table_names)))
            cursor.execute(sql_statement)
            data = cursor.fetchall()
            self.write_csv(data)
            db.close()
        else:
            sql_statement = "SELECT * FROM {}".format(table_names[0])
            cursor.execute(sql_statement)
            data = cursor.fetchall()
            self.write_csv(data)
            db.close()
       
if __name__ == "__main__":
    app = LoadKey("/landing_zone/page_%s.html" % datetime.today().strftime('%Y_%m_%d'),
    "/MySQL_Config.yaml")
    app.get_key()
    app.read_config()
    app.save_to_db()
    app.get_tables_names()
    app.save_to_csv()