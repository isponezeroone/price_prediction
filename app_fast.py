import pandas as pd
import pickle
import numpy as np
from preproccessing import valid_prep
from fastapi import FastAPI
from pydantic import BaseModel

class FlatFeatures(BaseModel):
    Тип_квартиры: str
    Район: str
    Адрес: str
    Этаж: str
    о: float
    ж: float
    к: float

class PredictPriceResponse(BaseModel):
    price: float

with open('model.pickle', 'rb') as f_model:
	model = pickle.load(f_model)
with open('scaler.pickle', 'rb') as g:
	scaler = pickle.load(g)
	
app = FastAPI()


@app.post("/predict_price/", response_model=PredictPriceResponse)
def predict_price(flat_features: FlatFeatures):
	df = pd.DataFrame(
        {
            'Тип квартиры': [flat_features.Тип_квартиры],
            'Район': [flat_features.Район],
            'Адрес': [flat_features.Адрес],
            'Этаж': [flat_features.Этаж],
            'o': [flat_features.о],
            'ж': [flat_features.ж],
            'к': [flat_features.к],
        }
    )
	columns_name=pd.read_json('columns_name.json')
	columns_list=list(columns_name.columns)
	df=valid_prep(df)
	df=pd.get_dummies(data=df,columns=['Тип квартиры','Район','Этаж'], dummy_na=False)
	df=df.reset_index(drop=True)   
	df_end=pd.DataFrame(np.nan,columns=columns_list,index=range(len(df)))
	df_end.update(df)
	df_end.fillna(0,inplace=True)
	df_end=scaler.transform(df_end) 
	my_pred=model.predict(df_end)

	return PredictPriceResponse(price=my_pred)

