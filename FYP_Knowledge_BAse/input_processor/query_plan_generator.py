#!/usr/bin/env python3
"""
PostgreSQL Query Plan Parser
Parses EXPLAIN (FORMAT JSON) output and generates compact query plan summaries
"""

import json
import re
from pathlib import Path


def clean_json_string(json_str):
    """
    Clean JSON string by removing '+' line continuation characters and normalizing whitespace.
    
    Args:
        json_str: Raw JSON string with potential '+' continuations
        
    Returns:
        Cleaned JSON string
    """
    # Remove '+' continuation characters followed by newline
    cleaned = re.sub(r'\+\s*\n', '', json_str)
    # Normalize whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()


def extract_node_summary(node, depth=0):
    """
    Recursively extract a compact summary of a query plan node.
    
    Args:
        node: Dictionary representing a plan node
        depth: Current recursion depth
        
    Returns:
        String representation of the node in format: NodeType(cost=X.X)(child1; child2; ...)
    """
    if not isinstance(node, dict):
        return ""
    
    node_type = node.get("Node Type", "Unknown")
    total_cost = node.get("Total Cost", 0)
    
    # Format: NodeType(cost=X.X)
    summary = f"{node_type}(cost={total_cost:.1f})"
    
    # Process child plans
    plans = node.get("Plans", [])
    if plans:
        child_summaries = []
        for child_plan in plans:
            child_summary = extract_node_summary(child_plan, depth + 1)
            if child_summary:
                child_summaries.append(child_summary)
        
        if child_summaries:
            # Join child summaries with semicolons
            summary += "(" + "; ".join(child_summaries) + ")"
    
    return summary


def parse_query_plans_from_file(file_path):
    """
    Parse query plans from a file containing PostgreSQL EXPLAIN output.
    
    Args:
        file_path: Path to the input file
        
    Returns:
        List of query plan summaries
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content by "(N row)" pattern which separates different queries
    query_sections = re.split(r'\(\d+\s+rows?\)', content)
    
    query_plans = []
    
    for section in query_sections:
        section = section.strip()
        if not section:
            continue
        
        # Extract JSON array from the section
        # Look for the JSON array pattern: [ ... ]
        json_match = re.search(r'(\[.*?\])\s*$', section, re.DOTALL)
        
        if not json_match:
            continue
        
        json_str = json_match.group(1)
        
        # Clean the JSON string
        cleaned_json = clean_json_string(json_str)
        
        try:
            # Parse JSON
            data = json.loads(cleaned_json)
            
            if isinstance(data, list) and len(data) > 0:
                # Get the first element which contains the Plan
                plan_data = data[0]
                
                if "Plan" in plan_data:
                    # Extract compact summary
                    summary = extract_node_summary(plan_data["Plan"])
                    if summary:
                        query_plans.append(summary)
        
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(f"Cleaned JSON preview: {cleaned_json[:200]}...")
            continue
    
    return query_plans


def save_to_text(query_plans, output_file):
    """Save query plans to a text file."""
    output_path = Path(output_file)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("PostgreSQL Query Plan Summaries\n")
        f.write("=" * 80 + "\n\n")
        
        for i, plan in enumerate(query_plans, 1):
            f.write(f"Query {i}:\n")
            f.write(f"{plan}\n")
            f.write("-" * 80 + "\n\n")
    
    print(f"Saved text output to: {output_path}")


def save_to_json(query_plans, output_file):
    """Save query plans to a JSON file."""
    output_path = Path(output_file)
    
    data = {
        "query_plans": query_plans,
        "count": len(query_plans)
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved JSON output to: {output_path}")


def save_as_python_list(query_plans, output_file):
    """Save query plans as a Python list definition."""
    output_path = Path(output_file)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# PostgreSQL Query Plans\n")
        f.write("# Auto-generated query plan summaries\n\n")
        f.write("query_plans = [\n")
        
        for plan in query_plans:
            # Escape quotes in the plan string
            escaped_plan = plan.replace('"', '\\"')
            f.write(f'    "{escaped_plan}",\n')
        
        f.write("]\n")
    
    print(f"Saved Python list to: {output_path}")


def main():
    """Main function to demonstrate usage."""
    # Get the script's directory
    script_dir = Path(__file__).parent.parent
    
    # Default input file path relative to script
    input_file = script_dir / "olap_input_files" / "job_0_plans.txt"
    
    try:
        # Parse query plans
        print(f"Parsing query plans from: {input_file}")
        query_plans = parse_query_plans_from_file(input_file)
        
        print(f"\nExtracted {len(query_plans)} query plans:\n")
        
        # Display plans
        for i, plan in enumerate(query_plans, 1):
            print(f"Query {i}:")
            print(f"  {plan}\n")
        
        # Get the input file's directory for output files
        output_dir = input_file.parent
        
        # Save to same directory as input file

        save_to_json(query_plans, output_dir / "query_plans.json")
        
        
        print("\n✓ All outputs generated successfully!")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease ensure the input file exists at the specified path.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()