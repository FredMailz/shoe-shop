import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from app.catalog_window import CatalogWindow
from app.config import ConfigError, load_database_config
from app.database import Database, DatabaseError

CONNECTION_ERROR_TEXT = (
    "Не удалось подключиться к базе данных.\n"
    "Проверьте параметры подключения в файле config.ini.\n{error}"
)


def main():
    application = QApplication(sys.argv)
    try:
        database = Database(load_database_config())
        window = CatalogWindow(database)
    except (ConfigError, DatabaseError) as error:
        QMessageBox.critical(None, "Ошибка подключения", CONNECTION_ERROR_TEXT.format(error=error))
        return 1
    window.show()
    return application.exec_()


if __name__ == "__main__":
    sys.exit(main())
