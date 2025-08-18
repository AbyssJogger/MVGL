from django import template

register = template.Library()

@register.filter
def comma_seperated(values, attr):
    try:
        print(values)
        return ', '.join([getattr(value, attr) for value in values])
    except Exception:
        return ''
