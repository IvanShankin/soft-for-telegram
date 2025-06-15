import sys
import os
import shutil  # для удаления папки
import sqlite3

from app.general.views.info import DialogInfo
from app.general.check_html_parse import check_html_parse
from app.create_bot.ui.dialog_list_BIO_bot_ui import DialogListBIOBotUi

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")  # 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():  # 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path  # 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel,QFileDialog, QCheckBox
from PyQt5.QtCore import Qt, pyqtSignal

class DialogListBIOBot(DialogListBIOBotUi):
    data_returned = pyqtSignal(str)
    def __init__(self, bio: str):
        super().__init__()

        self.textEdit_BIO_list.setText(bio)

        # события
        self.pushButton_close.clicked.connect(lambda: self.close())
        self.pushButton_info.clicked.connect(lambda: self._info())
        self.pushButton_save.clicked.connect(lambda: self._save())
        # события

    def _info(self):
        info = DialogInfo('Информация',
                          '''
Максимальная длинная БИО - 120 символов.
БИО разделяются по знаку &.
Если БИО одно, то нет необходимости его разделять.
                          ''',
                          'notification.mp3')
        info.exec_()

    def _save(self):
        bio = self.textEdit_BIO_list.toPlainText().split('&')
        for counter in range(len(bio)):
            if len(bio[counter]) > 120:
                info = DialogInfo('Внимание!', "БИО не может превышать 120 символов!\n"
                                               f"Ваше {counter} БИО не проходит по этому ограничению",
                                  "notification.mp3")
                info.exec_()
                return

        self.data_returned.emit(self.textEdit_BIO_list.toPlainText())

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"UPDATE saved_data_creating_bots SET BIO = ?", ( self.textEdit_BIO_list.toPlainText(), ))
        connection.commit()
        connection.close()

        self.close()

