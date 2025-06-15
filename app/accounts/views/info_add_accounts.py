import sys
import os
import sqlite3

from app.accounts.views.info_add_folder_accounts import InfoAddFolder
from app.accounts.ui.dialog_info_add_accounts_ui import DialogInfoAddAccountsUi

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5.QtWidgets import QCheckBox
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSignal  # Импортируем pyqtSignal


class DialogInfoAddAccounts(DialogInfoAddAccountsUi):
    # Сигнал для возврата данных в главное окно
    data_returned = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.root_project_dir = '..'
        # события
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_info_folder.clicked.connect(lambda: self.open_info_folder())
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_choose.clicked.connect(lambda: self.open_folder_dialog())
        self.checkBox_use_autofill.clicked.connect(lambda: self.change_checkbox_use_autofill())

        self.checkBox_avatar_man.clicked.connect(lambda: self.change_checkbox_avatar(self.checkBox_avatar_man,self.checkBox_avatar_man.isChecked()))
        self.checkBox_avatar_neutral.clicked.connect(lambda: self.change_checkbox_avatar(self.checkBox_avatar_neutral,self.checkBox_avatar_neutral.isChecked()))
        self.checkBox_avatar_woman.clicked.connect(lambda: self.change_checkbox_avatar(self.checkBox_avatar_woman,self.checkBox_avatar_woman.isChecked()))

        self.checkBox_name_man.clicked.connect(lambda: self.change_checkbox_name(self.checkBox_name_man,self.checkBox_name_man.isChecked()))
        self.checkBox_name_neutral.clicked.connect(lambda: self.change_checkbox_name(self.checkBox_name_neutral,self.checkBox_name_neutral.isChecked()))
        self.checkBox_name_woman.clicked.connect(lambda: self.change_checkbox_name(self.checkBox_name_woman,self.checkBox_name_woman.isChecked()))

        self.checkBox_surname_man.clicked.connect(lambda: self.change_checkbox_surname(self.checkBox_surname_man, self.checkBox_surname_man.isChecked()))
        self.checkBox_surname_neutral.clicked.connect(lambda: self.change_checkbox_surname(self.checkBox_surname_neutral, self.checkBox_surname_neutral.isChecked()))
        self.checkBox_surname_woman.clicked.connect(lambda: self.change_checkbox_surname(self.checkBox_surname_woman, self.checkBox_surname_woman.isChecked()))
        # события

    def open_info_folder(self):
        info = InfoAddFolder()  # Создаем экземпляр
        info.exec_()  # Открываем


    def change_checkbox_avatar(self,checkbox_target: QCheckBox,last_checked: bool):
        self.checkBox_avatar_man.setChecked(False)
        self.checkBox_avatar_neutral.setChecked(False)
        self.checkBox_avatar_woman.setChecked(False)
        checkbox_target.setChecked(last_checked)

    def change_checkbox_name(self, checkbox_target: QCheckBox,last_checked: bool):
        self.checkBox_name_man.setChecked(False)
        self.checkBox_name_neutral.setChecked(False)
        self.checkBox_name_woman.setChecked(False)
        checkbox_target.setChecked(last_checked)

    def change_checkbox_surname(self, checkbox_target: QCheckBox,last_checked: bool):
        self.checkBox_surname_man.setChecked(False)
        self.checkBox_surname_neutral.setChecked(False)
        self.checkBox_surname_woman.setChecked(False)
        checkbox_target.setChecked(last_checked)

    def change_checkbox_use_autofill(self):
        state = self.checkBox_use_autofill.isChecked()
        if state:  # Чекбокс отмечен
            self.groupBox.setVisible(True)  # Показываем groupBox
            self.resize(486, 350)
        else:
            self.groupBox.setVisible(False)
            self.resize(486, 170)
            self.resize(486, 170)    # необходимо 2 раза поменять размер, иначе размер не поменяется


    def open_folder_dialog(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Получаем путь к рабочему столу
        # Открываем диалог выбора папки, начнем с рабочего стола
        # если пользователь выбрал папку, то вернётся путь иначе None
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку", desktop_path)

        if folder_path:  # если пользователь выбрал папку
            # делаем запросы в БД
            connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
            cursor = connection.cursor()
            if self.checkBox_use_autofill.isChecked(): # если необходимо использовать автозаполнение
                avatar = 'None'
                name = 'None'
                surname = 'None'
                user_name = False
                description = False

                if self.checkBox_avatar_man.isChecked():
                    avatar = 'man'
                elif self.checkBox_avatar_neutral.isChecked():
                    avatar = 'neutral'
                elif self.checkBox_avatar_woman.isChecked():
                    avatar = 'woman'

                if self.checkBox_name_man.isChecked():
                    name = 'man'
                elif self.checkBox_name_neutral.isChecked():
                    name = 'neutral'
                elif self.checkBox_name_woman.isChecked():
                    name = 'woman'

                if self.checkBox_surname_man.isChecked():
                    surname = 'man'
                elif self.checkBox_surname_neutral.isChecked():
                    surname = 'neutral'
                elif self.checkBox_surname_woman.isChecked():
                    surname = 'woman'

                if self.checkBox_user_name.isChecked():
                    user_name = True

                if self.checkBox_description.isChecked():
                    description = True

                cursor.execute(f"UPDATE autofill_settings SET use = ?, avatar = ?, name = ?, surname = ?, user_name = ?, description = ?",
                               (1, avatar, name, surname, int(user_name), int(description) ))
                connection.commit()
            else:
                cursor.execute(f"UPDATE autofill_settings SET use = ?, avatar = ?,  name = ?, surname = ?, user_name = ?, description = ?",
                    (0, 'None', 'None', 'None', 0, 0))
                connection.commit()
            connection.close()
            self.close()
            self.data_returned.emit(folder_path)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = DialogInfoAddAccounts()
    ui.show()
    sys.exit(app.exec_())
