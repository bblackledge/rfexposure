from django import template

register = template.Library()


@register.filter(name='int_to_band_plan')
def int_to_band_plan(value):
    """
    Converts an integer to a specific string based on its value (Version 1).
    """

    try:
        value = int(value)
    except (TypeError, ValueError):
        return "Invalid Number"

    if value < 0:
        return "Invalid Negative Number"
    elif value == 0:
        return "MF/HF"
    elif value == 1:
        return "VHF/UHF"
    else:
        return "Invalid Number"


@register.filter(name='int_to_frequency_position')
def int_to_frequency_position(value):
    """
    Converts an integer to a specific string based on its value (Version 2).
    """

    try:
        value = int(value)
    except (TypeError, ValueError):
        return "Invalid Number"

    if value < 0:
        return "Invalid Negative Number"
    elif value == 0:
        return "Lowest"
    elif value == 1:
        return "Center"
    elif value == 2:
        return "Highest"
    else:
        return "Invalid Number"
