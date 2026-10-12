import asyncio

from a2a.helpers import new_text_message
from a2a.types import SendMessageRequest
from a2a.client import ClientFactory

from dungeon_agents.common.game_state import GameState


agent_urls = {
    "fighter": "http://127.0.0.1:9001",
    "mage": "http://127.0.0.1:9002",
    "rogue": "http://127.0.0.1:9003",
}

factory = ClientFactory()

client_dict = {
    "fighter": None,
    "mage": None,
    "rogue": None,
}

game_state = GameState()  # Initialize the game state with default NPC HP

async def main():
    while True:
        character = input("Who should act? ").lower()

        if character == "quit":
            print("Game over!")
            break

        current_url = agent_urls.get(character)
        if not current_url:
            print(f"Unknown character: {character}")
            continue

        client = client_dict.get(character)
        if not client:
            client = await factory.create_from_url(current_url)
            client_dict[character] = client

        user_message = input("What should the character do? ")
        if not user_message:
            print("No action provided. Next turn.")
            continue

        message = new_text_message(user_message)

        message_request = SendMessageRequest(
            message=message
        )

        # Send the message and print the response here
        responses = client.send_message(message_request)

        async for response in responses:
            response_text = response.message.parts[0].text
            print(f'[{character.capitalize()}]\n  {response_text}')


asyncio.run(main())