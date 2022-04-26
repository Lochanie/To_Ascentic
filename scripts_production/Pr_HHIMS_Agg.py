import pandas as pd
#from sqlalchemy import create_engine
import mysql.connection as mysql
import HHIMS_logging
import HHIMS_Fetch



def Aggregate_DF(df):
   

    try:
        #engine = create_engine("mysql://hhimsv3:Pass@235!hhims#word@127.0.0.1/hhims_grafana")
        #con = engine.connect()

        #df.to_sql(con=con, name='hhims_stage',if_exists='append',index=False)

        #con.close()
        HOST='127.0.0.1'
        DATABASE='hhims_grafana'
        USER='grafana_new'
        PASSWORD='Lra234%$Sol*123'

        db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cursor=db_connection.cursor()

        for index,row in df.iterrows():

            sql_insert_query = """ INSERT INTO `hhims_stage`
                           (`Catergory`,`PDHS`,`RDHS`,`Hospital`,`Date`,`Hour`,`patient_Count`,`admission_Count`,`clinic_visits_count`,`Lab_Order_count`,`Lab_test_count`,`OPD_Treatment_count`,`OPD_Visit_count`,`Vaccination_count`,`N_Disease_count`,`ECG_count`,`DICOM_count`,`DICOM_Order_count`,`OPD_Prescription_count`,`OPD_Prescription_Dispense_count`,`OPD_Prescription_Pending_count`,`Clinic_Prescription_count`,`Clinic_Prescription_Dispense_count`,`Clinic_Prescription_Pending_count`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            insert_tuple =(row['Catergory'],row['PDHS'],row['RDHS'],row['Hospital'],row['Date'],row['Hour'],row['patient_Count'],row['admission_Count'],row['clinic_visits_count'],row['Lab_Order_count'],row['Lab_test_count'],row['OPD_Treatment_count'],row['OPD_Visit_count'],row['Vaccination_count'],row['N_Disease_count'],row['ECG_count'],row['DICOM_count'],row['DICOM_Order_count'],row['OPD_Prescription_count'],row['OPD_Prescription_Dispense_count'],row['OPD_Prescription_Pending_count'],row['Clinic_Prescription_count'],row['Clinic_Prescription_Dispense_count'],row['Clinic_Prescription_Pending_count'])
            result  = cursor.execute(sql_insert_query,insert_tuple)
            db_connection.commit()

        db_connection.close()

    
    except Exception as e:
        HHIMS_logging.logger.error(e)

   




