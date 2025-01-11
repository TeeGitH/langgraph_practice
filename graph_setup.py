from langgraph.graph import StateGraph, END
from agent_state import AgentState
from nodes import chief_node, assistant1_node, assistant2_node, summarizer_node

# Initialize the graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("chief", chief_node)
graph.add_node("assistant1", assistant1_node)
graph.add_node("assistant2", assistant2_node)
graph.add_node("summarizer", summarizer_node)

# Define the flow:
# 1. Start with the chief
graph.set_entry_point("chief")

# 2. After chief, go to both assistants in parallel
graph.add_edge("chief", "assistant1")
graph.add_edge("chief", "assistant2")

# 3. After both assistants complete, go to summarizer
def should_continue(state):
    if "assistant1_plan" in state and "assistant2_plan" in state:
        return "summarizer"
    return None

# Changed from add_conditional_edge to add_conditional_edges
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

# 4. After summarizer, end the graph
graph.add_edge("summarizer", END)

# Compile the graph
workflow = graph.compile() 