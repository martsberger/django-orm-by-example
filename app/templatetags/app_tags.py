from django.template import Library

register = Library()


@register.filter
def get_dictionary_item(d, key):
    return d.get(key)
