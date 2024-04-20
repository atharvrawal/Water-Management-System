import pandas as pd
import matplotlib
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
weather = pd.read_csv("2023-2024.csv",index_col = "datetime")
weather.drop(columns = ["windgust","visibility","winddir","solarenergy","sunrise","sunset","windspeed","sealevelpressure","solarradiation","cloudcover","uvindex","severerisk","description","conditions","icon"],axis = 1,inplace = True)
weather.index = pd.to_datetime(weather.index,format="mixed")
weather["target"] = weather.shift(-1)["precip"]
weather = weather.iloc[:-1,:].copy()
reg = Ridge(alpha = .1)
predictors = ["tempmax","tempmin","dew","humidity","moonphase"]
weather = weather.sort_index()
train = weather.loc[:'31-05-2023']
test = weather.loc['01-06-2023':] 
reg.fit(train[predictors],train["target"])
predictions = reg.predict(test[predictors])
combined = pd.concat([test["target"],pd.Series(predictions, index = test.index)],axis=1)

def create_predictions(predictions,weather, reg):
    train = weather.loc[:'31-05-2023']
    test = weather.loc['01-06-2023':] 
    reg.fit(train[predictors],train["target"])
    predictions = reg.predict(test[predictors])
    error = mean_absolute_error(test["target"],predictions)
    combined = pd.concat([test["target"],pd.Series(predictions, index = test.index)],axis=1)
    combined.columns = ["actual","predictions"]
    return error, combined


print(create_predictions(predictions,weather,reg))
# Function to convert degrees to radians
def degrees_to_radians(degrees):
  return degrees * (pi / 180)
