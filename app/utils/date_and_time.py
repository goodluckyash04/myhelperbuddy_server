import datetime


class DateAndTime:
    @staticmethod
    def get_today_date(
        include_time: bool = True,
        as_string: bool = False,
        date_format: str = "%d-%m-%Y",
        timezone: datetime.timezone = None
    ) -> str | datetime.date | datetime.datetime:
        """Returns today's date or datetime, optionally formatted as a string."""
        now = datetime.datetime.now(tz=timezone) if timezone else datetime.datetime.now()

        result = now if include_time else now.date()
        return result.strftime(date_format) if as_string else result

    @staticmethod
    def format_date(date_obj: datetime.date | datetime.datetime | str, output_format: str = "%d-%m-%Y",
                    input_format: str = None):
        """Formats a given date/datetime object or string into a specified format."""

        if isinstance(date_obj, str):
            if not input_format:
                raise ValueError("input_format must be provided when date_obj is a string.")
            date_obj = datetime.datetime.strptime(date_obj, input_format)  # Convert string to datetime

        return date_obj.strftime(output_format)

    @staticmethod
    def date_difference(date1: datetime.date, date2: datetime.date):
        """Returns the difference in days between two dates."""
        return abs((date2 - date1).days)

    @staticmethod
    def add_days(date_obj: datetime.date, days: int):
        """Adds or subtracts days from a given date."""
        return date_obj + datetime.timedelta(days=days)


date = DateAndTime()