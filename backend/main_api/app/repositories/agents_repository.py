from app.repositories.base import BaseRepository
from sqlalchemy import insert, select
from app.models.agents import Agent
from app.schemas.agents import AgentCreateRepository, AgentUpdate
class AgentRepository(BaseRepository[Agent, AgentCreateRepository, AgentUpdate]):
    model = Agent
