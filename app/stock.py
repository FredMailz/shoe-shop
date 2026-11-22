def stock_label(quantity):
    return "много" if quantity > 5 else "мало"


def is_low_stock(quantity):
    return quantity <= 3
