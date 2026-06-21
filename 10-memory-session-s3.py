from strands import Agent
import boto3
import json
from botocore.exceptions import ClientError

BUCKET_NAME = "learning-strands"
SESSION_ID = "abhay"

s3 = boto3.client("s3")


def load_session(session_id):
    try:
        response = s3.get_object(
            Bucket=BUCKET_NAME,
            Key=f"sessions/{session_id}.json"
        )

        return json.loads(
            response["Body"].read().decode("utf-8")
        )

    except ClientError:
        return []


def save_session(session_id, messages):
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=f"sessions/{session_id}.json",
        Body=json.dumps(messages, default=str),
        ContentType="application/json"
    )



messages = load_session(SESSION_ID)
print(messages)
agent = Agent(messages=messages)

print("Welcome to S3-backed memory!")

while True:
    user_prompt = input("User: ").strip()

    if user_prompt.lower() == "exit":
        break

    response = agent(user_prompt)

    save_session(
        SESSION_ID,
        agent.messages
    )

print("Goodbye!")