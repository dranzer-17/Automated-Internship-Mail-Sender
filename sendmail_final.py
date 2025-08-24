# sendmail_final.py

import os
import smtplib
import ssl
import time
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# --- Configuration ---
# Make sure you have a .env file in the same directory with these variables:
# EMAIL_USER=your_email@gmail.com
# EMAIL_PASS=your_gmail_app_password
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

# The name of your resume file
RESUME_FILE = "resume.pdf"
# The master CSV file
CSV_FILE = "companies.csv"
# Maximum number of emails to send per run
EMAIL_BATCH_SIZE = 50
# Delay in seconds between each email to avoid spam filters
DELAY_BETWEEN_EMAILS = 10 # 10 seconds

# --- Email Content ---
def create_message(company, recipient_email):
    """Creates the email message, including the subject, body, and resume attachment."""
    subject = f"Exploring Career Opportunities with {company}"
    body = f"""
Hello,

My name is Kavish Shah, and I am currently working as a Research Engineering Intern at SimPPL.
I am very interested in exploring potential career opportunities with {company} and would love the chance to connect and have a brief chat.

My resume is attached for your consideration.

Looking forward to your response.

Best regards,
Kavish Shah
"""

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach resume
    try:
        with open(RESUME_FILE, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={RESUME_FILE}")
        msg.attach(part)
    except FileNotFoundError:
        print(f"Warning: Resume file '{RESUME_FILE}' not found. Sending email without attachment.")
    
    return msg

# --- Main Execution ---
def main():
    """Main function to read CSV, send emails, and update status."""
    # Check for required files and credentials
    if not all([EMAIL_ADDRESS, EMAIL_PASSWORD]):
        print("Error: EMAIL_USER and EMAIL_PASS must be set in your .env file.")
        return
        
    if not os.path.exists(CSV_FILE):
        print(f"Error: The file '{CSV_FILE}' was not found. Please run the scraping script first.")
        return

    df = pd.read_csv(CSV_FILE)

    # Filter for rows with "unsent" status and take the next batch
    unsent_df = df[df["status"] == "unsent"].head(EMAIL_BATCH_SIZE)

    if unsent_df.empty:
        print("All emails have been sent. No companies with 'unsent' status found.")
        return

    print(f"Found {len(unsent_df)} emails to send in this batch...")
    sent_count = 0

    # Connect to the SMTP server once for the whole batch
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            
            for idx, row in unsent_df.iterrows():
                company = row["Company"]
                # Take the first email if multiple are listed, and strip any whitespace
                recipient = str(row["Emails"]).split(',')[0].strip()

                if recipient == "N/A" or "@" not in recipient:
                    print(f"⏭️  [SKIPPED] {company} - Invalid or missing email address.")
                    df.loc[idx, "status"] = "no_email_found"
                    continue
                
                print(f"🚀 Sending to {company} ({recipient})...")
                try:
                    # Create and send the email
                    msg = create_message(company, recipient)
                    server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
                    print(f"✅ [SENT] Email successfully sent to {company}.")
                    # Update status in the DataFrame
                    df.loc[idx, "status"] = "sent"
                    sent_count += 1
                
                except Exception as e:
                    print(f"❌ [FAILED] Could not send to {company}. Error: {e}")
                    df.loc[idx, "status"] = "failed"
                
                # Wait before sending the next email
                time.sleep(DELAY_BETWEEN_EMAILS)

    except smtplib.SMTPAuthenticationError:
        print("\n--- SMTP Authentication Error ---")
        print("Please check your EMAIL_USER and EMAIL_PASS in the .env file.")
        print("Note: For Gmail, you need to use an 'App Password', not your regular password.")
        return
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        return

    # Save the updated DataFrame back to the CSV file
    df.to_csv(CSV_FILE, index=False)
    print(f"\n✨ Batch complete. Sent {sent_count} emails. '{CSV_FILE}' has been updated.")

if __name__ == "__main__":
    main()