from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from platformdirs import user_config_path

from .file import ConfigFile
from .ini_file import INIFile


CONFIG_DIR = Path(user_config_path("lifetimer", appauthor=False, roaming=True))

_default_config: Config | None = None


class Config:
    default_config: dict[str, Any] = {
        "year": 0,
        "month": 12,
        "day": 31,
        "hour": 23,
        "minute": 59,
        "second": 59,
    }

    def __init__(self) -> None:
        self._config = deepcopy(self.default_config)

    @classmethod
    def create(cls) -> Config:
        global _default_config

        if _default_config is None:
            _default_config = cls()
            config_file = INIFile(CONFIG_DIR / "config.ini")
            _default_config.set_config_source_file(config_file)

            if config_file.exists():
                _default_config.merge(config_file.read())

        return _default_config

    def get(self, setting_name: str, default: Any = None) -> Any:
        return self._config[setting_name] or default

    def set(self, setting_name: str, value: str | int) -> None:
        self._config[setting_name] = value

    def merge(self, config: dict[str, Any]) -> None:
        for key in config.keys():
            self._config[key] = config[key]

    def set_config_source_file(self, file: ConfigFile) -> None:
        self._file = file

    def save(self) -> None:
        self._file.write(self._config)
