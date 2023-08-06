from utils.proxy import get_proxy
from colorama import init, Fore, Style
from newspaper import Article, Config
import requests
import time
from fake_useragent import UserAgent
from utils.database import save_article_to_db
import queue

start_time = time.time()

# Define lists to keep track of scraped and failed URLs
scraped_urls = set()
failed_urls = set()

# Set up user agent rotation using fake_useragent library
ua = UserAgent()

# Define global variables
url_queue = queue.Queue()

# set cache duration to 30 minutes
CACHE_DURATION = 30 * 60

# Define the colors
GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'
GRAY = '\033[90m'
YELLOW = '\033[33m'

# Read in a file of previously scraped URLs, if it exists
def check_url():
    scraped_urls = set()
    try:
        with open('scraped_urls.txt', 'r') as f:
            for line in f:
                scraped_urls.add(line.strip())
    except FileNotFoundError:
        pass

def scrape_url(url):
    # Get a random proxy server from Proxyscrape
    proxy = get_proxy()
    # Initialize wait period to 2 seconds
    wait_period = 2
    # Skip the URL if it has already been scraped
    if url in scraped_urls:
        print(f"\r{Style.BRIGHT}{Fore.GREEN}Skipping {Style.RESET_ALL} |{Fore.RED}(already scraped){Style.RESET_ALL}|          -----          {url}")
        return
    while True:
        try:
            # Rotate user agent
            config = Config()
            config.browser_user_agent = ua.random

            # Print current IP and user agent being used

            start_time_scrape = time.time()
            response = requests.get(url, proxies=proxy, timeout=3)
            print("Using IP:", proxy["http"].split("//")[1].rstrip())
            print("User agent:", config.browser_user_agent)
            end_time = time.time()

            article = Article(url, config=config)
            article.download(input_html=response.text)
            article.parse()
            article.nlp()

            # Store the data to MySQL database
            save_article_to_db(article)

            # Save scraped URL to file
            with open("scraped_urls.txt", "a") as f:
                f.write(url + "\n")

            # Add URL to scraped URLs list
            scraped_urls.append(url)

            # Print status

            # Calculate wait period dynamically based on server response time
            urls_remaining = url_queue.qsize()
            elapsed_time = end_time - start_time
            time_remaining = urls_remaining * (end_time - start_time + wait_period)
            estimated_time = time.strftime("%H:%M:%S", time.gmtime(time_remaining))
            wait_period = max(0, 2 - (end_time - start_time)) + 1  # Add 1 second buffer
            print(f"Scraped {Fore.YELLOW}(Sleeping for {wait_period} seconds...){Style.RESET_ALL}{Style.RESET_ALL}", )
            print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            print(f"Elapsed time: {Style.BRIGHT}{Fore.GREEN}{elapsed_time:.2f}s/{Style.RESET_ALL}Estimated time remaining: {Fore.RED}{estimated_time}{Style.RESET_ALL}/", end="\r", flush=True )
            print(f"{Style.BRIGHT}{Fore.GREEN}Scraping {Style.RESET_ALL}{url}")
            break
        except requests.exceptions.Timeout:
            # Timeout occurred, retry with longer timeout
            print(f"Timeout occurred while scraping {url}, retrying with timeout 6s...",)
            time.sleep(6)
        except Exception as e:
            print(f"Error occurred while scraping {url}: {e}",)
            failed_urls.append(url)
            with open("failed_urls.txt", "a") as f:
                f.write(url + "\n")
            # Add URL to scraped URLs list to prevent it from being scraped again
            scraped_urls.append(url)
            # Wait for 5 seconds before scraping the next article
            wait_period = 5
            break