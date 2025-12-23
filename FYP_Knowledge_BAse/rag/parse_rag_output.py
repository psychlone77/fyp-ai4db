import json
import os
import re
from pathlib import Path
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union, Tuple
from dotenv import load_dotenv
load_dotenv()

RAM = 40  # System RAM in GB (configurable)

# ========== UNIT CONVERSION FUNCTIONS ==========

def parse_memory_unit(value_str: str) -> Tuple[float, str]:
    """
    Extract numeric value and unit from memory string.
    Returns: (value, unit) e.g., ("32 MB") -> (32.0, "MB")
    """
    match = re.search(r'(\d+\.?\d*)\s*(KB|MB|GB|TB|kb|mb|gb|tb)', value_str, re.IGNORECASE)
    if match:
        return (float(match.group(1)), match.group(2).upper())
    return (None, None)

def parse_time_unit(value_str: str) -> Tuple[float, str]:
    """
    Extract numeric value and unit from time string.
    Returns: (value, unit) e.g., ("30min") -> (30.0, "min")
    """
    match = re.search(r'(\d+\.?\d*)\s*(s|sec|second|min|minute|h|hr|hour|ms|millisecond)s?', value_str, re.IGNORECASE)
    if match:
        return (float(match.group(1)), match.group(2).lower())
    return (None, None)

def parse_percentage(value_str: str) -> Union[float, Tuple[float, float], None]:
    """
    Parse percentage strings with flexible formatting.
    "5% of RAM" -> 5.0
    "≈ 5 % of system RAM" -> 5.0
    "25%–40% of RAM" -> (25.0, 40.0)
    "25 % – 40 % of total system RAM" -> (25.0, 40.0)
    """
    if 'ram' not in value_str.lower() or '%' not in value_str:
        return None
    
    # Clean up - remove all RAM-related text and special chars
    cleaned = value_str.replace('≈', '').replace('of RAM', '').replace('of ram', '')
    cleaned = cleaned.replace('of system RAM', '').replace('of total system RAM', '')
    cleaned = cleaned.replace('of total RAM', '').strip()
    
    # Check for range - handles spaces around % and various dash types (–, -, ‑)
    # Pattern matches: "25 % – 40 %", "25%–40%", "25%-40%", "25 %‑40 %"
    range_match = re.search(r'(\d+\.?\d*)\s*%\s*[–\-‑]\s*(\d+\.?\d*)\s*%', cleaned)
    if range_match:
        return (float(range_match.group(1)), float(range_match.group(2)))
    
    # Single percentage - handles "5 %" or "5%"
    single_match = re.search(r'(\d+\.?\d*)\s*%', cleaned)
    if single_match:
        return float(single_match.group(1))
    
    return None

def parse_range(value_str: str) -> Union[Tuple[str, str], None]:
    """
    Parse range string with various dash types.
    "10-50 MB" -> ("10 MB", "50 MB")
    "10 – 50 MB" -> ("10 MB", "50 MB")
    "30min-1h" -> ("30min", "1h")
    "4-6" -> ("4", "6")
    "4‑6" -> ("4", "6")  (non-breaking hyphen U+2011)
    """
    # Try to find range with units - handles multiple dash types: -, –, ‑
    range_match = re.match(r'(\d+\.?\d*)\s*([A-Za-z]*)\s*[-–‑]\s*(\d+\.?\d*)\s*([A-Za-z]*)', value_str.strip())
    if range_match:
        min_val, min_unit, max_val, max_unit = range_match.groups()
        # If min has no unit but max does, apply max unit to min too
        if not min_unit and max_unit:
            min_unit = max_unit
        return (f"{min_val} {min_unit}".strip(), f"{max_val} {max_unit}".strip())
    
    # Simple numeric range - handles -, –, ‑
    simple_range = re.match(r'(\d+\.?\d*)\s*[-–‑]\s*(\d+\.?\d*)', value_str.strip())
    if simple_range:
        return (simple_range.group(1), simple_range.group(2))
    
    return None

