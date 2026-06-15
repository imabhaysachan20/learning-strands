from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from strands_tools import file_read, file_write, editor

SYSTEM_PROMPT = """
You are a Basic Copilot Agent.
You can read and write local files.
You help users identify bugs in code and generate corrected versions.
"""

session_manager = FileSessionManager(
    session_id="basic-copilot"
)

copilot = Agent(
    system_prompt=SYSTEM_PROMPT,
    session_manager=session_manager,
    tools=[
        file_read,
        file_write,
        editor
    ]
)

response = copilot("""
Read 'buggy.py'.
Find the bug.
Write the corrected version to 'fixed_buggy.py'.
Explain what you fixed.
""")

print(response)