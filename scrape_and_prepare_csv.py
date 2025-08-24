# scrape_and_prepare_csv.py (Corrected Version)

import re
import pandas as pd
from requests_html import HTMLSession
import os
from urllib.parse import urlparse

def get_company_name_from_url(url):
    """
    Extract a clean company name from a URL.
    """
    try:
        domain = urlparse(url).netloc
        name = domain.replace('www.', '').split('.')[0]
        return name.capitalize()
    except Exception:
        return "Unknown"

# --- Main Logic ---

CSV_FILE = "companies.csv"

# Step 1: Create companies.csv with headers if it doesn't exist.
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Company", "Website", "Title", "Emails", "status"]).to_csv(CSV_FILE, index=False)
    print(f"'{CSV_FILE}' not found. Creating a new file.")

# Step 2: Read existing CSV to prevent re-scraping.
df_existing = pd.read_csv(CSV_FILE)
scraped_websites = df_existing["Website"].tolist()
print(f"Found {len(scraped_websites)} companies already in '{CSV_FILE}'.")

# Step 3: Read the URLs from the source file.
try:
    with open("ai_company_urls.txt", "r") as f:
        urls_to_scrape = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print("Error: 'ai_company_urls.txt' not found. Please run the URL scraper first.")
    exit()

# Step 4: Filter for only new URLs.
new_urls = [url for url in urls_to_scrape if url not in scraped_websites]

if not new_urls:
    print("No new URLs to scrape. Your 'companies.csv' is up to date.")
    exit()

print(f"Found {len(new_urls)} new URLs to process.")
results = []
session = HTMLSession() # Using the session from your original script

# Step 5: Scrape new URLs using the original, proven logic.
for url in new_urls:
    company_name = get_company_name_from_url(url)
    print(f"🔎 Scraping {company_name} ({url}) ...")

    try:
        # THIS IS THE CORE LOGIC FROM YOUR ORIGINAL SCRIPT
        r = session.get(url, timeout=20)
        title = r.html.find("title", first=True).text if r.html.find("title", first=True) else company_name

        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", r.text)
        unique_emails = sorted(list(set(email.lower() for email in emails)))
        
        results.append({
            "Company": company_name,
            "Website": url,
            "Title": title,
            "Emails": ", ".join(unique_emails) if unique_emails else "N/A",
            "status": "unsent" if unique_emails else "no_email_found"
        })
        print(f"✅ {company_name} scraped successfully.")

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        results.append({
            "Company": company_name,
            "Website": url,
            "Title": "Scraping Error",
            "Emails": "N/A",
            "status": "scraping_failed"
        })

# Step 6: Append the new results to the CSV file.
if results:
    df_new = pd.DataFrame(results)
    df_new.to_csv(CSV_FILE, mode='a', index=False, header=False)
    print(f"\n📊 Process complete. Added {len(results)} new companies to '{CSV_FILE}'.")