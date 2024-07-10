import datetime
from django import template
from django.utils.timezone import localtime

register = template.Library()

@register.filter
def humanize_due_date(due_date):
    now = localtime()
    if due_date.date() == now.date():
        return due_date.strftime('%I:%M %p')
    elif due_date < now:
        return f"Overdue ({(now - due_date).days} days ago)"
    else:
        return due_date.strftime('%b %d, %Y')
    
@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})