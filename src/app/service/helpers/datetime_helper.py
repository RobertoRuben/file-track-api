from datetime import datetime
import pytz


class DateTimeHelper:
    """
    Helper class for datetime-related operations.
    Provides functionalities for timezone conversion and formatting.
    """

    @staticmethod
    def to_lima_timezone(dt: datetime) -> datetime:
        """
        Converts a datetime to Lima/Peru timezone.

        :param dt: Datetime object to convert
        :return: Datetime object in Lima/Peru timezone with tzinfo removed
        """
        if dt is None:
            return None

        lima_tz = pytz.timezone('America/Lima')

        if dt.tzinfo:
            dt_lima = dt.astimezone(lima_tz)
        else:
            dt_lima = pytz.utc.localize(dt).astimezone(lima_tz)

        return dt_lima.replace(tzinfo=None)


datetime_helper = DateTimeHelper()
