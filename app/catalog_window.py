from datetime import date
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.database import DatabaseError
from app.pricing import previous_month_range, price_with_discount
from app.stock import is_low_stock, stock_label

RESOURCES_DIR = Path(__file__).resolve().parent.parent / "resources"
PLACEHOLDER_IMAGE = RESOURCES_DIR / "picture.png"
LOW_STOCK_COLOR = "#ffcccc"
IMAGE_WIDTH = 150
IMAGE_HEIGHT = 110


def format_price(value):
    return f"{value:,.2f}".replace(",", " ").replace(".", ",") + " ₽"


def load_pixmap(image_name):
    if image_name:
        image_path = RESOURCES_DIR / "images" / image_name
        if image_path.is_file():
            pixmap = QPixmap(str(image_path))
            if not pixmap.isNull():
                return pixmap
    return QPixmap(str(PLACEHOLDER_IMAGE))


class ProductCard(QFrame):
    def __init__(self, product, ordered_last_month):
        super().__init__()
        quantity = int(product["quantity"])
        background = LOW_STOCK_COLOR if is_low_stock(quantity) else "#ffffff"
        self.setObjectName("productCard")
        self.setStyleSheet(
            f"#productCard {{ background: {background}; border: 1px solid #555555; }}"
        )

        image_label = QLabel()
        image_label.setFixedSize(IMAGE_WIDTH, IMAGE_HEIGHT)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setPixmap(
            load_pixmap(product["image"]).scaled(
                IMAGE_WIDTH, IMAGE_HEIGHT, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

        title_label = QLabel(f"{product['manufacturer']} | {product['name']}")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        category_label = QLabel(f"Категория: {product['category']}")
        quantity_label = QLabel(f"Количество: {stock_label(quantity)}")
        composition_label = QLabel(f"Состав: {product['composition'] or '—'}")
        composition_label.setWordWrap(True)
        composition_label.setStyleSheet("font-size: 11px;")

        details_layout = QVBoxLayout()
        details_layout.addWidget(title_label)
        details_layout.addWidget(category_label)
        details_layout.addWidget(quantity_label)
        details_layout.addWidget(composition_label)

        price = product["price"]
        final_price = price_with_discount(price, ordered_last_month)
        if final_price == price:
            price_text = f"<span style='font-size:20px'>{format_price(price)}</span>"
        else:
            price_text = (
                f"<s style='color:#cc0000'>{format_price(price)}</s><br>"
                f"<span style='font-size:20px'>{format_price(final_price)}</span>"
            )
        price_label = QLabel(price_text)
        price_label.setAlignment(Qt.AlignCenter)
        price_label.setFixedWidth(160)

        layout = QHBoxLayout(self)
        layout.addWidget(image_label)
        layout.addLayout(details_layout, 1)
        layout.addWidget(price_label)


class CatalogWindow(QMainWindow):
    def __init__(self, database):
        super().__init__()
        self.setWindowTitle("Магазин обуви")
        self.resize(900, 700)

        container = QWidget()
        self._cards_layout = QVBoxLayout(container)
        self._cards_layout.setAlignment(Qt.AlignTop)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container)
        self.setCentralWidget(scroll_area)

        self._load_products(database)

    def _load_products(self, database):
        period_start, period_end = previous_month_range(date.today())
        try:
            products = database.fetch_catalog(period_start, period_end)
        except DatabaseError as error:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить каталог.\n{error}")
            return
        for product in products:
            self._cards_layout.addWidget(ProductCard(product, product["ordered_in_period"]))
