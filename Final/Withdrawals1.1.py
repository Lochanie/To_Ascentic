# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 16:26:13 2020

@author: lochanie

This code is consists with the error logging 
"""


# Import relevant libraries
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
    
Root_dir = os.path.abspath(os.path.join(os.getcwd(),'../../../NDB EJ_1'))
Destination_path='D:/NDB_New/NDB_New'
NDB_New= os.path.dirname(Destination_path)
Source_path = Root_dir
Error_path= r'D:/NDB_New/'




# Error handling functions definitions
def Errors_Save_log(Test_path,e):
    logging.basicConfig(filename=Error_path+'Errors_Save.log',level= logging.DEBUG)
    logger = logging.getLogger()
    logger.error("Exception in TEST_Path {} and Error is {}".format(Test_path,e))
    
    
    
    
def OSERROR_log(e):
    logging.basicConfig(filename=Error_path+'OSERRORs.log',level= logging.DEBUG)
    logger = logging.getLogger()
    logger.error("Exception in Destination Folder_creation and Error is {}".format(e))
    
    
   
    
def Regex_Errors_log(item,e):
    logging.basicConfig(filename=Error_path+'Hashing_Errors.log',level= logging.DEBUG)
    logger = logging.getLogger()
    logger.error("Exception in Hashing Function in file {} and Error is {}".format(item,e))
    
    



# Function Definition for the regex mapping
def Get_RegEx(*args):
    str = args[0]




    switcher={
            #'Application Status' : "Status : (\w+)",
         #'Send Cash Loading Info ' : ".*?Send Cash Loading Info - (\w+).*?AUX NO : ([\w :xA-]+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?",
         #'Get Cash Unit Info' : "(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?(REJC|RETR|BILL) +(---|LKR) +(\d+) +(\d+) +(\d+) +(\d+).*?",
         'Dispense Command Executed' : "Amount +: (\d+).*?Mix +: (\d+).*?(BILL|REJ|RET) +(\d+) +(\d+).*?(BILL|REJ|RET) +(\d+) +(\d+).*?(BILL|REJ|RET) +(\d+) +(\d+).*?(BILL|REJ|RET) +(\d+) +(\d+).*?(BILL|REJ|RET) +(\d+) +(\d+).*?(BILL|REJ|RET) +(\d+) +(\d+)",
         #"Amount +: (\d+).*?Mix +: (\d+).*?" : "Denomination.*? (BILL|REJ|RET) +(\d+) +(\d+).*?(BILL|REJ|RET) +(\d+) +(\d+).*?(BILL|REJ|RET) +(\d+) +(\d+).*?(BILL|REJ|RET) +(\d+) +(\d+).*?(BILL|REJ|RET) +(\d+) +(\d+).*?(BILL|REJ|RET) +(\d+) +(\d+)",


        }
    
    return switcher.get(str,'')


# Function definition for the extraction of relevant information from e- journals

def Extract(*args):
    
    
    journal_id=args[1]
    dirs=args[2]
    New_Amount_List=[]
    item=args[3]
    
    #print(journal_id)
    
    MsgBlock = args[0]
    #print(MsgBlock)
    Ext_Main = re.search('^\[(\d+) (\d+).*?> ([\w -/]+)',MsgBlock)
    
    
    
    if Ext_Main:
        Type = Ext_Main.group(3).strip('- ').split('-')
        
        TS = Ext_Main.group(1) + " " + Ext_Main.group(2) 
        RegEx = Get_RegEx(Type[0])
        #print(TS+'|'+Type[0]+'|')
        
        if RegEx:
            try:
                Para = re.findall(RegEx, MsgBlock)
                #print(Para)
                new_Para=Para[0]
                #print(new_Para)
                
                Transaction_Date,Transaction_Time=CreateDates(Ext_Main)
                #print(date_list)
                
                Amount,Notes_5000n,Notes_1000n,Notes_500n,Notes_100n=CreateAmounts(new_Para)
                #print(Amount_List)
                
                (New_Amount_List.append(dirs),New_Amount_List.append(journal_id),New_Amount_List.append(Transaction_Date),New_Amount_List.append(Transaction_Time),New_Amount_List.append(Amount),New_Amount_List.append(Notes_5000n),New_Amount_List.append(Notes_1000n),New_Amount_List.append(Notes_500n),New_Amount_List.append(Notes_100n))
                
            except Exception as e:
                #print("Exception in REegex : {}".format(e))
                Regex_Errors_log(item,e)
            
    #print("The new_Amount List is : ",New_Amount_List)
    #print("Extraction Done")
    return New_Amount_List



# Function definition for the extraction of dates and time from the e- journals

def CreateDates(Ext_Main):
    
    try:
        date_list=[]
        
        Transaction_Date=''
        Transaction_Time=''
        
        Transaction_Date=Ext_Main.group(1)
        Transaction_Date=Transaction_Date[4:]+"-"+Transaction_Date[2:4]+"-"+Transaction_Date[0:2]
        Transaction_Time=Ext_Main.group(2)
        Transaction_Time=Transaction_Time[0:2]+":"+Transaction_Time[2:4]+":"+Transaction_Time[4:]
        
       
        return Transaction_Date,Transaction_Time
    
    except Exception as e:
        print("Error in date_list : {}".format(e))
        
        

# Function definition for extraction of cash mix details from the e-journals
        
def CreateAmounts(new_Para):
    try:
       
        Amount=''
        Notes_5000n=''
        Notes_1000n=''
        Notes_500n=''
        Notes_100n=''
        
        
        Amount=new_Para[0]
        #print(Amount)
        Notes_5000n=new_Para[10]
        Notes_1000n=new_Para[13]
        Notes_500n=new_Para[16]
        Notes_100n=new_Para[19]
        
        return Amount,Notes_5000n,Notes_1000n,Notes_500n,Notes_100n
    
    except Exception as e:
         print("Error in Amount_list : {}".format(e))
         
         
# Function definition for getting withdrawal details from e-journals
         
def GET_withdrawals(item,dirs,Test_path):
    
    try:
        
        MsgSeperator = "======================================"

        SourceFileName=item
    
        new_List=[]

        with open(SourceFileName,'r') as log:
            Message =""
            journal_id=""
            
            
            for line in log:
                
                try:
                    if '----AUX NO ' in line:
                        
                        if (re.search(r'xx:(.*?)\d{14}\-\d{2}\n', line)) is not None:
                            journal_id = re.findall(r'xx:(.*?)\d{14}\-\d{2}\n', line)[0]
                    
                    
                    if (MsgSeperator in line):
                        
                        Final_List=Extract(Message,journal_id,dirs,item)
                        Message ="" 
                        new_List.append(Final_List)
                        
                        
                        
                    else:
                        Stripline = line.replace("\n", "").strip()
                        Message += Stripline
                        
                except Exception as e:
                    print("Error in lines in log",e)
                    
                    
    except Exception as e:
        print("Error in Source File open",e)
                    
    CreateDataFrame(new_List,Test_path)
    
    
    
# Function Definition for create data frame function
def CreateDataFrame(new_List,Test_path):
    
    try:
        df=pd.DataFrame(new_List,columns=['Branch','Journal_id','Date','Time','Amount','Five_Th','THousand','Five_Hud','Hundred'])
        df.replace('',np.nan,inplace=True)
        df.dropna(how='any',axis=0,inplace=True)
        #print(Test_path)
        #print(df)
        df.to_csv(Test_path,index=False)
    
    except Exception as e:
        print("Exception is :{} in the file : {}".format(e,Test_path))
        
    #FileConcatanate(NDB_New +'/'+dirs,NDB_New +'/'+dirs+'/'+'out'+'.csv')
    
    
    
# Function Definition for File concatenation function
    
def FileConcatanate(indir,outfile,dirs):
    print(indir,outfile)
    os.chdir(indir)  # Set the current working directory to the input directory
    file_list=glob.glob("*.csv")  # Create a list of files

    df_list=[]  # Then stacking a data frames in to a simple python list-to do that first create a empty list
    colnames=['Branch','Journal_id','Date','Time','Amount','Five_Th','THousand','Five_Hud','Hundred']  # put the column names outside the loop which can be insert in to the large file

            # iterate for loop through file_list
    for filename in file_list:
        #print(filename)#once the for loop iterates print the each file name
        df= pd.read_csv(filename,header=None)
        df_list.append(df)  # put each and every filename and insert them into list and append them
        #print(df_list)
    concatDF=pd.concat(df_list,axis=0)  # get the files in the file list and concatenate it to a one data frame
    #print(concatDF)
    concatDF.columns=colnames  # pass the column name list to the object name columns by calling columns method
    #print(concatDF)
    concatDF.to_csv('out'+'.csv',index=None,header=None)
    
    
# Function Definition for get root directory
    
def GETRoot():
   
    
    if not os.path.exists(NDB_New):
        
        try:
            NDB_Withdrawals = os.path.dirname(Destination_path)
            
        except OSError as e:
            #print("OSERROR",e)
            OSERROR_log(e)
    
    #print(Source_path,NDB_New)
    GetDirectories(Source_path,NDB_New)
    
# Function definition for get directory names
    
def GetDirectories(Source_path,NDB_New):
   
    directories=os.listdir(Source_path)
    #print(directories)
    
    for (dirs) in directories:

        current_dir=os.path.abspath(os.path.join(os.getcwd(),Source_path+'/'+dirs))
        

        if not os.path.exists(NDB_New +'/'+dirs):
            try:
                E_Journal_Des_dir=os.makedirs(NDB_New +'/'+dirs)

            except OSError as e:
                #print("OSERROR",e)
                OSERROR_log(e)
        #print(current_dir,dirs,NDB_New)
        GetFiles(current_dir,dirs,NDB_New)
        
        try:
            FileConcatanate(NDB_New +'/'+dirs,NDB_New +'/'+dirs+'/'+'out'+'.csv')
            
        except Exception as e:
            print ("ERROR in FileConcatanate : {}".format(e))
        
# Function definition for get files in a directory
def GetFiles(current_dir,dirs,NDB_New):
    #print(dirs)
    for f in os.walk(current_dir):
            #print(f)

            #print(f[2],type(f[2]))

            #files.append(f[2])

            for file in f[2]:
                
                try:
                    
                #print(file)
                    item=os.path.abspath(os.path.join(current_dir, file))
    
                    #print(item)
    
                    filename, file_extension = os.path.splitext(file)
    
                    Test_path=os.path.join(NDB_New +'/'+dirs+'/',filename+'.csv')
                    
                    #print("item : {}".format(item))
                    #print("Test_path : {}".format(Test_path))
    
                    GET_withdrawals(item,dirs,Test_path)
                    
                except Exception as e:
                    Errors_Save_log(Test_path,e)

# Main function
def main():
    GETRoot()
    
    
main()
