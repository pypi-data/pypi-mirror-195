from datetime import datetime


class Lifetimer:
    def __init__(
        self,
        year: int,
        month: int = 12,
        day: int = 31,
        hour: int = 23,
        minute: int = 59,
        second: int = 59,
    ) -> None:
        self.end_day = self.validate_datetime(
            year,
            month,
            day,
            hour,
            minute,
            second,
        )

    def __str__(self) -> str:
        if self.get_lifespan() == 0:
            return "You get another life!"
        else:
            return f"You have {self.get_lifespan():,} seconds to live."

    def get_lifespan(self) -> int:
        today = datetime.today()

        if today < self.end_day:
            delta = self.end_day - today
            total_seconds = round(delta.total_seconds())
            return total_seconds
        else:
            return 0

    @classmethod
    def validate_datetime(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
    ) -> datetime:
        try:
            dt = datetime(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                second=second,
            )
            delta = dt - datetime.today()
            total_seconds = round(delta.total_seconds())

            if total_seconds > 9223372036:
                raise OverflowError
            if total_seconds < 0:
                raise ValueError

            return dt
        except ValueError:
            raise ValueError("Invalid datetime value")
        except TypeError:
            raise TypeError("Invalid datetime type")
        except OverflowError:
            raise OverflowError("Too large to count the datetime")
