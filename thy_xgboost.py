import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

#Load dataset and get data info
df = pd.read_csv('extracted_by_person_filtered.csv') 
# df.head()
# df.shape
# df.describe()
# df.info()

# 1. Preprocessing the data
# Target variable 'deportation_risk' (assuming this is 1 since all were deported)
  # You mentioned they have all been deported

# Convert boolean columns to integers (0, 1)
df['visa_status'] = df['visa_status'].astype(int)
df['activism_status'] = df['activism_status'].astype(int)

# Encoding categorical columns using LabelEncoder
label_encoder = LabelEncoder()
df['universities'] = label_encoder.fit_transform(df['universities'])
df['countries'] = label_encoder.fit_transform(df['countries'])
df['source_url'] = label_encoder.fit_transform(df['source_url'].astype(str))

# Drop unused or non-feature columns
df = df.drop(columns=['person_name', 'source_url'])

# Features (X) and target (y)
X = df[['universities', 'countries', 'visa_status']]
y = df['activism_status'].astype(int)  # Make sure it's 0/1

# 2. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Train an XGBoost model
model = xgb.XGBClassifier(eval_metric='logloss')
model.fit(X_train, y_train)

# 4. Plot feature importance
xgb.plot_importance(model, importance_type="weight", title="Feature Importance", height=0.8)
plt.savefig("plot1.png")

# Or using a more detailed bar chart:
feature_importance = model.get_booster().get_score(importance_type='weight')
importance_df = pd.DataFrame.from_dict(feature_importance, orient='index', columns=['Importance'])
importance_df = importance_df.sort_values(by='Importance', ascending=False)

# Plotting detailed feature importance
sns.barplot(x=importance_df['Importance'], y=importance_df.index)
plt.title('Feature Importance from XGBoost Model')
plt.savefig("plot2.png")
