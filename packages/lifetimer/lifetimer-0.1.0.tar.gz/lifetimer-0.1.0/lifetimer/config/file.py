from typing import Any


class ConfigFile:
    def exists(self) -> bool:
        raise NotImplementedError()

    def read(self) -> dict[str, Any]:
        raise NotImplementedError()

    def write(self, config: dict[str, Any]) -> None:
        raise NotImplementedError()
