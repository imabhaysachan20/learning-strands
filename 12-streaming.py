import asyncio
from strands import Agent,tool
import requests

@tool
def add(a,b):
    '''returns sum of two number a,b'''
    return a+b

@tool
def get_weather(location: str) -> dict:
    """
    Get current weather for any location.

    Returns:
    {
        "location": "Lucknow",
        "temperature_c": 32.1,
        "wind_speed_kmh": 12.5,
        "weather_code": 1
    }
    """

    # Step 1: Convert location -> coordinates
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_res = requests.get(
        geo_url,
        params={"name": location, "count": 1},
        timeout=10
    )
    geo_res.raise_for_status()

    results = geo_res.json().get("results")

    if not results:
        raise ValueError(f"Location '{location}' not found")

    place = results[0]
    lat = place["latitude"]
    lon = place["longitude"]

    # Step 2: Get weather
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_res = requests.get(
        weather_url,
        params={
            "latitude": lat,
            "longitude": lon,
            "current": [
                "temperature_2m",
                "wind_speed_10m",
                "weather_code",
            ],
        },
        timeout=10,
    )
    weather_res.raise_for_status()

    current = weather_res.json()["current"]

    return {
        "location": place["name"],
        "country": place.get("country"),
        "temperature_c": current["temperature_2m"],
        "wind_speed_kmh": current["wind_speed_10m"],
        "weather_code": current["weather_code"],
    }




agent = Agent(
    tools=[add,get_weather]
)


async def stream_chat(prompt: str):
    print("\n🤖 Assistant\n")

    full_response = ""
    currentTool = None
    stream = agent.stream_async(prompt)

    async for event in stream:
        try:

            # Text token
            if "data" in event:
                chunk = event["data"]

                full_response += chunk

                print(chunk, end="", flush=True)

            # Tool call
            elif event.get("type") == "tool_use_stream":
                tool = event["current_tool_use"]["name"]
                if (currentTool!=tool):
                    currentTool = tool
                    print(f"\n\n🔧 Using Tool: {tool}\n")

            # Final result
            elif "result" in event:

                print("\n\n✅ Complete")
        except Exception as e:
              print(f"\n\n❌ Stream Error: {e}",flush=True)

              if full_response:
                print("\n📄 Partial response preserved.",flush=True)


    return full_response


async def main():

    while True:

        prompt = input("\n🧑 You: ")

        if prompt.lower() in ["exit", "quit"]:
            break

        await stream_chat(prompt)


asyncio.run(main())