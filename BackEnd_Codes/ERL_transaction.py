import datetime
import mysql.connector
from datetime import datetime as dt
import pandas as pd
import logging


logging.basicConfig(filename='/home/grafana/Error_Log/error.log', filemode='w', format='%(asctime)s -%(name)s - %(levelname)s - %(message)s')



def Original_to_staging():

    try:


        
        mydb=mysql.connector.connect(host="XX.XX.XX.XX",user="xxx",password="xxxx",database="erl_central_dbase")

        mycursor=mydb.cursor()

        mycursor.execute("select DATE(Transaction_Time),HOUR(Transaction_Time),province_id, sum(case when Transaction_Status='ACCEPTED' then 1 else 0 end) as Accepted_Transactions,sum(case when Transaction_Status='ACCEPTED' then Payment_Amount else 0 end) as Revenue_Accepted,sum(case when Transaction_Status='REJECTED' then 1 else 0 end) as Rejected_Transactions, sum(case when (Transaction_Status='ACCEPTED' and Payment_Gateway_Name='ntb') then 1 else 0 end) as ntb_Transactions,sum(case when (Transaction_Status='ACCEPTED' and Payment_Gateway_Name='ntb') then Payment_Amount else 0 end) as ntb_Revenue,sum(case when  (Transaction_Status='ACCEPTED' and Payment_Gateway_Name='LGPS') then 1 else 0 end) as LGPS_Transactions,sum(case when (Transaction_Status='ACCEPTED' and Payment_Gateway_Name='LGPS') then Payment_Amount else 0 end) as LGPS_Revenue,sum(case when (Transaction_Status='ACCEPTED' and Payment_Gateway_Name='paycorp') then 1 else 0 end) as PayCorp_Transactions,sum(case when (Transaction_Status='ACCEPTED' and Payment_Gateway_Name='paycorp') then Payment_Amount else 0 end) as ezcash_Revenue,sum(case when (Transaction_Status='ACCEPTED' and Payment_Gateway_Name='ezcash') then Vehicle_Reg_No else 0 end) as ezcash_Transactions,sum(case when (Transaction_Status='ACCEPTEDd' and Payment_Gateway_Name='ezcash') then Payment_Amount else 0 end) as ezcash_Revenue, count(case when (Transaction_Status='ACCEPTED' and Payment_Gateway_Name='sampathnet' or Payment_Gateway_Name='samapthnet' ) then Vehicle_Reg_No else 0 end) as sampathnet_Transactions,sum(case when (Transaction_Status='ACCEPTED' and Payment_Gateway_Name='sampathnet' or Payment_Gateway_Name='samapthnet') then Payment_Amount else 0 end) as sampathnet_Revenue from transaction_details where DATE(Transaction_Time)= CURDATE() - INTERVAL 1 DAY group by DATE(Transaction_Time), HOUR(Transaction_Time), province_id")

        rows=mycursor.fetchall()

        #-----------------------------------------------------------------------------------------------------

        mydb_2=mysql.connector.connect(host="localhost",user="root",password="xxxxx",database="ERL")


        mycursor_2=mydb_2.cursor()

        sql_sts="INSERT INTO transaction_new(Entered_Date,Hour,province_id,Accepted_Transactions,Revenue_Accepted,Rejected_Transactions,ntb_Transactions,ntb_Revenue,LGPS_Transactions,LGPS_Revenue,PayCorp_Transactions,PayCorp_Revenue,ezcash_Transactions,ezcash_Revenue,sampathnet_Transactions,sampathnet_Revenue) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

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

