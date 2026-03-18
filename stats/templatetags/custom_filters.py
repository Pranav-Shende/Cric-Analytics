from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# from django import template

# register = template.Library()

# @register.filter
# def get_item(dictionary, key):
#     """Allows accessing dictionary keys like rankings|get_item:'batting'"""
#     if dictionary:
#         return dictionary.get(key)
#     return None
