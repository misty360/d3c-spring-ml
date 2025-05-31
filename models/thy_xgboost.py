import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OrdinalEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Load dataset
df = pd.read_csv('master_data_set.csv')

# Convert boolean columns to integers
df['visa_status'] = df['visa_status'].astype(int)
df['activism_status'] = df['activism_status'].astype(int)

# Clean and encode target
df['deported'] = df['deported'].astype(str).str.strip().str.upper()
df['deported'] = df['deported'].map({'YES': 1, 'NO': 0})
df = df.dropna(subset=['deported'])
df['deported'] = df['deported'].astype(int)

# Drop unused columns
df = df.drop(columns=['student_id', 'source_url'])

# Use OrdinalEncoder with unknown handling
uni_encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
df[['universities']] = uni_encoder.fit_transform(df[['universities']])

country_encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
df[['countries']] = country_encoder.fit_transform(df[['countries']])

# Features and target
X = df[['universities', 'countries', 'visa_status', 'activism_status']]
y = df['deported']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train XGBoost model
model = xgb.XGBClassifier(eval_metric='logloss')
model.fit(X_train, y_train)

# Save model and encoders
joblib.dump(model, "xgb_model.pkl")
joblib.dump(uni_encoder, "uni_encoder.pkl")
joblib.dump(country_encoder, "country_encoder.pkl")

# Feature importance plot
xgb.plot_importance(model, importance_type="weight", title="Feature Importance", height=0.8)
plt.savefig("feature_importance_plot.png")

# Accuracy
preds = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))

# ------------- Inference Section -------------------

# Load model and encoders for prediction
model = joblib.load("xgb_model.pkl")
uni_encoder = joblib.load("uni_encoder.pkl")
country_encoder = joblib.load("country_encoder.pkl")

# Input
uni_input = input("Enter university name: ")
country_input = input("Enter country name: ")
visa_status = int(input("Enter visa status (0 = No, 1 = Yes): "))
activism_status = int(input("Enter activism status (0 = No, 1 = Yes): "))

# Encode input (OrdinalEncoder handles unseen values as -1)
encoded_uni = uni_encoder.transform([[uni_input]])[0][0]
encoded_country = country_encoder.transform([[country_input]])[0][0]

# Optional warnings for unseen data
if encoded_uni == -1:
    print(f"Note: University '{uni_input}' was not seen during training.")
if encoded_country == -1:
    print(f"Note: Country '{country_input}' was not seen during training.")

# Build input DataFrame
input_data = pd.DataFrame([{
    'universities': encoded_uni,
    'countries': encoded_country,
    'visa_status': visa_status,
    'activism_status': activism_status
}])

# Predict
proba = model.predict_proba(input_data)
deportation_probability = proba[0][1]

print(f"Predicted probability of deportation: {deportation_probability:.2%}")

# Predictions on training set
train_preds = model.predict(X_train)
train_accuracy = accuracy_score(y_train, train_preds)

# Predictions on test set
test_preds = model.predict(X_test)
test_accuracy = accuracy_score(y_test, test_preds)

print(f"Training Accuracy: {train_accuracy:.2%}")
print(f"Testing Accuracy: {test_accuracy:.2%}")

# Optional: Show gap
accuracy_gap = train_accuracy - test_accuracy
print(f"Accuracy Gap: {accuracy_gap:.2%}")