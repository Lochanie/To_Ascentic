import pandas as pd
import mysql.connector as mysql
import numpy as np
import HHIMS_logging
import HHIMS_DB_Conn 
import HHIMS_Agg


def Fetch_Data(db_connection,Catergory,PDHS,RDHS,Hospital):

    try:

    
        df_1=pd.read_sql("select DATE(CreateDate) as Date, DATE_FORMAT(CreateDate,'%H:00:00') as Hour,COUNT(PID) as patient_Count from patient where DATE(CreateDate) between '2020-01-01' and '2021-08-30'  GROUP BY DATE(CreateDate),Hour(CreateDate)",db_connection)
        df_1['Catergory']=Catergory
        df_1['PDHS']=PDHS
        df_1['RDHS']=RDHS
        df_1['Hospital']=Hospital
        df_new_1=pd.DataFrame(df_1,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','patient_Count'])
        df_new_1=df_new_1.replace(np.nan,0)


        df_2=pd.read_sql("select DATE(AdmissionDate) as Date, DATE_FORMAT(AdmissionDate,'%H:00:00') as Hour,COUNT(PID) as admission_Count from admission where DATE(AdmissionDate) between '2020-01-01' and '2021-08-30'  GROUP BY DATE(AdmissionDate),HOUR(AdmissionDate)",db_connection)
        df_2['Catergory']=Catergory
        df_2['PDHS']=PDHS
        df_2['RDHS']=RDHS
        df_2['Hospital']=Hospital
        df_new_2=pd.DataFrame(df_2,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','admission_Count'])
        df_new_2.replace('',np.nan,inplace=True)
        df_new_2.replace(np.nan,0,inplace=True)


        df_3=pd.read_sql("select DATE(DateTimeOfVisit) as Date,HOUR(DateTimeOfVisit,'%H:00:00') as Hour,COUNT(PID) as clinic_visits_count from clinic_visits where DATE(DateTimeOfVisit) between '2020-01-01' and '2021-08-30'  GROUP BY DATE(DateTimeOfVisit),HOUR(DateTimeOfVisit)",db_connection)
        df_3['Catergory']=Catergory
        df_3['PDHS']=PDHS
        df_3['RDHS']=RDHS
        df_3['Hospital']=Hospital
        df_new_3=pd.DataFrame(df_3,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','clinic_visits_count'])
        df_new_3.replace('',np.nan,inplace=True)
        df_new_3.replace(np.nan,0,inplace=True)

        df_4=pd.read_sql("select DATE(CreateDate),HOUR(CreateDate,'%H:00:00')as Hour,COUNT(LAB_ORDER_ID) as Lab_Order_count from lab_order where DATE(CreateDate) between '2020-01-01' and '2021-08-30' and Status='Available'  GROUP BY DATE(CreateDate),HOUR(CreateDate)",db_connection)
        df_4['Catergory']=Catergory
        df_4['PDHS']=PDHS
        df_4['RDHS']=RDHS
        df_4['Hospital']=Hospital
        df_new_4=pd.DataFrame(df_4,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','Lab_Order_count'])
        df_new_4.replace('',np.nan,inplace=True)
        df_new_4.replace(np.nan,0,inplace=True)


        df_5=pd.read_sql("select DATE(CreateDate) as Date,HOUR(CreateDate,'%H:00:00') as Hour,COUNT(LAB_ORDER_ID) as Lab_test_count from lab_order where DATE(CreateDate) between '2020-01-01' and '2021-08-30'  GROUP BY DATE(CreateDate),HOUR(CreateDate)",db_connection)
        df_5['Catergory']=Catergory
        df_5['PDHS']=PDHS
        df_5['RDHS']=RDHS
        df_5['Hospital']=Hospital
        df_new_5=pd.DataFrame(df_5,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','Lab_Order_count'])
        df_new_5.replace('',np.nan,inplace=True)
        df_new_5.replace(np.nan,0,inplace=True)
        
        
        df_6=pd.read_sql("select DATE(CreateDate) as Date,Hour(CreateDate,'%H:00:00') as Hour,COUNT(OPDTREATMENTID) as OPD_Treatment_count from opd_treatment where DATE(CreateDate) between '2020-01-01' and '2021-08-30'  GROUP BY DATE(CreateDate),HOUR(CreateDate)",db_connection)
        df_6['Catergory']=Catergory
        df_6['PDHS']=PDHS
        df_6['RDHS']=RDHS
        df_6['Hospital']=Hospital
        df_new_6=pd.DataFrame(df_6,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','Lab_Order_count'])
        df_new_6.replace('',np.nan,inplace=True)
        df_new_6.replace(np.nan,0,inplace=True)
        
        df_7=pd.read_sql("select DATE(DateTimeOfVisit) as Date,Hour(DateTimeOfVisit,'%H:00:00') as Hour,COUNT(PID) as OPD_Visit_count from opd_visits where DATE(DateTimeOfVisit) between '2020-01-01' and '2021-08-30'  GROUP BY DATE(DateTimeOfVisit),HOUR(DateTimeOfVisit)",db_connection)
        df_7['Catergory']=Catergory
        df_7['PDHS']=PDHS
        df_7['RDHS']=RDHS
        df_7['Hospital']=Hospital
        df_new_7=pd.DataFrame(df_7,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','Lab_Order_count'])
        df_new_7.replace('',np.nan,inplace=True)
        df_new_7.replace(np.nan,0,inplace=True)
        
        
        df_8=pd.read_sql("select DATE(CreateDate) as Date,Hour(CreateDate,'%H:00:00') as Hour,COUNT(patient_injection_id) as Vaccination_count from patient_injection where DATE(CreateDate) between '2020-01-01' and '2021-08-30' GROUP BY DATE(CreateDate),HOUR(CreateDate)",db_connection)
        df_8['Catergory']=Catergory
        df_8['PDHS']=PDHS
        df_8['RDHS']=RDHS
        df_8['Hospital']=Hospital
        df_new_8=pd.DataFrame(df_8,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','Lab_Order_count'])
        df_new_8.replace('',np.nan,inplace=True)
        df_new_8.replace(np.nan,0,inplace=True)
        
        df_9=pd.read_sql("select DATE(CreateDate) as Date,Hour(CreateDate,'%H:00:00') as Hour,COUNT(NOTIFICATION_ID) as N_Disease_count from notification where DATE(CreateDate) between '2020-01-01' and '2021-08-30'  GROUP BY DATE(CreateDate),HOUR(CreateDate)",db_connection)
        df_9['Catergory']=Catergory
        df_9['PDHS']=PDHS
        df_9['RDHS']=RDHS
        df_9['Hospital']=Hospital
        df_new_9=pd.DataFrame(df_9,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','Lab_Order_count'])
        df_new_9.replace('',np.nan,inplace=True)
        df_new_9.replace(np.nan,0,inplace=True)
        
        
        df_10=pd.read_sql("select DATE(CreateDate) as Date,Hour(CreateDate,'%H:00:00') as Hour,COUNT(ECGID) as ECG_count from ecg where DATE(CreateDate) between '2020-01-01' and '2021-08-30' GROUP BY DATE(CreateDate),HOUR(CreateDate)",db_connection)
        df_10['Catergory']=Catergory
        df_10['PDHS']=PDHS
        df_10['RDHS']=RDHS
        df_10['Hospital']=Hospital
        df_new_10=pd.DataFrame(df_10,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','Lab_Order_count'])
        df_new_10.replace('',np.nan,inplace=True)
        df_new_10.replace(np.nan,0,inplace=True)
        
        
        df_11=pd.read_sql("select DATE(CreateDate) as Date,Hour(CreateDate,'%H:00:00')as Hour,COUNT(did) as DICOM_count from dicom where DATE(CreateDate) between '2020-01-01' and '2021-08-30'  GROUP BY DATE(CreateDate),HOUR(CreateDate)",db_connection)
        df_11['Catergory']=Catergory
        df_11['PDHS']=PDHS
        df_11['RDHS']=RDHS
        df_11['Hospital']=Hospital
        df_new_11=pd.DataFrame(df_11,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','Lab_Order_count'])
        df_new_11.replace('',np.nan,inplace=True)
        df_new_11.replace(np.nan,0,inplace=True)
        
        
        df_11=pd.read_sql("select DATE(Order_Date) as Date,Hour(Order_Date,'%H:00:00')as Hour,COUNT(PID) as DICOM_Order_count from Dicom_Order where DATE(Order_Date) between '2020-01-01' and '2021-08-30'  GROUP BY DATE(Order_Date),HOUR(Order_Date)",db_connection)
        df_11['Catergory']=Catergory
        df_11['PDHS']=PDHS
        df_11['RDHS']=RDHS
        df_11['Hospital']=Hospital
        df_new_11=pd.DataFrame(df_11,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','Lab_Order_count'])
        df_new_11.replace('',np.nan,inplace=True)
        df_new_11.replace(np.nan,0,inplace=True)
        
        #df_NHSL['Admission_Prescription_count']=pd.read_sql("select COUNT(admission_prescription_id) as Admission_Prescription_count from admission_prescription where DATE(PrescribeDate) between '2020-01-01' and '2021-08-30'  GROUP BY DATE(PrescribeDate),HOUR(PrescribeDate)",db_connection)
        #df_NHSL['Admission_Prescription_Dispense_count']=pd.read_sql("select COUNT(admission_prescription_id) as Admission_Prescription_Dispense_count from admission_prescription where DATE(PrescribeDate) between '2020-01-01' and '2021-08-30' and Status='Open'  GROUP BY DATE(PrescribeDate),HOUR(PrescribeDate)",db_connection)
        df_12=pd.read_sql("select DATE(PrescribeDate)as Date,Hour(PrescribeDate,'%H:00:00') as Hour,COUNT(PRSID) as OPD_Prescription_count from opd_presciption where DATE(PrescribeDate) between '2020-01-01' and '2021-08-30' GROUP BY DATE(PrescribeDate),HOUR(PrescribeDate)",db_connection)
        df_12['Catergory']=Catergory
        df_12['PDHS']=PDHS
        df_12['RDHS']=RDHS
        df_12['Hospital']=Hospital
        df_new_12=pd.DataFrame(df_12,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','Lab_Order_count'])
        df_new_12.replace('',np.nan,inplace=True)
        df_new_12.replace(np.nan,0,inplace=True)
        
        
        df_13=pd.read_sql("select DATE(PrescribeDate) as Date,Hour(PrescribeDate,'%H:00:00') as Hour,COUNT(PRSID) as OPD_Prescription_Dispense_count from opd_presciption where DATE(PrescribeDate) between '2020-01-01' and '2021-08-30' and Status=' Dispensed'  GROUP BY DATE(PrescribeDate),HOUR(PrescribeDate)",db_connection)
        df_13['Catergory']=Catergory
        df_13['PDHS']=PDHS
        df_13['RDHS']=RDHS
        df_13['Hospital']=Hospital
        df_new_13=pd.DataFrame(df_13,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','Lab_Order_count'])
        df_new_13.replace('',np.nan,inplace=True)
        df_new_13.replace(np.nan,0,inplace=True)
        
        df_14=pd.read_sql("select DATE(PrescribeDate) as Date,Hour(PrescribeDate,'%H:00:00') as Hour,COUNT(PRSID) as OPD_Prescription_Pending_count from opd_presciption where DATE(PrescribeDate) between '2020-01-01' and '2021-08-30' and Status='Pending'  GROUP BY DATE(PrescribeDate),HOUR(PrescribeDate)",db_connection)
        df_14['Catergory']=Catergory
        df_14['PDHS']=PDHS
        df_14['RDHS']=RDHS
        df_14['Hospital']=Hospital
        df_new_14=pd.DataFrame(df_14,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','Lab_Order_count'])
        df_new_14.replace('',np.nan,inplace=True)
        df_new_14.replace(np.nan,0,inplace=True)
        
        df_15=pd.read_sql("select DATE(PrescribeDate) as Date,Hour(PrescribeDate,'%H:00:00') as Hour,COUNT(clinic_prescription_id) as Clinic_Prescription_count from clinic_prescription where DATE(PrescribeDate) between '2020-01-01' and '2021-08-30' GROUP BY DATE(PrescribeDate),HOUR(PrescribeDate)",db_connection)
        df_15['Catergory']=Catergory
        df_15['PDHS']=PDHS
        df_15['RDHS']=RDHS
        df_15['Hospital']=Hospital
        df_new_15=pd.DataFrame(df_15,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','Lab_Order_count'])
        df_new_15.replace('',np.nan,inplace=True)
        df_new_15.replace(np.nan,0,inplace=True)
        
        df_16=pd.read_sql("select DATE(PrescribeDate) as Date,Hour(PrescribeDate,'%H:00:00') as Hour,COUNT(clinic_prescription_id) as Clinic_Prescription_Dispense_count from clinic_prescription where DATE(PrescribeDate) between '2020-01-01' and '2021-08-30' and Status=' Dispensed'  GROUP BY DATE(PrescribeDate),HOUR(PrescribeDate)",db_connection)
        df_16['Catergory']=Catergory
        df_16['PDHS']=PDHS
        df_16['RDHS']=RDHS
        df_16['Hospital']=Hospital
        df_new_16=pd.DataFrame(df_16,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','Lab_Order_count'])
        df_new_16.replace('',np.nan,inplace=True)
        df_new_16.replace(np.nan,0,inplace=True)
        
        df_17=pd.read_sql("select DATE(PrescribeDate) as Date,Hour(PrescribeDate,'%H:00:00')as Hour,COUNT(clinic_prescription_id) as Clinic_Prescription_Pending_count from clinic_prescription where DATE(PrescribeDate) between '2020-01-01' and '2021-08-30' and Status='Pending'  GROUP BY DATE(PrescribeDate),HOUR(PrescribeDate)",db_connection)
        df_17['Catergory']=Catergory
        df_17['PDHS']=PDHS
        df_17['RDHS']=RDHS
        df_17['Hospital']=Hospital
        df_new_17=pd.DataFrame(df_17,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','Lab_Order_count'])
        df_new_17.replace('',np.nan,inplace=True)
        df_new_17.replace(np.nan,0,inplace=True)
        
        
        #df_NHSL['Catergory']=Catergory
        #df_NHSL['PDHS']=PDHS
        #df_NHSL['RDHS']=RDHS
        #df_NHSL['Hospital']=Hospital

        #df_NHSL=df_NHSL.replace(np.nan,0)
        #df_new=pd.DataFrame(df_NHSL,columns=['Catergory','PDHS','RDHS','Hospital','Date','Hour','patient_Count','admission_Count','clinic_visits_count','Lab_Order_count','Lab test_count','OPD_Treatment_count','OPD_Visit_count','Vaccination_count','N_Disease_count','ECG_count','DICOM_count','DICOM_Order_count','OPD_Prescription_count','OPD_Prescription_Dispense_count','OPD_Prescription_Pending_count','Clinic_Prescription_count','Clinic_Prescription_Dispense_count','Clinic_Prescription_Pending_count'])

        print(df_new.head(10))
        #df_new.to_csv('test.csv')
        HHIMS_Agg.Aggregate_DF(df_new_1,df_new_2,df_new_3,df_new_4,df_new_5,df_new_6,df_new_7,df_new_8,df_new_9,df_new_10,df_new_11,df_new_12,df_new_13,df_new_14,df_new_15,df_new_16,df_new_17)


        
   
       

    except Exception as e:
        HHIMS_logging.logger.error(e)
