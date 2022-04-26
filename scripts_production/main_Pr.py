import pandas as pd
import mysql.connector as mysql
import numpy as np
import HHIMS_logging
import HHIMS_DB_Conn



def Connect_DB():

    

    try:

        USER='root'
        PASSWORD='password'
        HOST='127.0.0.1'
        DATABASE=''
        Catergory='1'
        PDHS='1'
        RDHS='1'
        Hospital='1'        
        
        #df = pd.read_csv('Details.txt', sep=",",index_col=False)

        """for ind in df.index:
            USER=df['USER'][ind]
            PASSWORD= df['PASSWORD'][ind]
            HOST= df['HOST'][ind]
            DATABASE= df['DATABASE'][ind]
            Catergory=df['catergory'][ind]
            PDHS=df['PDHS'][ind]
            RDHS=df['RDHS'][ind]
            Hospital=df['Hospital'][ind]"""

        HHIMS_DB_Conn.DB_connection(USER,PASSWORD,HOST,DATABASE,Catergory,PDHS,RDHS,Hospital)
            

        
            
            

    except Exception as e:
        HHIMS_logging.logger.error(e)



if __name__=="__main__":
    Connect_DB()
    
   
    

