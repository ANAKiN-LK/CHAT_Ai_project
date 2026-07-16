from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.graph.nodes import (
    retrieve_node,
    grade_node,
    generate_rag_node,
    generate_direct_node
)
from app.graph.edges import route_after_grade
def create_rag_workflow():
    workflow = StateGraph(AgentState)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("grade", grade_node)
    workflow.add_node("generate_rag", generate_rag_node)
    workflow.add_node("generate_direct", generate_direct_node)
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "grade")
    workflow.add_conditional_edges(
        "grade",
        route_after_grade,
        {
            "generate_rag": "generate_rag",
            "generate_direct": "generate_direct"
        }
    )
    
    workflow.add_edge("generate_rag", END)
    workflow.add_edge("generate_direct", END)
    return workflow.compile()
agent_app = create_rag_workflow()