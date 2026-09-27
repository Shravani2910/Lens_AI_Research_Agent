from app.config import llm
from app.state import ResearchState


def synthesizer_agent(state: ResearchState) -> ResearchState:
    """
    Synthesize collected research into a final report.
    """

    goal = state["user_goal"]
    findings = state.get("search_results", [])

    if not findings:
        return {
            "final_report": "No research results were collected.",
            "status": "completed",
        }

    # Keep the synthesis prompt small enough for the LLM token limit.
    # Remove duplicate URLs and keep only the strongest 20 results.
    unique_results = []
    seen_urls = set()

    for result in findings:
        url = result.get("url", "")

        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(result)

        if len(unique_results) >= 20:
            break

    research_text = "\n\n".join(
        [
            f"Source: {result.get('title', '')}\n"
            f"URL: {result.get('url', '')}\n"
            f"Information: {result.get('snippet', '')[:600]}"
            for result in unique_results
        ]
    )

    prompt = f"""
You are the synthesis agent for an AI research system called Lens.

Research goal:
{goal}

Collected research:

{research_text}

Create a concise research report that directly answers the research goal.

Use this structure:

# Research Summary

## Key Findings
- Finding 1
- Finding 2
- Finding 3
- Finding 4
- Finding 5

## Analysis
Explain the main patterns and important observations.

## Sources
List the most relevant source titles and URLs.

Rules:
- Use only information present in the collected research.
- Do not invent facts.
- Clearly distinguish reported information from your analysis.
- Prefer information supported by multiple sources.
- Keep the report concise.
"""

    response = llm.invoke(prompt)

    return {
        "final_report": response.content,
        "status": "completed",
    }