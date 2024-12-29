from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from typing import Dict
import os
from agent_state import AgentState

# Initialize the model
model = ChatOpenAI(model="gpt-3.5-turbo")

def chief_node(state: AgentState) -> Dict:
    """The Chief analyzes the task and delegates to assistants"""
    messages = [
        HumanMessage(content=f"""You are The Chief, a high-level executive manager.
        You need to delegate this task to your two assistants:
        Assistant 1 handles: Personnel, Logistics, and Public Relations
        Assistant 2 handles: Intelligence and Operation Planning
        
        Task: {state['task']}
        
        Break down this task for both assistants based on their areas of responsibility.
        """)
    ]
    response = model.invoke(messages)
    return {
        "chief_messages": [*messages, response]
    }

def assistant1_node(state: AgentState) -> Dict:
    """Assistant 1 handles personnel, logistics and PR planning"""
    messages = [
        *state["chief_messages"],
        HumanMessage(content="""You are Assistant 1 responsible for Personnel, Logistics and Public Relations.
        Based on the task and The Chief's delegation, create a detailed plan for your areas of responsibility.
        Format your response as a structured plan.""")
    ]
    response = model.invoke(messages)
    return {
        "assistant1_messages": [*messages, response],
        "assistant1_plan": {"plan": response.content}
    }

def assistant2_node(state: AgentState) -> Dict:
    """Assistant 2 handles intelligence and operations planning"""
    messages = [
        *state["chief_messages"],
        HumanMessage(content="""You are Assistant 2 responsible for Intelligence and Operation Planning.
        Based on the task and The Chief's delegation, create a detailed plan for your areas of responsibility.
        Format your response as a structured plan.""")
    ]
    response = model.invoke(messages)
    return {
        "assistant2_messages": [*messages, response],
        "assistant2_plan": {"plan": response.content}
    }

def summarizer_node(state: AgentState) -> Dict:
    """Summarizer creates final execution plan based on both assistants' input"""
    messages = [
        HumanMessage(content=f"""You are the Summary Agent. Review the plans from both assistants:

        Assistant 1 (Personnel, Logistics, PR) Plan:
        {state['assistant1_plan']['plan']}

        Assistant 2 (Intelligence, Operations) Plan:
        {state['assistant2_plan']['plan']}

        Create a comprehensive execution summary that integrates both plans.
        """)
    ]
    response = model.invoke(messages)
    return {
        "summarizer_messages": [*messages, response],
        "final_summary": response.content
    } 