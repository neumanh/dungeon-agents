import asyncio

from dotenv import load_dotenv
from agents import Runner, SQLiteSession

from dungeon_agents.dm.agent import dm_agent


load_dotenv()


async def main():
    # Initialize the SQLite session for storing game sessions
    session = SQLiteSession(
        "dungeon_game",
        "data/dungeon_sessions.db",
    )

    print("=== Dungeon Adventure ===")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        result = await Runner.run(
            dm_agent,
            user_input,
            session=session,
        )

        print(f"\nDM: {result.final_output}\n")


if __name__ == "__main__":
    asyncio.run(main())