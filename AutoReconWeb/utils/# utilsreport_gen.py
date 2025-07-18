# utils/report_gen.py
import json
import os
from jinja2 import Environment, FileSystemLoader
import datetime

def generate_report(data, output_dir="reports"):
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate JSON report
    json_report = os.path.join(output_dir, "report.json")
    with open(json_report, 'w') as f:
        json.dump(data, f, indent=4)
    
    # Generate HTML report
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report_template.html')
    
    html_report = os.path.join(output_dir, "report.html")
    with open(html_report, 'w') as f:
        f.write(template.render(
            data=data,
            generated_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            title=f"AutoRecon Web Report - {data.get('target', 'Unknown')}"
        ))
    
    return json_report, html_report