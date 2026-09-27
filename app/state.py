from typing import TypedDict, List, Dict, Any


class ResearchState(TypedDict, total=False):
    user_goal: str

    research_plan: List[str]
    current_step: int

    search_queries: List[str]
    search_results: List[Dict[str, Any]]
    findings: List[Dict[str, Any]]

    missing_information: List[str]

    iteration_count: int

    final_report: str
    status: str
