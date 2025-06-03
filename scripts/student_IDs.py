import pandas as pd
import hashlib

df = pd.read_csv("updated_extracted_by_person_filtered.csv")

def generate_student_id(name, index):
    return 'S' + hashlib.sha1(f'{name}_{index}'.encode()).hexdigest()[:8]

df['student_id'] = [generate_student_id(name, idx) for idx, name in enumerate(df['person_name'])]
df = df.drop(columns=['person_name'])
df = df[['student_id'] + [col for col in df.columns if col != 'student_id']]

df.to_csv('data/added_positive_data.csv', index=False)
