import pandas as pd
from newspaper import Article

urls = [
    "https://apnews.com/article/international-student-f1-visa-revoked-college-f12320b435b6bf9cf723f1e8eb8c67ae#",
    "https://www.justsecurity.org/109069/u-s-ai-driven-catch-and-revoke-initiative-threatens-first-amendment-rights/", 
    "https://sahanjournal.com/education/international-students-data-collection-ice-arrests/",
    "https://www.bbc.com/news/articles/c20xq5nd8jeo"
]

articles_data = []

for idx, url in enumerate(urls):
    try:
        print(f"\n--- Processing URL {idx + 1}: {url} ---")
        article = Article(url)
        article.download()
        article.parse()
        
        articles_data.append({
            'url': url,
            'title': article.title,
            'text': article.text
        })
        
        print(f"Title: {article.title}\n")
        print(f"Text Preview: {article.text[:200]}...\n")
        
    except Exception as e:
        print(f"Error with {url}: {str(e)}")
        articles_data.append({
            'url': url,
            'title': 'FAILED',
            'text': f'Error: {str(e)}'
        })

df = pd.DataFrame(articles_data)
print("\n=== DataFrame Output ===")
print(df)  # This prints the formatted DataFrame to terminal
df.to_csv('raw_articles.csv', index=False)
print("\nCheck 'raw_articles.csv' for full data.")