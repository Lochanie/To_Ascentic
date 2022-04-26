import datetime
import mysql.connector
from datetime import datetime as dt
import pandas as pd
import logging


logging.basicConfig(filename='/home/grafana/Error_Log/govsms_error.log', filemode='w', format='%(asctime)s -%(name)s - %(levelname)s - %(message)s')



def Original_to_staging():

    try:


        
        mydb=mysql.connector.connect(host="XX.XX.XX.XX",user="xxx",password="xxxx",database="govsms")

        mycursor=mydb.cursor()

        mycursor.execute("select receivedDate, HOUR(receivedTime) as Hour,UPPER(depCode) as deptCode,count(sms) as Total_Count,sum(case when UPPER(depCode='DMT' or depCode='DLB' or depCode='EXAM' or depCode='POST' or depCode='PEC' or depCode='SS' or depCode='ETF' or depCode='SLRD' or depCode='RPD' or depCode='AGRI' or depCode='PLC' or depCode='SLTB' or depCode='CFC' or depCode='RGD' or depCode='WMS' or depCode='TSHDA' or depCode='CMC' or depCode='DWC' or depCode='ESLIMS' or depCode='SLP' or depCode='PARLIMENT' or depCode='HMG-PS' or depCode='SWK-UC' or depCode='TELLGOV' or depCode='NGB-MC' or depCode='NHSL' or depCode='EROC' or depCode='LOCALGOV' or depCode='IECD' or depCode='CCF' or depCode='ELECTIONS' or depCode='ECRD' or depCode='MFA' or depCode='FOREST_DEPT' or depCode='HIGHEREDU' or depCode='LANGUAGDEPT' or depCode='PUBLICWIFI' or depCode='MEPA' or depCode='MYCOVACC' or depCode='NCPA' or depCode='UGC') then 1 else 0 end) as Correct_Count, sum(case when smsc='mobitel' then 1 else 0 end) as Mobitel_Count,sum(case when smsc='dgsm' then 1 else 0 end) as Dialog_Count,sum(case when smsc='airtel' then 1 else 0 end) as Airtel_Count,sum(case when smsc='hutch' then 1 else 0 end) as Hutch_Count from tbl_incoming where receivedDate=CURDATE()-INTERVAL 1 DAY group by receivedDate, HOUR(receivedTime),UPPER(depCode)")

        rows=mycursor.fetchall()

        #-----------------------------------------------------------------------------------------------------

        mydb_2=mysql.connector.connect(host="localhost",user="root",password="xxxxx",database="govsms")


        mycursor_2=mydb_2.cursor()

        sql_sts="INSERT INTO tbl_incoming(receivedDate,Hour,deptCode,Total_Count,Correct_Count,Mobitel_Count,Dialog_Count,Airtel_Count,Hutch_Count) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

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

