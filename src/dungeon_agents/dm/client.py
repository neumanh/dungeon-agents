import asyncio

from a2a.helpers import new_text_message
from a2a.types import SendMessageRequest
from a2a.client import ClientFactory


fighter_url = "http://127.0.0.1:9001"
mage_url = "http://127.0.0.1:9002"
rogue_url = "http://127.0.0.1:9003"

factory = ClientFactory()

message = new_text_message("What do you do against the goblin?")

message_request = SendMessageRequest(
    message=message
)


async def main():
    client = await factory.create_from_url(rogue_url)

    responses = client.send_message(message_request)

    async for response in responses:
        print(response)


asyncio.run(main())