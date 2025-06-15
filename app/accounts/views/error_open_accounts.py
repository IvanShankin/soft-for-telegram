import os
import sys
from app.general.views.info import DialogInfo
from app.accounts.ui.dialog_error_add_accounts_ui import DialogErrorAddAccountsUi

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QTableWidgetItem

class DialogErrorOpenAccounts(DialogErrorAddAccountsUi):
    def __init__(self,accounts: list):
        super().__init__()
        self.accounts = accounts

        self.show_accounts()
        self.show_info()

        self.pushButton_close.clicked.connect(self.close)

    def show_accounts(self):
        self.tableWidget_account.setRowCount(0)
        counter = 0
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignCenter)  # Центрируем текст в ячейке
        for one_account in self.accounts:
            col = 1
            self.tableWidget_account.insertRow(counter)
            item = QTableWidgetItem(str(counter))
            item.setTextAlignment(Qt.AlignCenter)  # Центрируем текст в ячейке
            self.tableWidget_account.setItem(counter, 0, item)

            for info in one_account:
                item = QTableWidgetItem(str(info))
                item.setTextAlignment(Qt.AlignCenter)  # Центрируем текст в ячейке
                if col == self.tableWidget_account.columnCount() - 1:  # Если это последняя строка
                    item.setFlags(item.flags() | Qt.ItemIsEditable)  # Разрешаем редактирование
                else:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Запрещаем редактирование
                self.tableWidget_account.setItem(counter, col, item)
                col += 1
            counter += 1

    def show_info(self):
        error_info = DialogInfo('Внимание!','При попытке загрузки данных\nпроизошла ошибка входа в аккаунт','notification.mp3')  # Создаем экземпляр
        error_info.exec_()  # Открываем


if __name__ == "__main__":
    accounts = [[432432,'user_name','У аккаунта установленна двухфакторная аутентификация','если аккаунт не заблокирован, то войдите в tg аккаунт и добавьте новую tdata в программу'],
                [432432,'user_name','Неизвестная ошибка входа','если аккаунт не заблокирован, то войдите в tg аккаунт и добавьте новую tdata в программу'],
                [872432,'user_name','Неизвестная ошибка входа','если аккаунт не заблокирован, то войдите в tg аккаунт и добавьте новую tdata в программу'],
                [432432,'user_name','Неизвестная ошибка входа','если аккаунт не заблокирован, то войдите в tg аккаунт и добавьте новую tdata в программу']]
    app = QtWidgets.QApplication(sys.argv)
    ui = DialogErrorOpenAccounts(accounts)
    ui.show()
    ui.show_info()
    sys.exit(app.exec_())
