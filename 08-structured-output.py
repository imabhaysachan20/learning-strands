# Normal LLM Output
# The customer's name is John.
# Priority is High.
# Issue relates to payment failure.
# Structured Output
# {
#   "customer_name": "John",
#   "priority": "High",
#   "issue": "Payment Failure"
# }

#Pydanctic Python's goto data validation library

from pydantic import BaseModel,Field,ValidationError
from typing import List,Literal,Annotated
from datetime import datetime,UTC
from strands import Agent

class User(BaseModel):
    username:str
    email:str
    age:int

u1 = User(username="imabhaysachan",email="abhay@gmail.com",age=3)
print(u1)
print(u1.model_dump()) #converts to python dict
print(u1.model_dump_json()) #json

try:
    u2 = User(username="imabhaysachan",email=None,age=3)
except ValidationError as e:
    print(e)


class User(BaseModel):
    uid:Annotated[int,Field(gt=0)]
    username:Annotated[str,Field(min_length=3,max_length=20)]
    email:str
    age:Annotated[int,Field(gt=13,lt=130)]
    verified_at: datetime|None = None
    bio:str=""
    is_active: bool = True
    full_name:str|None = None
 
u1 = User(uid=123,username="name",email="abhay@gmail.com")
u1.bio="hey"
print(u1.bio)
print(u1.model_dump_json(indent=2))

class BlogPost(BaseModel):
    title:str
    content:str
    view_count:int = 0
    is_published:bool = False
    tags:list[str] = Field(default_factory=list)
    created_at:datetime = Field(default_factory=lambda:datetime.now(tz=UTC))
    author_id:int|str
    status:Literal['published','draft','archieved'] = 'draft'
    slug:Annotated[str,Field(pattern="^[\w]+$")]

post = BlogPost(title="Hey there",content="lorem epsom 232",author_id=23,tag="22d")
print(post)



class Customer(BaseModel):
    name: str | None = None
    order_id: str | None = None

class Ticket(BaseModel):
    category: str = Field(description="Type of issue") #describe the feild for llm
    priority: str = Field(description="High, Medium or Low")
    issue: str = Field(description="Short summary of the problem")
    sentiment: str = Field(description="Positive, Neutral or Negative")
    customer: Customer



# When you define a Pydantic model:
# class Ticket(BaseModel):
#     priority: Literal["High", "Medium", "Low"]
#     issue: str

# Pydantic generates a JSON Schema:

# {
#   "type": "object",
#   "properties": {
#     "priority": {
#       "enum": ["High", "Medium", "Low"]
#     },
#     "issue": {
#       "type": "string"
#     }
#   },
#   "required": ["priority", "issue"]
# }

# This schema is sent to the LLM.

# Validation happens after the LLM generates output.

# Example:

# class Ticket(BaseModel):
#     priority: str
#     issue: str

# LLM returns:

# {
#   "priority": 123,
#   "issue": "Payment failed"
# }

# Pydantic checks:

# Ticket.model_validate(response)

# and raises:

# ValidationError:
# priority
#   Input should be a valid string
# Missing fields

# Schema:

# class Ticket(BaseModel):
#     priority: str
#     issue: str

# Response:

# {
#   "priority": "High"
# }

# Validation error:

# ValidationError:
# issue
#   Field required

# So invalid data never reaches your code.

# Without validation:

# print(ticket.issue)

# might crash later.

# With validation:

# ValidationError

# is raised immediately.


agent = Agent(system_prompt='''
You are a support ticket analysis agent.

Your job is to analyze support tickets and extract information into the provided structured schema.

Rules:
1. Read the ticket carefully.
2. Identify the primary issue being reported.
3. Classify the ticket into the most appropriate category.
4. Assign a priority level:
   - High: payment failures, account lockouts, security issues, service unavailable, multiple failed attempts.
   - Medium: subscription problems, feature malfunctions, delayed processing.
   - Low: general questions, feature requests, minor inconveniences.
5. Determine the customer's sentiment:
   - Positive
   - Neutral
   - Negative
6. Extract all available customer information.
7. If a field cannot be determined from the ticket, use null instead of guessing.
8. Return only information supported by the ticket.
9. Do not invent names, order IDs, dates, or other details.
10. Follow the provided output schema exactly.
''')

ticket_text = '''
Analyze this ticket Customer Name: John Smith
                Order ID: ORD-12345
                I purchased the Premium Plan yesterday, but my account is still showing the Free Plan.
                Payment was deducted successfully from my credit card.
                Please activate my subscription as soon as possible.
'''

try:
    result = agent(ticket_text,structured_output_model=Ticket
    )
    print(result)
except ValueError:
    print( {
        'error':'invalid response generated'
    })


try:
    result = agent(ticket_text,structured_output_model=Ticket
    )
    print(result)
except ValueError as e: #better message
    print({
        "error": "Validation failed",
        "details": str(e)
    })

MAX_RETRIES = 3

for attempt in range(MAX_RETRIES):
    try:
        result = agent(
            ticket_text,
            structured_output_model=Ticket
        )

        print(result)
        break

    except ValueError:
        print(f"Attempt {attempt+1} failed")

else:
    print({
        "error": "Failed after 3 retries"
    })

