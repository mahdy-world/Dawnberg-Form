from django import template
from ..models import QuestionOption

register = template.Library()


@register.filter(name='get_option')
def get_option(value):
    options = value.split(',')
    string_options = []
    for option_id in options:
        option = QuestionOption.objects.get(id=int(option_id))
        string_options.append(option.option)
    return string_options