def memory_to_mb(value: float, unit: str) -> float:
    """Convert memory value to MB."""
    conversions = {
        'KB': 1 / 1024,
        'MB': 1,
        'GB': 1024,
        'TB': 1024 * 1024
    }
    return value * conversions.get(unit.upper(), 1)

def time_to_seconds(value: float, unit: str) -> float:
    """Convert time value to seconds."""
    conversions = {
        's': 1, 'sec': 1, 'second': 1,
        'min': 60, 'minute': 60,
        'h': 3600, 'hr': 3600, 'hour': 3600,
        'ms': 0.001, 'millisecond': 0.001
    }
    return value * conversions.get(unit.lower(), 1)

def convert_to_target_unit(value_mb: float, target_unit: str, value_type: str = 'integer') -> Union[int, float]:
    """
    Convert MB to target unit based on config schema unit.
    
    Args:
        value_mb: Value in MB
        target_unit: Target unit from schema (e.g., "8KB", "1KB", "count")
        value_type: "integer" or "float"
    """
    target_unit_lower = target_unit.lower().strip()
    
    if '8kb' in target_unit_lower or '8 kb' in target_unit_lower:
        # Convert MB to 8KB blocks: MB * 128
        result = value_mb * 128
    elif 'kb' in target_unit_lower:
        # Convert MB to 1KB blocks: MB * 1024
        result = value_mb * 1024
    else:
        # Direct value (MB or count)
        result = value_mb
    
    return int(round(result)) if value_type == 'integer' else float(result)

def convert_time_to_target_unit(seconds: float, target_unit: str, value_type: str = 'integer') -> Union[int, float]:
    """
    Convert seconds to target time unit based on config schema unit.
    
    Args:
        seconds: Value in seconds
        target_unit: Target unit from schema (e.g., "s", " s", "milli s", "micro s", "ms")
        value_type: "integer" or "float"
    """
    target_unit_lower = target_unit.lower().strip()
    
    if 'micro' in target_unit_lower:
        # Convert to microseconds: seconds * 1,000,000
        result = seconds * 1_000_000
    elif 'milli' in target_unit_lower or target_unit_lower == 'ms':
        # Convert to milliseconds: seconds * 1,000
        result = seconds * 1000
    else:
        # Keep as seconds (handles "s", " s", "sec", "second")
        result = seconds
    
    return int(round(result)) if value_type == 'integer' else float(result)

