from django import template
from django.urls import resolve

register = template.Library()


@register.simple_tag(takes_context=True)
def get_url_name(context):
    request = context["request"]
    print(resolve(request.path_info).url_name)
    return resolve(request.path_info).url_name
