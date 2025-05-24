import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import logging

# Setting up logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_soup(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        logging.error(f"Failed to get the soup for {url}: {e}")
        return None

def clean_text(text):
    # Remove excessive newlines and strip leading/trailing whitespace
    cleaned = " ".join(text.split())
    return cleaned

def scrape_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    soup = get_soup(url, headers)
    if not soup:
        return None
    
    data = {}

    # Extract title
    data["Title"] = soup.title.text.strip() if soup.title else "No title found"
    
    # Extract all paragraphs
    data["Paragraphs"] = list(set([clean_text(p.text) for p in soup.find_all("p")])) if soup.find_all("p") else ["No paragraphs found"]
    
    # Extract all divs
    data["Divs"] = list(set([clean_text(div.text) for div in soup.find_all("div")])) if soup.find_all("div") else ["No divs found"]
    
    # Extract all spans
    data["Spans"] = list(set([clean_text(span.text) for span in soup.find_all("span")])) if soup.find_all("span") else ["No spans found"]
    
    # Extract external links
    data["External Links"] = []
    for link in soup.find_all('a', href=True):
        full_url = urljoin(url, link['href'])
        if full_url.startswith('http'):
            data["External Links"].append(full_url)
    
    # Extract images
    data["Images"] = []
    for img in soup.find_all('img', src=True):
        img_url = urljoin(url, img['src'])
        data["Images"].append(img_url)
    
    # Extract meta tags
    meta_description = soup.find("meta", attrs={"name": "description"})
    data["Meta Description"] = clean_text(meta_description['content']) if meta_description else "No description found"
    
    meta_keywords = soup.find("meta", attrs={"name": "keywords"})
    data["Meta Keywords"] = clean_text(meta_keywords['content']) if meta_keywords else "No keywords found"
    
    # Save data to JSON file
    with open('scraped_data.json', mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

    logging.info(f"Scraped {url} successfully.")
    return data

def main():
    print("insde pyn main")
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
        return

    url = sys.argv[1]

    scraped_data = scrape_website(url)
    if scraped_data:
        print("Scraping completed. Data saved to scraped_data.json and scraper.log.")
    else:
        print("Scraping failed.")

if __name__ == "__main__":
    main()
