from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression, Ridge , SGDRegressor, Lasso
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.svm import LinearSVR
import pickle


df=pd.read_json('parsed_train_data.json')


X_train, X_test, y_train, y_test = train_test_split(df.loc[:, df.columns != 'цена(т.р.)'], df['цена(т.р.)'], random_state=45, test_size=0.3)

X_test, X_valid, y_test, y_valid = train_test_split(X_test, y_test, random_state=45, test_size=0.1)

scaler=RobustScaler()
scaler.fit(df.loc[:, df.columns != 'цена(т.р.)'])

with open('scaler.pickle', 'wb') as f:
    pickle.dump(scaler, f)


X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)


model=Lasso(alpha=10, random_state=47).fit(X_train_scaled,y_train)


with open('model.pickle', 'wb') as f:
    pickle.dump(model, f)



print("Правильность на тренировочном наборе(кросс-валидация):",(cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='r2')))
print("Правильность на тестовом наборе(кросс-валидация):",(cross_val_score(model, X_test_scaled, y_test, cv=5, scoring='r2')))


print("Правильность на тренировочном наборе: {:.2f}",(model.score(X_train_scaled, y_train)))
print("Правильность на тестовом наборе: {:.2f}".format(model.score(X_test_scaled, y_test)))
