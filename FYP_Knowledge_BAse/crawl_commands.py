import os
import asyncio
import json
from dotenv import load_dotenv
from crawl4ai import (
    AsyncWebCrawler, 
    BrowserConfig, 
    CrawlerRunConfig, 
    CacheMode,
    LLMExtractionStrategy,
    LLMConfig
)

from pydantic import BaseModel
import re

# Load environment variables from .env file
load_dotenv()


def extract_url(md_string):
    """Extract URL from markdown link format."""
    match = re.search(r'\[[^\]]*\]\(([^)]*)\)', md_string)
    if match:
        raw_url = match.group(1).strip()
        raw_url = re.sub(r'\s*".*"$', '', raw_url)
        cleaned_url = re.sub(r'</[^>]*>', '', raw_url)
        return cleaned_url
    return md_string


async def crawl_and_extract(url, prompt, browser_cfg):
    """
    Generic function to crawl a URL and extract information based on a prompt.
    Uses Groq API for LLM extraction.
    """
    url = extract_url(url)
    print(f"\n{'='*60}")
    print(f"Crawling URL: {url}")
    print(f"Prompt: {prompt}")
    print(f"{'='*60}\n")

    # Create LLM config for Groq
    llm_config = LLMConfig(
        provider="groq/openai/gpt-oss-120b",
        api_token=os.getenv("GROQ_API_KEY")
    )

    # Use Groq with crawl4ai
    llm_strategy = LLMExtractionStrategy(
        llm_config=llm_config,
        extraction_type="schema",
        instruction=prompt,
        chunk_token_threshold=2000,
        overlap_rate=0.1, 
        apply_chunking=False,
        input_format="markdown",
        extra_args={
            "temperature": 0.3,
            "max_tokens": 8000,
            "top_p": 1
        },
        verbose=True,
        schema={
            "type": "object",
            "properties": {
                "result": {
                    "type": "string",
                    "description": "The extracted information"
                }
            },
            "required": ["result"]
        }
    )

    # Configure the crawler
    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS,
        process_iframes=False,
        remove_overlay_elements=True,
        excluded_tags=["form", "header", "footer"],
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(url=url, config=crawl_config)

        if result.success:
            print(f"\n✓ Crawl successful")
            print(f"Raw extracted content: {result.extracted_content}")
            
            # Try to parse the result
            try:
                if not result.extracted_content or result.extracted_content == "[]":
                    print("⚠ Warning: Empty extraction result")
                    return None
                
                # Parse JSON response
                response_json = json.loads(result.extracted_content)
                
                # Handle different response formats
                if isinstance(response_json, list):
                    if len(response_json) == 0:
                        print("⚠ Warning: Empty list in response")
                        return None
                    # Try to extract from list format
                    if "content" in response_json[0]:
                        extracted_content = str(response_json[0]["content"][0]).strip()
                    elif "result" in response_json[0]:
                        extracted_content = str(response_json[0]["result"]).strip()
                    else:
                        extracted_content = str(response_json[0]).strip()
                elif isinstance(response_json, dict):
                    # Try to extract from dict format
                    if "result" in response_json:
                        extracted_content = str(response_json["result"]).strip()
                    elif "content" in response_json:
                        extracted_content = str(response_json["content"]).strip()
                    else:
                        extracted_content = str(response_json).strip()
                else:
                    extracted_content = str(response_json).strip()
                
                print(f"✓ Extracted: {extracted_content}")
                
                # Show token usage if available
                if hasattr(llm_strategy, 'show_usage'):
                    llm_strategy.show_usage()
                
                return extracted_content
                
            except (json.JSONDecodeError, KeyError, IndexError, TypeError) as e:
                print(f"✗ Error parsing extracted content: {e}")
                print(f"Raw content was: {result.extracted_content}")
                return None
        else:
            print(f"✗ Crawl failed: {result.error_message}")
            return None


async def main():
    # Check for API key
    if not os.getenv("GROQ_API_KEY"):
        print("✗ Error: GROQ_API_KEY environment variable not set")
        print("\nTo fix this:")
        print("1. Get your API key from https://console.groq.com/keys")
        print("2. Create a .env file with: GROQ_API_KEY=your-key-here")
        print("3. Or set environment variable: set GROQ_API_KEY=your-key-here")
        return
    
    # Target URL for PostgreSQL tuning parameters
    website_url = "https://www.tigerdata.com/learn/postgresql-performance-tuning-key-parameters"

    # Define the commands to extract parameter relationships
    commands = [
        """Extract all PostgreSQL tuning parameters mentioned in the article. 
        For each parameter, provide: parameter name, its purpose, and recommended values. 
        Format as JSON array with structure: [{"parameter": "name", "purpose": "description", "recommended_value": "value"}]""",
        
        """Identify relationships between PostgreSQL parameters. 
        List which parameters affect or depend on each other. 
        Format as JSON array: [{"parameter1": "name1", "parameter2": "name2", "relationship": "how they relate"}]""",
        
        """Extract any performance implications or trade-offs mentioned for these parameters. 
        Format as JSON array: [{"parameter": "name", "impact": "performance effect", "tradeoff": "what you sacrifice"}]""",
    ]

    # Create a browser config
    browser_cfg = BrowserConfig(headless=True)

    # Track results - all commands operate on the same URL
    results = {}

    # Process each command on the same URL
    for i, prompt in enumerate(commands, 1):
        print(f"\n{'#'*60}")
        print(f"# EXTRACTION {i}/{len(commands)}")
        print(f"{'#'*60}")
        
        # Crawl and extract
        result = await crawl_and_extract(website_url, prompt, browser_cfg)

        if result:
            # Store results with descriptive keys
            if i == 1:
                results['parameters'] = result
            elif i == 2:
                results['relationships'] = result
            elif i == 3:
                results['performance_implications'] = result
                
            print(f"\n✓ Extraction {i} completed successfully")
            print(f"Result preview: {result[:200]}..." if len(result) > 200 else f"Result: {result}")
        else:
            print(f"\n✗ Extraction {i} failed")
            # Continue to next extraction even if one fails
            continue
    
    # Summary and save results
    print(f"\n{'='*60}")
    print("EXTRACTION SUMMARY")
    print(f"{'='*60}")
    
    for key, value in results.items():
        print(f"\n{key.upper()}:")
        print(f"{value[:300]}..." if len(value) > 300 else value)
    
    # Save to file
    output_file = "postgres_tuning_relationships.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Results saved to {output_file}")
    except Exception as e:
        print(f"\n✗ Error saving results: {e}")


if __name__ == "__main__":
    asyncio.run(main())