# recon/crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

class WebCrawler:
    def __init__(self, target, logger):
        self.target = target
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutoReconWeb/1.0'
        })
        self.visited = set()
        self.found_urls = set()
        self.max_depth = 2

    def run(self):
        self.crawl(f"https://{self.target}", depth=0)
        return {
            'urls': list(self.found_urls),
            'forms': self.extract_forms(),
            'comments': self.extract_comments()
        }

    def crawl(self, url, depth):
        if depth > self.max_depth or url in self.visited:
            return
        
        self.visited.add(url)
        self.logger.info(f"Crawling: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract all links
                for link in soup.find_all('a', href=True):
                    absolute_url = urljoin(url, link['href'])
                    if self.is_valid_url(absolute_url):
                        self.found_urls.add(absolute_url)
                        self.crawl(absolute_url, depth + 1)
                
                # Extract scripts and iframes
                for tag in ['script', 'iframe']:
                    for element in soup.find_all(tag, src=True):
                        absolute_url = urljoin(url, element['src'])
                        if self.is_valid_url(absolute_url):
                            self.found_urls.add(absolute_url)
        except Exception as e:
            self.logger.error(f"Crawling failed for {url}: {str(e)}")

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return parsed.netloc.endswith(self.target) and parsed.scheme in ['http', 'https']

    def extract_forms(self):
        forms = []
        for url in self.visited:
            try:
                response = self.session.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                for form in soup.find_all('form'):
                    form_info = {
                        'action': urljoin(url, form.get('action', '')),
                        'method': form.get('method', 'get').upper(),
                        'inputs': []
                    }
                    for input_tag in form.find_all('input'):
                        form_info['inputs'].append({
                            'name': input_tag.get('name'),
                            'type': input_tag.get('type'),
                            'value': input_tag.get('value')
                        })
                    forms.append(form_info)
            except:
                continue
        return forms

    def extract_comments(self):
        comments = []
        for url in self.visited:
            try:
                response = self.session.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                    comments.append({
                        'url': url,
                        'comment': str(comment).strip()
                    })
            except:
                continue
        return comments