from django import template

register = template.Library()

# Currency filter
@register.filter(name='currency')
def currency(number):
    return "₹ " + str(number)

# Multiply filter
@register.filter(name='multiply')
def multiply(number, multiplier):
    try:
        return float(number) * float(multiplier)
    except (ValueError, TypeError):
        return 0





# from django import template
# from django.utils.formats import number_format

# register = template.Library()

# # Enhanced Currency Filter
# @register.filter(name='currency')
# def currency(number):
#     """
#     Format the number as Indian Rupee with proper thousand separators.
#     Example: ₹ 1,23,456.78
#     """
#     try:
#         formatted_number = number_format(number, decimal_pos=2, use_l10n=True)
#         return f"₹ {formatted_number}"
#     except (ValueError, TypeError):
#         return "₹ 0.00"

# # Enhanced Multiply Filter
# @register.filter(name='multiply')
# def multiply(number, multiplier):
#     """
#     Multiply two numbers and return the result.
#     Example: 123 * 2 = 246.00
#     """
#     try:
#         result = float(number) * float(multiplier)
#         return round(result, 2)  # Limit to 2 decimal places
#     except (ValueError, TypeError):
#         return 0
