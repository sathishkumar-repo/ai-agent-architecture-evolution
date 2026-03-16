from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
import operator

# import TypedDict, Annotated from typing
# Import BaseMessage from langchain_core.messages
# Import operator
# LangGraph requires a state object that flows between nodes. 
# This state object is a dictionary that can contain any information you want to pass between nodes. 
# In this example, we will create a state object that contains a list of messages. 
# Each message is an instance of BaseMessage, which is a class from the LangChain library that represents a message in a conversation.
# The Annotated type is used to specify that the messages list should be combined using the operator.add function.
# messages list accumulates conversation history, allowing the agent to maintain context across interactions.

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

