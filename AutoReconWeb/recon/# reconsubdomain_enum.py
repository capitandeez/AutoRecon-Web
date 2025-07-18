# recon/subdomain_enum.py
import requests
import dns.resolver
from concurrent.futures import ThreadPoolExecutor

class SubdomainEnumerator:
    def __init__(self, target, logger):
        self.target = target
        self.logger = logger
        self.wordlist = "wordlists/subdomains.txt"  # You should provide this
        self.api_keys = {
            'virustotal': 'YOUR_API_KEY',
            'securitytrails': 'YOUR_API_KEY'
        }

    def run(self):
        results = {
            'bruteforce': self.bruteforce_subdomains(),
            'api_based': self.api_based_enumeration()
        }
        return results

    def bruteforce_subdomains(self):
        found = []
        try:
            with open(self.wordlist, 'r') as f:
                subdomains = [line.strip() + '.' + self.target for line in f]
            
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = {executor.submit(self.check_subdomain, sub): sub for sub in subdomains}
                for future in futures:
                    if future.result():
                        found.append(futures[future])
        except Exception as e:
            self.logger.error(f"Bruteforce failed: {str(e)}")
        
        return found

    def check_subdomain(self, subdomain):
        try:
            answers = dns.resolver.resolve(subdomain, 'A')
            return len(answers) > 0
        except:
            return False

    def api_based_enumeration(self):
        results = {}
        
        # VirusTotal
        try:
            url = f"https://www.virustotal.com/api/v3/domains/{self.target}/subdomains"
            headers = {"x-apikey": self.api_keys['virustotal']}
            response = requests.get(url, headers=headers)
            results['virustotal'] = response.json().get('data', [])
        except Exception as e:
            self.logger.error(f"VirusTotal API failed: {str(e)}")
        
        # SecurityTrails
        try:
            url = f"https://api.securitytrails.com/v1/domain/{self.target}/subdomains"
            headers = {"APIKEY": self.api_keys['securitytrails']}
            response = requests.get(url, headers=headers)
            results['securitytrails'] = response.json().get('subdomains', [])
        except Exception as e:
            self.logger.error(f"SecurityTrails API failed: {str(e)}")
        
        return results