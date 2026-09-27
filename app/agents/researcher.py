from app.config import llm
from app.state import ResearchState
from app.tools.web_search import web_search


def researcher_agent(state: ResearchState) -> ResearchState:
    """
    Generate search queries and perform web research
    for the current research step.
    """

    goal = state["user_goal"]
    plan = state.get("research_plan", [])
    current_step = state.get("current_step", 0)

    if not plan:
        return {
            "status": "research_failed",
            "missing_information": ["No research plan available."],
        }

    if current_step >= len(plan):
        return {
            "status": "research_complete",
        }

    current_task = plan[current_step]

    prompt = f"""
You are the research agent for an AI research system called Lens.

Research goal:
{goal}

Overall research plan:
{plan}

Current research step:
{current_task}

Generate exactly 3 focused web search queries that will help
complete the current research step.

Rules:
- Queries must be specific and useful.
- Prefer recent information.
- Include relevant years when appropriate.
- Return ONLY the 3 queries, one per line.
"""

    response = llm.invoke(prompt)

    queries = []

    for line in response.content.splitlines():
        line = line.strip()

        if not line:
            continue

        if line[0].isdigit():
            line = line.lstrip("0123456789. ").strip()

        if line:
            queries.append(line)

    queries = queries[:3]

    all_results = []

    for query in queries:
        results = web_search(query, max_results=5)

        for result in results:
            result["query"] = query
            all_results.append(result)

    existing_results = state.get("search_results", [])

    return {
        "search_queries": queries,
        "search_results": existing_results + all_results,
        "status": "researching",
    }