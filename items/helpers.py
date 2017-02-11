from datetime import datetime, timedelta

from .models import Category


def get_choices(items):
    """
    Return list of tuples
    """
    return [(item.id, "{} {} / {}".format(
            item.title,
            item.part_number,
            item.notes)) for item in items]


def get_date_range(range_start, range_stop):
    """
    Return list of dates between two dates
    """
    if range_start > range_stop:
        range_start, range_stop = range_stop, range_start
    date_range = []
    while range_start <= range_stop:
        date_range.append(range_start)
        range_start += timedelta(days=1)
    return date_range


def get_objects_list(objects_, total_changes, field_name):
    """
    Return list of of next lists: [object, [changes of this object]]
    """
    objects_list = []
    for object_ in objects_:
        objects_list.append(
            [object_, total_changes.filter(**{field_name: object_})])
    return objects_list


def get_categories_list(objects_, total_changes, field_name):
    """
    Return list of next lists: [category, objects_list]
    """
    categories = Category.objects.all()
    categories_list = dict()
    for category in categories:
        category_objects = objects_.filter(category=category)
        if category_objects:
            categories_list[category.title] = get_objects_list(
                objects_=category_objects,
                total_changes=total_changes,
                field_name=field_name
            )
    return sorted(categories_list.items())


def get_context_for_list_by_dates(
        object_model,
        objectchange_model,
        field_name,
        range_start,
        range_stop
):
    if range_start is None:
        range_start = datetime.today() - timedelta(days=7)
    if range_stop is None:
        range_stop = datetime.today()

    data = dict()
    data['objects_'] = object_model.objects.all()
    data['total_changes'] = objectchange_model.objects.filter(
        changed_at__gte=range_start,
        changed_at__lte=range_stop)
    data['field_name'] = field_name

    if field_name == 'item':
        data_list = get_categories_list(**data)
    else:
        data_list = get_objects_list(**data)

    context = {
        'initial_range_start': datetime.strftime(range_start, "%Y-%m-%d"),
        'initial_range_stop': datetime.strftime(range_stop, "%Y-%m-%d"),
        'date_range': get_date_range(range_start, range_stop),
        'data_list': data_list}
    return context
