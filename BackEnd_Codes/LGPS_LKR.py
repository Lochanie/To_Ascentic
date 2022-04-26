import datetime
import mysql.connector
from datetime import datetime as dt
import pandas as pd
import logging


logging.basicConfig(filename='/home/grafana/Error_Log/LGPS_error.log', filemode='w', format='%(asctime)s -%(name)s - %(levelname)s - %(message)s')



def Original_to_staging():

    try:


        
        mydb=mysql.connector.connect(host="XX.XX.XX.XX",user="xxx",password="xxxx",database="lgps")

        mycursor=mydb.cursor()

        mycursor.execute("select date(tx_complete_date) as TX_Date,HOUR(tx_complete_date) as TX_Hour,dept_id,service_id,sum(CASE WHEN tx_status=1 then 1 else 0 end) as Accepted_LKR_Count,sum(CASE WHEN tx_status=0 then 1 else 0 end) as Rejected_LKR_Count,sum(CASE WHEN tx_status=1 then tx_amount else 0 end) as Accepted_LKR_Amount,sum(CASE WHEN tx_status=1 then convenience_fee_amount else 0 end) as Accepted_LKR_BankFee, sum(CASE WHEN (tx_status=1 and (pg_name='paycorp' or pg_name='paycorpauto' or pg_name='sampathnet')) then 1 else 0 end) as Sampath_BankCount,sum(CASE WHEN (tx_status=1 and (pg_name='paycorp' or pg_name='paycorpauto' or pg_name='sampathnet')) then tx_amount else 0 end) as Sampath_BankAmount,sum(CASE WHEN (tx_status=1 and (pg_name='paycorp' or pg_name='paycorpauto' or pg_name='sampathnet')) then convenience_fee_amount else 0 end) as Sampath_BankFee,sum(CASE WHEN (tx_status=1 and pg_name='ntb') then 1 else 0 end) as NTB_BankCount,sum(CASE WHEN (tx_status=1 and pg_name='ntb') then tx_amount else 0 end) as NTB_BankAmount,sum(CASE WHEN (tx_status=1 and pg_name='ntb') then convenience_fee_amount else 0 end) as NTB_BankFee from transaction_detail where Date(tx_complete_date)= CURDATE() - INTERVAL 1 DAY and service_id NOT IN (select service_id from transaction_detail where (service_id =85 or service_id =1 or service_id =79 or service_id =41 or service_id =14 or service_id =5 or service_id =21 or service_id =76 or service_id =84)) group by date(tx_complete_date),HOUR(tx_complete_date),dept_id,service_id")

        rows=mycursor.fetchall()

        #-----------------------------------------------------------------------------------------------------

        mydb_2=mysql.connector.connect(host="localhost",user="root",password="xxxx",database="lgps")


        mycursor_2=mydb_2.cursor()

        sql_sts="INSERT INTO lkr_transactions(TX_Date,TX_Hour,dept_id,service_id,Accepted_LKR_Count,Rejected_LKR_Count,Accepted_LKR_Amount,Accepted_LKR_BankFee,Sampath_BankCount,Sampath_BankAmount,Sampath_BankFee,NTB_BankCount,NTB_BankAmount,NTB_BankFee) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

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

