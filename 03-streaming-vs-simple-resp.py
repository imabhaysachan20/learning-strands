from strands import agent,Agent
import asyncio
from strands import Agent
# Without streaming
# 0s : User clicks send.
# 1s : ...
# 2s : ...
# 3s : ...
# 4s : ...
# 5s : ...
# 6s : ...
# 7s : ...
# 8s : Entire answer appears.


# With streaming
# 0s : User clicks send.
# 1s : "Python "
# 2s : "Python generators "
# 3s : "Python generators are "
# 4s : "Python generators are special..."
# ...
# 8s : Answer complete.

# The total generation time is the same, but the application feels much faster and responsive as resonsese are received in chunks
# and shown.

#without streaming 
# agent = Agent()

# response = agent("Explain Python generators.")
# print(response)


#with streaming 


agent = Agent()

# async def main():
#     async for event in agent.stream_async(
#         "Explain Python generators in 2 lines"
#     ):
#         print(event)

# asyncio.run(main())


# Each event is a dictionary-like object. The actual generated text arrives in contentBlockDelta events.

async def main():
    async for event in agent.stream_async("Tell me a short story."):
        if "data" in event:
            data = event["data"]

            if (
                "contentBlockDelta" in data
                and "delta" in data["contentBlockDelta"]
                and "text" in data["contentBlockDelta"]["delta"]
            ):
                print(
                    data["contentBlockDelta"]["delta"]["text"],
                    end="",
                    flush=True,
                )

asyncio.run(main())