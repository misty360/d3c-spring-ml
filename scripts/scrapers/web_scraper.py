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

    person_df.to_csv("updated_extracted_by_person_filtered.csv", index=False)

# Run everything
scrape_urls(urls)
extract_info()
