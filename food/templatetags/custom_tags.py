from django import template
register = template.Library()

@register.filter(name='remove')
def remove(value):
    return value.replace('_',' ')


# print("rajesh_sharma".split('_').join(' '))