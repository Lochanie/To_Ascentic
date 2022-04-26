# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from __future__ import print_function
#from os.path import join

import re
import os.path
import os
import pandas as pd
import numpy as np
import logging
#import csv
import glob

cwd=os.getcwd()
print(cwd)
    
Root_dir = os.path.abspath(os.path.join(os.getcwd(),'../../../NDB EJ'))
#Root_dir = os.path.abspath(os.getcwd(),'../../NDB_TEST')
Destination_path='D:/NDB_New_T/NDB_New_T'
NDB_New= os.path.dirname(Destination_path)
Error_path= r'D:/NTB_test3_T1/'




def Errors_Save_log(Test_path,e):
    logging.basicConfig(filename='D:/NDB_New_T/Errors_Save.log',level= logging.DEBUG)
    logger = logging.getLogger()
    logger.error("Exception in TEST_Path {} and Error is {}".format(Test_path,e))
    
    
    
    
def OSERROR_log(e):
    logging.basicConfig(filename='D:/NDB_New_T/OSERRORs.log',level= logging.DEBUG)
    logger = logging.getLogger()
    logger.error("Exception in Destination Folder_creation and Error is {}".format(e))
    
    
   
    
def Regex_Errors_log(item,e):
    logging.basicConfig(filename='D:/NDB_New_T/Hashing_Errors.log',level= logging.DEBUG)
    logger = logging.getLogger()
    logger.error("Exception in Hashing Function in file {} and Error is {}".format(item,e))
    
    
# Function definitions for error handling in file concatenation    
def File_Concatanation_Error(indir,outdir,e):
    logging.basicConfig(filename=Error_path+'File_Concatanation_Errors.log',level= logging.DEBUG)
    logger = logging.getLogger()
   
    logger.error("Directory: {},{},{}".format(indir,outdir,e))



#Function Definition for Regex mapping
def Get_RegEx(*args):
    str = args[0]

    switcher = {
        #'Application Status' : "Status : (\w+)",
        #'Send Cash Loading Info (Get) ' : ".*?Send Cash Loading Info (Get) - (\w+).*?AUX NO : ([\w :xA-]+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?",
        #'Get Cash Unit Info' : "(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?",
        #'Dispense Command Executed' : "Amount +: (\d+).*?Mix +: (\d+).*?(BILL|REJ|RET) +(\d+) +(\d+).*?(BILL|REJ|RET) +(\d+) +(\d+).*?(BILL|REJ|RET) +(\d+) +(\d+).*?(BILL|REJ|RET) +(\d+) +(\d+).*?(BILL|REJ|RET) +(\d+) +(\d+).*?(BILL|REJ|RET) +(\d+) +(\d+)",
         #'Send Cash Loading Info ' :"REJC|RETR|BILL| ---|LKR |.[0-9]{4}.|.[0-9]{3}",
         #'Get Cash Unit Info' :"^\[(\d{2})(\d{2})(\d{4}) (\d{2})(\d{2})(\d{2}).*LKR \| (\d{4}) \| (\d{4}) \| (\d{4}) \| (\d{3}).*LKR \| (\d{4}) \| (\d{4}) \| (\d{4}) \| (\d{3}).*LKR \| (\d{4}) \| (\d{4}) \| (\d{4}) \| (\d{3}).*LKR \| (\d{4}) \| (\d{4}) \| (\d{4}) \| (\d{3}).*",
         #'Cash Loading Info Sending Completed ' :"^\[(\d{2})(\d{2})(\d{4}) (\d{2})(\d{2})(\d{2}).*LKR \| (\d{4}) \| (\d{4}) \| (\d{4}) \| (\d{3}).*LKR \| (\d{4}) \| (\d{4}) \| (\d{4}) \| (\d{3}).*LKR \| (\d{4}) \| (\d{4}) \| (\d{4}) \| (\d{3}).*LKR \| (\d{4}) \| (\d{4}) \| (\d{4}) \| (\d{3}).*",
         'Send Cash Loading Info (Get)' :"^\[.*LKR \| (\d{4}) \| (\d{4}) \| (\d{4}) \| (\d{3}).*LKR \| (\d{4}) \| (\d{4}) \| (\d{4}) \| (\d{3}).*LKR \| (\d{4}) \| (\d{4}) \| (\d{4}) \| (\d{3}).*LKR \| (\d{4}) \| (\d{4}) \| (\d{4}) \| (\d{3}).*",
         #'Close Session' :"^\[.*LKR \| (\d{4}) \| (\d{4}) \| (\d{4}) \| (\d{3}).*LKR \| (\d{4}) \| (\d{4}) \| (\d{4}) \| (\d{3}).*LKR \| (\d{4}) \| (\d{4}) \| (\d{4}) \| (\d{3}).*LKR \| (\d{4}) \| (\d{4}) \| (\d{4}) \| (\d{3}).*",
        
        
        


        }


    return switcher.get(str,'')


