from langgraph.graph import StateGraph, START, END

from app.state import ResearchState
from app.agents.planner import planner_agent
from app.agents.researcher import researcher_agent
from app.agents.validator import validator_agent
from app.agents.synthesizer import synthesizer_agent


def should_continue(state: ResearchState) -> str:
    """
    Decide what the agent should do after validation.
    """

    status = state.get("status", "")
    current_step = state.get("current_step", 0)
    plan = state.get("research_plan", [])
    iteration_count = state.get("iteration_count", 0)

    # Safety limit to prevent an infinite research loop.
    max_iterations = 2 * max(len(plan), 1)

    if iteration_count >= max_iterations:
        return "finish"

    # More research is required for the current step.
    if status == "needs_more_research":
        return "research"

    # Current step is complete, so move to the next step.
    if current_step + 1 < len(plan):
        return "next_step"

    # All planned steps are complete.
    return "finish"


def move_to_next_step(state: ResearchState) -> ResearchState:
    """
    Move the agent to the next research-plan step.
    """

    return {
        "current_step": state.get("current_step", 0) + 1,
        "status": "step_complete",
    }


def build_graph():
    """
    Build and compile the Lens agent workflow.
    """

    graph = StateGraph(ResearchState)

    # Add workflow nodes.
    graph.add_node("planner", planner_agent)
    graph.add_node("researcher", researcher_agent)
    graph.add_node("validator", validator_agent)
    graph.add_node("next_step", move_to_next_step)
    graph.add_node("synthesizer", synthesizer_agent)

    # Start with planning.
    graph.add_edge(START, "planner")

    # Planning → Research.
    graph.add_edge("planner", "researcher")

    # Research → Validation.
    graph.add_edge("researcher", "validator")

    # Validation decides the next action.
    graph.add_conditional_edges(
        "validator",
        should_continue,
        {
            "research": "researcher",
            "next_step": "next_step",
            "finish": "synthesizer",
        },
    )

    # Move to the next research-plan step.
    graph.add_edge("next_step", "researcher")

    # Synthesis → Final output.
    graph.add_edge("synthesizer", END)

    return graph.compile()


# Compiled Lens agent.
lens_graph = build_graph()