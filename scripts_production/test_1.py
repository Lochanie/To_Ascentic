import pandas as pd
import mysql.connector as mysql
import HHIMS_logging


USER='root'
PASSWORD='password'
HOST='127.0.0.1'
DATABASE='hhimsv3_nhsl'


def DB_connection(USER,PASSWORD,HOST,DATABASE):

    try:
        db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cursor = db_connection.cursor()
        print(cursor)
        return cursor

    except Exception as e:
        HHIMS_logging.logger.error(e)



cursor=DB_connection(USER,PASSWORD,HOST,DATABASE)
