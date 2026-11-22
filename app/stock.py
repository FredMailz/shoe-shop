MANY_THRESHOLD = 5
LOW_STOCK_THRESHOLD = 3


def stock_label(quantity):
    return "много" if quantity > MANY_THRESHOLD else "мало"


def is_low_stock(quantity):
    return quantity <= LOW_STOCK_THRESHOLD
