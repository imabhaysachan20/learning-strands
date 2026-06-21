# Session State

# Information needed only during the current conversation.

# If the conversation ends, this can be discarded.

# Think:

# Session = temporary working memory

# Memory

# Information that should survive future conversations.

# Example:

# User: I am a vegetarian.

# Weeks later:

# User: Recommend restaurants.

# Agent recalls:

# User prefers vegetarian food.


# Store conversation history in:

# RAM
# JSON files
# SQLite database
# local filesystem

##ram storage using simple dictionary

# session = {
#     "messages": [
#         {"role":"user","content":"Hi"},
#         {"role":"assistant","content":"Hello"}
#     ]
# }
print("SCRIPT VERSION 123")
# Every new message:

# session["messages"].append(new_message)

# Lost when application restarts

# Doesn't work across multiple servers

# Not suitable for production scaling

from strands import Agent

# #by default strands already maintains this convo history in ram

# agent = Agent()


# agent('hi my name is abhay')

# agent('what is my name')





import json
from pathlib import Path

SESSION_FILE = "session.json"

if Path(SESSION_FILE).exists():
    with open(SESSION_FILE, "r") as f:
        messages = json.load(f)
else:
    messages = []

agent = Agent(messages=messages)

print("Welcome to agent with memory!")

while True:
    user_prompt = input("User: ").strip()

    if user_prompt.lower() == "exit":
        break

    response = agent(user_prompt)

    with open(SESSION_FILE, "w") as f:
        json.dump(agent.messages, f, indent=2, default=str)

print("Session saved. Goodbye!")



#using strands in built file memory manager

from strands.session.file_session_manager import FileSessionManager

# Create a persistent session
session_manager = FileSessionManager(
    session_id="abhay-chat"
)

agent = Agent(
    session_manager=session_manager
)
