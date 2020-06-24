from django import template
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter('markdown', autoescape=True)
@stringfilter
def formatted_markdown(text):
    print('from markdown')
    print(text)
    return mark_safe(markdownify(text))
