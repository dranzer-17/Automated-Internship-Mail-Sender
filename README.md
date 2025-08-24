Of course. A good README is essential for any project. Here is a comprehensive README.md file that explains the purpose, setup, and usage of your automated outreach system.

AI Startup Outreach Automator

This project is a semi-automated pipeline designed to identify, scrape contact information for, and send personalized outreach emails to AI startups. The system is built with three Python scripts that work together to manage the entire workflow, from URL discovery to final email dispatch, while ensuring no company is contacted more than once.

Features

Web Scraping: Uses Selenium to scrape company URLs from a directory website (theresanaiforthat.com), handling basic anti-bot measures.

Email Extraction: Parses company websites to find publicly available email addresses.

Duplicate Prevention: Maintains a master companies.csv file to track all processed companies and prevent re-scraping or sending duplicate emails.

Status Tracking: Each company in the CSV is assigned a status (unsent, sent, failed, no_email_found) for clear visibility into the outreach campaign.

Batched & Throttled Emailing: Sends emails in configurable batches (e.g., 50 per day) with a delay between each to avoid being flagged as spam.

Secure Credential Management: Uses a .env file to securely store email login credentials.

Automated Resume Attachment: Automatically attaches your resume to every outgoing email.

Workflow

The process is broken down into three simple steps:

Scrape URLs: You run the first script (ai_url_scraper.py), which opens a browser and navigates to the target website. You manually solve a CAPTCHA, and the script then scrapes hundreds of AI company URLs, cleans them, and saves them to ai_company_urls.txt.

Gather Emails: The second script (scrape_and_prepare_csv.py) reads the new URLs from the text file, scrapes each website for email addresses, and appends the new company data to the master companies.csv file with an initial status of "unsent".

Send Emails: The final script (sendmail_final.py) reads the companies.csv file, finds up to 50 companies with the "unsent" status, sends them a personalized email with your resume, and updates their status to "sent" or "failed".

Prerequisites

Python 3.8 or newer

pip (Python package installer)

Google Chrome browser installed

ChromeDriver matching your Chrome version (Selenium needs this to control the browser). Make sure it's accessible in your system's PATH.

Setup & Installation

Clone the Repository

code
Bash
download
content_copy
expand_less

git clone <your-repository-url>
cd <your-repository-directory>

Create a Virtual Environment (Recommended)

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install Dependencies
Create a file named requirements.txt with the following content:

code
Txt
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
selenium
beautifulsoup4
requests-html
pandas
python-dotenv

Then, install the packages:

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
pip install -r requirements.txt

Set Up Environment Variables
Create a file named .env in the root directory. This will store your email credentials securely.
Important: For Gmail, you must use an App Password, not your regular login password. Learn how to create one here.

code
Env
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
# .env file
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_16_digit_app_password

Add Your Resume
Place your resume file (e.g., resume.pdf) in the root project directory. Ensure the filename matches the RESUME_FILE variable in sendmail_final.py.

Usage Guide

Execute the scripts in the following order.

Step 1: Scrape Company URLs

This is the only manual step. Run the script and follow the on-screen prompt.

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
python ai_url_scraper.py

Selenium will open a Chrome browser window.

You must manually solve the "I am not a robot" CAPTCHA in the browser.

Once solved, go back to your terminal and press Enter.

The script will then scrape the URLs and create a clean ai_company_urls.txt file.

Step 2: Scrape Emails and Prepare CSV

This script reads the new URLs and populates the master tracking file.

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
python scrape_and_prepare_csv.py

It reads ai_company_urls.txt.

It checks companies.csv to avoid processing duplicates.

It scrapes each new website for emails and adds the results to companies.csv.

Step 3: Send Emails in Batches

This script performs the daily email outreach. You can run this script once a day.

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
python sendmail_final.py

It reads companies.csv and finds the first 50 entries with the status "unsent".

It sends a personalized email with your resume attached to each one.

It updates the status for each email to "sent" or "failed".

File Descriptions

ai_url_scraper.py: Scrapes company URLs from the source website. Requires manual CAPTCHA solving.

scrape_and_prepare_csv.py: The core data processing script. It scrapes emails for new URLs and updates the master CSV.

sendmail_final.py: The email sending module. Reads the CSV and sends emails in batches.

companies.csv: The master database. This is the single source of truth for which companies have been scraped and contacted.

ai_company_urls.txt: A temporary file holding the URLs scraped in Step 1.

.env: A private file for storing your email credentials. Do not commit this file to Git.

requirements.txt: A list of the required Python packages for the project.