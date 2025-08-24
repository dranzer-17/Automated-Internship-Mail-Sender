from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urlparse, urlunparse
import random

def setup_driver():
    """
    Setup Chrome driver with options to bypass Cloudflare
    """
    chrome_options = Options()
    
    # Essential options to appear more human-like
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-plugins')
    chrome_options.add_argument('--disable-images')  # Faster loading
    chrome_options.add_argument('--disable-javascript')  # Try without JS first
    
    # Use a common user agent
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Run in headless mode for better performance
    # chrome_options.add_argument('--headless')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    # Execute script to remove webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def wait_for_cloudflare(driver, timeout=30):
    """
    Wait for Cloudflare challenge to complete
    """
    print("Waiting for Cloudflare challenge to complete...")
    
    # Wait for either the main content to load or timeout
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # Check if we're still on Cloudflare challenge page
            if "challenge" in driver.current_url.lower() or "cloudflare" in driver.page_source.lower():
                print("Still on Cloudflare challenge page, waiting...")
                time.sleep(2)
                continue
            
            # Check if we have actual content
            if len(driver.find_elements(By.TAG_NAME, "a")) > 5:
                print("Page loaded successfully!")
                return True
                
        except:
            pass
        
        time.sleep(1)
    
    print("Timeout waiting for Cloudflare challenge")
    return False

def scrape_with_selenium(max_urls=500):
    """
    Scrape AI tools URLs with Cloudflare bypass
    """
    driver = None
    
    try:
        print("Setting up Chrome driver...")
        driver = setup_driver()
        
        url = "https://theresanaiforthat.com/s/automation/"
        print(f"Navigating to: {url}")
        
        driver.get(url)
        
        # Wait for Cloudflare challenge to complete
        if not wait_for_cloudflare(driver):
            print("Failed to bypass Cloudflare protection")
            return []
        
        # Additional wait for content to load
        time.sleep(random.uniform(3, 6))
        
        # Try scrolling to load more content
        print("Scrolling to load more content...")
        for i in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        print("Extracting URLs from page...")
        
        # Method 1: Direct link extraction
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"Found {len(links)} link elements")
        
        company_urls = set()
        
        for link in links:
            try:
                href = link.get_attribute('href')
                if href and href.startswith('http') and 'theresanaiforthat.com' not in href:
                    parsed_url = urlparse(href)
                    domain = parsed_url.netloc.lower()
                    
                    # Skip common non-company domains
                    skip_domains = [
                        'google.com', 'facebook.com', 'twitter.com', 'linkedin.com',
                        'youtube.com', 'instagram.com', 'github.com', 'medium.com',
                        'reddit.com', 'discord.com', 'telegram.org', 'apple.com',
                        'play.google.com', 'apps.apple.com', 'chrome.google.com',
                        'producthunt.com', 'crunchbase.com', 'techcrunch.com',
                        'cloudflare.com'
                    ]
                    
                    if not any(skip_domain in domain for skip_domain in skip_domains):
                        company_urls.add(href)
                        print(f"Found URL {len(company_urls)}: {href}")
                        
                        if len(company_urls) >= max_urls:
                            break
                            
            except Exception as e:
                continue
        
        # Method 2: Look for specific patterns in the page source
        if len(company_urls) < 10:  # If we didn't find many URLs
            print("Searching page source for additional URLs...")
            page_source = driver.page_source
            
            # Look for URLs in the HTML source
            url_pattern = r'https?://(?!.*theresanaiforthat\.com)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s"\'<>]*)?'
            found_urls = re.findall(url_pattern, page_source)
            
            for url in found_urls:
                parsed_url = urlparse(url)
                domain = parsed_url.netloc.lower()
                
                skip_domains = [
                    'google.com', 'facebook.com', 'twitter.com', 'linkedin.com',
                    'youtube.com', 'instagram.com', 'github.com', 'medium.com',
                    'reddit.com', 'discord.com', 'telegram.org', 'apple.com',
                    'play.google.com', 'apps.apple.com', 'chrome.google.com',
                    'producthunt.com', 'crunchbase.com', 'techcrunch.com',
                    'cloudflare.com', 'w3.org', 'mozilla.org'
                ]
                
                if (not any(skip_domain in domain for skip_domain in skip_domains) and 
                    len(domain.split('.')) >= 2):
                    company_urls.add(url)
                    print(f"Found URL from source {len(company_urls)}: {url}")
                    
                    if len(company_urls) >= max_urls:
                        break
        
        return list(company_urls)[:max_urls]
        
    except Exception as e:
        print(f"Error during scraping: {e}")
        return []
        
    finally:
        if driver:
            print("Closing browser...")
            driver.quit()

def try_requests_fallback():
    """
    Fallback method using requests with session persistence
    """
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    
    print("\nTrying requests fallback method...")
    
    session = requests.Session()
    
    # Setup retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    session.headers.update(headers)
    
    try:
        # Try the main page first
        response = session.get("https://theresanaiforthat.com/s/automation/", timeout=15)
        
        if response.status_code == 200 and 'cloudflare' not in response.text.lower():
            print("Successfully bypassed with requests!")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            
            company_urls = set()
            for link in links:
                href = link.get('href', '').strip()
                if (href.startswith('http') and 
                    'theresanaiforthat.com' not in href and
                    'cloudflare.com' not in href):
                    company_urls.add(href)
            
            return list(company_urls)
        
    except Exception as e:
        print(f"Requests fallback failed: {e}")
    
    return []

def save_urls_to_file(urls, filename="ai_company_urls.txt"):
    """
    Cleans the URLs by removing tracking parameters and saves them to a text file.
    """
    try:
        # Use a set to store the cleaned URLs to ensure uniqueness
        cleaned_urls = set()
        for url in urls:
            parsed_url = urlparse(url)
            # Reconstruct the URL without query parameters or fragments
            clean_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
            # Add the cleaned URL to the set
            cleaned_urls.add(clean_url)

        # Write the unique, cleaned URLs to the file
        with open(filename, 'w', encoding='utf-8') as f:
            for url in sorted(list(cleaned_urls)): # Sorting is optional, but nice for consistency
                f.write(url + '\n')
        print(f"Cleaned and saved {len(cleaned_urls)} unique URLs to {filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")

def main():
    """
    Main function with multiple approaches
    """
    print("AI Tools Directory URL Scraper with Cloudflare Bypass")
    print("=" * 55)
    
    # Try Selenium first
    print("Method 1: Using Selenium with Cloudflare bypass...")
    urls = scrape_with_selenium(max_urls=500)
    
    # If Selenium didn't work well, try requests
    if len(urls) < 5:
        urls.extend(try_requests_fallback())
        # Remove duplicates
        urls = list(set(urls))[:500]
    
    if urls:
        print(f"\nFound {len(urls)} unique company URLs:")
        print("-" * 40)
        for i, url in enumerate(urls, 1):
            print(f"{i:2d}. {url}")
        
        # Save to file
        save_urls_to_file(urls)
        
    else:
        print("\nNo URLs found. Possible reasons:")
        print("1. Cloudflare protection is too strong")
        print("2. Page structure has changed")
        print("3. Site requires JavaScript to load content")
        print("\nTry running the script again or check the website manually.")

if __name__ == "__main__":
    main()