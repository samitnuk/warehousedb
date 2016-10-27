from datetime import timedelta


def get_choices(items):

    return [(item.id, "{} {} ~~~ {}".format(
            item.title,
            item.part_number,
            item.notes)) for item in items]


def get_date_range(range_start, range_stop):
    """
    Receives two dates.
    :return: list of dates between two dates

    """

    if range_start > range_stop:
        range_start, range_stop = range_stop, range_start

    date_range = []
    while range_start <= range_stop:
        date_range.append(range_start)
        range_start += timedelta(days=1)

    return date_range


def get_objects_list(
        range_start,
        range_stop,
        object_model,
        objectchange_model,
        field_name
):
    """

    :return: list of lists [object, [changes of this object]]
    """
    total_changes = objectchange_model.objects.filter(
        changed_at__gte=range_start,
        changed_at__lte=range_stop
    )

    objects_ = object_model.objects.all()

    objects_list = []
    for object_ in objects_:
        objects_list.append(
            [object_, total_changes.filter(**{field_name: object_})]
        )

    return objects_list
