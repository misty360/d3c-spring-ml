import pandas as pd
from newspaper import Article 
import spacy
#import re

#Load the spacy English model for natural language processing
nlp = spacy.load("en_core_web_sm")
#List of urls containing articles to webscrape
urls = ['https://www.cnn.com/2025/03/31/us/what-we-know-college-activists-immigration-hnk/index.html',
        'https://www.aljazeera.com/news/2025/4/18/us-revokes-nearly-1500-student-visas-who-are-the-targets',
        'https://www.insidehighered.com/news/global/international-students-us/2025/04/21/five-key-takeaways-tracking-student-visa',
        'https://www.democratandchronicle.com/story/news/2025/04/17/how-many-student-visas-have-been-revoked-in-ny-under-trump-the-latest/83100642007/'
        ]

#Function to create a csv file with the article url, title, and text
def scrape_urls(urls):
    url_list = []
    title_list = []
    text_list = []

    for url in urls:
        try:
            #Download and parse the articles. Append the url, title, and text to the respective lists
            article = Article(url)
            article.download()
            article.parse()

            url_list.append(url)
            title_list.append(article.title)
            text_list.append(article.text)

        #If the url cannot be opened, print the error message and append "error"
        except Exception as e:
            print("Could not open url:", url)
            url_list.append(url)
            title_list.append("Error")
            text_list.append("")

    #Create a data frame to store the scraped data
    df = pd.DataFrame({
        "url": url_list,
        "title": title_list,
        "text": text_list
    })
    print(df.head())
    df.to_csv("raw_articles.csv", index=False)

#Function to extract the country, university, visa status, and activism status
def extract_info():
    #Read the raw_articles.csv file and load the scraped articles
    df = pd.read_csv("raw_articles.csv")

    universities = []
    countries = []
    visa_status = []
    activism_status = []

    for text in df["text"]:
        doc = nlp(text)
        #Extract organizations with "ORG" and countries/locations with "GPE"
        orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        gpes = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

        #Check for the keywords of visa and activism after converting the text all to lower case as it is case sensitive
        lowercase_text = text.lower()
        visa_status.append("visa" in lowercase_text)
        activism_status.append("activism" in lowercase_text)

        #Store the first university if orgs is not empty
        if orgs:
            universities.append(orgs[0])
        else:
            universities.append("")
        
        #Store the first country if gpes is not empty
        if gpes:
            countries.append(gpes[0])
        else:
            countries.append("")
        
        #universities.append(orgs[0] if orgs else "")
        #countries.append(gpes[0] if gpes else "")
    
    #Add the extracted features to the original data frame and save it in a new csv file called extracted_articles.csv
    df["university"] = universities
    df["country"] = countries
    df["visa_status"] = visa_status
    df["activism_status"] = activism_status
    df.to_csv("extracted_articles.csv", index=False)

scrape_urls(urls)
extract_info()