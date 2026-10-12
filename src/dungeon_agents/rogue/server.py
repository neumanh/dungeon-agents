from dotenv import load_dotenv

load_dotenv()

import uvicorn

from a2a.types import AgentCard, AgentInterface, AgentSkill
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes

from starlette.applications import Starlette

from dungeon_agents.common.executor import PlayerAgentExecutor

from dungeon_agents.rogue.agent import rogue_agent
from agents import SQLiteSession


# Define the Rogue agent skill
rogue_skill = AgentSkill(
    id="stealth",
    name="Stealth",
    description="Can move silently and set traps.",
    tags=["stealth", "rogue", "fantasy"],
    examples=[
        "Attack the goblin",
        "Defend the party",
        "Move silently",
        "Set a trap",
        "What do you do?",
    ],
    input_modes=["text/plain"],
    output_modes=["text/plain"],
)

# Define the Rogue agent card with its skill
rogue_card = AgentCard(
    name="Rogue",
    description="A skilled and cunning fantasy rogue who specializes in stealth and traps.",
    version="0.1.0",
    supported_interfaces=[
        AgentInterface(
            url="http://127.0.0.1:9003",
            protocol_binding="JSONRPC",
            protocol_version="1.0",
        )
    ],
    skills=[rogue_skill],
)

# Define the SQLite session for storing game sessions
rogue_session = SQLiteSession(
    "dungeon_game",
    "data/rogue_sessions.db",
)

rogue_executor = PlayerAgentExecutor(player_agent=rogue_agent, session=rogue_session)

# Set up the request handler for the Rogue agent
request_handler = DefaultRequestHandler(
    agent_executor=rogue_executor,
    task_store=InMemoryTaskStore(),
    agent_card=rogue_card,
)

routes = []

routes.extend(create_agent_card_routes(rogue_card))

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
        port=9003,
    )
