from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='kb')
def kb(value, arg):
    return "{}".format(value/1000)[:3] + "KB"