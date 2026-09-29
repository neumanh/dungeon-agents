import uvicorn

from a2a.types import AgentCard, AgentInterface, AgentSkill

from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore

from a2a.server.routes import (
    create_agent_card_routes,
    create_jsonrpc_routes,
)
from starlette.applications import Starlette

from dungeon_agents.fighter.executor import FighterAgentExecutor

# Define the Fighter agent skill
fighter_skill = AgentSkill(
    id="combat",
    name="Combat",
    description="Can participate in fantasy combat and make combat decisions.",
    tags=["combat", "fighter", "fantasy"],
    examples=[
        "Attack the goblin",
        "Defend the party",
        "What do you do?",
    ],
    input_modes=["text/plain"],
    output_modes=["text/plain"],
)

# Define the Fighter agent card with its skill
fighter_card = AgentCard(
    name="Fighter",
    description="A brave fantasy fighter who specializes in combat.",
    version="0.1.0",
    supported_interfaces=[
        AgentInterface(
            url="http://127.0.0.1:9001",
            protocol_binding="JSONRPC",
            protocol_version="1.0",
        )
    ],
    skills=[fighter_skill],
)

# Set up the request handler for the Fighter agent
request_handler = DefaultRequestHandler(
    agent_executor=FighterAgentExecutor(),
    task_store=InMemoryTaskStore(),
    agent_card=fighter_card,
)

routes = []

routes.extend(create_agent_card_routes(fighter_card))

routes.extend(
    create_jsonrpc_routes(
        request_handler,
        rpc_url="/",
    )
)

app = Starlette(routes=routes)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=9001,
    )
