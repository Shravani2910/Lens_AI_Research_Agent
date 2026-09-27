import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from app.graph import lens_graph


st.set_page_config(
    page_title="Lens — AI Research Agent",
    page_icon="🔎",
    layout="wide",
)


st.title("🔎 Lens")
st.subheader("AI Research Agent")

st.write(
    "Give Lens a research goal. It plans, searches, validates, "
    "and generates a structured research report."
)


research_goal = st.text_area(
    "Research Goal",
    placeholder="Example: Research the latest AI agent trends in 2026",
    height=120,
)


if st.button("🚀 Start Research", type="primary"):

    if not research_goal.strip():
        st.warning("Please enter a research goal.")
        st.stop()

    st.divider()

    st.subheader("Agent Workflow")

    planning_status = st.empty()
    research_status = st.empty()
    validation_status = st.empty()
    synthesis_status = st.empty()

    planning_status.info("🧠 Planning...")

    with st.spinner("Lens is researching..."):

        result = lens_graph.invoke(
            {
                "user_goal": research_goal.strip()
            }
        )

    planning_status.success("🧠 Planning complete")

    research_status.success(
        f"🔎 Research complete — "
        f"{len(result.get('search_results', []))} sources collected"
    )

    iterations = result.get("iteration_count", 0)

    validation_status.success(
        f"🔍 Validation complete — {iterations} workflow iterations"
    )

    synthesis_status.success("📝 Report generated")

    st.divider()

    st.subheader("Research Report")

    final_report = result.get(
        "final_report",
        "No final report was generated.",
    )

    st.markdown(final_report)

    with st.expander("View Agent State"):

        st.write(
            {
                "status": result.get("status"),
                "plan_steps": len(
                    result.get("research_plan", [])
                ),
                "search_results": len(
                    result.get("search_results", [])
                ),
                "iterations": result.get("iteration_count"),
            }
        )

