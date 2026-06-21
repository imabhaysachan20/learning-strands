# SESSION
# -------
# Stores conversation history for the current chat.
# Answers:
# "What happened in this conversation?"

# Example:
# User: My name is Abhay
# User: What is my name?
# Agent remembers because both messages are in the same session.

# Characteristics:
# - Short-term
# - Stores chat history/messages
# - Scoped to a single conversation
# - Identified by session_id
# - Can be discarded when the conversation ends


# MEMORY
# ------
# Stores durable user facts and preferences.
# Answers:
# "What do I know about this user?"

# Example:
# Session 1:
# User: I am vegetarian
#
# Session 2 (weeks later):
# User: Recommend a restaurant
# Agent recalls the user's dietary preference.

# Characteristics:
# - Long-term
# - Stores facts/preferences
# - Shared across sessions
# - Identified by user_id
# - Persists beyond conversation boundaries


# AgentCore Session
# -----------------
# AWS-managed conversation state.
#
# session_id -> load history -> run agent -> save history


# AgentCore Memory
# ----------------
# AWS-managed long-term memory.
#
# user_id -> store facts -> retrieve facts -> personalize responses



# ----------
# Session = Current conversation context
# Memory  = Long-term user knowledge


# Example
# --------
# user_id = "abhay"
#
# session_id = "chat_001"
# session_id = "chat_002"
#
# chat_001 and chat_002 have different conversation histories,
# but both can access the same long-term memory associated with user_id.


