from django import template

register = template.Library()

@register.filter
def add_attribute(value, attribute):
    attrs = value.field.widget.attrs
    attrs.update(attribute)
    return value