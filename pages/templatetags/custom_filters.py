from django import template

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
