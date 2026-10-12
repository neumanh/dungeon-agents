from dotenv import load_dotenv

load_dotenv()

import uvicorn

from a2a.types import AgentCard, AgentInterface, AgentSkill
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes

from starlette.applications import Starlette

from dungeon_agents.common.executor import PlayerAgentExecutor

from dungeon_agents.mage.agent import mage_agent
from agents import SQLiteSession


# Define the Mage agent skill
mage_skill = AgentSkill(
    id="magic",
    name="Magic",
    description="Can cast spells and use magical abilities.",
    tags=["magic", "mage", "fantasy"],
    examples=[
        "Attack the goblin",
        "Defend the party",
        "What do you do?",
    ],
    input_modes=["text/plain"],
    output_modes=["text/plain"],
)

# Define the Mage agent card with its skill
mage_card = AgentCard(
    name="Mage",
    description="A wise and powerful fantasy mage who specializes in magic.",
    version="0.1.0",
    supported_interfaces=[
        AgentInterface(
            url="http://127.0.0.1:9002",
            protocol_binding="JSONRPC",
            protocol_version="1.0",
        )
    ],
    skills=[mage_skill],
)

# Define the SQLite session for storing game sessions
mage_session = SQLiteSession(
    "dungeon_game",
    "data/mage_sessions.db",
)

mage_executor = PlayerAgentExecutor(player_agent=mage_agent, session=mage_session)

# Set up the request handler for the Mage agent
request_handler = DefaultRequestHandler(
    agent_executor=mage_executor,
    task_store=InMemoryTaskStore(),
    agent_card=mage_card,
)

routes = []

routes.extend(create_agent_card_routes(mage_card))

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
        port=9002,
    )
