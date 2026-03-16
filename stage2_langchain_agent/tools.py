from langchain.tools import tool
from datetime import datetime

@tool
def get_current_time():
    """Get the current system time"""
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

@tool
def read_notes():
    """Read notes.txt and return the content"""
    with open("stage2_langchain_agent/notes.txt", "r") as f:
        return f.read()