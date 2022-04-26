import datetime
import mysql.connector
from datetime import datetime as dt
import pandas as pd
import logging


logging.basicConfig(filename='/home/grafana/Error_Log/SLP_error.log', filemode='w', format='%(asctime)s -%(name)s - %(levelname)s - %(message)s')



def Original_to_staging():

    try:


        
        mydb=mysql.connector.connect(host="XX.XX.XX.XX",user="xxx",password="xxxx",database="police_db")

        mycursor=mydb.cursor()

        mycursor.execute("SELECT DATE(submitted_date)as submitted_date,HOUR(submitted_date)as submitted_hour,country_id,country_name,sum(case when application_type='ON' then 1 else 0 end)as 'Online_Count',sum(case when application_type='MA' then 1 else 0 end)as 'Manual_Count' FROM application where DATE(submitted_date)=CURDATE() - INTERVAL 1 DAY group by DATE(submitted_date),HOUR(submitted_date),country_id,country_name")

        rows=mycursor.fetchall()

        #-----------------------------------------------------------------------------------------------------

        mydb_2=mysql.connector.connect(host="localhost",user="root",password="xxxxx",database="police_db")


        mycursor_2=mydb_2.cursor()

        sql_sts="INSERT INTO application(submitted_date,submitted_hour,country_id,country_name,Online_Count,Manual_Count) VALUES (%s,%s,%s,%s,%s,%s)"

        val=rows
        mycursor_2.executemany(sql_sts,val)

        mydb_2.commit()

        mydb_2.close()

        mydb.close()


    except Exception as e:

        logging.error(e)



#********************************************************************************************************************************************#

if __name__ == '__main__':
    Original_to_staging()

