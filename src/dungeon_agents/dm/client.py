import asyncio

from a2a.helpers import new_text_message
from a2a.types import SendMessageRequest
from a2a.client import ClientFactory


fighter_url = "http://127.0.0.1:9001"

factory = ClientFactory()

message = new_text_message("Attack the goblin")

message_request = SendMessageRequest(
    message=message
)


async def main():
    client = await factory.create_from_url(fighter_url)

    responses = client.send_message(message_request)

    async for response in responses:
        print(response)


asyncio.run(main())