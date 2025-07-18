# AutoRecon-Web



AutoRecon-Web
AutoRecon-Web is a lightweight, modular recon tool I built to streamline web-based reconnaissance. It handles everything from DNS lookups to subdomain enum, crawling, stack detection, and screenshots — all in one place.

It's written in Python, fully modular, and easy to extend. The idea was simple: I was tired of juggling 10 different tools just to recon a single domain. So I made my own setup.

⚙️ What It Does
Here’s what it currently supports:

🔍 DNS Lookup – basic IP resolution

🌐 Subdomain Enumeration – finds subdomains using multiple sources

🕸️ Crawling – grabs internal links and JS files

🧠 Tech Stack Detection – figures out what the site’s running on (headers-based)

📸 Screenshotting – takes full-page screenshots using headless Chromium

📄 Report Generation – spits out clean HTML reports with your findings

More modules are in the works.

📂 Project Structure
bash
Copy
Edit
AutoRecon-Web/
├── recon/               # All recon modules
│   ├── dns_lookup.py
│   ├── subdomain_enum.py
│   ├── crawler.py
│   ├── tech_detect.py
│   ├── screenshot.py
│   └── logger.py
├── reports/             # HTML reports get saved here
├── main.py              # Entry point
├── config.json          # Configuration file
├── README.md
└── requirements.txt
🧪 Why Use This?
No BS, just recon.

Easy to add new modules or tweak existing ones.

Good starting point if you’re learning Python + web recon.

Saves time — all basic recon in one run.

📦 Setup
Install requirements

bash
Copy
Edit
pip install -r requirements.txt
Run the tool

bash
Copy
Edit
python main.py -d example.com
That’s it.

🛠️ Roadmap
 Add Shodan integration

 JavaScript link parser

 Passive OSINT plugins

 Port scan module

🧠 Notes
Tested on Linux (Ubuntu/Debian)

Needs chromedriver for screenshots (already handled in setup)

Doesn’t rely on paid APIs

Use responsibly ⚠️

🤝 Contributing
PRs and feedback are welcome. If you build a new module, fork it and drop a PR.

📜 License
MIT – do whatever you want, just don’t be a jerk with it.
