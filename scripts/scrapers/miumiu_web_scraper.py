import pandas as pd
from newspaper import Article

urls = [
    "https://apnews.com/article/international-student-f1-visa-revoked-college-f12320b435b6bf9cf723f1e8eb8c67ae#",
    "https://www.justsecurity.org/109069/u-s-ai-driven-catch-and-revoke-initiative-threatens-first-amendment-rights/", 
    "https://sahanjournal.com/education/international-students-data-collection-ice-arrests/",
    "https://www.bbc.com/news/articles/c20xq5nd8jeo",
    "https://www.insidehighered.com/news/global/international-students-us/2025/05/16/ice-warns-international-students-more-sevis",
    "https://apnews.com/article/international-student-status-restored-9e8a7cb90f4193ec52bf06edc5094cd9",
    "https://www.pbs.org/newshour/nation/international-students-stripped-of-legal-status-in-the-u-s-are-piling-up-wins-in-court",
    "https://www.bbc.com/news/articles/cgm8ekk173zo",
    "https://www.dhs.gov/news/2025/04/30/100-days-fighting-fake-news",
    "https://www.dhs.gov/news/2025/04/30/100-days-fighting-fake-news",
    "https://www.pbs.org/newshour/politics/visa-cancellations-and-deportations-sow-panic-for-international-students",
    "https://pennstatelaw.psu.edu/sites/default/files/FAQ-Understanding-Recent-International-Student-Visa-Revocations-and-Apprehensions_-Guidance-for-Colleges-Universities.pdf",
    "https://www.nafsa.org/ie-magazine/students-at-risk",
    "https://www.presidentsalliance.org/understanding-recent-international-student-visa-revocations-and-sevis-terminations/",
    "https://www.acenet.edu/News-Room/Pages/ACE-Assns-Demand-Answers-Visa-Revocations.aspx",
    "https://www.wusa9.com/article/news/nation-world/us-government-expands-grounds-canceling-international-students-legal-status/507-e12fe15f-2f73-4d04-aa0e-dfb2404b952f",
    "https://www.ice.gov/news/releases/ice-releases-2022-sevp-annual-report",
    "https://www.migrationpolicy.org/article/trump-2-immigration-first-100-days"
    
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
