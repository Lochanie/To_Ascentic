import pandas as pd
import numpy as np
import datetime as dt
from datetime import date
import datetime as datetime
from datetime import datetime
from datetime import datetime, date
from datetime import timedelta
import mysql.connector
from dateutil.relativedelta import relativedelta



Oracle_database_name='oracle_test'
oracledb_username='stg'
db_password=keyring.get_password(Oracle_database_name,oracledb_username)


while db_password==None:
    password=getpass.getpass(Oracle_database_name+"Password: \n")
    keyring.set_password(Oracle_database_name,oracledb_username,db_password)


connection=cx_Oracle.connect("stg",db_password,"xx.xx.xx.xx/bidb")
cursor=connection.cursor()

if connection:
    print("success")

    today = dt.date.today()
    # today='2019-01-02'
    start_date = today - relativedelta(days=1)
    date_generated =start_date

    sql_1 = """SELECT d.day,substr(b.account_no,2,3)SOL,b.account_name,a.DAY_END_BALANCE from dwh.fact_daily_balance_prt a,dwh.dim_dayend_account b,dwh.dim_date d where a.account_key=b.account_key and d.date_key=a.date_key and b.GL_SUB_HEAD_CODE='00000' and (substr(b.account_no,11,2) IN ('26','72','70','71') OR (substr(b.account_no,11,2)>= '75' AND substr(b.account_no,11,2)<='90')) and d.day=trunc(sysdate-1) order by SOL,b.account_no"""
    df_DE = pd.read_sql(sql_1, connection)

    sql_2 = """select KB_RCRE_TIME,KB_PSTD_DATE,KB_ACC_NUM,INIT_SOL_ID,TRAN_DATE,TRAN_TYPE,TRAN_SUB_TYPE,PART_TRAN_TYPE,TRAN_AMT,TRAN_AMT_IN_LKR from stg.KBSL_YDAY_VALULT"""
    df = pd.read_sql(sql_2, connection)

#Pre-Operations in vault transaction file


#Extract the relevant columns from the original transaction file
    df1=pd.DataFrame(df,columns=['KB_RCRE_TIME','TRAN_DATE','TRAN_SUB_TYPE','PART_TRAN_TYPE','TRAN_AMT','INIT_SOL_ID'])

    df1[['Date','Hours','Minutes','Seconds']] = df1['KB_RCRE_TIME'].str.split('_',expand=True)
    df1["Date&Time"] = df1["Date"].map(str)+" "+df1["Hours"].map(str) +":"+ df1["Minutes"].map(str)+":"+df1["Seconds"].map(str)
    df1['Date&Time']=pd.to_datetime(df1['Date&Time'],dayfirst=True, errors='coerce')
    df1['Date&Time']=pd.to_datetime(df1['Date&Time'],format='%Y-%m-%d %H:%M:%S')
    df2=pd.DataFrame(df1,columns=['Date&Time','TRAN_DATE','INIT_SOL_ID','TRAN_SUB_TYPE','PART_TRAN_TYPE','TRAN_AMT'])
    df2.sort_values(by=['INIT_SOL_ID','Date&Time'],inplace=True)
    df2['Received_Amount'] = np.where(((df2['TRAN_SUB_TYPE']=='NR') & (df2['PART_TRAN_TYPE']=='D')), (df2['TRAN_AMT'])*1,(df2['TRAN_AMT'])*-1)
    df2['Received_Amount']=pd.to_numeric(df2['Received_Amount'])
    df2['TRAN_DATE']=pd.to_datetime(df2['TRAN_DATE'],dayfirst=True,errors='coerce')
    df2['TRAN_DATE']=pd.to_datetime(df2['TRAN_DATE'],format='%Y-%m-%d')
    df2['TRAN_DATE']=df2.TRAN_DATE.dt.strftime('%Y-%m-%d')

