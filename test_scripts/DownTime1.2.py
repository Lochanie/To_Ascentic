import regex as re
import pandas as pd
from datetime import datetime
import os
import mysql.connector
from mysql.connector import errorcode,Error



# Define the directory

appPath="/home/KBSL_ATM/dev/rep_extract"
numOfLatestFile=10
folderpath = "/home/KBSL_ATM/log_org/"

dbUser="root"
dbPassword="password"
dbHost="127.0.0.1"
dbName="sampath_project_4"


#read DB config
def dbConfig():
    try:
        dbConfig=pd.read_csv((appPath+"/kbsl_dbConf.csv"),header=0)
    except Exception as e:
        print('db config file reding error....')
        myErrorLog(datetime.now().strftime("%Y-%m-%d %H:%M"),'dbConnfFileRead',str(e))
    else:
        return dbConfig.iloc[0]['hostname'],dbConfig.iloc[0]['username'],dbConfig.iloc[0]['password'],dbConfig.iloc[0]['db']


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
        # print(cursor)
        df = pd.read_sql(mySqlStr, con=cnx)
        # print(df)
        cursor.close()
        cnx.close()
        return df, len(df)


def myInsertTrans(transDate, replenishmentStTime, replenishmentTime, N5000, N1000, N500, N100, Atm_key_id, journal_id):
    queryInsert = "INSERT INTO replenishment(replenishment_date,replenishment_start_time,replenishment_end_time,replenishment_5000N,replenishment_1000N,replenishment_500N,replenishment_100N,atm_key_id,journal_id) " \
                  "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    argsInsert = (transDate, replenishmentStTime, replenishmentTime, N5000, N1000, N500, N100, Atm_key_id, journal_id)

    queryUpdate = """ UPDATE replenishment 
                SET  replenishment_5000N=%s,replenishment_1000N=%s,replenishment_500N=%s,replenishment_100N=%s,replenishment_start_time=%s 
                WHERE replenishment_date=%s and replenishment_end_time=%s and atm_key_id = %s and journal_id=%s """

    argsUpdate = (N5000, N1000, N500, N100, replenishmentStTime, transDate, replenishmentTime, Atm_key_id, journal_id)

    myResult = 0
    try:
        cnx = mysql.connector.connect(user=dbUser, password=dbPassword,
                                      database=dbName, host=dbHost)

        # ***********************
        myTmpSql = 'select * from replenishment where replenishment_date="{}" and replenishment_end_time="{}" and atm_key_id="{}" and journal_id="{}"'.format(
            transDate, replenishmentTime, Atm_key_id, journal_id)
        myTDresult, myTDresultCount = myQuary(myTmpSql)
        # print(str(myTDresultCount))
        if (myTDresultCount > 0):
            print('record available.......')
            cursor = cnx.cursor()
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

    except Error as e:
        print('Error:', e)
        myResult = 0

    finally:

        cnx.close()
        return myResult

def getLogFileName():
    myDay=datetime.now()
    return appPath+'/'+str(myDay.strftime("%Y-%m-%d"))


def getTime():
    myDay=datetime.now()
    return str(myDay.strftime("%d/%m/%y %H:%M"))


def myLog(message,logfile):
    text_file = open(logfile, "a")
    text_file.write("\n%s" % (message))
    text_file.close()



def getFileList(myHome,fileCount):
    data = []
    if(os.path.isdir(myHome)):
        for file in sorted(os.listdir(myHome)):
            if(file.startswith( 'EJournal' )):
                tmpDate=str(file.split('_')[1])
                tmpDate=datetime.strptime(tmpDate,'%d%m%Y')
                tmpDate=tmpDate.strftime('%Y-%m-%d')
                data.append((myHome, file,tmpDate))
    df=pd.DataFrame(data, columns=['Folder', 'File','Date'])
    df=df.sort_values('Date',ascending=False)
    return df.head(fileCount)


folder_checklist_name=getLogFileName()+'_replenish_folder_checklist.txt'
file_checklist_name=getLogFileName()+'_replenish_file_checklist.txt'

myLog(("ranga - "+getTime()),folder_checklist_name)
myLog(("ranga - "+getTime()),file_checklist_name)


file_checklist = [x.rstrip() for x in open(file_checklist_name)]

colNames = ('ATM_Name','ATM_ID','R_Date','R_STime','R_Time''R_5000s','R_1000s','R_500s','R_100s')


masterDF = pd.DataFrame(columns = colNames)

