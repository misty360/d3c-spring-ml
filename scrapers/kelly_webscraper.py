import pandas as pd
from newspaper import Article

urls = [
    'https://www.aljazeera.com/amp/news/2025/4/18/us-revokes-nearly-1500-student-visas-who-are-the-targets',
    'https://thepienews.com/data-trumps-student-visa-revocations-in-numbers/',
    'https://www.nafsa.org/reports-of-actions-targeting-international-students',
    'https://www.theguardian.com/us-news/2025/apr/10/how-many-student-visas-revoked'
]

data = []
for url in urls:
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    data.append({
        'Title': article.title,
        'Publish Date': article.publish_date,
        'Keywords': ', '.join(article.keywords),
        'URL': url
    })

df = pd.DataFrame(data)
df.to_csv('articles.csv', index=False)