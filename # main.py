# main.py
import argparse
from recon import DNSLookup, SubdomainEnumerator, WebCrawler, TechDetector, Screenshotter
from utils.logger import setup_logger
from utils.report_gen import generate_report

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="AutoRecon Web - Automated Web Reconnaissance Tool")
    parser.add_argument("target", help="Target domain or URL to scan")
    parser.add_argument("-o", "--output", help="Output directory for reports", default="reports")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    # Initialize logger
    logger = setup_logger(args.verbose)

    # Initialize modules
    modules = {
        'dns': DNSLookup(args.target, logger),
        'subdomains': SubdomainEnumerator(args.target, logger),
        'crawler': WebCrawler(args.target, logger),
        'tech': TechDetector(args.target, logger),
        'screenshots': Screenshotter(args.target, logger)
    }

    # Execute all modules
    results = {}
    for name, module in modules.items():
        logger.info(f"Running {name} module...")
        try:
            results[name] = module.run()
        except Exception as e:
            logger.error(f"Module {name} failed: {str(e)}")
            results[name] = {"error": str(e)}

    # Generate report
    generate_report(results, args.output)
    logger.info(f"Report generated in {args.output} directory")

if __name__ == "__main__":
    main()