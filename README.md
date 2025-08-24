# AI Company Automation Toolkit

A comprehensive Python toolkit for automating the process of finding AI companies, scraping their contact information, and sending professional outreach emails. This toolkit is designed for job seekers, business development professionals, and anyone looking to network within the AI industry.

## Features

- **Web Scraping with Cloudflare Bypass**: Advanced scraping techniques to extract AI company URLs from directories
- **Contact Information Extraction**: Automatically finds email addresses from company websites
- **Batch Email Sending**: Professional email automation with resume attachments
- **Progress Tracking**: CSV-based system to track scraping and email sending status
- **Error Handling**: Robust error handling and retry mechanisms
- **Rate Limiting**: Built-in delays to respect website policies and avoid spam filters

## Project Structure

```
├── ai_url_scraper.py          # Main scraper for AI company URLs
├── scrape_and_prepare_csv.py  # Email extraction and CSV preparation
├── sendmail_final.py          # Email automation system
├── .env                       # Environment variables (create this)
├── resume.pdf                 # Your resume file (add this)
├── ai_company_urls.txt        # Generated list of company URLs
└── companies.csv              # Main database with company information
```

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Gmail Setup](#gmail-setup)
- [Usage](#usage)
- [Configuration Options](#configuration-options)
- [CSV Structure](#csv-structure)
- [Email Template](#email-template)
- [Safety and Ethics](#safety-and-ethics)
- [Troubleshooting](#troubleshooting)
- [Legal and Ethical Considerations](#legal-and-ethical-considerations)

## Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- ChromeDriver (automatically managed by selenium)
- Gmail account with App Password enabled

## Installation

1. **Clone this repository:**
   ```bash
   git clone <repository-url>
   cd ai-company-automation-toolkit
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install individually:
   ```bash
   pip install selenium beautifulsoup4 pandas requests-html python-dotenv
   ```

3. **Create environment file:**
   Create a `.env` file in the project root directory:
   ```env
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_gmail_app_password
   ```

4. **Add your resume:**
   Place your resume file as `resume.pdf` in the project directory

## Gmail Setup

To enable email functionality with Gmail:

1. **Enable 2-Factor Authentication:**
   - Go to your Google Account settings
   - Navigate to Security > 2-Step Verification
   - Enable 2FA if not already enabled

2. **Generate App Password:**
   - Go to Security > App passwords
   - Select "Mail" as the app
   - Generate a 16-character app password

3. **Update .env file:**
   - Use your Gmail address for `EMAIL_USER`
   - Use the generated app password (not your regular password) for `EMAIL_PASS`

> **Note:** Regular Gmail passwords will not work. You must use an App Password.

## Usage

### Step 1: Scrape AI Company URLs

```bash
python ai_url_scraper.py
```

**What this does:**
- Navigates to AI company directories (currently targets TheresAnAIForThat.com)
- Implements Cloudflare bypass techniques
- Extracts company URLs using multiple methods
- Filters out non-company domains (social media, etc.)
- Saves results to `ai_company_urls.txt`

**Expected output:** A text file containing 500+ unique AI company URLs

---

### Step 2: Extract Contact Information

```bash
python scrape_and_prepare_csv.py
```

**What this does:**
- Reads URLs from `ai_company_urls.txt`
- Visits each company website
- Extracts email addresses using regex patterns
- Captures company names and page titles
- Creates or updates `companies.csv` with status tracking
- Skips already processed URLs to allow resuming

**Expected output:** A CSV file with company data and email addresses

---

### Step 3: Send Professional Emails

```bash
python sendmail_final.py
```

**What this does:**
- Processes companies with "unsent" status from CSV
- Sends personalized emails with resume attachments
- Implements rate limiting (10-second delays between emails)
- Updates status in CSV after each attempt
- Handles up to 50 emails per batch by default

**Expected output:** Professional emails sent to AI companies with status tracking

## Configuration Options

### ai_url_scraper.py
| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_urls` | 500 | Maximum number of URLs to scrape |
| Chrome options | Various | Browser configuration for stealth mode |

### scrape_and_prepare_csv.py
| Parameter | Default | Description |
|-----------|---------|-------------|
| Timeout | 20 seconds | Web request timeout |
| Email regex | Built-in | Pattern for email extraction |

### sendmail_final.py
| Parameter | Default | Description |
|-----------|---------|-------------|
| `EMAIL_BATCH_SIZE` | 50 | Emails sent per execution |
| `DELAY_BETWEEN_EMAILS` | 10 seconds | Delay between each email |
| `RESUME_FILE` | "resume.pdf" | Resume attachment filename |

## CSV Structure

The `companies.csv` file maintains the following structure:

| Column | Type | Description |
|--------|------|-------------|
| **Company** | String | Extracted company name from URL |
| **Website** | String | Company website URL |
| **Title** | String | Website page title |
| **Emails** | String | Comma-separated email addresses |
| **Status** | String | Processing status (see below) |

### Status Values
- `unsent`: Ready to send email
- `sent`: Email successfully sent
- `failed`: Email sending failed
- `no_email_found`: No email addresses found on website
- `scraping_failed`: Website scraping encountered errors

## Email Template

The default email template includes:
- Professional subject line with company name
- Introduction mentioning current role at SimPPL
- Interest in career opportunities
- Resume attachment
- Professional closing

You can customize the email content by modifying the `create_message()` function in `sendmail_final.py`.

## Safety and Ethics

- **Rate Limiting**: Built-in delays prevent overwhelming target servers
- **Respectful Scraping**: Uses appropriate headers and follows robots.txt guidelines
- **Error Handling**: Gracefully handles failures without crashing
- **Status Tracking**: Prevents duplicate emails and allows for resume functionality

## Troubleshooting

### Common Issues and Solutions

#### Cloudflare Protection
**Problem:** Scraper gets blocked by Cloudflare
**Solutions:**
- Run the script at different times of day
- Modify user agent strings in the code
- Try the requests fallback method built into the scraper

#### Gmail Authentication Errors
**Problem:** `SMTPAuthenticationError` when sending emails
**Solutions:**
- Verify you're using an App Password, not your regular password
- Ensure 2-Factor Authentication is enabled on your Google account
- Check that EMAIL_USER and EMAIL_PASS are correctly set in `.env`

#### No Emails Found
**Problem:** Many companies show "no_email_found" status
**Explanation:** Some websites don't publicly display email addresses
**Solutions:**
- This is expected behavior for privacy-conscious websites
- Focus on companies where emails were successfully found

#### Selenium WebDriver Issues
**Problem:** Browser automation fails
**Solutions:**
- Ensure Chrome browser is installed and updated
- ChromeDriver is managed automatically by modern selenium versions
- Try running in non-headless mode for debugging

#### File Not Found Errors
**Problem:** Script can't find required files
**Solutions:**
- Ensure `resume.pdf` exists in the project directory
- Run scripts in the correct order (URL scraper first)
- Check that all Python files are in the same directory

### Error Messages Reference

| Error Message | Cause | Solution |
|---------------|--------|----------|
| `"EMAIL_USER and EMAIL_PASS must be set"` | Missing environment variables | Check your `.env` file configuration |
| `"Resume file not found"` | Missing resume file | Add `resume.pdf` to project directory |
| `"No new URLs to scrape"` | All URLs processed | Normal - indicates completion |
| `"Cloudflare challenge timeout"` | Website protection | Retry at different time |
| `"SMTPAuthenticationError"` | Invalid Gmail credentials | Use App Password, not regular password |

## Legal and Ethical Considerations

- This tool is designed for legitimate professional networking and job searching
- Always respect website terms of service and robots.txt files
- Use reasonable delays between requests
- Only send professional, relevant communications
- Comply with applicable laws and regulations regarding automated communications

## Contributing

To improve this toolkit:
1. Test with different AI company directories
2. Enhance email extraction patterns
3. Add support for additional email providers
4. Improve error handling and logging

## License

This project is provided as-is for educational and professional networking purposes. Users are responsible for ensuring their usage complies with applicable laws and website terms of service.