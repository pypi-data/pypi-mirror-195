from typing import List, Optional

from pydantic import BaseModel


class Action(BaseModel):
    action_name: str
    path: str
    commands: List[str]
    timeout: Optional[float] = None


class Setting(BaseModel):
    name: str
    actions: List[Action]
