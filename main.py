import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from app.catalog_window import CatalogWindow
from app.config import ConfigError, load_database_config
from app.database import Database, DatabaseError


def main():
    application = QApplication(sys.argv)
    try:
        database = Database(load_database_config())
        window = CatalogWindow(database)
    except (ConfigError, DatabaseError) as error:
        QMessageBox.critical(None, "Ошибка", f"Не удалось подключиться к базе данных.\n{error}")
        return 1
    window.show()
    return application.exec_()


if __name__ == "__main__":
    sys.exit(main())
