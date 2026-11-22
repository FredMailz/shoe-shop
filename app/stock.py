MANY_THRESHOLD = 5
LOW_STOCK_THRESHOLD = 3


def stock_label(quantity):
    return "Много в наличии" if quantity > MANY_THRESHOLD else "Мало в наличии"


def is_low_stock(quantity):
    return quantity <= LOW_STOCK_THRESHOLD
