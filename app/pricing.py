from datetime import date
from decimal import ROUND_HALF_UP, Decimal

DISCOUNT_PERCENT = 25


def previous_month_range(today):
    month_start = today.replace(day=1)
    if month_start.month == 1:
        previous_start = date(month_start.year - 1, 12, 1)
    else:
        previous_start = date(month_start.year, month_start.month - 1, 1)
    return previous_start, month_start


def price_with_discount(price, ordered_last_month):
    price = Decimal(price)
    if ordered_last_month:
        return price
    discounted = price * (100 - DISCOUNT_PERCENT) / 100
    return discounted.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
