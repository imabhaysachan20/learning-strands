import asyncio
from strands import Agent
from strands.session.file_session_manager import FileSessionManager

SYSTEM_PROMPT = """
You are an expert Personal Tutor AI.

Your responsibilities:
- Teach concepts clearly and patiently.
- Explain ideas step by step.
- Use examples and analogies whenever possible.
- Adapt your explanations to the user's level.
- Encourage learning instead of simply giving answers.
- Ask follow-up questions to verify understanding.
- If previous conversation context is available, use it.
"""

## simple chat bot based agent using inmemory persitence memory lost after program exited using streaming response


agent = Agent(
    system_prompt=SYSTEM_PROMPT
)

# async def tutor_chat():
#     prompt = input("You: ")

#     print("Tutor: ", end="", flush=True)

#     agent_stream = agent.stream_async(prompt)

#     async for event in agent_stream:
#         if "data" in event:
#             # Stream generated text chunks
#             print(event["data"], end="", flush=True)
# while(True):
#     asyncio.run(tutor_chat())

##adding a persistence using file session based method

session_manager = FileSessionManager(
    session_id="abhay-chat"
)

# agent2 = Agent(session_manager=session_manager,system_prompt=SYSTEM_PROMPT)


# async def tutor_chat():
#     prompt = input("You: ")

#     print("Tutor: ", end="", flush=True)

#     agent_stream = agent2.stream_async(prompt)

#     async for event in agent_stream:
#         if "data" in event:
#             # Stream generated text chunks
#             print(event["data"], end="", flush=True)
# while(True):
#     asyncio.run(tutor_chat())


# Tuning a couple of agent parameters. 
agent3 = Agent(session_manager=session_manager,system_prompt="You are a famous content creator and you make reels about tech so write the script as if you areand answe ")




