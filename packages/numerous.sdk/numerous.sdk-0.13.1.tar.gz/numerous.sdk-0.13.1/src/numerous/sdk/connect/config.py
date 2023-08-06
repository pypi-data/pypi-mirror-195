import os
from dataclasses import Field, dataclass, fields


def extract_field(field: Field, value: str) -> tuple[str, int]:
    if field.name == "MAX_STATUS_MESSAGE_LENGTH":
        return (field.name, int(value))
    elif field.name == "GRPC_MAX_MESSAGE_SIZE":
        return (field.name, int(value))
    else:
        raise ValueError(f"Unexpected field {field.name}")


@dataclass
class Config:
    MAX_STATUS_MESSAGE_LENGTH: int = 32
    GRPC_MAX_MESSAGE_SIZE: int = 2**28

    @staticmethod
    def from_environment():
        extracted_fields = (
            extract_field(field, os.environ[field.name])
            for field in fields(Config)
            if field.name in os.environ
        )
        environment = {key: value for key, value in extracted_fields}
        return Config(**environment)
