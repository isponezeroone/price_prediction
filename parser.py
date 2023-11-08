import requests                   #выполняет HTTP-запросы
from bs4 import BeautifulSoup     #работа с HTML
import csv                        #работа с форматом данных CSV
from multiprocessing import Pool  #предоставляет возможность параллельных процессов
import pandas as pd
import numpy as np

df=pd.DataFrame(index=range(30000),columns=['Тип квартиры','Район','Адрес','Этаж','o','ж','к','цена(т.р.)'])

for i in range(30):
    url = f'http://www.citystar.ru/detal.htm?d=43&nm=%CE%E1%FA%FF%E2%EB%E5%ED%E8%FF+%2D+%CF%F0%EE%E4%E0%EC+%EA%E2%E0%F0%F2%E8%F0%F3+%E2+%E3%2E+%CC%E0%E3%ED%E8%F2%EE%E3%EE%F0%F1%EA%E5&pN={i}'
    page = requests.get(url)
    page.encoding = 'cp1251'
    allNews = []
    soup = BeautifulSoup(page.text, "html.parser")
    allNews = soup.findAll('tr', class_='tbb')
    for k in range(int((len(allNews)))):
        try:
            df.iloc[i*k,0]=allNews[k].findAll('td', class_='ttx')[1].text
            df.iloc[i*k,1]=allNews[k].findAll('td', class_='ttx')[2].text
            df.iloc[i*k,2]=allNews[k].findAll('td', class_='ttx')[3].text
            df.iloc[i*k,3]=allNews[k].findAll('td', class_='ttx')[4].text
            df.iloc[i*k,4]=allNews[k].findAll('td', class_='ttx')[5].text
            df.iloc[i*k,5]=allNews[k].findAll('td', class_='ttx')[6].text
            df.iloc[i*k,6]=allNews[k].findAll('td', class_='ttx')[7].text
            df.iloc[i*k,7]=allNews[k].findAll('td', class_='ttx')[9].text
        except:
            pass
        
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

threshold = 0.01
for col in df:
    counts = df['Район'].value_counts(normalize=True)
    df = df.loc[df['Район'].isin(counts[counts > threshold].index), :]
    
df.rename(columns={'Этаж_end':'Этаж'},inplace=True)

df['o']=pd.to_numeric(df['o'])
df['ж']=pd.to_numeric(df['ж'])
df['к']=pd.to_numeric(df['к'])
df['цена(т.р.)']=pd.to_numeric(df['цена(т.р.)'])





df=pd.get_dummies(data=df,columns=['Тип квартиры',\
                                          'Район','Этаж'], dummy_na=False)
                                          


df.iloc[1:2,df.columns != 'цена(т.р.)'].to_json('columns_name.json')

df.iloc[:-3,:].to_json('parsed_train_data.json')
