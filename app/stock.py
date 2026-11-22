def stock_label(quantity):
    return "Много в наличии" if quantity > 5 else "Мало в наличии"


def is_low_stock(quantity):
    return quantity <= 3
