import signal
import sys
import time

import click

from datetime import datetime
from pathlib import Path
from typing import Optional

from yaspin import yaspin, Spinner

from .lifetimer import Lifetimer
from .config.config import Config


def init() -> int:
    print("Please, enter your last date/time of your life.")
    while True:
        year = click.prompt("Year", type=click.IntRange(datetime.today().year, 9999))
        month = click.prompt("Month", default=12, type=click.IntRange(1, 12))
        day = click.prompt("Day", default=31, type=click.IntRange(1, 31))
        hour = click.prompt("Hour", default=23, type=click.IntRange(0, 23))
        minute = click.prompt("Minute", default=59, type=click.IntRange(0, 59))
        second = click.prompt("Second", default=59, type=click.IntRange(0, 59))

        try:
            Lifetimer.validate_datetime(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                second=second,
            )
        except ValueError:
            print("Please, check again your last date/time.")
            continue
        except OverflowError:
            print("It's too large to count your lifespan.")
            continue
        else:
            break

    config = Config.create()
    config.set("year", year)
    config.set("month", month)
    config.set("day", day)
    config.set("hour", hour)
    config.set("minute", minute)
    config.set("second", second)
    config.save()

    return 0


class Command:
    def __init__(self, argv: Optional[str] = None) -> None:
        self.argv = argv or sys.argv[:]
        self.prog_name = Path(self.argv[0]).name
        if self.prog_name == "__main__.py":
            self.prog_name = "python -m lifetimer"

    def execute(self) -> int:
        if len(self.argv) > 1 and self.argv[1] == "init":
            return init()

        config = Config.create()

        if config.get("year") is None:
            init()

        lifetimer = Lifetimer(
            int(config.get("year")),
            int(config.get("month", 12)),
            int(config.get("day", 31)),
            int(config.get("hour", 23)),
            int(config.get("minute", 59)),
            int(config.get("second", 59)),
        )

        sp = Spinner(
            [
                "🕛",
                "🕐",
                "🕑",
                "🕒",
                "🕓",
                "🕔",
                "🕕",
                "🕖",
                "🕗",
                "🕘",
                "🕙",
                "🕚",
            ],
            1000,
        )

        def signal_handler(signum: int, frame: str, spinner: Spinner) -> None:
            spinner.fail("Bye! Remember")
            spinner.stop()
            sys.exit(0)

        with yaspin(spinner=sp, sigmap={signal.SIGINT: signal_handler}, text=lifetimer):
            time.sleep(lifetimer.get_lifespan())

        print("Your last day of your life was gone.")
        print("See you again!")

        return 0


def execute_from_command_line(argv: Optional[str] = None) -> int:
    command = Command(argv)
    return command.execute()


if __name__ == "__main__":
    execute_from_command_line()
