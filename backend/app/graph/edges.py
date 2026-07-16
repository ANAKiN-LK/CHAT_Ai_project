from app.graph.state import AgentState
def route_after_grade(state: AgentState) -> str:
    if state.get("is_relevant", False):
        return "generate_rag"
    else:
        return "generate_direct"