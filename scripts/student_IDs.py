import pandas as pd
import hashlib

df = pd.read_csv("scripts/negative_data.csv")

def generate_student_id(name, index):
    return 'S' + hashlib.sha1(f'{name}_{index}'.encode()).hexdigest()[:8]

df['student_id'] = [generate_student_id(name, idx) for idx, name in enumerate(df['person_name'])]
df = df.drop(columns=['person_name'])
df = df[['student_id'] + [col for col in df.columns if col != 'student_id']]

df.to_csv('anonymized_negative.csv', index=False)
