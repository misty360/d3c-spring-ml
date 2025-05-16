import pandas as pd
from newspaper import Article
import spacy

urls = [
    "https://time.com/7272060/international-students-targeted-trump-ice-detention-deport-campus-palestinian-activism/",
    "https://www.nytimes.com/2025/03/27/us/students-trump-ice-detention.html",
    "https://www.aljazeera.com/news/2025/3/27/who-are-the-students-trump-wants-to-deport"
]

data = []

for url in urls:
    try:
        article = Article(url)
        article.download()
        article.parse()
        data.append({'url': url, 'title': article.title, 'text': article.text})
    except Exception as e:
        print(f"Failed to process {url}: {e}")

df = pd.DataFrame(data)

print(df)

nlp = spacy.load("en_core_web_sm")

# Sample text (you can replace this with any article or scraped text)
text = """

# Process the text
doc = nlp(text)

universities = set()
countries = set()
people = set()

for ent in doc.ents:
    if ent.label_ == "ORG" and "University" in ent.text:
        universities.add(ent.text)
    elif ent.label_ == "GPE":
        countries.add(ent.text)
    elif ent.label_ == "PERSON":
        people.add(ent.text)

# Output results
print("ORG (Universities):", universities)
print("GPE (Countries):", countries)
print("PERSON (Names):", people)