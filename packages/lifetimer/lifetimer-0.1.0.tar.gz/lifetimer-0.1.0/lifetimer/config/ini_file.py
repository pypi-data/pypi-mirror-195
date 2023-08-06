from configparser import ConfigParser
from pathlib import Path
from typing import Any

from .file import ConfigFile


class INIFile(ConfigFile):
    def __init__(self, path: str | Path) -> None:
        if isinstance(path, str):
            path = Path(path)
        self._path = path
        self._config_parser = ConfigParser()

    def exists(self) -> bool:
        return self._path.exists()

    def read(self) -> dict[str, Any]:
        self._config_parser.read(self._path)
        return dict(self._config_parser.items("ENDTIME"))

    def write(self, config: dict[str, Any]) -> None:
        if self.exists() is False:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.touch(mode=0o600)

        self._config_parser["ENDTIME"] = config

        with open(self._path, "w", encoding="utf-8", newline="") as config_file:
            self._config_parser.write(config_file)
