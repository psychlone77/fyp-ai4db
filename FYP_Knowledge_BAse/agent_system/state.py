from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    workload_features: Dict[str, Union[int, float, str]]
    query_plans: List[str]
    inner_metrics: Dict[str, Union[int, float]]
    web_rag_input: str
    e2etune_input: str
    final_response: Optional[str]
    ram: Optional[int]
    cpu_cores: Optional[int]
