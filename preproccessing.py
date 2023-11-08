import pandas as pd
import numpy as np



def valid_prep(df):
      
	df=df.dropna()
	
	df['Тип квартиры']=df['Тип квартиры'].str.extract(r'(\w{1,}\b)')
	df['Район']=df['Район'].str.extract(r'(\w{1,}\b)')
	df=df.dropna(axis=0, how='any')
	df['Этаж'].replace('', np.nan, inplace=True)
	df['Этаж_1']=df['Этаж'].str.findall(r'\b\d{1,}')
	df.dropna(axis=0, how='any',inplace=True)
	df.reset_index(drop=True,inplace=True)




	for i in np.arange(len(df)):
		if int(df['Этаж_1'].str[0][i])==int(df['Этаж_1'].str[1][i]) and int(df['Этаж_1'].str[0][i])!=1:
			df.loc[i,'Этаж_end']='последний'
		elif int(df['Этаж_1'].str[0][i])==1:
			df.loc[i,'Этаж_end']='первый'
		else:
			df.loc[i,'Этаж_end']='промежуточный'
		
	df.drop(axis=1,columns=['Этаж','Адрес','Этаж_1'],inplace=True)

	    
	df.rename(columns={'Этаж_end':'Этаж'},inplace=True)

	df['o']=pd.to_numeric(df['o'])
	df['ж']=pd.to_numeric(df['ж'])
	df['к']=pd.to_numeric(df['к'])
	return df
