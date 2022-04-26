import datetime
import mysql.connector
from datetime import datetime as dt
import pandas as pd
import logging


logging.basicConfig(filename='/home/grafana/Error_Log/ERL_error.log', filemode='w', format='%(asctime)s -%(name)s - %(levelname)s - %(message)s')



def Original_to_staging():

    try:


        
        mydb=mysql.connector.connect(host="XX.XX.XX.XX",user="xxx",password="xxxx",database="erl_central_dbase")

        mycursor=mydb.cursor()

        mycursor.execute("select Date(Entered_Date),date_Format(Entered_Date,'%H'),province_id,Authority_ID,count(License_No) ,sum(coalesce(License_Amount)+coalesce(Arrears)+coalesce(Tax)+coalesce(Fine)) from rev_license_record where Date(Entered_Date) =CURDATE() - INTERVAL 1 DAY and (License_Type_ID =1 or License_Type_ID=3) and License_Status_ID=1 group by Date(Entered_Date),date_Format(Entered_Date,'%H'),province_id,Authority_ID")

        rows=mycursor.fetchall()

        #-----------------------------------------------------------------------------------------------------

        mydb_2=mysql.connector.connect(host="localhost",user="root",password="xxxxxx",database="ERL")


        mycursor_2=mydb_2.cursor()

        sql_sts="INSERT INTO revenue_old(Entered_Date,Hour,province_id,Authority_ID,License_Count,Total_Revenue) VALUES (%s,%s,%s,%s,%s,%s)"

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

