from django import template

register = template.Library()

@register.filter
def longitude(value):
    if value > 0:
        side = 'E'
    elif value < 0:
        side = 'W'
    else:
        side = ''
    return get_degree(value, side)

@register.filter
def latitude(value):
    if value > 0:
        side = 'N'
    elif value < 0:
        side = 'S'
    else:
        side = ''
    return get_degree(value, side)

def get_degree(value, side):
    result = u'{deg}\u00b0{min}\'{sec}"{side}'
    degree = int(value)
    minute = int((value - degree) * 60)
    second = round((((value - degree) * 60) - minute) * 60)
    if second >= 60:
        second = 0
        minute += 1
    return result.format(side=side, deg=degree, min=minute, sec=second)

