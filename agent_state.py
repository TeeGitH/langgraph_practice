from typing import TypedDict, Annotated, List, Dict
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    # Input task from user
    task: str
    # Chat history for each agent
    chief_messages: Annotated[List[BaseMessage], operator.add]
    assistant1_messages: Annotated[List[BaseMessage], operator.add]
    assistant2_messages: Annotated[List[BaseMessage], operator.add]
    summarizer_messages: Annotated[List[BaseMessage], operator.add]
    # Plans and outputs from each agent
    assistant1_plan: Dict
    assistant2_plan: Dict
    final_summary: str 