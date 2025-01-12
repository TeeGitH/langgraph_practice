from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from agent_state import AgentState
from nodes import chief_node, assistant1_node, assistant2_node, summarizer_node
from langgraph.graph import StateGraph, END

# Define the tasks
TASKS = {
    'A': "Organize a major corporate event for 500 people",
    'B': "Develop and execute a company-wide digital transformation strategy",
    'C': "Plan and implement a global market expansion into three new countries",
    'D': "Design and launch a comprehensive employee wellness and development program",
    'E': "Create a crisis management and business continuity plan for multiple scenarios"
}

print("OpenAI API Key:", bool(os.getenv("OPENAI_API_KEY")))

def print_task_menu():
    """Display the task selection menu"""
    print("\nAvailable Tasks:")
    print("-" * 80)  # Increased width for longer task descriptions
    for key, task in TASKS.items():
        print(f"Task {key}: {task}")
    print("\nType 'x' to exit")
    print("-" * 80)

def get_user_choice():
    """Get and validate user input"""
    while True:
        choice = input("\nPlease select a task (A/B/C/D/E) or 'x' to exit: ").upper()
        if choice in ['A', 'B', 'C', 'D', 'E', 'X']:
            return choice
        print("Invalid choice. Please select A, B, C, D, E, or x to exit.")

def run_workflow(task):
    """Run the agent workflow with the selected task"""
    try:
        # Create a fresh graph for each run
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

        # Initialize a fresh state for each run
        initial_state = {
            "task": task,
            "chief_messages": [],
            "assistant1_messages": [],
            "assistant2_messages": [],
            "summarizer_messages": [],
            "assistant1_plan": {},
            "assistant2_plan": {},
            "final_summary": ""
        }

        # Run the workflow with fresh state
        result = workflow.invoke(initial_state)
        
        # Validate result
        if not result or 'final_summary' not in result:
            raise ValueError("Workflow did not produce a valid result")
            
        return result

    except Exception as e:
        print(f"Error in workflow execution: {str(e)}")
        raise  # Re-raise the exception for proper handling in app.py

def main():
    """Main program loop"""
    print("Welcome to the Agent Workflow System")
    print("This system uses multiple AI agents to help plan and execute complex tasks")
    
    while True:
        print_task_menu()
        choice = get_user_choice()
        
        if choice == 'X':
            print("\nThank you for using the Agent Workflow System. Goodbye!")
            break
            
        print(f"\nExecuting Task {choice}: {TASKS[choice]}")
        print("=" * 80)  # Increased width for consistency
        result = run_workflow(TASKS[choice])
        print("\nFinal Summary:")
        print("-" * 80)  # Increased width for consistency
        print(result["final_summary"])
        print("-" * 80)
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 