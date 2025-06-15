import sys
import os
import sqlite3

from pathlib import Path
import PyQt5

from app.accounts.ui.dialog_error_add_accounts_ui import DialogErrorAddAccountsUi

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути

if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt


class DialogErrorAddAccounts(DialogErrorAddAccountsUi):
    def __init__(self,list_tg_id: list):
        super().__init__()
        self.list_tg_id = list_tg_id
        self.root_project_dir = '..'

        # события
        self.pushButton_close.clicked.connect(self.close)
        # события

        self.add_rows(self.list_tg_id)

    def add_rows(self,list_tg_id):
        list_tg_id = list(set(list_tg_id)) # убираем все повторяющие элементы
        row_counts = 0
        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()

        for tg_id in list_tg_id:
            cursor.execute(f"SELECT id,id_tg,user_name,account_status FROM accounts WHERE id_tg = ?", (tg_id,))
            account_info = cursor.fetchone()

            self.tableWidget_account.insertRow(row_counts)
            col = 0
            for info in account_info:
                item = None
                if col == 3:  # если это колонка со статусом аккаунта
                    if info == 'active':
                        info = 'Активный'
                    elif info == 'archive':
                        info = 'В архиве'
                    elif info == 'main':
                        info = 'Главный'
                    elif info == 'temporary_ban':
                        info = 'Во временном бане'
                    elif info == 'login_error':
                        info = 'С ошибкой входа'
                    else:
                        info = 'Активный'

                item = QTableWidgetItem(str(info))

                item.setTextAlignment(Qt.AlignCenter)  # Центрируем текст в ячейке
                font = QtGui.QFont()
                font.setPointSize(9)
                item.setFont(font)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Запрещаем редактирование
                self.tableWidget_account.setItem(row_counts, col, item)
                col += 1
            row_counts += 1
        connection.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = DialogErrorAddAccounts([7352730490,7612581345])
    ui.show()
    sys.exit(app.exec_())
