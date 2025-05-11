import pandas as pd
from newspaper import Article 
import spacy
import difflib
#import re

#Load the spacy English model for natural language processing
nlp = spacy.load("en_core_web_sm")
#List of urls containing articles to webscraper
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

def is_partial_match(existing_name, new_name):
    # Check if one name is a part of the other OR a close match
    return (
        new_name in existing_name or
        existing_name in new_name or
        difflib.SequenceMatcher(None, existing_name, new_name).ratio() > 0.85
    )

def extract_info():
    df = pd.read_csv("raw_articles.csv")
    rows = {}

    university_keywords = ["university", "college", "institute", "school", "academy"]

    for i, row in df.iterrows():
        text = row["text"]
        url = row["url"]
        doc = nlp(text)

        lowercase_text = text.lower()
        visa_status = "visa" in lowercase_text
        activism_status = "activism" in lowercase_text

        persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        gpes = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

        potential_universities = [org for org in orgs if any(k in org.lower() for k in university_keywords)]

        for sent in doc.sents:
            sentence_persons = [person for person in persons if person in sent.text]
            sentence_universities = [university for university in potential_universities if university in sent.text]
            sentence_gpes = [gpe for gpe in gpes if gpe in sent.text]

            for person in sentence_persons:
                normalized_person = " ".join([part.capitalize() for part in person.split()])
                
                # Check for duplicate or partial match
                matched_name = None
                for existing_name in rows:
                    if is_partial_match(existing_name, normalized_person):
                        matched_name = existing_name
                        break

                person_key = matched_name if matched_name else normalized_person

                if person_key not in rows:
                    rows[person_key] = {
                        "person_name": person_key,
                        "universities": set(),
                        "countries": set(),
                        "visa_status": visa_status,
                        "activism_status": activism_status,
                        "source_url": url
                    }

                rows[person_key]["universities"].update(sentence_universities)
                rows[person_key]["countries"].update(sentence_gpes)
                if visa_status:
                    rows[person_key]["visa_status"] = True
                if activism_status:
                    rows[person_key]["activism_status"] = True
                if url not in rows[person_key]["source_url"]:
                    rows[person_key]["source_url"] += ", " + url

    # Final output
    person_df = pd.DataFrame([
        {
            "person_name": key,
            "universities": ", ".join(sorted(value["universities"])),
            "countries": ", ".join(sorted(value["countries"])),
            "visa_status": value["visa_status"],
            "activism_status": value["activism_status"],
            "source_url": value["source_url"]
        }
        for key, value in rows.items()
    ])
    person_df.to_csv("extracted_by_person_filtered.csv", index=False)

scrape_urls(urls)
extract_info()