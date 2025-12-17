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
from typing import List, Dict, Any

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
        Generate up to 5 RAG questions from structured workload input.
        Output is a plain Python list of strings.
        """

        system_prompt = (
            "You are a database performance tuning expert.\n"
            "Your task is to generate concise, high-value questions that can be used\n"
            "to retrieve database configuration and tuning recommendations.\n\n"
            "Rules:\n"
            "- Generate AT MOST 5 questions\n"
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

        Generate up to 5 concise questions.
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
        return questions[:5]


# -----------------------------
# Example usage (thesis-style input)
# -----------------------------
if __name__ == "__main__":
    workload_features = {
        "size": 9,
        "read_ratio": 1.0,
        "group_by_ratio": 0.89,
        "order_by_ratio": 0.89,
        "avg_query_length": 281.9,
        "avg_joins": 1.2,
        "filter_ratio": 0.89,
    }

    query_plans = [
        "Merge Join(cost=1915.8)(Index Scan(cost=1016.9); Index Scan(cost=1066.1))",
        "Aggregate(cost=1004.1)(Seq Scan(cost=698.5))",
        "Hash Join(cost=2827.2)(Seq Scan(cost=896.0); Seq Scan(cost=1116.4))",
    ]

    inner_metrics = {
        "buffer_hit_ratio": 0.96,
        "avg_response_time": 166.5,
        "lock_wait": 0.02,
        "rows_returned": 1408,
        "deadlocks": 0,
    }

    generator = LLMRAGQuestionGenerator()
    questions = generator.generate_questions(
        workload_features, query_plans, inner_metrics
    )
    print("Generated RAG Questions:",questions)
    # for i, q in enumerate(questions, 1):
    #     print(f"Q{i}: {q}")
