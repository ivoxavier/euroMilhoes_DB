from getpass import getpass
import os
import mysql.connector
import yaml
from datetime import datetime


class CreateDW:
    global user, mysql_password, host
    user, mysql_password, host = None, None, None

    global root_dir
    root_dir = os.path.dirname(os.path.abspath(__file__ + "../../"))

    def __init__(self, config_file):
        self.config_file = config_file

    def connect_to_db(self):
        return mysql.connector.connect(
            host=host,
            user=user,
            password=mysql_password)

    #Ask's for connection details
    def save_MySQLConfigs(self):
        global user, mysql_password, host
        user = input("Enter user: ")
        mysql_password = getpass("Enter Connection Password:")
        host = input("Enter Host Name: ")
        with open(root_dir + self.config_file, 'w') as f:
            yaml.dump({
            'user' : user,
            'password' : mysql_password,
            'host' : host
            }, f)

    def load_MySQLConfigs(self):
        global user, mysql_password, host
        with open(root_dir + self.config_file, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            user = data['user']
            mysql_password = data['password']
            host = data['host']        

    '''def create_dw(self):
        mySQL_Server = self.connect_to_db()
        with open(root_dir + "/sql/createDW.sql", "r") as f:
            sql = f.read()
            mySQL_Server.cursor().execute(sql)
            mySQL_Server.close()'''
        
    def create_dw(self):
        db = self.connect_to_db()
        sql_drop_statement = "DROP DATABASE IF EXISTS `E_MilhoesDB`"
        sql_create_db_statement = "CREATE DATABASE `E_MilhoesDB`"
        sql_create_table_statement = "CREATE TABLE `E_MilhoesDB`.`%s` (\
        `id` INT NOT NULL AUTO_INCREMENT,\
        `date` DATE NOT NULL,\
        `n1` INT NOT NULL,\
        `n2` INT NOT NULL,\
        `n3` INT NOT NULL,\
        `n4` INT NOT NULL,\
        `n5` INT NOT NULL,\
        `e1` INT NOT NULL,\
        `e2` INT NOT NULL,\
        PRIMARY KEY (`id`)) ENGINE = InnoDB" % (datetime.today().strftime('%Y'))
        
        sql_statements = [sql_drop_statement,
        sql_create_db_statement,
        sql_create_table_statement]

        for i in sql_statements:
            db.cursor().execute(i)
        
if __name__ == "__main__":
    create_dw = CreateDW("/MySQL_Config.yaml")
    create_dw.save_MySQLConfigs()
    create_dw.load_MySQLConfigs()
    create_dw.create_dw()