#Function definition for data extraction
def Extract(*args):
    
    
    journal_id=args[1]
    dirs=args[2]
    New_Amount_List=[]
    Status=''
    item=args[3]
    
    #print(journal_id)
    
    MsgBlock = args[0]
    #print(MsgBlock)
    Ext_Main = re.search('^\[(\d+) (\d+).*?> ([\w -/]+)',MsgBlock)
    
    
    
    if Ext_Main:
        Type = Ext_Main.group(3).strip('- ').split('-')
        Status=Type[0]
        print(Type[0])
        
        TS = Ext_Main.group(1) + " " + Ext_Main.group(2) 
        RegEx = Get_RegEx(Type[0])
        #print(TS+'|'+Type[0]+'|')
        print(RegEx)
        
        if RegEx:
            try:
                Para = re.findall(RegEx, MsgBlock)
                print('Para is: ',Para)
                new_Para=Para[0]
                print(new_Para)
                
                Transaction_Date,Transaction_Time=CreateDates(Ext_Main)
                #print(date_list)
                
                Notes_5000n,Notes_5000_Initial,Notes_5000_Accepted,Notes_5000_Status,Notes_1000n,Notes_1000_Initial,Notes_1000_Accepted,Notes_1000_Status,Notes_500n,Notes_500_Initial,Notes_500_Accepted,Notes_500_Status,Notes_100n,Notes_100_Initial,Notes_100_Accepted,Notes_100_Status=CreateAmounts(new_Para)
                #print(Amount_List)
                
                (New_Amount_List.append(dirs),New_Amount_List.append(journal_id),New_Amount_List.append(Transaction_Date),New_Amount_List.append(Transaction_Time),New_Amount_List.append(Status),New_Amount_List.append(Notes_5000n),New_Amount_List.append(Notes_5000_Initial),New_Amount_List.append(Notes_5000_Accepted),New_Amount_List.append(Notes_5000_Status),New_Amount_List.append(Notes_1000n),New_Amount_List.append(Notes_1000_Initial),New_Amount_List.append(Notes_1000_Accepted),New_Amount_List.append(Notes_1000_Status),New_Amount_List.append(Notes_500n),New_Amount_List.append(Notes_500_Initial),New_Amount_List.append(Notes_500_Accepted),New_Amount_List.append(Notes_500_Status),New_Amount_List.append(Notes_100n),New_Amount_List.append(Notes_100_Initial),New_Amount_List.append(Notes_100_Accepted),New_Amount_List.append(Notes_100_Status))
                
            except Exception as e:
                print("Exception in REegex : {}".format(e))
                Regex_Errors_log(item,e)
                #Errors_Save_log(dirs,journal_id,Transaction_Date,Transaction_Time,e)
            
    #print("The new_Amount List is : ",New_Amount_List)
    #print("Extraction Done")
    return New_Amount_List



#Function definition for date extraction 
def CreateDates(Ext_Main):
    
    try:
        
        
        Transaction_Date=''
        Transaction_Time=''
        
        Transaction_Date=Ext_Main.group(1)
        Transaction_Date=Transaction_Date[4:]+"-"+Transaction_Date[2:4]+"-"+Transaction_Date[0:2]
        Transaction_Time=Ext_Main.group(2)
        Transaction_Time=Transaction_Time[0:2]+":"+Transaction_Time[2:4]+":"+Transaction_Time[4:]
        
       
        return Transaction_Date,Transaction_Time
    
    except Exception as e:
        print("Error in date_list : {}".format(e))



