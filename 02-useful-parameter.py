from strands import Agent
from strands import tool
from pydantic import BaseModel



# some useful parameters available in strands agent instance

# agent2 = Agent(
#     name="Python teacher",
#     description="Python teacher",
#     system_prompt="You are a helpful Python tutor. Teach concept asked using some real life example",
   
# )

# response = agent2("what is a iterator")

# help(Agent) ##to see all the available parameters in the Agent instance

#some very frequently used and useful parameters

#model

# agent = Agent(
#     model="deepseek.v3.2"
# )

# response = agent("Who are you?")
# print(response)


# Hello! I'm DeepSeek, an AI assistant created by DeepSeek Company. I'm here to help you with a wide variety of questions and tasks! 😊

# I'm a text-based AI model with some pretty neat capabilities:
# - I can engage in detailed conversations and answer questions on many topics
# - I support file uploads (images, PDFs, Word docs, Excel files, etc.) and can read text content from them
# - I have a context window of 128K tokens
# - I offer web search functionality (though you'd need to manually enable it in the interface)
# - I'm completely free to use with no current plans for charges


##System prompt


# agent4 = Agent(
#     model="deepseek.v3.2",
#     system_prompt="""
#     You are a senior Python mentor.
#     Explain concepts with simple examples.
#     Never write more than 100 words unless asked.
#     """
# )

# print(agent4("Explain iterators."))

# tools
@tool
def multiply(a: int, b: int):
    """Multiply two numbers."""
    return a * b

# agent = Agent(
#     tools=[multiply]
# )

# print(agent("What is 123 times 456?"))

# # Let me calculate that for you!
# # Tool #1: multiply
# # 123 times 456 equals **56,088**!123 times 456 equals **56,088**!

#messages let you feed convo history into context window

# agent = Agent(
#     messages=[
#         {
#             "role": "user",
#             "content": [{"text": "My name is Abhay."}]
#         },
#         {
#             "role": "assistant",
#             "content": [{"text": "Nice to meet you, Abhay!"}]
#         }
#     ]
# )

# # Usually you won't use this directly—Strands manages history automatically—but it's useful for loading saved conversations.

# print(agent("What is my name?"))


#name descriotion

# agent = Agent(
#     name="PythonTutor",
#     description="Expert in Python programming and debugging."
# )

# Imagine you have three agents:

# ResearchAgent
# CodingAgent
# MathAgent

# A supervisor agent can decide which one should handle a task based on the descriptions.


# structured_output_model
# Instead of getting free-form text, you can force the model to return a Python object.
# class Person(BaseModel):
#     name: str
#     age: int
#     occupation: str

# agent = Agent(
#     structured_output_model=Person
# )

# result = agent(
#     "Extract details: Alice is a 28-year-old software engineer."
# )

# print(result)

# I have all the required details to extract the information. Let me call the tool now!
# Tool #1: Person
# {"name":"Alice","age":28,"occupation":"Software Engineer"}

# limits

# Limits prevent your agent from going out of control.
# agent = Agent(
#     tools=[multiply],
#     limits=Limits(
#         max_iterations=5
#     )
# )


