from django import template
register = template.Library()

@register.filter
def iconSelector(value):
    if value >0:
        return "dashboard/up.png"
    elif value <0:
        return "dn"
    else:
        return "-"

@register.filter
def playercheck(nlist, name):
    if name in nlist:
        return 1
    else:
        return '.'