#Function definition for amount extraction
def CreateAmounts(new_Para):
    try:
        
        Notes_5000n=''
        Notes_5000_Initial=''
        Notes_5000_Accepted=''
        Notes_5000_Status=''

        Notes_1000n=''
        Notes_1000_Initial=''
        Notes_1000_Accepted=''
        Notes_1000_Status=''


        Notes_500n=''
        Notes_500_Initial=''
        Notes_500_Accepted=''
        Notes_500_Status=''

        Notes_100n=''
        Notes_100_Initial=''
        Notes_100_Accepted=''
        Notes_100_Status=''
        
        
        Notes_5000n=new_Para[0]


        Notes_5000_Initial=new_Para[1]


        Notes_5000_Accepted=new_Para[2]


        Notes_5000_Status=new_Para[3]



        Notes_1000n=new_Para[4]


        Notes_1000_Initial=new_Para[5]


        Notes_1000_Accepted=new_Para[6]


        Notes_1000_Status=new_Para[7]



        Notes_500n=new_Para[8]


        Notes_500_Initial=new_Para[9]


        Notes_500_Accepted=new_Para[10]


        Notes_500_Status=new_Para[11]


        Notes_100n=new_Para[12]


        Notes_100_Initial=new_Para[13]


        Notes_100_Accepted=new_Para[14]


        Notes_100_Status=new_Para[15]
        
        
        print(Notes_5000n,Notes_5000_Initial,Notes_5000_Accepted,Notes_5000_Status,Notes_1000n,Notes_1000_Initial,Notes_1000_Accepted,Notes_1000_Status,Notes_500n,Notes_500_Initial,Notes_500_Accepted,Notes_500_Status,Notes_100n,Notes_100_Initial,Notes_100_Accepted,Notes_100_Status)

        
        return Notes_5000n,Notes_5000_Initial,Notes_5000_Accepted,Notes_5000_Status,Notes_1000n,Notes_1000_Initial,Notes_1000_Accepted,Notes_1000_Status,Notes_500n,Notes_500_Initial,Notes_500_Accepted,Notes_500_Status,Notes_100n,Notes_100_Initial,Notes_100_Accepted,Notes_100_Status
    
    except Exception as e:
         print("Error in Amount_list : {}".format(e))
         
         

#Function Definition for get replenishments
def GET_Replenishments(item,dirs,Test_path):
    MsgSeperator = "======================================"

    SourceFileName=item
    #print(SourceFileName)
    new_List=[]

    with open(SourceFileName,'r') as log:
        #print(log)
        
        Message =""
        journal_id=""
        
        for line in log:
            #print(line)
            
            if '----AUX NO ' in line:
                
                if (re.search(r'xx:(.*?)\d{14}\-\d{2}\n', line)) is not None:
                    journal_id = re.findall(r'xx:(.*?)\d{14}\-\d{2}\n', line)[0]
                    #print(journal_id)
                    
                    

            if (MsgSeperator in line):
                
                Final_List=Extract(Message,journal_id,dirs,item)
                #print(Final_List)
                Message ="" 
                
                new_List.append(Final_List)
                    
            else:
                
                Stripline = line.replace("\n", "").strip()
                Message += Stripline
        #print("The new list is : ",new_List)
        CreateDataFrame(new_List,Test_path)
        
        
        
#Function Definition for data frame creation        
def CreateDataFrame(new_List,Test_path):
    
    try:
        df=pd.DataFrame(new_List,columns=['Branch','Journal_id','Date','Time','Status','Notes_5000n','Notes_5000_Initial','Notes_5000_Accepted','Notes_5000_Status','Notes_1000n','Notes_1000_Initial','Notes_1000_Accepted','Notes_1000_Status','Notes_500n','Notes_500_Initial','Notes_500_Accepted','Notes_500_Status','Notes_100n','Notes_100_Initial','Notes_100_Accepted','Notes_100_Status'])
       
        df.replace('',np.nan,inplace=True)
        df.dropna(how='any',axis=0,inplace=True)
        #print(df)
        #df[df.Status=='Send Cash Loading Info (Set)']
        df_new=df[df['Notes_5000_Initial']==df['Notes_5000_Accepted']]
        #print(Test_path)
        print("The df_new is",df)
        df_new.to_csv(Test_path,index=False)
       
    
    except Exception as e:
        print("Exception in create data frame is :{} in the file : {}".format(e,Test_path))
        
        
        
