import os
from typing import Dict, Any
from dotenv import load_dotenv
from tavily import TavilyClient

# Load .env from FYP_Knowledge_BAse
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(ENV_PATH)


def _build_workload_query(workload_features: Dict[str, Any]) -> str:
    """
    Turn structured workload features into a natural-language query
    for Tavily (PostgreSQL knob tuning focus).
    """
    parts = [f"{k}={v}" for k, v in workload_features.items()]
    features_str = "; ".join(parts)

    return (
        "You are an expert PostgreSQL performance engineer. "
        "Given the following workload features, propose tuned values or ranges "
        "for important PostgreSQL configuration parameters (knobs) "
        f"Workload features: {features_str}"
    )


def generate_knob_configs(workload_features: Dict[str, Any]) -> str:
    """
    Use Tavily web+LLM RAG to generate knob recommendations for the given workload.
    Returns Tavily's synthesized answer as a text block.
    """
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError(f"TAVILY_API_KEY is not set (tried .env at: {ENV_PATH})")

    client = TavilyClient(api_key=api_key)

    query = _build_workload_query(workload_features)

    response = client.search(
        query=query,
        max_results=8,
        include_answer=True,   # Tavily returns an LLM-generated answer
        include_raw_content=False,
    )

    # response["answer"] is Tavily's synthesized knob config recommendation
    return response.get("answer", "")


if __name__ == "__main__":
    # Example usage
    example_workload = {
        "workload_type": "OLAP",
        "size": 9,
        "read_ratio": 1.0,
        "group_by_ratio": 0.89,
        "order_by_ratio": 0.89,
        "avg_query_length": 281.9,
        "avg_joins": 1.2,
        "filter_ratio": 0.89,
    }

    recommendations = generate_knob_configs(example_workload)
    print("Tavily-based knob recommendations:\n")
    print(recommendations)