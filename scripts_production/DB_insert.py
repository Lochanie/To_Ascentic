import pandas as pd
import mysql.connector as mysql
from sqlalchemy import create_engine
import numpy as np


#df=pd.read_excel(r'D:/ICTA_2020_08/HHIMS/code/catergory.xlsx',index_col=False)
#df=pd.read_excel(r'D:/ICTA_2020_08/HHIMS/code/PDHS.xlsx')
#df=pd.read_excel(r'D:/ICTA_2020_08/HHIMS/code/RDHS.xlsx')
df=pd.read_excel(r'D:/ICTA_2020_08/HHIMS/code/Hospital 1.xlsx')
#print(df)



engine = create_engine("mysql://root:password@127.0.0.1/hhims")
con = engine.connect()
#df.to_sql(con=con, name='catergory', if_exists='replace')
#df.to_sql(con=con, name='pdhs', if_exists='replace')
#df.to_sql(con=con, name='rdhs', if_exists='replace'
df.to_sql(con=con, name='hospital', if_exists='replace')