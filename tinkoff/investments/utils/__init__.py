from datetime import datetime, timezone


def offset_aware_datetime(
    dt: datetime, tzinfo: timezone = timezone.utc
) -> datetime:
    if dt.tzinfo:
        return dt
    else:
        return dt.replace(tzinfo=tzinfo)


__all__ = ["offset_aware_datetime"]
