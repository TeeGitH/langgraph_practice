from graph_setup import workflow, graph

# Initialize the state
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

# Access the final summary
print(result["final_summary"])

# To save the image instead of displaying it
graph.get_graph().write_png("agent_flow.png") 