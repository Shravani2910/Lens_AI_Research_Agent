from app.config import llm
from app.state import ResearchState


def validator_agent(state: ResearchState) -> ResearchState:
    """
    Evaluate whether the collected research is sufficient
    to answer the user's research goal.
    """

    goal = state["user_goal"]
    plan = state.get("research_plan", [])
    current_step = state.get("current_step", 0)
    results = state.get("search_results", [])
    iteration_count = state.get("iteration_count", 0)

    recent_results = results[-15:]

    research_text = "\n\n".join(
        [
            f"Title: {result.get('title', '')}\n"
            f"URL: {result.get('url', '')}\n"
            f"Snippet: {result.get('snippet', '')}"
            for result in recent_results
        ]
    )

    prompt = f"""
You are the validation agent for an AI research system called Lens.

Research goal:
{goal}

Research plan:
{plan}

Current step:
{current_step + 1} of {len(plan)}

Research results:
{research_text}

Determine whether the current research is sufficient to continue.

Return exactly this format:

STATUS: COMPLETE
MISSING: None

OR:

STATUS: INCOMPLETE
MISSING:
- missing information 1
- missing information 2

Rules:
- Mark COMPLETE only when the available information is reasonably sufficient
  for the current research step.
- If information is missing, identify the specific information needed.
- Do not invent facts.
"""

    response = llm.invoke(prompt)
    validation = response.content.strip()

    if "STATUS: COMPLETE" in validation:
        status = "validated"
        missing_information = []
    else:
        status = "needs_more_research"

        missing_information = []

        capture = False

        for line in validation.splitlines():
            line = line.strip()

            if line.startswith("MISSING:"):
                capture = True
                continue

            if capture and line.startswith("-"):
                item = line[1:].strip()

                if item and item.lower() != "none":
                    missing_information.append(item)

    return {
        "missing_information": missing_information,
        "iteration_count": iteration_count + 1,
        "status": status,
    }