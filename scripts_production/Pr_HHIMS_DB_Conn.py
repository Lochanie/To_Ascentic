import pandas as pd
import mysql.connector as mysql
import numpy as np
import HHIMS_logging
import HHIMS_Fetch


def DB_connection(USER,PASSWORD,HOST,DATABASE,Catergory,PDHS,RDHS,Hospital):

    try:
        db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        
        HHIMS_Fetch.Fetch_Data(db_connection,Catergory,PDHS,RDHS,Hospital)
        
        db_connection.close()
        
               
        

    except Exception as e:
        HHIMS_logging.logger.error(e)







#df=DB_connection(USER,PASSWORD,HOST,DATABASE)
