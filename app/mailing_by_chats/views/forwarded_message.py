import sys
import os
import shutil  # для удаления папки
import sqlite3

from app.general.views.info import DialogInfo
from app.general.check_html_parse import check_html_parse
from app.mailing_by_chats.ui.dialog_forwarded_message_ui import DialogForwardedMessageUi

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

class DialogForwardedMessage(DialogForwardedMessageUi):
    """
    принимает и возвращает dict: \n
    { 'user_name_channel', 'message_ID' }
    """
    data_returned = pyqtSignal(dict)  # Сигнал для возврата данных в главное окно

    def __init__(self, data: dict):
        super().__init__()
        self.root_project_dir = '..'

        # установка переданных данных
        self.lineEdit_user_name_group.setText(data['user_name_channel'])
        self.lineEdit_ID_message.setText(data['message_ID'])

        # события
        self.pushButton_close.clicked.connect(lambda: self.close())
        self.pushButton_info.clicked.connect(lambda: self._info())
        self.pushButton_save.clicked.connect(lambda: self._save())
        # события

    def _info(self):
        info = DialogInfo('Информация',
                          """
Канал или чат обязательно должен быть публичным!   

Как узнать ID сообщения в Telegram:
Нажмите правой кнопкой мыши по сообщению (на ПК)
Нажмите и удерживайте сообщение (на телефоне)
В меню выберите "Копировать ссылку"
Ссылка будет вида t.me/username/123
Где 123 - ID сообщения
                          """,
                          'notification.mp3')  # Создаем экземпляр)
        info.exec_()


    def _save(self):

        if len(self.lineEdit_user_name_group.text()) < 1:
            info = DialogInfo('Внимание!', 'Заполните поле с user_name чата/канала!', 'notification.mp3')
            info.exec_()
            return

        if len(self.lineEdit_ID_message.text()) < 1:
            info = DialogInfo('Внимание!', 'Заполните поле с ID сообщения!', 'notification.mp3')
            info.exec_()
            return

        self.data_returned.emit({
                                'user_name_channel': self.lineEdit_user_name_group.text(),
                                'message_ID': self.lineEdit_ID_message.text(),
                                })

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"UPDATE saved_data_mailing_by_chats SET user_name_group_for_forwarded = ?,"
                       f" message_ID_for_forwarded_message = ?",
                       (self.lineEdit_user_name_group.text(), self.lineEdit_ID_message.text()))
        connection.commit()
        connection.close()

        self.close()