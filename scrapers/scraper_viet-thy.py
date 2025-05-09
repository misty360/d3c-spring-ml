
import pandas as pd
from newspaper import Article

import nltk
nltk.download('punkt_tab')
# List of article URLs
urls = [
    "https://www.nbcnews.com/news/asian-america/international-students-revoked-visas-reasons-why-rcna200313",  
"https://abcnews.go.com/Politics/foreign-college-students-targeted-deportation/story?id=120210587",  
"https://thepienews.com/applyboard-launches-new-ai-feature-for-student-applications/", 
"https://www.insidehighered.com/news/global/international-students-us/2025/04/21/five-key-takeaways-tracking-student-visa" 

]

articles_data = []

# Loop through each URL and extract info
for url in urls:
    try:
        article = Article(url, language='en')
        article.download()
        article.parse()
        article.nlp()

        articles_data.append({
        "url": url,
        "title": article.title,
        "authors": ", ".join(article.authors),
        "publish_date": article.publish_date,
        "text": article.text,
        "summary": article.summary,
        "keywords": ", ".join(article.keywords)
    })

        print("Title:", article.title)
        print("Authors:", article.authors)
        print("Publish Date:", article.publish_date)
        print("Text:", article.text[:200])  # Preview first 200 characters
        print("Summary:", article.summary)
        print("Keywords:", article.keywords)
    except Exception as e:
        print(f"Failed to scrape {url}. Reason: {e}")


df = pd.DataFrame(articles_data)

df.to_csv('viet-thy_articles.csv', index=False)
