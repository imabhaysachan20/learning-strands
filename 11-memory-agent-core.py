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

import os
import asyncio
from datetime import datetime
from strands import Agent
from strands.tools import tool 
from strands.models import BedrockModel
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager

# Provide the Memory ID (Created via AWS Console or setup script)
MEM_ID = os.environ.get("AGENTCORE_MEMORY_ID", "memory_shd15-7sWcguC2Rt")
ACTOR_ID = "test_actor_id"
SESSION_ID = "test_session_id"

user_prefs_retrieval = RetrievalConfig(
    strategy_id="userPreferenceMemoryStrategy",
    top_k=5,
    relevance_score=0.3
)

semantic = RetrievalConfig(
    strategy_id="semantic_builtin_xe88f",
    top_k=5,
    relevance_score=0.3
)

summary_retrival = RetrievalConfig(
    strategy_id="summary_builtin_h08by",
    top_k=2,
    relevance_score=0.2
)

episodes = RetrievalConfig(
    strategy_id="episodes_builtin",
    top_k=3,
    relevance_score=0.3
)


# Add the retrieval_config to your AgentCoreMemoryConfig

agent_core_config = AgentCoreMemoryConfig(
    memory_id=MEM_ID,
    actor_id=ACTOR_ID,
    session_id=SESSION_ID,

    retrieval_config={
        "/strategies/summary_builtin_h08by/actors/{actorId}/sessions/{sessionId}/": summary_retrival
    }
)
bedrock_model = BedrockModel(
    model_id="global.anthropic.claude-sonnet-4-6",
    region_name="us-west-2",
    temperature=0.2,
    max_tokens=1000 
)

# # Use a Context Manager (with block) to safely handle the session and prevent data loss
# with AgentCoreMemorySessionManager(agent_core_config,region_name="ap-south-1") as session_manager:

#     copilot = agent = Agent(
#     session_manager=session_manager,
#     system_prompt="""
#     You are an AI assistant.
#     Use retrieved summaries from previous conversations
#     to answer follow-up questions.
#     """
#     )

#     while True:

#             question = input("You: ")

#             if question.lower() == "exit":
#                 break

#             response = agent(question)

#             print("\nAssistant:")
#             print(response)







# config = AgentCoreMemoryConfig(
#     memory_id=MEM_ID,
#     actor_id=ACTOR_ID,
#     session_id=SESSION_ID,

#     retrieval_config={
#         "/strategies/semantic_builtin_xe88f/actors/{actorId}/": semantic
#     }
# )



# with AgentCoreMemorySessionManager(
#     config,
#     region_name="ap-south-1"
# ) as session_manager:

#     agent = Agent(
#         session_manager=session_manager,
#         system_prompt="""
#         You are a helpful AI assistant.
#         Use retrieved semantic memories whenever they are relevant.
#         """
#     )

#     while True:

#         query = input("You: ")

#         if query.lower() == "exit":
#             break

#         response = agent(query)

#         print(response)



agent_core_config = AgentCoreMemoryConfig(
    memory_id=MEM_ID,
    actor_id=ACTOR_ID,
    session_id=SESSION_ID,

    retrieval_config={
        "/strategies/{memoryStrategyId}/actors/{actorId}/": episodes
    }
)

with AgentCoreMemorySessionManager(
    agent_core_config,
    region_name="ap-south-1"
) as session_manager:

    copilot = Agent(
        system_prompt="""
        You are a helpful assistant.
        Remember previous experiences, problems, solutions,
        and outcomes to help the user in future conversations.
        """,
        session_manager=session_manager,
        model=bedrock_model
    )
    print("\nUser:")
    print("""
    Yesterday I deployed my Flask application on EC2.

    The deployment failed because port 5000 was blocked
    by the security group.

    I opened port 5000 in the EC2 security group,
    redeployed the application,
    and everything worked successfully.
    """)

    response = copilot("""
    Yesterday I deployed my Flask application on EC2.

    The deployment failed because port 5000 was blocked
    by the security group.

    I opened port 5000 in the EC2 security group,
    redeployed the application,
    and everything worked successfully.
    """)

    print(response)

