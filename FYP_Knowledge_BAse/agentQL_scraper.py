import asyncio
import json
import os
from datetime import datetime
from url_list import urls
from dotenv import load_dotenv
from agentql.client import Client as AgentQLClient
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

load_dotenv()

# Get API keys
AGENTQL_API_KEY = os.getenv("AGENTQL_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
groq_llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="mixtral-8x7b-32768",
    temperature=0.3
)

def extract_domain_name(url):
    """Extract domain name from URL using regex"""
    import re
    match = re.search(r'www\.([a-zA-Z0-9-]+)\.', url)
    if match:
        return match.group(1)
    return "data"

async def scrape_parameters_with_agentql(url: str):
    """
    Scrape database parameters from URL using AgentQL
    """
    extraction_prompt = """
    Extract all database tuning parameters from this page.
    Return a JSON with this structure:
    {
      "parameter_categories": [
        {
          "category_name": "string (e.g., Memory, Cache, Query Processing)",
          "description": "string"
        }
      ],
      "parameters": [
        {
          "parameter_name": "string",
          "category": "string",
          "description": "string",
          "recommended_value_oltp": "string or number",
          "recommended_value_olap": "string or number",
          "default_value": "string or number",
          "unit": "string (e.g., MB, percentage)",
          "impact": "string (High/Medium/Low)"
        }
      ]
    }
    Extract only the information present on the page. Be precise with values.
    """
    
    client = AgentQLClient(api_key=AGENTQL_API_KEY)
    
    print(f"Scraping with AgentQL: {url}")
    print("="*60)
    
    try:
        # Open page
        page = await client.get(url)
        
        # Extract structured data using AgentQL
        response = await page.query(extraction_prompt)
        
        # Parse response
        extracted_data = json.loads(response)
        
        return extracted_data
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
    finally:
        await page.close()

def process_with_groq(data: dict, domain: str, url: str):
    """
    Process extracted data with Groq for refinement and formatting
    """
    if not data:
        return None
    
    prompt_template = PromptTemplate(
        input_variables=["domain", "url", "data"],
        template="""
Analyze and refine the following database parameters extracted from {domain}:

Source: {url}
Data: {data}

Please:
1. Validate the parameter names and descriptions
2. Ensure OLTP and OLAP recommendations are realistic
3. Fill in any missing values with reasonable defaults based on database best practices
4. Organize parameters by category
5. Return as structured JSON

Return valid JSON only, no markdown formatting.
"""
    )
    
    formatted_prompt = prompt_template.format(
        domain=domain,
        url=url,
        data=json.dumps(data, indent=2)
    )
    
    print(f"Processing with Groq: {domain}")
    
    try:
        response = groq_llm.invoke(formatted_prompt)
        refined_data = json.loads(response.content)
        return refined_data
    except Exception as e:
        print(f"Error processing with Groq: {e}")
        return data

def save_results_markdown(data: dict, domain: str, url: str):
    """Save extracted parameters to markdown file"""
    filename = f"{domain}_parameters.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {domain.upper()} - Database Parameters\n\n")
        f.write(f"**Source:** {url}\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
        f.write("---\n\n")
        
        # Write categories
        if "parameter_categories" in data:
            f.write("## Categories\n\n")
            for cat in data["parameter_categories"]:
                f.write(f"### {cat.get('category_name', 'N/A')}\n")
                f.write(f"{cat.get('description', 'N/A')}\n\n")
        
        # Write parameters
        if "parameters" in data:
            f.write("## Parameters\n\n")
            for param in data["parameters"]:
                f.write(f"### {param.get('parameter_name', 'N/A')}\n\n")
                f.write(f"**Category:** {param.get('category', 'N/A')}\n\n")
                f.write(f"**Description:** {param.get('description', 'N/A')}\n\n")
                f.write(f"**Default Value:** {param.get('default_value', 'N/A')}\n\n")
                f.write(f"**OLTP Recommended:** {param.get('recommended_value_oltp', 'N/A')}\n\n")
                f.write(f"**OLAP Recommended:** {param.get('recommended_value_olap', 'N/A')}\n\n")
                f.write(f"**Unit:** {param.get('unit', 'N/A')}\n\n")
                f.write(f"**Impact:** {param.get('impact', 'N/A')}\n\n")
                f.write("---\n\n")
    
    print(f"✓ Results saved to {filename}")

async def main():
    all_parameters = {
        "generated": datetime.now().isoformat(),
        "sources": []
    }
    
    for url in urls:
        print(f"\n{'='*60}")
        
        # Step 1: Scrape with AgentQL
        data = await scrape_parameters_with_agentql(url)
        
        if data:
            domain = extract_domain_name(url)
            
            # Step 2: Refine with Groq
            refined_data = process_with_groq(data, domain, url)
            
            all_parameters["sources"].append({
                "url": url,
                "domain": domain,
                "data": refined_data
            })
            
            # Step 3: Save as markdown
            save_results_markdown(refined_data, domain, url)
    
    # Save consolidated JSON
    with open("all_parameters.json", 'w', encoding='utf-8') as f:
        json.dump(all_parameters, f, indent=2, ensure_ascii=False)
    print(f"\n✓ All results consolidated in all_parameters.json")

if __name__ == "__main__":
    asyncio.run(main())