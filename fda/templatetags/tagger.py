from django import template

register = template.Library()


@register.filter(name='get_id')
def get(all_data, index):
    return all_data[index].get('_id')


@register.filter(name='zfill')
def get(some_string):
    return some_string.zfill(10)