for folderName in os.listdir(folderpath):

    # if not folderName in folder_checklist :
    if True:
        homePath = folderpath + "\\" + folderName

        if (os.path.isdir(homePath)):
            # print('************************************************')
            file_checklist = [x.rstrip() for x in open(file_checklist_name)]
            fileListDf = getFileList(homePath, numOfLatestFile)

            for n in range(0, len(fileListDf)):
                # print('&&&&&&&&&&&&&&&&&&&&&&&&&')

                itemName = fileListDf.iloc[n]['Folder'] + "/" + fileListDf.iloc[n]['File']
                print(itemName)

                if not itemName in file_checklist:
                    # if itemName in file_checklist :
                    # print('********************************************************************')
                    # try:
                    # Loops over each itemName in the path. Joins the path and the itemName
                    # and assigns the value to itemName.
                    # itemName = os.path.join(path, itemName)
                    # print(itemName)
                    data = []
                    # print(data)


                    f = open(itemName)
                    # print(f)
                    s = f.readlines()

                    strtosearch1 = ""
                    for line1 in reversed(s):
                        strtosearch1 += line1

                    ATMkey = re.findall(r'xx:(.*?)\d{14}\-\d{2}\n', strtosearch1, re.DOTALL)[0]
                    print(ATMkey)

                    list1 = re.findall(
                        r'Status : ATM_In_Service.*TTU Back Panel Log Out(.*?)Cash Unit Info - 1 Value 02',
                        strtosearch1, re.DOTALL)

                    # list2 = re.findall(r'Status : ATM_In_ServiceCash Rejected True.*TTU Back Panel Log Out(.*?)User Login Success',strtosearch1,re.DOTALL)
                    list2 = re.findall(r'Status : ATM_In_Service.*Cash Rejected True(.*?)User Login Success',
                                       strtosearch1, re.DOTALL)

                    strtosearch2 = ""
                    for line2 in list1:
                        strtosearch2 += line2

                    strtosearch3 = ""
                    for line3 in list2:
                        strtosearch3 += line3
                        # print(strtosearch3)

                    match1 = bool(
                        re.findall(r"\[\d{8}\s\d{6}\s\d{3}\]\[\d{1}\]\[\bINFO\b\].\W+\bStatus : ATM_Out_Of_Service\b",
                                   strtosearch3, re.DOTALL))
                    match2 = bool(re.findall(r"\[\d{8}\s\d{6}\s\d{3}\]\[\d{1}\]\[\bINFO\b\].\W+\bCash Load Started\b",
                                             strtosearch3, re.DOTALL))
                    match3 = bool(re.findall(r"\[\d{8}\s\d{6}\s\d{3}\]\[\d{1}\]\[\bINFO\b\].\W+\bStart Cash Exchange\b",
                                             strtosearch3, re.DOTALL))
                    match4 = bool(
                        re.findall(r"\[\d{8}\s\d{6}\s\d{3}\]\[\d{1}\]\[\bINFO\b\].\W+\bSafe Door Status : OPEN\b",
                                   strtosearch3, re.DOTALL))

                    if (match1 == True & match2 == True & match3 == True & match4 == True):
                        # print("Conditions are O.K")
                        list3 = re.findall(
                            r"\[\d{8}\s\d{6}\s\d{3}\]\[\d{1}\]\[\bINFO\b\].\W+\bStatus : ATM_Out_Of_Service\b",
                            strtosearch3, re.DOTALL)

                        # list1 = re.findall(r'Status : ATM_In_Service.*TTU Back Panel Log Out(.*?)Cash Unit Info - 1 Value 02',strtosearch3,re.DOTALL)


                        #                         strtosearch2=""
                        #                         for line2 in list1:
                        #                             strtosearch2 += line2



                        strtosearch4 = ""
                        for line4 in list3:
                            strtosearch4 += line4

                        Start_Down_Time = re.findall(r'\s\d{6}', strtosearch4, re.DOTALL)

                        notes5000s = re.findall('Value 03  BILL  LKR  5000\s+(.*?)\s+\d+\s+\d+\s+\w+\n', strtosearch2,
                                                re.DOTALL)
                        notes1000s = re.findall('Value 04  BILL  LKR  1000\s+(.*?)\s+\d+\s+\d+\s+\w+\n', strtosearch2,
                                                re.DOTALL)
                        notes500s = re.findall('Value 05  BILL  LKR  0500\s+(.*?)\s+\d+\s+\d+\s+\w+\n', strtosearch2,
                                               re.DOTALL)
                        notes100s = re.findall('Value 06  BILL  LKR  0100\s+(.*?)\s+\d+\s+\d+\s+\w+\n', strtosearch2,
                                               re.DOTALL)

                        transactionDate = re.findall(
                            r'Cash Unit Info - 5 Value 06  BILL  LKR  0100\s+\d{4}\s+\d{4}\s+\d{3}\s+\w+\n\[(.*?)\s',
                            strtosearch2, re.DOTALL)
                        transactionTime = re.findall(
                            r'Cash Unit Info - 5 Value 06  BILL  LKR  0100\s+\d{4}\s+\d{4}\s+\d{3}\s+\w+\n\[\d{8}\s(.*?)\s',
                            strtosearch2, re.DOTALL)

                        transDate = []
                        transTime = []
                        Start_Down_Time_S = []
                        ATM_name_list = []
                        ATM_key_list = []

                        for time in Start_Down_Time:
                            newTime = "".join(time.split())
                            tmpSTransTime = datetime.strptime(newTime, '%H%M%S').time()
                            Start_Down_Time_S.append(tmpSTransTime)
                            print(tmpSTransTime)

                        for date in transactionDate:
                            #                         #print('{}/{}/{}'. format(str_date[:2], str_date[2:4], str_date[4:]))
                            tmpTransDate = datetime.strptime(date, '%d%m%Y').date()
                            transDate.append(tmpTransDate)

                        for time in transactionTime:
                            # #                         #print('{}:{}:{}'. format(str_time[:2], str_time[2:4], str_time[4:]))
                            tmpTransTime = datetime.strptime(time, '%H%M%S').time()
                            transTime.append(tmpTransTime)
                            #                         #print(tmpTransTime)
                        for i in transactionDate:
                            tmpFolderName = folderName
                            ATM_name_list.append(folderName)

                        for j in transactionDate:
                            tmp_ATM_KEY = ATMkey
                            ATM_key_list.append(ATMkey)

                        tempDF = pd.DataFrame(columns=colNames)

                        tempDF['ATM_Name'] = pd.Series(ATM_name_list)
                        tempDF['ATM_ID'] = pd.Series(ATM_key_list)
                        tempDF['R_Date'] = pd.Series(transDate)
                        tempDF['R_STime'] = pd.Series(Start_Down_Time_S)
                        tempDF['R_Time'] = pd.Series(transTime)
                        tempDF['R_5000s'] = pd.Series(notes5000s)
                        tempDF['R_1000s'] = pd.Series(notes1000s)
                        tempDF['R_500s'] = pd.Series(notes500s)
                        tempDF['R_100s'] = pd.Series(notes100s)

                        for n in range(0, len(tempDF)):
                            print('hi')

                            print(tempDF.iloc[n]['ATM_Name'] + '---' + tempDF.iloc[n]['ATM_ID'] + '---' + str(
                                tempDF.iloc[n]['R_Date']) + '---' + str(tempDF.iloc[n]['R_STime']) + '---' + str(
                                tempDF.iloc[n]['R_Time']) + '----' + tempDF.iloc[n]['R_5000s'] + '--' + tempDF.iloc[n][
                                      'R_1000s'] + '--' + tempDF.iloc[n]['R_500s'] + '--' + tempDF.iloc[n]['R_100s'])

                            # print(tempDF.iloc[n]['R_1000s'])


                            ##################### SEND TO DB ######################

                            myTmpSql = 'select atm_key from atm where journal_id="{}"'.format(tempDF.iloc[n]['ATM_ID'])
                            print(myTmpSql)
                            myResult, myResultCount = myQuary(myTmpSql)
                            print('------------------{}---------------------'.format(n))

                            if (myResultCount > 0):
                                myAtmKey = myResult['atm_key'].values
                                print('Atm key : ' + str(myAtmKey))

                                # transDate,replenishmentTime,N5000,N1000,N500,N100,Atm_key_id,journal_id

                                myResult = myInsertTrans(tempDF.iloc[n]['R_Date'], tempDF.iloc[n]['R_STime'],
                                                         tempDF.iloc[n]['R_Time']
                                                         , int(tempDF.iloc[n]['R_5000s']),
                                                         int(tempDF.iloc[n]['R_1000s']),
                                                         int(tempDF.iloc[n]['R_500s']), int(tempDF.iloc[n]['R_100s']),
                                                         int(myAtmKey), tempDF.iloc[n]['ATM_ID'])
                                print(myResult)

                            else:
                                print('record no available in db')



                        myLog(itemName, file_checklist_name)

                    else:
                        print("Error in Matching")


                    except Exception as exception:

                    print(str(exception))
                    print(itemName)
                    # print(folderName)
                    text_file = open("replenishment_errorLog.txt", "a")
                    text_file.write("Error Folder: %s    Error File: %s" % (folderName, itemName))
                    text_file.write("    Error Statement: %s\n" % str(exception))
                    text_file.close()


                else:
                    print(' bypassed file  --> ' + itemName)

            myLog(folderName, folder_checklist_name)


        else:

            print(' bypassed folder --> ' + folderName)