#Pre-Operations in Day End File
    df_DE.rename(columns={'DAY':'TRAN_DATE','SOL':'INIT_SOL_ID'},inplace=True)
    df_DE=pd.DataFrame(df_DE,columns=['TRAN_DATE','INIT_SOL_ID','DAY_END_BALANCE'])
    df_DE['TRAN_DATE']= pd.to_datetime(df_DE['TRAN_DATE'], dayfirst=True, errors='coerce')
    df_DE['TRAN_DATE'] = df_DE['TRAN_DATE'] + timedelta(days=1)
    df_DE['TRAN_DATE']=df_DE.TRAN_DATE.dt.strftime('%Y-%m-%d')


    def CalculteMinValue(df2, INIT_SOL_ID, TRAN_DATE):
        # print(df2)
        # print(INIT_SOL_ID)
        # print(TRAN_DATE)



        # df3= df2[((df2.INIT_SOL_ID==INIT_SOL_ID)&(df2.TRAN_DATE==TRAN_DATE))]
        df3 = df2[(df2['TRAN_DATE'] == TRAN_DATE) & (df2['INIT_SOL_ID'] == (INIT_SOL_ID))]
        # print(df3.head(10))

        # df3.to_csv(r'C:\Users\lochanie\Documents\KBSL DATA_sampath\Solution\Test\Test5\ReceivedTest.csv', index=False)

        df3.sort_values(by=['Date&Time'], ascending=True, inplace=True)
        # print(df3.head(10))

        # df3.to_csv(r'C:\Users\lochanie\Documents\KBSL DATA_sampath\Solution\Test\Test5\SortTest.csv', index=False)

        df3['CUMSUM'] = df3['Received_Amount'].cumsum()
        # print(df3.head(10))

        # df3.to_csv(r'C:\Users\lochanie\Documents\KBSL DATA_sampath\Solution\Test\Test5\CUMTest.csv', index=False)

        df3['Minimum'] = df3['CUMSUM'].min()
        # print(df3.head(10))

        # df3.to_csv(r'C:\Users\lochanie\Documents\KBSL DATA_sampath\Solution\Test\Test5\MinTest.csv', index=False)

        df3.drop_duplicates(subset=['INIT_SOL_ID', 'TRAN_DATE'], keep='first', inplace=True)
        # print(df3.head(10))

        # df3.to_csv(r'C:\Users\lochanie\Documents\KBSL DATA_sampath\Solution\Test\Test5\DropDupTest.csv', index=False)

        df3['Minimum'] = np.where(df3['Minimum'] < 0, df3['Minimum'] * 1, df3['Minimum'] * 0)
        # print(df3.head(10))

        # df3.to_csv(r'C:\Users\lochanie\Documents\KBSL DATA_sampath\Solution\Test\Test5\PlusTest.csv', index=False)

        df3['Minimum'] = df3['Minimum'].abs()
        # print(df3.head(10))

        # df3.to_csv(r'C:\Users\lochanie\Documents\KBSL DATA_sampath\Solution\Test\Test5\FinalTest.csv', index=False)
        DF_list = []
        df4 = df3.append(df3)
        # df4.to_csv(r'C:\Users\lochanie\Documents\KBSL DATA_sampath\Solution\Test\Test5\FinalTest.csv', index=False)
        # print(DF_list)
        # DF_list.to_csv(r'C:\Users\lochanie\Documents\KBSL DATA_sampath\Solution\Test\Test5\FinalTest.csv', index=False)

        for index, row in df3.iterrows():
            myInsertMinimun(row['INIT_SOL_ID'], row['TRAN_DATE'], row['Minimum'])


    def myQuary(mySqlStr):
        try:
            cnx = mysql.connector.connect(user='root', password='password',
                                          database='sampath_project_4', host='localhost')
        except mysql.connector.Error as err:

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                myErr = "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                myErr = "Database does not exist"
            else:
                myErr = "unknown error"
            return myErr, -1
        else:
            cursor = cnx.cursor()
            df = pd.read_sql(mySqlStr, con=cnx)
            cursor.close()
            cnx.close()
            return df, len(df)


    def myInsertMinimun(INIT_SOL_ID, TRAN_DATE, Minimum):
        queryInsert = """ INSERT INTO `vault`
                               (`branch_key_id`,`vault_date`,`vault_actual`) VALUES (%s,%s,%s)"""
        # print(queryInsert)

        argsInsert = (INIT_SOL_ID, TRAN_DATE, Minimum)
        # print(argsInsert)



        queryUpdate = """ UPDATE vault
                    SET  branch_key_id=%s,vault_date=%s,vault_actual=%s 
                    WHERE branch_key_id=%s and vault_date=%s """
        # print(queryUpdate)

        argsUpdate = (INIT_SOL_ID, TRAN_DATE, Minimum, INIT_SOL_ID, TRAN_DATE)
        # print(argsUpdate)


        myResult = 0
        # try:
        cnx = mysql.connector.connect(user='root', password='password',
                                      database='sampath_project_4', host='localhost')

        # print('***********************')
        myTmpSql = 'select vault_actual from vault where branch_key_id="{}" and vault_date="{}"'.format(INIT_SOL_ID,
                                                                                                        TRAN_DATE)
        # print(myTmpSql)
        myTDresult, myTDresultCount = myQuary(myTmpSql)

        # print(str(myTDresultCount))

        # print(str(myTDresult))
        if (myTDresultCount > 0):
            print('record available.......')
            cursor = cnx.cursor()
            print(cursor)
            cursor.execute(queryUpdate, argsUpdate)
            cnx.commit()
            print('successfuly updated')
        else:
            print('record not available....')
            cursor = cnx.cursor()
            cursor.execute(queryInsert, argsInsert)
            cnx.commit()
            cursor.close()
            print('successfuly inserted')
            # ***********************

        myResult = 1

        # except Error as e:
        # print('Error:', e)
        # myResult=0

        # finally:
        cnx.close()
        return myResult



