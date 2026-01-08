import asyncio
import os
from crawl4ai import *
from datetime import datetime
import re
from url_list import urls

def extract_filename_from_url(url):
    """Extract a unique filename from URL using domain and path.
    
    """
    # Extract domain name
    domain_match = re.search(r'www\.([a-zA-Z0-9-]+)\.', url)
    domain = domain_match.group(1) if domain_match else "data"
    
    # Extract last meaningful part of the path (before .html or similar)
    path_match = re.search(r'/([a-zA-Z0-9_-]+)(?:\.\w+)?$', url)
    if path_match:
        path_part = path_match.group(1)
        return f"{domain}-{path_part}"
    
    return domain

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
            
            # Extract unique filename from URL
            filename = extract_filename_from_url(url)
            
            # Save full content as markdown in resources folder
            md_filename = os.path.join(resources_folder, f"{filename}.md")
            with open(md_filename, 'w', encoding='utf-8') as f:
                f.write(f"# {filename.upper()}\n\n")
                f.write(f"**Source:** {result.url}\n")
                f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
                f.write("---\n\n")
                f.write(result.markdown)
            print(f"✓ Markdown saved to {md_filename}")

if __name__ == "__main__":
    asyncio.run(main())