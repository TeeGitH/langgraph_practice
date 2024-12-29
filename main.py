from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from agent_state import AgentState
from nodes import chief_node, assistant1_node, assistant2_node, summarizer_node
from langgraph.graph import StateGraph, END
from IPython.display import Image, display

# Create the graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("chief", chief_node)
graph.add_node("assistant1", assistant1_node)
graph.add_node("assistant2", assistant2_node)
graph.add_node("summarizer", summarizer_node)

# Set entry point
graph.set_entry_point("chief")

# Add edges
graph.add_edge("chief", "assistant1")
graph.add_edge("chief", "assistant2")

# Add conditional edges
def should_continue(state):
    if "assistant1_plan" in state and "assistant2_plan" in state:
        return "summarizer"
    return None

graph.add_conditional_edges(
    "assistant1",
    should_continue,
    {
        "summarizer": "summarizer",
        None: "assistant1"
    }
)

graph.add_conditional_edges(
    "assistant2",
    should_continue,
    {
        "summarizer": "summarizer",
        None: "assistant2"
    }
)

graph.add_edge("summarizer", END)

# Compile the graph
workflow = graph.compile()

# Save the graph visualization using the correct method
try:
    import graphviz
    graph_viz = graphviz.Digraph()
    
    # Add nodes
    graph_viz.node("start", "_start_")
    graph_viz.node("chief", "chief")
    graph_viz.node("assistant1", "assistant1")
    graph_viz.node("assistant2", "assistant2")
    graph_viz.node("summarizer", "summarizer")
    graph_viz.node("end", "_end_")
    
    # Add edges
    graph_viz.edge("start", "chief")
    graph_viz.edge("chief", "assistant1")
    graph_viz.edge("chief", "assistant2")
    graph_viz.edge("assistant1", "summarizer")
    graph_viz.edge("assistant2", "summarizer")
    graph_viz.edge("summarizer", "end")
    
    # Save the visualization
    graph_viz.render("agent_flow", format="png", cleanup=True)
except Exception as e:
    print(f"Could not generate visualization: {e}")

# Initialize and run the workflow
initial_state = {
    "task": "Organize a major corporate event for 500 people",
    "chief_messages": [],
    "assistant1_messages": [],
    "assistant2_messages": [],
    "summarizer_messages": [],
    "assistant1_plan": {},
    "assistant2_plan": {},
    "final_summary": ""
}

# Run the workflow
result = workflow.invoke(initial_state)

# Print the final summary
print("\nFinal Summary:")
print(result["final_summary"]) 