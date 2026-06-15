# Without session management: the agent only remembers things while the Python Agent object exists.
# With session management: the conversation state is stored externally, so the agent can continue a conversation even after your script exits and restarts.



# A session manager stores the conversation history somewhere persistent:

# memory cache,
# file,
# database,
# Redis,
# DynamoDB,
# etc.
from strands import Agent
from strands.session.file_session_manager import FileSessionManager

# Create a persistent session
session_manager = FileSessionManager(
    session_id="abhay-chat"
)

agent = Agent(
    session_manager=session_manager
)

response = agent("My name is Abhay.")
#close the application then try
#it remembers !
response = agent("what is my name")

# S3SessionManager — stores sessions in an Amazon S3 bucket.