def convert_recommended_value(
    knob_name: str,
    recommended_value: str,
    config_schema: Dict,
    system_ram_gb: float = 40,
    reasoning: str = ""
) -> Dict:
    """
    Convert recommended value to expected unit from config schema.
    
    Returns dict with:
        - converted_value: Single value or "min - max" string
        - converted_min: Min value (for ranges)
        - converted_max: Max value (for ranges)
        - is_range: Boolean
        - original_value: Original recommendation
    """
    if not recommended_value or knob_name not in config_schema:
        return {'original_value': recommended_value, 'converted_value': None}
    
    schema = config_schema[knob_name]
    target_unit = schema.get('unit', '').strip()
    value_type = schema.get('type', 'integer')
    
    result = {
        'original_value': recommended_value,
        'converted_value': None,
        'is_range': False,
        'target_unit': target_unit
    }
    
    # Handle percentage of RAM
    percentage = parse_percentage(recommended_value)
    if percentage is not None:
        if isinstance(percentage, tuple):
            # Range: "25%–40% of RAM"
            min_pct, max_pct = percentage
            min_gb = (min_pct / 100) * system_ram_gb
            max_gb = (max_pct / 100) * system_ram_gb
            
            min_val = convert_to_target_unit(min_gb * 1024, target_unit, value_type)
            max_val = convert_to_target_unit(max_gb * 1024, target_unit, value_type)
            
            result['converted_min'] = min_val
            result['converted_max'] = max_val
            result['converted_value'] = f"{min_val} - {max_val}"
            result['is_range'] = True
        else:
            # Single: "5% of RAM"
            value_gb = (percentage / 100) * system_ram_gb
            converted = convert_to_target_unit(value_gb * 1024, target_unit, value_type)
            result['converted_value'] = converted
        
        return result
    
    # Handle ranges (memory or numeric)
    range_vals = parse_range(recommended_value)
    if range_vals:
        min_str, max_str = range_vals
        result['is_range'] = True
        
        # Check if it's memory range
        min_mem = parse_memory_unit(min_str)
        max_mem = parse_memory_unit(max_str)
        
        if min_mem[0] is not None and max_mem[0] is not None:
            # Memory range: "10-50 MB"
            min_mb = memory_to_mb(min_mem[0], min_mem[1])
            max_mb = memory_to_mb(max_mem[0], max_mem[1])
            
            result['converted_min'] = convert_to_target_unit(min_mb, target_unit, value_type)
            result['converted_max'] = convert_to_target_unit(max_mb, target_unit, value_type)
            result['converted_value'] = f"{result['converted_min']} - {result['converted_max']}"
        else:
            # Check if it's time range
            min_time = parse_time_unit(min_str)
            max_time = parse_time_unit(max_str)
            
            if min_time[0] is not None and max_time[0] is not None:
                # Time range: "30min-1h"
                min_sec = time_to_seconds(min_time[0], min_time[1])
                max_sec = time_to_seconds(max_time[0], max_time[1])
                
                # Convert to target unit (microseconds, milliseconds, or seconds)
                result['converted_min'] = convert_time_to_target_unit(min_sec, target_unit, value_type)
                result['converted_max'] = convert_time_to_target_unit(max_sec, target_unit, value_type)
                result['converted_value'] = f"{result['converted_min']} - {result['converted_max']}"
            else:
                # Simple numeric range: "4-6"
                try:
                    min_val = float(min_str)
                    max_val = float(max_str)
                    result['converted_min'] = int(min_val) if value_type == 'integer' else min_val
                    result['converted_max'] = int(max_val) if value_type == 'integer' else max_val
                    result['converted_value'] = f"{result['converted_min']} - {result['converted_max']}"
                except ValueError:
                    pass
        
        return result
    
    # Handle single memory value: "16 MB"
    mem_val = parse_memory_unit(recommended_value)
    if mem_val[0] is not None:
        value_mb = memory_to_mb(mem_val[0], mem_val[1])
        result['converted_value'] = convert_to_target_unit(value_mb, target_unit, value_type)
        return result
    
    # Handle single time value: "60s"
    time_val = parse_time_unit(recommended_value)
    if time_val[0] is not None:
        seconds = time_to_seconds(time_val[0], time_val[1])
        result['converted_value'] = convert_time_to_target_unit(seconds, target_unit, value_type)
        return result
    
    # Handle simple numeric value: "0.9", "50", "2"
    try:
        value = float(recommended_value.strip())
        
        # Check reasoning for context clues about the actual unit
        if reasoning and ('ram' in reasoning.lower() or 'gb' in reasoning.lower() or 'memory' in reasoning.lower()):
            # If reasoning mentions RAM/GB/memory and target is KB, assume GB
            if 'kb' in target_unit.lower() and value < 100:
                # Likely GB value (e.g., "2" means 2 GB based on "~5% of RAM" in reasoning)
                value_mb = value * 1024  # Convert GB to MB
                result['converted_value'] = convert_to_target_unit(value_mb, target_unit, value_type)
                return result
        
        # For memory parameters without clear context
        if ('kb' in target_unit.lower()) and value < 100:
            # Assume GB for small numbers with memory units
            value_mb = value * 1024
            result['converted_value'] = convert_to_target_unit(value_mb, target_unit, value_type)
        else:
            # Direct value (for fractions, counts, etc.)
            result['converted_value'] = int(value) if value_type == 'integer' else value
    except ValueError:
        pass
    
    return result

