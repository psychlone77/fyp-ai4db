import json
import os
from pathlib import Path
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from dotenv import load_dotenv
load_dotenv()


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
    
    # Read config schema by executing the Python file
    config_schema_path = script_dir.parent / 'llm_output' / 'config_schema.py'
    config_schema_globals = {}
    with open(config_schema_path, 'r') as f:
        exec(f.read(), config_schema_globals)
    config_schema = config_schema_globals['config_schema']
    
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
2. recommended_value: the specific value or range recommended (e.g., "64MB-256MB", "160MB", "1.1", "8")
3. unit: unit if applicable (MB, GB, ms, or null for dimensionless)
4. reasoning: brief summary of why this value is recommended
5. workload_context: OLAP, OLTP, or general

IMPORTANT: 
- Only include knobs that exist in the config_params list
- Extract numeric values and ranges accurately
- Preserve units (MB, GB, ms, etc.)
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

def validate_and_enrich(parsed_knobs: Dict, config_schema: Dict) -> List[Dict]:
    """Validate parsed knobs against schema and add schema information"""
    
    validated_knobs = []
    
    for knob in parsed_knobs.get('knobs', []):
        knob_name = knob.get('knob_name')
        
        # Check if knob exists in schema
        if knob_name not in config_schema:
            print(f"Warning: Knob '{knob_name}' not found in config schema, skipping...")
            continue
        
        schema_info = config_schema[knob_name]
        
        # Enrich with schema information
        enriched_knob = {
            'knob_name': knob_name,
            'recommended_value': knob.get('recommended_value'),
            'unit': knob.get('unit'),
            'reasoning': knob.get('reasoning'),
            'workload_context': knob.get('workload_context'),
            'schema_info': {
                'type': schema_info.get('type'),
                'min': schema_info.get('min'),
                'max': schema_info.get('max'),
                'default': schema_info.get('default'),
                'step': schema_info.get('step')
            }
        }
        
        validated_knobs.append(enriched_knob)
    
    return validated_knobs

def format_output(knobs: List[Dict]) -> str:
    """Format knobs for display"""
    output = []
    output.append("=" * 80)
    output.append("STRUCTURED KNOB RECOMMENDATIONS")
    output.append("=" * 80)
    output.append("")
    
    for i, knob in enumerate(knobs, 1):
        output.append(f"{i}. {knob['knob_name']}")
        output.append(f"   Recommended: {knob['recommended_value']} {knob.get('unit', '')}")
        output.append(f"   Context: {knob['workload_context']}")
        output.append(f"   Reasoning: {knob['reasoning']}")
        output.append(f"   Schema: type={knob['schema_info']['type']}, "
                     f"range=[{knob['schema_info']['min']}, {knob['schema_info']['max']}], "
                     f"default={knob['schema_info']['default']}")
        output.append("")
    
    return "\n".join(output)

def main():
    """Main execution function"""
    print("Loading files...")
    rag_output, config_schema, script_dir = load_files()
    
    print("Parsing knobs with LLM...")
    parsed_knobs = parse_knobs_with_llm(rag_output, config_schema)
    
    print("Validating and enriching...")
    validated_knobs = validate_and_enrich(parsed_knobs, config_schema)
    
    print(f"\nFound {len(validated_knobs)} valid knob recommendations\n")
    
    # Format and display
    formatted_output = format_output(validated_knobs)
    print(formatted_output)
    
    # Save to JSON
    output_file = script_dir / 'structured_knob_recommendations.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_knobs': len(validated_knobs),
            'knobs': validated_knobs
        }, f, indent=2)
    
    print(f"\nStructured output saved to: {output_file}")
    
    # Save formatted text
    text_output_file = script_dir / 'structured_knob_recommendations.txt'
    with open(text_output_file, 'w', encoding='utf-8') as f:
        f.write(formatted_output)
    
    print(f"Text output saved to: {text_output_file}")

if __name__ == "__main__":
    main()