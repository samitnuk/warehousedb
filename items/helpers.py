from datetime import timedelta


def get_date_range(range_start, range_stop):
    """
    Receives two dates.
    Returns list of dates between two dates

    """

    if range_start > range_stop:
        range_start, range_stop = range_stop, range_start

    date_range = []
    while range_start <= range_stop:
        date_range.append(range_start)
        range_start += timedelta(days=1)

    return date_range
