from __future__ import annotations
import sys
from sqlmodel import SQLModel, Field

class TestUser(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str

print(f"Python Version: {sys.version}")
print(f"TestUser annotations: {TestUser.__annotations__}")
print(f"TestUser dict keys: {TestUser.__dict__.keys()}")
