from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.helpers import new_text_message
from agents import Runner, SQLiteSession, Agent



class PlayerAgentExecutor(AgentExecutor):
    """Executor for the Player agent, responsible for handling requests
      and executing the agent's logic."""

    def __init__(self, player_agent: Agent, session: SQLiteSession):
        """Initialize the PlayerAgentExecutor with the provided agent and session."""
        self.player_agent = player_agent
        self.session = session

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Execute the Player agent's logic based on the provided context
          and enqueue events to the event queue."""
        user_input = context.get_user_input()

        # response = f"Fighter received: {user_input}"
        result = await Runner.run(
            self.player_agent,
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