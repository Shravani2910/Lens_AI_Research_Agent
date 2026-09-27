from app.config import llm
from app.state import ResearchState


def planner_agent(state: ResearchState) -> ResearchState:
    """
    Create a research plan from the user's goal.
    """

    goal = state["user_goal"]

    prompt = f"""
You are the planning agent for an AI research system called Lens.

The user has given you this research goal:

{goal}

Create a clear research plan with 3 to 5 logical steps.

The plan should:
- Break the goal into specific research tasks.
- Focus on information that can be verified through web research.
- Avoid unnecessary steps.
- Return ONLY a numbered list.
"""

    response = llm.invoke(prompt)

    plan_text = response.content

    plan = []

    for line in plan_text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line[0].isdigit():
            cleaned = line.lstrip("0123456789. ").strip()

            if cleaned:
                plan.append(cleaned)

    return {
        "research_plan": plan,
        "current_step": 0,
        "iteration_count": 0,
        "status": "planned",
    }