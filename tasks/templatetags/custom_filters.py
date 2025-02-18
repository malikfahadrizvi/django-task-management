from django import template

register = template.Library()

@register.filter
def status_color(status):
    return {
        'pending': 'warning',
        'in-progress': 'primary',
        'completed': 'success'
    }.get(status, 'secondary')

@register.filter
def priority_color(priority):
    return {
        'low': 'success',
        'medium': 'warning',
        'high': 'danger'
    }.get(priority, 'secondary')