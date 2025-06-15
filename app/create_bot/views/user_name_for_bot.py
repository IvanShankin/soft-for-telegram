import sys
import os
import sqlite3
import itertools
import random

from app.general.views.info import DialogInfo
from app.general.check_html_parse import check_html_parse
from app.create_bot.ui.dialog_user_name_for_bot_ui import DialogUserNameForBotUi

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")  # 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():  # 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path  # 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel,QFileDialog, QCheckBox, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal

class DialogUserNameForBot(DialogUserNameForBotUi):
    """
    Принимает и возвращает dict: \n
    { \n
    'first_list': str, \n
    'second_list': str, \n
    'third_list': str, \n
    'use_first_list': bool, \n
    'use_second_list': bool, \n
    'use_third_list': bool, \n
    'set_numbers_end_user_name': bool \n
    }
    """
    data_returned = pyqtSignal(dict)

    def __init__(self, data: dict):
        super().__init__()
        self.root_project_dir = '..'

        # заполнение данных
        self.textEdit_list_1.setText(data['first_list'])
        self.textEdit_list_2.setText(data['second_list'])
        self.textEdit_list_3.setText(data['third_list'])
        self.checkBox_use_list_1.setChecked(data['use_first_list'])
        self.checkBox_use_list_2.setChecked(data['use_second_list'])
        self.checkBox_use_list_3.setChecked(data['use_third_list'])
        self.checkBox_set_numbers_end_user_name.setChecked(data['set_numbers_end_user_name'])

        # события
        self.pushButton_close.clicked.connect(lambda: self.close())
        self.pushButton_info.clicked.connect(lambda: self._info())
        self.pushButton_save.clicked.connect(lambda: self._save())

        self.textEdit_list_1.textChanged.connect(lambda: self._remove_spaces(self.textEdit_list_1))
        self.textEdit_list_2.textChanged.connect(lambda: self._remove_spaces(self.textEdit_list_2))
        self.textEdit_list_3.textChanged.connect(lambda: self._remove_spaces(self.textEdit_list_3))
        # события

    def _generate_unique_user_name(self, data: list[str]) -> dict:
        """Генерирует уникальные имена пользователей из входных данных.

        Разделяет строки по переходам на новую строку, проверяет их на соответствие
        критериям валидности и возвращает словарь с результатами.

        Args:
        data (list[str]): Список строк, содержащих потенциальные имена пользователей.
                Каждая строка может содержать несколько имён, разделённых переводом строки.

        Returns:
        dict: Словарь с двумя ключами:
                - "user_names" (list): Список валидных имён пользователей.
                - "there_are_inappropriate_values" (bool): Флаг, указывающий на наличие
                невалидных имён во входных данных.
        """
        generated_list = []
        try:
            counter = 0
            while True:
                generated_list.append(data[counter].lower().split('\n'))
                counter += 1
        except IndexError:
            pass

        if len(generated_list) == 1:
            user_name_list = generated_list[0]
        else:
            combinations = itertools.product(*generated_list)  # Генерируем все возможные комбинации
            user_name_list = [''.join(combination) for combination in
                              combinations]  # Объединяем слова в каждой комбинации

        result = []
        there_are_inappropriate_values = False
        for user_name in user_name_list:
            if len(user_name) < 1 or len(user_name) > 28:
                there_are_inappropriate_values = True
                continue
            if user_name[0] == '_' or user_name[len(user_name) - 1] == '_':
                there_are_inappropriate_values = True
                continue
            if user_name == "admin" or user_name == "telegram" or user_name == "support":
                there_are_inappropriate_values = True
                continue
            if user_name[0].isdigit():  # если первый символ цифра
                there_are_inappropriate_values = True
                continue
            result.append(user_name + '_bot')

        result = list((set(result)))  # убираем повторяющиеся элементы
        random.shuffle(result)  # перемешивание всех элементов списка

        return {"user_names": result, "there_are_inappropriate_values": there_are_inappropriate_values}

    def _info(self):
        info = DialogInfo('Информация',
                          '''Формирование user_name бота
Ограничения:
🔹 Основные правила:
1. Длина: от 5 до 28 символов (включительно, без учёта приписки _bot).
Приписка _bot будет выставляться автоматически!

2. Допустимые символы:
Латинские буквы (a-z, A-Z) Цифры (0-9) Нижнее подчёркивание (_)
Нельзя использовать другие спецсимволы (например, -, @, # и т. д.)
Имя не может начинаться с (_) или заканчиваться на (_)
Имя не может начинаться с цифры

3. Регистр букв не имеет значения:
@USERNAME и @username — это одно и то же.
Telegram автоматически преобразует имя в нижний регистр.

4.Уникальность:
Каждый username должен быть уникальным в рамках Telegram.
Если имя занято, придётся выбрать другое.

5. Запрещённые имена:
Нельзя использовать зарезервированные имена: admin, telegram, support.

🛠️ Как это работает:
User_name создаётся путём объединения случайных слов из выбранных списков.

Шаги:
1. Отметьте галочкой списки, которые хотите использовать (можно выбрать один, два или все три).
2. Система случайно выберет по одному слову из каждого отмеченного списка и объединит их в user_name.

Пример:
- Первый список: необычный, большой, маленький
- Второй список: канал, группа, чат
- Результат: "Необычный чат", "маленький канал", "большая группа" и т.д.

Важно:
- Каждый user_name генерируется случайно.
- Слова в списках должны быть разделены переносом строки.
                          ''',
                          'notification.mp3')
        info.exec_()

    def _save(self):
        use_list_1 = self.checkBox_use_list_1.isChecked()
        use_list_2 = self.checkBox_use_list_2.isChecked()
        use_list_3 = self.checkBox_use_list_3.isChecked()
        error_message = ''

        if (not self.checkBox_use_list_1.isChecked() and not self.checkBox_use_list_2.isChecked() and
                not self.checkBox_use_list_3.isChecked()):
            info = DialogInfo('Внимание!', 'Выберите хотя бы один список!', 'notification.mp3')
            info.exec_()
            return

        if len(self.textEdit_list_1.toPlainText().replace('\n', '')) < 1 and self.checkBox_use_list_1.isChecked():
            error_message += 'Первый список не будет использоваться!\nт.к. в нём нет ни одного слова!\n'
            use_list_1 = False

        if len(self.textEdit_list_2.toPlainText().replace('\n', '')) < 1 and self.checkBox_use_list_2.isChecked():
            error_message += 'Второй список не будет использоваться!\nт.к. в нём нет ни одного слова!\n'
            use_list_2 = False

        if len(self.textEdit_list_3.toPlainText().replace('\n', '')) < 1 and self.checkBox_use_list_3.isChecked():
            error_message += 'Третий список не будет использоваться!\nт.к. в нём нет ни одного слова!\n'
            use_list_3 = False

        if use_list_1 == False and use_list_2 == False and use_list_3 == False:
            info = DialogInfo('Внимание!', 'Ни один из списков не подходит, заполните их корректно!',
                              'notification.mp3')
            info.exec_()
            return

        if error_message:
            info = DialogInfo('Внимание!', error_message, 'notification.mp3')
            info.exec_()

        list_for_generate_user_name = []  # список для формирования всех возможных user_name для канала
        if use_list_1:
            list_for_generate_user_name.append(self.textEdit_list_1.toPlainText())
        if use_list_2:
            list_for_generate_user_name.append(self.textEdit_list_2.toPlainText())
        if use_list_3:
            list_for_generate_user_name.append(self.textEdit_list_3.toPlainText())

        dict_witch_user_names = self._generate_unique_user_name(list_for_generate_user_name)

        error_message_2 = ""
        if dict_witch_user_names["there_are_inappropriate_values"]:
            error_message_2 = ("\n\nНекоторые user_name сформированы некорректно, \n"
                               "они не будут включены в финальный список. \n\n"
                               "Проверьте на корректность введённые значения!\n"
                               "1. Длина: от 1 до 28 символов (включительно без учёта приписки _bot)\n"
                               "2. Имя не может начинаться с (_) или заканчиваться на (_)\n"
                               "3. Имя не может начинаться с цифры \n"
                               "4. @USERNAME и @username — это одно и то же")

        info = DialogInfo('Внимание!', f"Удалось сформировать {len(dict_witch_user_names['user_names'])}"
                          + error_message_2, 'notification.mp3')
        info.exec_()

        self.data_returned.emit({
            'first_list': self.textEdit_list_1.toPlainText(),
            'second_list': self.textEdit_list_2.toPlainText(),
            'third_list': self.textEdit_list_3.toPlainText(),
            'use_first_list': use_list_1,
            'use_second_list': use_list_2,
            'use_third_list': use_list_3,
            'set_numbers_end_user_name': self.checkBox_set_numbers_end_user_name.isChecked(),
        })

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(
            f"UPDATE saved_data_creating_bots SET first_user_name_list = ?, second_user_name_list = ?, "
            f"third_user_name_list = ?",
            (self.textEdit_list_1.toPlainText(), self.textEdit_list_2.toPlainText(),self.textEdit_list_3.toPlainText()))
        connection.commit()
        connection.close()

        self.close()

    def _remove_spaces(self, text_edit: QTextEdit):
        cursor = text_edit.textCursor()
        text = text_edit.toPlainText()
        if " " in text:
            new_text = text.replace(" ", "")
            text_edit.setPlainText(new_text)
            text_edit.setTextCursor(cursor)  # сохраняем позицию курсора