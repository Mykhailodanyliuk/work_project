from django import template

register = template.Library()


@register.filter(name='get_id')
def get(all_data, index):
    return all_data[index].get('_id')
