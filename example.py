import openai
import asyncio

client = openai.OpenAI(
    api_key="anything",
    base_url="http://0.0.0.0:4000"
)

# request sent to model set on litellm proxy, `litellm --model`
# set tempature to 0 to get deterministic response
response = client.chat.completions.create(model="fireworks-llama-v3p1-70b-instruct", messages = [
    {
        "role": "user",
        "content": "this is a test request, write a short poem"
    }
], temperature=0)

print(response)

response = client.embeddings.create(
  model="fireworks-nomic-embed-text-v1.5",
  input="The food was delicious and the waiter...",
)

print(response)

# async example
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key="anything",
    base_url="http://0.0.0.0:4000"
)


async def main() -> None:
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="fireworks-llama-v3p1-70b-instruct",
        temperature=0
    )
    print(chat_completion)

asyncio.run(main())