import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# 1. Load the data
df = pd.read_csv("temporarydata.csv")  # Replace with actual path

# 2. Preprocess
# Drop unnecessary columns
df = df[['universities', 'countries', 'visa_status', 'activism_status', 'deported']]

# Encode categorical features
label_enc_uni = LabelEncoder()
label_enc_ctry = LabelEncoder()

df['universities'] = label_enc_uni.fit_transform(df['universities'].astype(str))
df['countries'] = label_enc_ctry.fit_transform(df['countries'].astype(str))
df['visa_status'] = df['visa_status'].astype(int)
df['activism_status'] = df['activism_status'].astype(int)
df['deported'] = df['deported'].apply(lambda x: 1 if x == 'YES' else 0)

# 3. Define features and target
X = df[['universities', 'countries', 'visa_status', 'activism_status']]
y = df['deported']

# 4. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# 6. Evaluation
y_pred = model.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
