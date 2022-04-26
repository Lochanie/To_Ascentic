import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode


data=pd.read_csv(r'C:\Users\lochanie\Documents\KBSL\SampathBank\Test\log.csv',index_col=None,error_bad_lines=False)

df1=pd.DataFrame(data,columns=['journal_id','error_date','error_start_time','error_type','error_code'])


df1['error_date']=pd.to_datetime(df1['error_date'],dayfirst=True,errors='coerce')

df1['error_date']=pd.to_datetime(df1['error_date'],format='%Y-%m-%d')

df1['error_date']=df1.error_date.dt.strftime('%Y-%m-%d')

cnx=mysql.connector.connect(host='localhost',
                            database='sampath_project_4',
                            user='sandy',
                            password='1234')

sql_select_query="select atm_key,journal_id from atm"
cursor=cnx.cursor()#create a cursor object
cursor.execute(sql_select_query)

result=cursor.fetchall()

df_sql=pd.DataFrame(result)

df_sql.rename(columns={0:'atm_key',1:'journal_id'},inplace=True)
Merged_df=pd.merge(df_sql,df1,on=['journal_id'])


def myQuary(mySqlStr):
    try:
        cnx = mysql.connector.connect(user='sandy', password='1234',
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


def myInsertError(atm_key, error_date, error_start_time, error_type, error_code):
    queryInsert = """ INSERT INTO `errors`
                           (`atm_key_id`,`error_date`,`error_start_time`,`error_type`,`error_code`) VALUES (%s,%s,%s,%s,%s)"""
    print(queryInsert)

    argsInsert = (atm_key, error_date, error_start_time, error_type, error_code)
    print(argsInsert)

    queryUpdate = """ UPDATE errors
                SET  atm_key_id=%s,error_date=%s,error_start_time=%s,error_type=%s,error_code=%s 
                WHERE atm_key_id=%s and error_date=%s """
    print(queryUpdate)

    argsUpdate = (atm_key, error_date, error_start_time, error_type, error_code, atm_key, error_date)
    print(argsUpdate)

    myResult = 0
    # try:
    cnx = mysql.connector.connect(user='sandy', password='1234',
                                  database='sampath_project_4', host='localhost')

    print('***********************')
    myTmpSql = 'select error_start_time,error_type,error_code from errors where atm_key_id="{}" and error_date="{}"'.format(
        atm_key, error_date)
    print(myTmpSql)
    myTDresult, myTDresultCount = myQuary(myTmpSql)

    print(str(myTDresultCount))

    print(str(myTDresult))
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
        print(cursor)
        cursor.execute(queryInsert, argsInsert)
        print('*****************###############')
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


for index,row in Merged_df.iterrows():
    myInsertError(row['atm_key'],row['error_date'],row['error_start_time'],row['error_type'],row['error_code'])

