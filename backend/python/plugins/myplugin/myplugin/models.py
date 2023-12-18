from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import SecretStr
from pydevlake import ScopeConfig, ToolScope, Connection, ToolModel, Field

class CommerceCloudConnection(Connection):
    name: str
    token: SecretStr
    subscription_code: str

class FakeConnection(Connection):
    token: SecretStr


class FakeProject(ToolScope, table=True):
    url: str


class FakeScopeConfig(ScopeConfig):
    env: str

class FakePipeline(ToolModel, table=True):
    class State(Enum):
        PENDING = "pending"
        RUNNING = "running"
        FAILURE = "failure"
        SUCCESS = "success"

    id: str = Field(primary_key=True)
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    state: State