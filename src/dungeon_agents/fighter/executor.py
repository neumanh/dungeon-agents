from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.helpers import new_text_message
from agents import Runner, SQLiteSession

from dungeon_agents.fighter.agent import fighter_agent



class FighterAgentExecutor(AgentExecutor):

    def __init__(self):
        # Initialize the SQLite session for storing game sessions
        self.session = SQLiteSession(
            "dungeon_game",
            "data/fighter_sessions.db",
        )

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        user_input = context.get_user_input()

        # response = f"Fighter received: {user_input}"
        result = await Runner.run(
            fighter_agent,
            user_input,
            session=self.session,
        )
        response = result.final_output

        await event_queue.enqueue_event(
            new_text_message(response)
        )

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        raise NotImplementedError