from django import template
from django.utils.timezone import now
from django.utils.timesince import timesince
register = template.Library()

@register.filter
def comma_seperated(values, attr):
    try:
        return ', '.join([getattr(value, attr) for value in values])
    except Exception:
        return ''

@register.filter
def js_str(value):
    return value.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')

@register.filter
def humanize_time(value):
    try:
        time_diff = now() - value
        time_diff = time_diff.total_seconds()
        if time_diff < 60:
            return 'just now'
        if time_diff > 2592000:
            return value
        return f'{timesince(value)} ago'
    except Exception as e:
        return ''
