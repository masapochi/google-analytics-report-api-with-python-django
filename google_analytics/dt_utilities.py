from django.utils import timezone


def convert_dt_to_str(dt_obj):
    return dt_obj.strftime("%Y-%m-%d")


def calc_beginning_of_week():
    today = timezone.now()
    day_of_week = today.weekday()
    to_beginning_of_week = timezone.timedelta(days=day_of_week)
    beginning_of_week = today - to_beginning_of_week

    return beginning_of_week
