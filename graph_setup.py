from langgraph.graph import StateGraph, END

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
# We need to ensure both assistants are done before moving to summarizer
def should_continue(state):
    if "assistant1_plan" in state and "assistant2_plan" in state:
        return "summarizer"
    return None

graph.add_conditional_edge(
    "assistant1",
    should_continue,
    {
        "summarizer": "summarizer",
        None: "assistant1"  # Wait if not ready
    }
)

graph.add_conditional_edge(
    "assistant2",
    should_continue,
    {
        "summarizer": "summarizer",
        None: "assistant2"  # Wait if not ready
    }
)

# 4. After summarizer, end the graph
graph.add_edge("summarizer", END)

# Compile the graph
workflow = graph.compile() 