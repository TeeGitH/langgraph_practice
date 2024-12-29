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
    # Create a new directed graph
    dot = graphviz.Digraph('Agent Workflow', format='png')
    
    # Graph attributes
    dot.attr(rankdir='TB', splines='ortho')
    
    # Node styling
    dot.attr('node', 
            style='filled',
            shape='box',
            fontname='Arial',
            fontsize='12',
            margin='0.2')
    
    # Add nodes with different colors
    dot.node('START', 'START', shape='oval', fillcolor='lightgrey')
    dot.node('chief', 'Chief\nManager', fillcolor='lightblue')
    dot.node('assistant1', 'Assistant 1\nPersonnel, Logistics, PR', fillcolor='lightgreen')
    dot.node('assistant2', 'Assistant 2\nIntelligence, Operations', fillcolor='lightgreen')
    dot.node('summarizer', 'Summarizer', fillcolor='lightyellow')
    dot.node('END', 'END', shape='oval', fillcolor='lightgrey')
    
    # Add edges with labels
    dot.edge('START', 'chief')
    dot.edge('chief', 'assistant1', 'delegate')
    dot.edge('chief', 'assistant2', 'delegate')
    dot.edge('assistant1', 'summarizer', 'report')
    dot.edge('assistant2', 'summarizer', 'report')
    dot.edge('summarizer', 'END', 'final plan')
    
    # Save the graph
    dot.render('agent_flow', view=True, cleanup=True)
    print("Visualization saved as 'agent_flow.pdf' and 'agent_flow.png'")
except Exception as e:
    print(f"Visualization error: {e}") 