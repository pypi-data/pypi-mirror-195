from dataclasses import dataclass
from typing import Any

from .component import Component, get_components_from_scenario_document


@dataclass
class Scenario:
    id: str
    name: str
    components: dict[str, Component]

    @staticmethod
    def from_document(data: dict[str, Any]) -> "Scenario":
        return Scenario(
            id=data["id"],
            name=data.get("scenarioName", ""),
            components=get_components_from_scenario_document(data),
        )
