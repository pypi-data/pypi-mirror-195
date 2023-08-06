from dataclasses import dataclass
from typing import Any


@dataclass
class Scenario:
    id: str
    name: str

    @staticmethod
    def from_document(data: dict[str, Any]) -> "Scenario":
        return Scenario(id=data["id"], name=data.get("scenarioName", ""))
