import sys
import os
import shutil  # для удаления папки
import sqlite3

from app.general.views.info import DialogInfo
from app.general.check_html_parse import check_html_parse
from app.create_channel.ui.dialog_first_message_for_group_ui import DialogFirstMessageUi

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


class DraggableLabel(QLabel):  # спец класс для Label
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.oldPos = None  # Переменная для хранения позиции мыши

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  # Проверка на левую кнопку мыши
            self.oldPos = event.globalPos() - self.parent().frameGeometry().topLeft()  # Запоминаем позицию мыши
            event.accept()  # Принять событие

    def mouseMoveEvent(self, event):
        if self.oldPos is not None and event.buttons() == Qt.LeftButton:  # Проверка, что кнопка мыши удерживается
            self.parent().move(event.globalPos() - self.oldPos)  # Перемещения окна
            event.accept()  # Принять событие

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:  # Проверка на отпускание кнопки мыши
            self.oldPos = None  # Обнуляем позицию
            event.accept()  # Принять событие



class DialogFirstMessage(DialogFirstMessageUi):
    """
    принимает и возвращает dict: \n
    { \n
    'message': str, \n
    'user_name_channel': str, \n
    'message_ID': str, \n
    'file_path': str, \n
    'use_file_for_message': bool, \n
    'use_new_message': bool,\n
    'use_the_forwarded_message': bool \n
    } \n
    """
    data_returned = pyqtSignal(dict)  # Сигнал для возврата данных в главное окно

    def __init__(self,data: dict):
        super().__init__()
        self.root_project_dir = '..'
        self.file_path = '' # путь где хранится файл для сообщения

        # установление переданных данных
        self.textEdit_message.setText(data['message'])
        self.lineEdit_user_name_group.setText(data['user_name_channel'])
        self.lineEdit_ID_message.setText(data['message_ID'])
        self.file_path = data['file_path']
        self.checkBox_use_file_for_message.setChecked(data['use_file_for_message'])
        self.checkBox_use_new_message.setChecked(data['use_new_message'])
        self.checkBox_use_the_forwarded_message.setChecked(data['use_the_forwarded_message'])

        # события
        self.pushButton_close.clicked.connect(lambda: self.close())
        self.pushButton_info_forwarded_message.clicked.connect(lambda: self._info_forwarded_message())
        self.pushButton_choose_file_for_message.clicked.connect(lambda: self._choose_file_for_message())
        self.pushButton_save.clicked.connect(lambda: self._save())

        self.checkBox_use_new_message.clicked.connect(lambda: self._change_checkbox_message(
            self.checkBox_use_new_message, self.checkBox_use_new_message.isChecked()))
        self.checkBox_use_the_forwarded_message.clicked.connect(lambda: self._change_checkbox_message(
            self.checkBox_use_the_forwarded_message, self.checkBox_use_the_forwarded_message.isChecked()))
        # события

    def _info_forwarded_message(self):
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

    def _choose_file_for_message(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Получаем путь к рабочему столу
        # Открываем диалог выбора папки, начнем с рабочего стола
        # если пользователь выбрал папку, то вернётся путь иначе None
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", desktop_path, "Все файлы (*);",options=options)

        if file_path:
            size = os.path.getsize(file_path)  # возвращает размер файла в байтах
            file_name = os.path.basename(file_path)  # получаем имя файла
            if size > 2 * 1024 * 1024 * 1024:  # 2 ГБ = 2 * 1024^3 байт
                self.show_info('Внимание!', 'Файл не сохранён!\nРазмер файла не должен превышать 2гб.')
                return
            else:
                title_dialog = 'Готово!'
                message_dialog = 'Файл успешно сохранён!'
                try:
                    shutil.copy(file_path, self.root_project_dir + f'/working_files/file_from_user/{file_name}')
                    self.file_path_for_mailing = self.root_project_dir + f'/working_files/file_from_user/{file_name}'
                    self.file_path = self.root_project_dir + f'/working_files/file_from_user/{file_name}'
                except PermissionError:
                    title_dialog = 'Внимание!'
                    message_dialog = 'Файл не сохранён!\n\nДанный файл занят другим процессом\nЗакройте все процессы связанные с этим файлом.'
                except Exception as e:
                    title_dialog = 'Внимание!'
                    message_dialog = f'Файл не сохранён!\n\nПроизошла ошибка при сохранении файла:\n{e}\n\nПопробуйте ещё раз.'

                info = DialogInfo(title_dialog, message_dialog, 'notification.mp3')
                info.exec_()

    def _change_checkbox_message(self,checkbox_target: QCheckBox,last_checked: bool):
        self.checkBox_use_new_message.setChecked(False)
        self.checkBox_use_the_forwarded_message.setChecked(False)
        checkbox_target.setChecked(last_checked)


    def _save(self):
        if self.checkBox_use_new_message.isChecked():
            if len(self.textEdit_message.toPlainText().replace(" ", "").replace("\n", "")) < 1:
                info = DialogInfo('Внимание!', 'Заполните поле с сообщением!',
                                   'notification.mp3')
                info.exec_()
                return

            if not check_html_parse(self.textEdit_message.toPlainText()): # если неверный HTML синтаксис
                info = DialogInfo('Внимание!', 'В сообщении введён некорректный HTML синтаксис!',
                                   'notification.mp3')
                info.exec_()
                return

            if len(self.textEdit_message.toPlainText()) > 4024 and self.checkBox_use_file_for_message.isChecked() == False:
                info = DialogInfo('Внимание!', 'Для одного сообщение максимум 4024 символов,\n'
                                                f'у вас: {len(self.textEdit_message.toPlainText())}', 'notification.mp3')
                info.exec_()
                return
            elif len(self.textEdit_message.toPlainText()) > 1024 and self.checkBox_use_file_for_message.isChecked() == True:
                info = DialogInfo('Внимание!', 'Для одного сообщение c файлом максимум 1024 символов,\n'
                                                f'у вас: {len(self.textEdit_message.toPlainText())}', 'notification.mp3')
                info.exec_()
                return
            if self.checkBox_use_file_for_message.isChecked() == True and self.file_path == '':
                info = DialogInfo('Внимание!', 'Выберите файл для сообщения или уберите необходимость отсылать файл!',
                                   'notification.mp3')
                info.exec_()
                return

        elif self.checkBox_use_the_forwarded_message.isChecked():
            if len(self.lineEdit_user_name_group.text()) < 1:
                info = DialogInfo('Внимание!', 'Заполните поле с user_name чата/канала!', 'notification.mp3')
                info.exec_()
                return

            if len(self.lineEdit_ID_message.text()) < 1:
                info = DialogInfo('Внимание!', 'Заполните поле с ID сообщения!', 'notification.mp3')
                info.exec_()
                return

        else:
            info = DialogInfo('Внимание!', 'Выберите какое сообщение использовать!','notification.mp3')
            info.exec_()
            return

        self.data_returned.emit({
                                'message': self.textEdit_message.toPlainText(),
                                'user_name_channel': self.lineEdit_user_name_group.text(),
                                'message_ID': self.lineEdit_ID_message.text(),
                                'file_path': self.file_path,
                                'use_file_for_message': self.checkBox_use_file_for_message.isChecked(),
                                'use_new_message': self.checkBox_use_new_message.isChecked(),
                                'use_the_forwarded_message': self.checkBox_use_the_forwarded_message.isChecked()
                                })

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"UPDATE saved_data_creating_channels SET new_message = ?, forwarding_username = ?, "
                       f"forwarding_id_message = ?",
                       (self.textEdit_message.toPlainText(), self.lineEdit_user_name_group.text(),
                        self.lineEdit_ID_message.text()))
        connection.commit()
        connection.close()

        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = DialogFirstMessage({'message': 'это сообщение', 'user_name_channel': '@user_name', 'message_ID': '5647', 'file_path': '',
                             'use_file_for_message': False, 'use_new_message': True, 'use_the_forwarded_message': False})
    ui.show()
    sys.exit(app.exec_())
