from datetime import datetime, timezone


def get_current_df() -> datetime:
    df = datetime.now(tz=timezone.utc)
    return df.replace(tzinfo=None)