# Define the output structure
class KnobRecommendation(BaseModel):
    knob_name: str = Field(description="PostgreSQL configuration parameter name")
    recommended_value: Optional[str] = Field(description="Recommended value or range")
    unit: Optional[str] = Field(description="Unit of measurement (MB, GB, etc.)")
    reasoning: Optional[str] = Field(description="Brief explanation for the recommendation")
    workload_context: Optional[str] = Field(description="Workload context (OLAP, OLTP, etc.)")

class StructuredKnobOutput(BaseModel):
    knobs: List[KnobRecommendation] = Field(description="List of knob recommendations")

def load_files():
    """Load RAG output and config schema"""
    script_dir = Path(__file__).parent
    
    # Read RAG output JSON
    rag_results_path = script_dir / 'rag_results.json'
    with open(rag_results_path, 'r', encoding='utf-8') as f:
        rag_data = json.load(f)
    
    # Combine all query-answer pairs into a single text for parsing
    rag_output = ""
    for item in rag_data:
        query = item.get('query', '')
        answer = item.get('answer', '')
        rag_output += f"\nQuery: {query}\n"
        rag_output += f"Answer: {answer}\n"
        rag_output += "="*80 + "\n"
    
    # Read config schema from JSON file
    config_schema_path = script_dir.parent / 'config_map' / 'config_schema.json'
    with open(config_schema_path, 'r', encoding='utf-8') as f:
        config_schema = json.load(f)
    
    return rag_output, config_schema, script_dir

def parse_knobs_with_llm(rag_output: str, config_schema: Dict) -> Dict:
    """Use Groq LLM to parse knob recommendations from RAG output"""
    
    # Initialize LLM
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="openai/gpt-oss-120b",
        temperature=0.3
    )
    
    # Create parser
    parser = JsonOutputParser(pydantic_object=StructuredKnobOutput)
    
    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a PostgreSQL database tuning expert. Your task is to extract structured knob recommendations from RAG output.

Available PostgreSQL configuration parameters:
{config_params}

Extract ONLY the knobs that are mentioned in the RAG output and exist in the config schema above.
For each knob, provide:
1. knob_name: exact parameter name from the schema
2. recommended_value: PRESERVE THE EXACT recommendation as stated in the RAG output, including units and percentages
   Examples: "25%–40% of RAM", "10-50 MB", "2 GB", "≈5% of RAM", "30min-1h", "0.9"
3. unit: unit if explicitly mentioned (MB, GB, ms, s, etc.) or null if not specified
4. reasoning: brief summary of why this value is recommended
5. workload_context: OLAP, OLTP, or general

IMPORTANT: 
- Only include knobs that exist in the config_params list
- PRESERVE units and context in recommended_value (e.g., "25% of RAM" NOT just "25")
- Keep the FULL recommendation string with percentages, ranges, and units intact
- Keep reasoning concise (1-2 sentences max)

