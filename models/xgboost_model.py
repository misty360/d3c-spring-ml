#Import dependencies/libraries
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from xgboost import XGBClassifier

import matplotlib.pyplot as plt
import shap

#Load dataset and get data info
df = pd.read_csv("./abirami/extracted_by_person_filtered.csv") 
df.head()
df.shape
df.describe()
df.info()

#Determine input and output columns
x = df[['university', 'country', 'visa status', 'activism score']]
y = df['deportation_risk'] #1 = deported, 0 = not deported

#Convert category words into encoded values
x = pd.get_dummies(x)

#Split data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

#Create XGB model
xgb_model = XGBClassifier(objective='binary:logistic') 

#Use GridSearchCV to find optimal hyperparameters
param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.001, 0.01, 0.1],
    'max_depth': [3, 5, 7],
}
grid_search = GridSearchCV(xgb_model, param_grid, scoring='accuracy', cv=5, n_jobs=-1, verbose=1)
grid_search.fit(x_train, y_train) 
best_model = grid_search.best_estimator_

#Make predictions
y_pred = best_model.predict(x_test)
y_prob = best_model.predict_proba(x_test)[:, 1] 
accuracy = accuracy_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_prob)
r2 = r2_score(y_test, y_prob) 

#Evaluate the model
print("Accuracy: ", accuracy)
print("Mean Squared Error: ", mse)
print("R² Score: ", r2)
print("Optimal parameters: ", grid_search.best_params_)

#Plot probability of deportation
plt.figure(figsize=(10,5))
plt.hist(y_prob, bins=10, color='white', edgecolor='black')
plt.title('XGBoost Model to Predict Deportation Risk')
plt.xlabel('Predicted Deportation Risk')
plt.ylabel('Number of People')
plt.grid(True)
plt.show()

#Use SHAP to determine how much each factor contributed to deportation risk
explanation = shap.Explainer(best_model, x_train)
shap_values = explanation(x_test)
shap.summary_plot(shap_values, x_test)
shap.plots.force(shap_values[0])