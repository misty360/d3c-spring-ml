import pandas as pd
from newspaper import Article
import spacy
import difflib
import pycountry

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Valid country names
valid_countries = {country.name for country in pycountry.countries}

# List of university-related keywords
university_keywords = ["university", "college", "institute", "school", "academy"]

# List of URLs
urls = [
    'https://www.cnn.com/2025/03/31/us/what-we-know-college-activists-immigration-hnk/index.html',
    'https://www.aljazeera.com/news/2025/4/18/us-revokes-nearly-1500-student-visas-who-are-the-targets',
    'https://www.insidehighered.com/news/global/international-students-us/2025/04/21/five-key-takeaways-tracking-student-visa',
    'https://www.democratandchronicle.com/story/news/2025/04/17/how-many-student-visas-have-been-revoked-in-ny-under-trump-the-latest/83100642007/',
    'https://time.com/7272060/international-students-targeted-trump-ice-detention-deport-campus-palestinian-activism/',
    'https://www.nytimes.com/2025/03/27/us/students-trump-ice-detention.html',
    'https://www.nbcnews.com/news/asian-america/international-students-revoked-visas-reasons-why-rcna200313',
    'https://abcnews.go.com/Politics/foreign-college-students-targeted-deportation/story?id=120210587',
    'https://thepienews.com/applyboard-launches-new-ai-feature-for-student-applications/',
    'https://www.justsecurity.org/109069/u-s-ai-driven-catch-and-revoke-initiative-threatens-first-amendment-rights/',
    'https://sahanjournal.com/education/international-students-data-collection-ice-arrests/',
    'https://www.bbc.com/news/articles/c20xq5nd8jeo',
    'https://www.nafsa.org/reports-of-actions-targeting-international-students',
    'https://www.theguardian.com/us-news/2025/apr/10/how-many-student-visas-revoked',
    'https://www.usatoday.com/story/graphics/2025/05/03/how-many-international-students-visas-revoked/83216625007/',
    'https://www.news-leader.com/story/news/education/2025/04/15/missouri-state-university-international-student-visas-revoked/83096413007/',
    'https://capitolnewsillinois.com/news/chilling-silence-waves-of-illinois-international-university-students-lose-their-visas/',
    'https://www.insidehighered.com/news/global/international-students-us/2025/04/07/where-students-have-had-their-visas-revoked',
    'https://en.wikipedia.org/wiki/Catch_and_Revoke',
    'https://www.nbcbayarea.com/news/local/student-visas-revoked-bay-area/3839632/',
    'https://time.com/7284578/judge-orders-release-of-rumeysa-ozturk-tuft-student-detained-by-ice/',
    'https://abc7news.com/post/dept-homeland-security-revokes-visas-uc-berkeley-stanford-international-students-tied-past-activism/16136682/',
    'https://www.insidehighered.com/news/global/international-students-us/2025/04/07/where-students-have-had-their-visas-revoked',
    'https://eccunion.com/news/2025/04/23/international-students-f-1-visa-revoked-at-el-camino/',
    'https://timesofindia.indiatimes.com/world/us/warning-shot-over-political-activism-by-foreign-students-on-us-campuses-after-chinese-scholars-visa-is-revoked/articleshow/118814657.cms',
    'https://www.washingtonpost.com/nation/2024/05/03/international-students-campus-protest-visas/',
    'https://haitiantimes.com/2025/05/11/haitian-students-visa-revocation-trump-crackdown/',
    'https://www.bigimmigrationlawblog.com/2025/04/the-new-risk-for-global-talent-f-1-sevis-terminations-and-student-visa-revocations/',
    'https://en.wikipedia.org/wiki/Activist_deportations_in_the_second_Trump_presidency',
    'https://www.npr.org/2025/04/22/nx-s1-5366021/international-students-face-visa-cancellations-despite-no-criminal-records'
]

# Check for vague/unhelpful university names
def is_valid_university_name(name):
    name = name.lower().strip()
    return (
        any(k in name for k in university_keywords) and 
        len(name.split()) >= 2 and 
        name not in {"college", "university", "institute", "academy", "school"}
    )

# Partial match logic
def is_partial_match(existing_name, new_name):
    return (
        new_name in existing_name or
        existing_name in new_name or
        difflib.SequenceMatcher(None, existing_name, new_name).ratio() > 0.85
    )

# Scrape article contents
def scrape_urls(urls):
    url_list = []
    title_list = []
    text_list = []

    for url in urls:
        try:
            article = Article(url)
            article.download()
            article.parse()
            url_list.append(url)
            title_list.append(article.title)
            text_list.append(article.text)
        except Exception as e:
            print("Could not open url:", url)
            url_list.append(url)
            title_list.append("Error")
            text_list.append("")

    df = pd.DataFrame({
        "url": url_list,
        "title": title_list,
        "text": text_list
    })
    df.to_csv("raw_articles.csv", index=False)

# Extract information
def extract_info():
    df = pd.read_csv("raw_articles.csv")
    rows = {}

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

        # Valid university names
        universities = [org.strip() for org in orgs if is_valid_university_name(org)]
        # Valid country names
        article_countries = [g for g in gpes if g in valid_countries]

        for sent in doc.sents:
            sentence_text = sent.text

            sentence_persons = [p for p in persons if p in sentence_text]
            sentence_universities = [u for u in universities if u in sentence_text]
            sentence_countries = [g for g in gpes if g in sentence_text and g in valid_countries]

            for person in sentence_persons:
                normalized_person = " ".join([part.capitalize() for part in person.split()])
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

                if sentence_universities:
                    rows[person_key]["universities"].update(sentence_universities)
                if sentence_countries:
                    rows[person_key]["countries"].update(sentence_countries)
                if visa_status:
                    rows[person_key]["visa_status"] = True
                if activism_status:
                    rows[person_key]["activism_status"] = True
                if url not in rows[person_key]["source_url"]:
                    rows[person_key]["source_url"] += ", " + url

        # Fallback: assign most frequent country in article if none was found in-person sentences
        for person_key in rows:
            if not rows[person_key]["countries"]:
                if article_countries:
                    # Use the most common country
                    fallback = max(set(article_countries), key=article_countries.count)
                    rows[person_key]["countries"].add(fallback)

    # Final output
    person_df = pd.DataFrame([
        {
            "person_name": key,
            "universities": next(iter(value["universities"]), ""),  # Just 1 university per person
            "countries": next(iter(value["countries"]), ""),        # Just 1 country per person
            "visa_status": value["visa_status"],
            "activism_status": value["activism_status"],
            "source_url": value["source_url"]
        }
        for key, value in rows.items()
        if value["universities"]  # Only include people with a university
    ])

    person_df.to_csv("extracted_by_person_filtered.csv", index=False)

# Run everything
scrape_urls(urls)
extract_info()
