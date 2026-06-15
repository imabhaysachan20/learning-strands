# inbuilt calculator tool

from strands import Agent
from strands_tools.calculator import calculator
from strands import tool
# agent = Agent(
#     system_prompt="You are a helpful assistant.",
#     tools=[calculator]
# )

# response = agent("What is (123 * 456) / 8?")
# print(response)

#custom grading tool

@tool
def calculate_grade(marks: int, total: int) -> str:
    """
    Calculate the percentage and assign a grade.
    Use this tool whenever the user asks about exam grades.
    """
    percentage = (marks / total) * 100

    if percentage >= 90:
        grade = "A"
    elif percentage >= 75:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    else:
        grade = "D"

    return f"Percentage: {percentage:.2f}% | Grade: {grade}"


# Tool Descriptions Matter!!
# The docstring of a custom tool is extremely important. The LLM reads it to understand:

# When to call the tool.
# What the tool does.
# What arguments it expects.
# What output it returns.

agent = Agent(
    system_prompt="You are a personal tutor.",
    tools=[calculate_grade]
)

print(agent("I scored 82 out of 100. What is my grade?"))