#Function Definition for file concatenation        
def FileConcatanate(indir,outfile,dirs):
    print(indir,outfile)
    os.chdir(indir) #Set the current working directory to the input directory
    file_list=glob.glob("*.csv")#Create a list of files

    df_list=[]#Then stacking a data frames in to a simple python list-to do that first create a empty list
    colnames=['Branch','Journal_id','Date','Time','Status','Notes_5000n','Notes_5000_Initial','Notes_5000_Accepted','Notes_5000_Status','Notes_1000n','Notes_1000_Initial','Notes_1000_Accepted','Notes_1000_Status','Notes_500n','Notes_500_Initial','Notes_500_Accepted','Notes_500_Status','Notes_100n','Notes_100_Initial','Notes_100_Accepted','Notes_100_Status']#put the column names outside the loop which can be insert in to the large file

            #iterate for loop through file_list
    for filename in file_list:
        #print(filename)#once the for loop iterates print the each file name
        df= pd.read_csv(filename,header=None)
        df_list.append(df)#put each and every filename and insert them into list and append them
        #print(df_list)
    concatDF=pd.concat(df_list,axis=0)#get the files in the file list and concatenate it to a one data frame
    #print(concatDF)
    concatDF.columns=colnames #pass the column name list to the object name columns by calling columns method
    #print(concatDF)
    concatDF.to_csv('out'+'.csv',index=None,header=None)
    print("Concat DF Done")
    
    
#Get root directory information    
def GETRoot():
    cwd=os.getcwd()
    print(cwd)
    
    Root_dir = os.path.abspath(os.path.join(os.getcwd(),'../../../NDB EJ'))
    #Root_dir = os.path.abspath(os.getcwd(),'../../NDB_TEST')
    Destination_path='D:/NDB_New_T/NDB_New_T'
    NDB_New_T= os.path.dirname(Destination_path)
    
    if not os.path.exists(NDB_New_T):
        
        try:
            NDB_Withdrawals = os.path.dirname(Destination_path)
            
        except OSError as e:
            print("OSERROR",e)
            OSERROR_log(e)
    Source_path = Root_dir
    #print(Source_path,NDB_New)
    GetDirectories(Source_path,NDB_New_T)
    
    
    
    
def GetDirectories(Source_path,NDB_New_T):
   
    directories=os.listdir(Source_path)
    print(directories)
    
    for (dirs) in directories:

        #current_dir=os.path.abspath(os.path.join(os.getcwd(),Source_path+'/'+dirs))
        current_dir=os.path.abspath(Source_path+'/'+dirs)
        

        if not os.path.exists(NDB_New_T +'/'+dirs):
            try:
                E_Journal_Des_dir=os.makedirs(NDB_New_T +'/'+dirs)

            except OSError as e:
                print("OSERROR",e)
                OSERROR_log(e)
        #print(current_dir,dirs,NDB_New)
        
        GetFiles(current_dir,dirs,NDB_New_T)
        
        try:
            if not os.path.exists(NDB_New +'/'+'outfiles'):
                try:
                    os.makedirs(NDB_New +'/'+'outfiles')
                    

                except OSError as e:
                    OSERROR_log(e)
            
            FileConcatanate(NDB_New +'/'+dirs,NDB_New +'/'+'outfiles'+'/'+dirs+'.csv',dirs)
            
        except Exception as e:
            #print ("ERROR in FileConcatanate : {}".format(e))
            File_Concatanation_Error(NDB_New +'/'+dirs,NDB_New +'/'+'outfiles'+'/'+dirs+'.csv',e)
            
            
            
def GetFiles(current_dir,dirs,NDB_New_T):
    #print(dirs)
    for f in os.walk(current_dir):
            #print(f)

            #print(f[2],type(f[2]))

            #files.append(f[2])

            for file in f[2]:
                #print(file)
                item=os.path.abspath(os.path.join(current_dir, file))
                #item=os.path.abspath(current_dir, file)

                #print(item)

                filename, file_extension = os.path.splitext(file)

                Test_path=os.path.join(NDB_New_T +'/'+dirs+'/',filename+'.csv')
                
                #print("item : {}".format(item))
                #print("Test_path : {}".format(Test_path))

                try:
                    GET_Replenishments(item,dirs,Test_path)
                    
                except Exception as e:
                    Errors_Save_log(Test_path,e)
                    
                
                
                
                
                
def main():
    GETRoot()
    
    
    



main()
    
    
    
    
    

    
    
    
    


