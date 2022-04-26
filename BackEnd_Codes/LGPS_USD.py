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

        mycursor.execute("select date(tx_complete_date) as TX_Date,HOUR(tx_complete_date) as TX_Hour,dept_id,service_id,sum(CASE WHEN tx_status=1 then 1 else 0 end) as Accepted_USD_Count,sum(CASE WHEN tx_status=0 then 1 else 0 end) as Rejected_USD_Count,sum(CASE WHEN tx_status=1 then tx_amount else 0 end) as Accepted_USD_Amount,sum(CASE WHEN tx_status=1 then convenience_fee_amount else 0 end) as Accepted_USD_BankFee from transaction_detail where (service_id =85 or service_id =1 or service_id =79 or service_id =41 or service_id =14 or service_id =5 or service_id =21 or service_id =76 or service_id =84) and Date(tx_complete_date)= CURDATE() - INTERVAL 1 DAY group by date(tx_complete_date),HOUR(tx_complete_date),dept_id,service_id")

        rows=mycursor.fetchall()

        #-----------------------------------------------------------------------------------------------------

        mydb_2=mysql.connector.connect(host="localhost",user="root",password="xxxxxx",database="lgps")


        mycursor_2=mydb_2.cursor()

        sql_sts="INSERT INTO USD_transactions(TX_Date,TX_Hour,dept_id,service_id,Accepted_USD_Count,Rejected_USD_Count,Accepted_USD_Amount,Accepted_USD_BankFee) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

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

