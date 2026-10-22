import requests
from bs4 import BeautifulSoup

class TechNewsScraper:
    def __init__(self, url):
        self.url = url

    def fetch_articles(self):
        print(f"Fetching articles from {self.url}...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []

        # Hacker News story rows use class 'athing'
        for item in soup.find_all('tr', class_='athing')[:10]:
            title_elem = item.find('span', class_='titleline')
            if title_elem:
                link_elem = title_elem.find('a')
                if link_elem:
                    articles.append({
                        'title': link_elem.text.strip(),
                        'source_url': link_elem.get('href', ''),
                        'content': "Scraped automated summary content from Hacker News..."
                    })

        return articles