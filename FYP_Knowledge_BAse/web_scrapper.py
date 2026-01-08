import asyncio
import os
from crawl4ai import *
from datetime import datetime
import re
from url_list import urls

def extract_domain_name(url):
    """Extract domain name from URL using regex.
    
    """
    match = re.search(r'www\.([a-zA-Z0-9-]+)\.', url)
    if match:
        return match.group(1)
    return "data"

async def main():
    # Create resources folder if it doesn't exist
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_folder = os.path.join(script_dir, "resources")
    if not os.path.exists(resources_folder):
        os.makedirs(resources_folder)
    
    for url in urls:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=url,
            )
            
            # Extract domain name for filename
            domain_name = extract_domain_name(url)
            
            # Save full content as markdown in resources folder
            md_filename = os.path.join(resources_folder, f"{domain_name}.md")
            with open(md_filename, 'w', encoding='utf-8') as f:
                f.write(f"# {domain_name.upper()}\n\n")
                f.write(f"**Source:** {result.url}\n")
                f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
                f.write("---\n\n")
                f.write(result.markdown)
            print(f"✓ Markdown saved to {md_filename}")

if __name__ == "__main__":
    asyncio.run(main())