from flask import Flask, render_template,request
import pandas as pd
import pickle
import numpy as np
from preproccessing import valid_prep

app = Flask(__name__)

     
@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  
    
         
      
@app.route('/predict', methods = ['POST','GET'])
def predict():
	if request.method == 'POST':
		file = request.files['file']
#		file.save(secure_filename(f.filename))
		if file:			
			df=pd.read_json(file.filename)
			df_preproc_columns=df.copy()	
					
			df=valid_prep(df)
			
					
			columns_name=pd.read_json('columns_name.json')
			columns_list=columns_name.columns
			df=pd.get_dummies(data=df,columns=['Тип квартиры','Район','Этаж'], dummy_na=False)
			df=df.reset_index(drop=True)   
			df_end=pd.DataFrame(np.nan,columns=columns_list,index=range(len(df)))
			df_end.update(df)
			df_end.fillna(0,inplace=True)
			df_end=scaler.transform(df_end) 
			my_pred=model.predict(df_end)
	return render_template("predict.html", name = my_pred, o=df_preproc_columns.loc[:,'o'].values,g=df_preproc_columns.loc[:,'ж'].values,  k=df_preproc_columns.loc[:,'к'].values,flat_type=df_preproc_columns.loc[:,'Тип квартиры'].values,flat_dis=df_preproc_columns.loc[:,'Район'].values,flat_floor=df_preproc_columns.loc[:,'Этаж'].values,
	adress=df_preproc_columns.loc[:,'Адрес'].values)


if __name__ == '__main__':
	with open('model.pickle', 'rb') as f_model:
        	model = pickle.load(f_model)
	with open('scaler.pickle', 'rb') as g:
		scaler = pickle.load(g)
	app.run(host='localhost', port=7777,debug=True)
