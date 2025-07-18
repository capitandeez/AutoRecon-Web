# recon/tech_detect.py
import requests
import re
from bs4 import BeautifulSoup

class TechDetector:
    def __init__(self, target, logger):
        self.target = target
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutoReconWeb/1.0'
        })

    def run(self):
        results = {
            'headers': self.analyze_headers(),
            'content': self.analyze_content(),
            'wappalyzer': self.wappalyzer_analysis()
        }
        return results

    def analyze_headers(self):
        url = f"https://{self.target}"
        try:
            response = self.session.head(url, allow_redirects=True, timeout=10)
            headers = dict(response.headers)
            
            tech = []
            
            # Server detection
            if 'server' in headers:
                tech.append({'type': 'server', 'value': headers['server']})
            
            # Powered-by detection
            if 'x-powered-by' in headers:
                tech.append({'type': 'framework', 'value': headers['x-powered-by']})
            
            return tech
        except Exception as e:
            self.logger.error(f"Header analysis failed: {str(e)}")
            return []

    def analyze_content(self):
        url = f"https://{self.target}"
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            tech = []
            
            # Meta generator tags
            for meta in soup.find_all('meta', attrs={'name': 'generator'}):
                tech.append({'type': 'cms', 'value': meta.get('content')})
            
            # Script src analysis
            for script in soup.find_all('script', src=True):
                src = script['src']
                if 'jquery' in src.lower():
                    tech.append({'type': 'js_lib', 'value': 'jQuery'})
                elif 'react' in src.lower():
                    tech.append({'type': 'js_framework', 'value': 'React'})
                elif 'vue' in src.lower():
                    tech.append({'type': 'js_framework', 'value': 'Vue.js'})
            
            # CSS framework detection
            for link in soup.find_all('link', rel='stylesheet'):
                href = link['href']
                if 'bootstrap' in href.lower():
                    tech.append({'type': 'css_framework', 'value': 'Bootstrap'})
                elif 'foundation' in href.lower():
                    tech.append({'type': 'css_framework', 'value': 'Foundation'})
            
            return tech
        except Exception as e:
            self.logger.error(f"Content analysis failed: {str(e)}")
            return []

    def wappalyzer_analysis(self):
        # This is a simplified version. Consider using the actual Wappalyzer patterns
        url = f"https://{self.target}"
        try:
            response = self.session.get(url, timeout=10)
            tech = []
            
            # WordPress detection
            if '/wp-content/' in response.text:
                tech.append({'type': 'cms', 'value': 'WordPress'})
            
            # Joomla detection
            if '/media/system/js/' in response.text:
                tech.append({'type': 'cms', 'value': 'Joomla'})
            
            # Drupal detection
            if 'sites/all/themes' in response.text:
                tech.append({'type': 'cms', 'value': 'Drupal'})
            
            return tech
        except Exception as e:
            self.logger.error(f"Wappalyzer analysis failed: {str(e)}")
            return []