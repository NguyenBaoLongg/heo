from django import template

def format_price(value):
    if isinstance(value, (int, float)):
        return f"{value:,.0f} VNĐ"
    return value