"""
LLM-based RAG Question Generator
--------------------------------
Accepts structured thesis-style workload input consisting of:
- Workload features
- Query plans
- Inner performance metrics

Generates up to 5 high-quality RAG questions using an LLM (ChatGroq).
"""

import os
import re
import json
from typing import List, Dict, Any
from pathlib import Path

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
load_dotenv()

class LLMRAGQuestionGenerator:
    """
    Dynamically generates RAG-ready diagnostic and prescriptive questions
    from structured database workload summaries.
    """

    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="openai/gpt-oss-120b",
            temperature=0.3,
        )

    def generate_questions(
        self,
        workload_features: Dict[str, Any],
        query_plans: List[str],
        inner_metrics: Dict[str, Any],
    ) -> List[str]:
        """
        Generate up to 3 RAG questions from structured workload input.
        Output is a plain Python list of strings.
        """

        system_prompt = (
            "You are a database performance tuning expert.\n"
            "Your task is to generate concise, high-value questions that can be used\n"
            "to retrieve database configuration and tuning recommendations.\n\n"
            "Rules:\n"
            "- Generate AT MOST 3 questions\n"
            "- Focus on OLAP-style performance bottlenecks and tuning dimensions\n"
            "- Questions must be suitable for retrieval (RAG)\n"
            "- Avoid questions on indexing, partitioning, or physical design\n"
            "- Avoid generic database theory questions\n"
            "- Do not include answers, numbering, or explanations\n"
            "- Output ONLY the questions, one per line\n"
        )

        human_prompt = f"""
        Workload Features:
        {workload_features}

        Query Plans:
        {query_plans}

        Inner Metrics:
        {inner_metrics}

        Generate up to 3 concise questions.
        Each question must be a single sentence.
        """

        response = self.llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt),
            ]
        )

        return self._parse_questions(response.content)

    @staticmethod
    def _parse_questions(text: str) -> List[str]:
        """
        Convert raw LLM output into a clean Python list of questions.
        """
        lines = [line.strip("- •\t ") for line in text.split("\n") if line.strip()]
        questions = [line for line in lines if line.endswith("?")]
        return questions[:3]


def load_json_file(file_path: Path) -> Any:
    """
    Load and parse a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON data
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# -----------------------------
# Example usage (thesis-style input)
# -----------------------------
if __name__ == "__main__":
    # Get the script's directory and construct paths to input files
    script_dir = Path(__file__).parent.parent
    input_dir = script_dir / "olap_input_files"
    
    # Define input file paths
    workload_features_path = input_dir / "workload_features.json"
    query_plans_path = input_dir / "query_plans.json"
    inner_metrics_path = input_dir / "job_0_internal_metrics.json"
    
    try:
        # Load data from JSON files
        print(f"Loading workload features from: {workload_features_path}")
        workload_features = load_json_file(workload_features_path)
        
        print(f"Loading query plans from: {query_plans_path}")
        query_plans_data = load_json_file(query_plans_path)
        # Extract the query_plans list from the JSON structure
        query_plans = query_plans_data.get("query_plans", []) if isinstance(query_plans_data, dict) else query_plans_data
        
        print(f"Loading inner metrics from: {inner_metrics_path}")
        inner_metrics = load_json_file(inner_metrics_path)
        
        print("\n" + "="*80)
        print("Loaded Data Summary:")
        print("="*80)
        print(f"Workload Features: {len(workload_features)} features")
        print(f"Query Plans: {len(query_plans)} plans")
        print(f"Inner Metrics: {len(inner_metrics)} metrics")
        print("="*80 + "\n")
        
        # Generate questions
        generator = LLMRAGQuestionGenerator()
        print("Generating RAG questions...")
        questions = generator.generate_questions(
            workload_features, query_plans, inner_metrics
        )
        
        print("\n" + "="*80)
        print("Generated RAG Questions:")
        print("="*80)
        for i, q in enumerate(questions, 1):
            print(f"Q{i}: {q}")
        print("="*80)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease ensure the following files exist:")
        print(f"  - {workload_features_path}")
        print(f"  - {query_plans_path}")
        print(f"  - {inner_metrics_path}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
