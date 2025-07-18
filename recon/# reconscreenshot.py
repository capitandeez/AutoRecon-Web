# recon/screenshot.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
from PIL import Image

class Screenshotter:
    def __init__(self, target, logger):
        self.target = target
        self.logger = logger
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        # Configure Selenium
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=self.options)

    def run(self):
        results = {}
        
        # Take screenshot of main page
        main_url = f"https://{self.target}"
        results['main_page'] = self.take_screenshot(main_url)
        
        # Take screenshots of common admin pages
        admin_paths = ['/admin', '/wp-admin', '/administrator', '/login']
        results['admin_pages'] = []
        
        for path in admin_paths:
            url = main_url + path
            screenshot_path = self.take_screenshot(url)
            if screenshot_path:
                results['admin_pages'].append({
                    'url': url,
                    'screenshot': screenshot_path
                })
        
        self.driver.quit()
        return results

    def take_screenshot(self, url):
        try:
            self.driver.get(url)
            time.sleep(3)  # Wait for page to load
            
            # Get scroll height and set window size
            scroll_height = self.driver.execute_script("return document.body.scrollHeight")
            self.driver.set_window_size(1920, scroll_height)
            
            # Generate filename
            filename = f"{self.screenshot_dir}/{url.replace('https://', '').replace('/', '_')}.png"
            
            # Take screenshot
            self.driver.save_screenshot(filename)
            
            # Optimize image
            img = Image.open(filename)
            img.save(filename, optimize=True, quality=85)
            
            return filename
        except Exception as e:
            self.logger.error(f"Screenshot failed for {url}: {str(e)}")
            return None