#Function Definitions Related to the Day End File
    def calculateDE(df_DE, INIT_SOL_ID, TRAN_DATE):
        # print('**************************************')
        df_DE_1 = df_DE[(df_DE['TRAN_DATE'] == TRAN_DATE) & (df_DE['INIT_SOL_ID'] == INIT_SOL_ID)]
        df_DE_1['REAL_DAY_END_BALANCE'] = df_DE_1['DAY_END_BALANCE'].sum()
        df_DE_1.drop_duplicates(subset=['INIT_SOL_ID', 'TRAN_DATE'], keep='first', inplace=True)
        df_DE_1['REAL_DAY_END_BALANCE'] = df_DE_1['REAL_DAY_END_BALANCE'].abs()

        # df_DE_1['TRAN_DATE']= pd.to_datetime(df_DE_1['TRAN_DATE'], dayfirst=True, errors='coerce')
        # df_DE_1['TRAN_DATE'] = df_DE_1['TRAN_DATE'] + timedelta(days=1)
        # df_DE_1['TRAN_DATE']=df_DE_1.TRAN_DATE.dt.strftime('%Y-%m-%d')

        # df_DE_new=pd.DataFrame(df_DE_1,columns=['TRAN_DATE','INIT_SOL_ID','REAL_DAY_END_BALANCE'])
        # df_DE_1.to_csv(r'C:\Users\lochanie\Documents\KBSL DATA_sampath\Solution\Test\Test5\FinalDEtest.csv', index=False)


        for index, row in df_DE_1.iterrows():
            myInsertDE(row['INIT_SOL_ID'], row['TRAN_DATE'], row['REAL_DAY_END_BALANCE'])


    def myInsertDE(INIT_SOL_ID, TRAN_DATE, REAL_DAY_END_BALANCE):
        queryInsert = """ INSERT INTO `vault`
                               (`branch_key_id`,`vault_date`,`vault_actual_ob`) VALUES (%s,%s,%s)"""
        # print(queryInsert)

        argsInsert = (INIT_SOL_ID, TRAN_DATE, REAL_DAY_END_BALANCE)
        # print(argsInsert)



        queryUpdate = """ UPDATE vault
                    SET  branch_key_id=%s,vault_date=%s,vault_actual_ob=%s 
                    WHERE branch_key_id=%s and vault_date=%s """
        # print(queryUpdate)

        argsUpdate = (INIT_SOL_ID, TRAN_DATE, REAL_DAY_END_BALANCE, INIT_SOL_ID, TRAN_DATE)
        # print(argsUpdate)


        myResult = 0
        # try:
        cnx = mysql.connector.connect(user='root', password='password',
                                      database='sampath_project_4', host='localhost')

        # print('***********************')
        myTmpSql = 'select vault_actual,vault_actual_ob from vault where branch_key_id="{}" and vault_date="{}"'.format(
            INIT_SOL_ID, TRAN_DATE)
        # print(myTmpSql)
        myTDresult, myTDresultCount = myQuary(myTmpSql)

        # print(str(myTDresultCount))

        # print(str(myTDresult))
        if (myTDresultCount > 0):
            print('record available.......')
            cursor = cnx.cursor()
            print(cursor)
            cursor.execute(queryUpdate, argsUpdate)
            cnx.commit()
            print('successfuly updated')
        else:
            print('record not available....')
            cursor = cnx.cursor()
            cursor.execute(queryInsert, argsInsert)
            cnx.commit()
            cursor.close()
            print('successfuly inserted')
            # ***********************

        myResult = 1

        # except Error as e:
        # print('Error:', e)
        # myResult=0

        # finally:
        cnx.close()
        return myResult



#MySql Connection
    connection=mysql.connector.connect(host='localhost',
                                    database='sampath_project_4',
                                    user='root',
                                    password='password')


    sql_branch_key="select branch_id from branch"


    cursor=connection.cursor()
    cursor.execute(sql_branch_key)
    records=cursor.fetchall()



    for branchId in range(1,len(records)):
        tmpDate=date_generated
        tmpDate = tmpDate.strftime("%Y-%m-%d")
        calculateDE(df_DE, branchId, tmpDate)
        CalculteMinValue(df2, branchId, tmpDate)


else:
    print("error")


cursor.close()
connection.close()


