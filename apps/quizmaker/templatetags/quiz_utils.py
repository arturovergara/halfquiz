# Django Imports
from django import template

register = template.Library()


@register.filter
def to_letter(value):
    letters_map = {1: "A", 2: "B", 3: "C", 4: "D"}

    return letters_map[int(value)]


@register.filter
def to_color(value):
    colors_map = {1: "primary", 2: "success", 3: "secondary", 4: "danger"}

    return colors_map[int(value)]