{format_instructions}"""),
        ("user", "RAG Output to parse:\n\n{rag_output}")
    ])
    
    # Get list of available config parameters
    config_params = list(config_schema.keys())
    
    # Create chain
    chain = prompt | llm | parser
    
    # Execute
    result = chain.invoke({
        "config_params": json.dumps(config_params, indent=2),
        "rag_output": rag_output,
        "format_instructions": parser.get_format_instructions()
    })
    
    return result

def validate_and_enrich(parsed_knobs: Dict, config_schema: Dict, system_ram_gb: float = 40) -> List[Dict]:
    """Validate parsed knobs against schema and add schema information with unit conversion"""
    
    validated_knobs = []
    
    for knob in parsed_knobs.get('knobs', []):
        knob_name = knob.get('knob_name')
        
        # Check if knob exists in schema
        if knob_name not in config_schema:
            print(f"Warning: Knob '{knob_name}' not found in config schema, skipping...")
            continue
        
        schema_info = config_schema[knob_name]
        recommended_value = knob.get('recommended_value', '')
        
        # Convert recommended value to expected unit
        conversion_result = convert_recommended_value(
            knob_name,
            recommended_value,
            config_schema,
            system_ram_gb,
            reasoning=knob.get('reasoning', '')
        )
        
        # Enrich with schema information and converted values
        enriched_knob = {
            'knob_name': knob_name,
            'recommended_value': recommended_value,
            'converted_value': conversion_result.get('converted_value'),
            'target_unit': schema_info.get('unit'),
            'reasoning': knob.get('reasoning'),
            'workload_context': knob.get('workload_context'),
            'schema_info': {
                'type': schema_info.get('type'),
                'min': schema_info.get('min'),
                'max': schema_info.get('max'),
                'default': schema_info.get('default'),
                'step': schema_info.get('step'),
                'unit': schema_info.get('unit')
            }
        }
        
        # Add range info if applicable
        if conversion_result.get('is_range'):
            enriched_knob['converted_min'] = conversion_result.get('converted_min')
            enriched_knob['converted_max'] = conversion_result.get('converted_max')
            enriched_knob['is_range'] = True
        
        validated_knobs.append(enriched_knob)
    
    return validated_knobs

def format_output(knobs: List[Dict], system_ram_gb: float = 40) -> str:
    """Format knobs for display with converted values"""
    output = []
    output.append("=" * 110)
    output.append(f"STRUCTURED KNOB RECOMMENDATIONS (System RAM: {system_ram_gb} GB)")
    output.append("=" * 110)
    output.append("")
    
    for i, knob in enumerate(knobs, 1):
        output.append(f"{i}. {knob['knob_name']}")
        output.append(f"   Original Recommendation: {knob.get('recommended_value', 'N/A')}")
        
        if knob.get('converted_value') is not None:
            output.append(f"   Converted Value: {knob['converted_value']}")
            if knob.get('is_range'):
                output.append(f"   Range: [{knob.get('converted_min')} - {knob.get('converted_max')}]")
            output.append(f"   Target Unit: {knob.get('target_unit', 'N/A')}")
        else:
            output.append(f"   Converted Value: [Could not convert]")
        
        output.append(f"   Workload Context: {knob.get('workload_context', 'N/A')}")
        output.append(f"   Reasoning: {knob.get('reasoning', 'N/A')}")
        
        schema = knob.get('schema_info', {})
        output.append(f"   Schema: type={schema.get('type', 'N/A')}, "
                     f"range=[{schema.get('min', 'N/A')}, {schema.get('max', 'N/A')}], "
                     f"default={schema.get('default', 'N/A')}")
        output.append("")
    
    return "\n".join(output)

def main():
    """Main execution function"""
    system_ram_gb = RAM  # Use global RAM setting
    
    print("Loading files...")
    rag_output, config_schema, script_dir = load_files()
    
    print("Parsing knobs with LLM...")
    parsed_knobs = parse_knobs_with_llm(rag_output, config_schema)
    
    print(f"Validating and enriching with unit conversion (System RAM: {system_ram_gb} GB)...")
    validated_knobs = validate_and_enrich(parsed_knobs, config_schema, system_ram_gb)
    
    print(f"\nFound {len(validated_knobs)} valid knob recommendations\n")
    
    # Format and display
    formatted_output = format_output(validated_knobs, system_ram_gb)
    print(formatted_output)
    
    # Save to JSON
    output_file = script_dir / 'structured_knob_recommendations.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_knobs': len(validated_knobs),
            'system_ram_gb': system_ram_gb,
            'knobs': validated_knobs
        }, f, indent=2)
    
    print(f"\nStructured output saved to: {output_file}")
    
    
if __name__ == "__main__":
    main()