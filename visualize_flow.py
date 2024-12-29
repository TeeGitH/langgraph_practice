from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from langchain_core.messages import BaseMessage
import operator

# Define our state
class AgentState(TypedDict):
    task: str
    chief_messages: List[BaseMessage]
    assistant1_messages: List[BaseMessage]
    assistant2_messages: List[BaseMessage]
    summarizer_messages: List[BaseMessage]
    assistant1_plan: dict
    assistant2_plan: dict
    final_summary: str

# Create the graph
graph = StateGraph(AgentState)

# Add all our nodes
graph.add_node("chief", chief_node)
graph.add_node("assistant1", assistant1_node)
graph.add_node("assistant2", assistant2_node)
graph.add_node("summarizer", summarizer_node)

# Set up the flow
graph.set_entry_point("chief")

# Define edges
graph.add_edge("chief", "assistant1")
graph.add_edge("chief", "assistant2")

# Add conditional edges for synchronization
def should_continue(state):
    if "assistant1_plan" in state and "assistant2_plan" in state:
        return "summarizer"
    return None

graph.add_conditional_edge(
    "assistant1",
    should_continue,
    {
        "summarizer": "summarizer",
        None: "assistant1"
    }
)

graph.add_conditional_edge(
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

# Add visualization code
from IPython.display import Image, display

try:
    import graphviz
    dot = graphviz.Digraph(comment='Agent Workflow')
    
    # Configure the graph
    dot.attr(rankdir='TB')  # Top to Bottom direction
    
    # Add nodes with custom styling
    dot.attr('node', shape='box', style='rounded')
    dot.node('START', 'START', shape='oval')
    dot.node('chief', 'Chief')
    dot.node('assistant1', 'Assistant 1\n(Personnel, Logistics, PR)')
    dot.node('assistant2', 'Assistant 2\n(Intelligence, Operations)')
    dot.node('summarizer', 'Summarizer')
    dot.node('END', 'END', shape='oval')
    
    # Add edges with custom styling
    dot.attr('edge', color='blue')
    dot.edge('START', 'chief')
    dot.edge('chief', 'assistant1')
    dot.edge('chief', 'assistant2')
    dot.edge('assistant1', 'summarizer')
    dot.edge('assistant2', 'summarizer')
    dot.edge('summarizer', 'END')
    
    # Save with specific engine
    dot.render('agent_flow', view=True, engine='dot')
except Exception as e:
    print(f"Visualization error: {e}")
    print("Please ensure Graphviz is installed and in your system PATH") 