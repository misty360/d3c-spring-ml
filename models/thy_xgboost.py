import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

#Load dataset and get data info
df = pd.read_csv('master_data_set.csv')
df.head()
# df.shape
#df.describe()
# df.info()


# 1. Preprocessing the data




# Convert boolean columns to integers (0, 1)
df['visa_status'] = df['visa_status'].astype(int)
df['activism_status'] = df['activism_status'].astype(int)




#list of universties and countries
original_universities_list = df['universities'].unique().tolist()
original_countries_list = df['countries'].unique().tolist()


# Encoding categorical columns using unique LabelEncoder for universties adn countries
uni_encoder = LabelEncoder()
df['universities'] = uni_encoder.fit_transform(df['universities'])
country_encoder = LabelEncoder()
df['countries'] = country_encoder.fit_transform(df['countries'])




# First clean any whitespace and make uppercase for consistency
df['deported'] = df['deported'].astype(str).str.strip().str.upper()
# Map values safely
df['deported'] = df['deported'].map({'YES': 1, 'NO': 0})
# Drop rows where mapping failed (i.e., unexpected or missing values)
df = df.dropna(subset=['deported'])




# Now it's safe to convert to int
df['deported'] = df['deported'].astype(int)




# Drop unused or non-feature columns
df = df.drop(columns=['student_id', 'source_url'])




# Features (X) and target (y)
X = df[['universities', 'countries', 'visa_status', 'activism_status']]
y = df['deported'].astype(int)  # Make sure it's 0/1




# 2. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)




# 3. Train an XGBoost model
model = xgb.XGBClassifier(eval_metric='logloss')
model.fit(X_train, y_train)

# Save the trained model and encoders
joblib.dump(model, "xgb_model.pkl")
joblib.dump(uni_encoder, "uni_encoder.pkl")
joblib.dump(country_encoder, "country_encoder.pkl")

# 4. Plot feature importance
xgb.plot_importance(model, importance_type="weight", title="Feature Importance", height=0.8)
plt.savefig("feature_importance_plot.png")




#calculate and display accruacy score
preds = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))




#input
uni_input = input("Enter university name: ")
country_input = input("Enter country name: ")
visa_status = int(input("Enter visa status (0 = No, 1 = Yes): "))
activism_status = int(input("Enter activism status (0 = No, 1 = Yes): "))




# Check if values exist in encoder classes
if uni_input not in original_universities_list:
    print(f"Warning: University '{uni_input}' not seen during training.")
elif country_input not in original_countries_list:
    print(f"Warning: Country '{country_input}' not seen during training. ")
else:
    encoded_uni = uni_encoder.transform([uni_input])[0]
    encoded_country = country_encoder.transform([country_input])[0]




    # Create input DataFrame
    input_data = pd.DataFrame([{
        'universities': encoded_uni,
        'countries': encoded_country,
        'visa_status': visa_status,
        'activism_status': activism_status
    }])




    # Predict probability of deportation = 1
    proba = model.predict_proba(input_data)
    deportation_probability = proba[0][1]  # class 1 = deported




    print(f"Predicted probability of deportation: {deportation_probability:.2%}")







