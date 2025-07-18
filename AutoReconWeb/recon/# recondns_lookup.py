# recon/dns_lookup.py
import dns.resolver
import socket
import ssl
import whois
from datetime import datetime

class DNSLookup:
    def __init__(self, target, logger):
        self.target = target
        self.logger = logger

    def run(self):
        results = {
            'basic': self.basic_lookup(),
            'whois': self.whois_lookup(),
            'ssl': self.ssl_info()
        }
        return results

    def basic_lookup(self):
        records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
        
        for rtype in record_types:
            try:
                answers = dns.resolver.resolve(self.target, rtype)
                records[rtype] = [str(r) for r in answers]
            except Exception as e:
                self.logger.debug(f"Failed to get {rtype} record: {str(e)}")
        
        try:
            records['IP'] = socket.gethostbyname(self.target)
        except Exception as e:
            self.logger.debug(f"Failed to get IP: {str(e)}")
        
        return records

    def whois_lookup(self):
        try:
            w = whois.whois(self.target)
            return {
                'registrar': w.registrar,
                'creation_date': str(w.creation_date),
                'expiration_date': str(w.expiration_date),
                'name_servers': w.name_servers,
                'status': w.status
            }
        except Exception as e:
            self.logger.error(f"WHOIS lookup failed: {str(e)}")
            return {"error": str(e)}

    def ssl_info(self):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.target, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=self.target) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'valid_from': cert['notBefore'],
                        'valid_to': cert['notAfter'],
                        'version': cert['version'],
                        'serial_number': cert['serialNumber']
                    }
        except Exception as e:
            self.logger.error(f"SSL info failed: {str(e)}")
            return {"error": str(e)}