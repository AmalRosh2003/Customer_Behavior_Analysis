import pandas as pd
from sqlalchemy import create_engine

df=pd.read_csv('customer_behav_final.csv')

# print(df.head()) #1st 5 entries
# print()
# print(df.shape) # total entries
# print()
# print(df.info()) # data types
# print()
# print(df.describe()) # statistical summary of numeric columns. TO CONSIDER CATEGORICAL DATA AS WELL USE "include='all' in this function"
# print()
# print(df.isnull().sum()) # total null values
# print(df.head(2))
#print(df.info())

# print(df.isnull().sum())
df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x:x.fillna(x.median()))
"""print(df.isnull().sum())"""

# column names to snake case
df.columns=df.columns.str.lower()             
df.columns=df.columns.str.replace(' ','_')

df.rename({'purchase_amount_(usd)':'purchase_amount'},axis=1,inplace=True)
# print(df.columns)

# age group column
labels=['Young Adult','Adult','Middle Aged','Senior']
df['age_group']=pd.qcut(df['age'],q=4,labels=labels)
# print(df[['age','age_group']])

# print(df['frequency_of_purchases'].unique())
freq_map={
    'Every 2 Weeks':14,
    'Once a Week':7,
    'Every 3 Months':90,
    'Once a Month':30,
    'Once a Year':365

}
#a new column with mapped values denoting each frequencies
df['purchase_frequency_days']=df['frequency_of_purchases'].map(freq_map)

# print((df['discount_applied']==df['promo_code_used']).all())

df.drop('promo_code_used',axis=1,inplace=True)
print(df.columns)

import mysql.connector
from sqlalchemy import engine
from urllib.parse import quote_plus
# mydb=mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='<your database password>',
#     database='cust_shopping_behavior')

# mycursor=mydb.cursor();

username='root'
password=quote_plus('system')
host='localhost'
database='cust_shopping_behavior'
port=3306
engine=create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

table_name='customers'

df.to_sql(table_name,engine,if_exists='replace',index=False)

print(f'data loaded into the {database} successfully')

