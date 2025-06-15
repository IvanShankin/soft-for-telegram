import os

from app.general.views.info import DialogInfo
from app.create_bot.ui.dialog_list_created_bot_ui import DialogListCreatedBotUi

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")  # 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():  # 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path  # 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5.QtWidgets import QFileDialog

class DialogCreateBot(DialogListCreatedBotUi):
    def __init__(self, user_name_create_channel: list):
        super().__init__()
        self.root_project_dir = '..'

        for user_name in user_name_create_channel:
            self.textEdit_user_name_list.setText(self.textEdit_user_name_list.toPlainText() + user_name + '\n')

        # события
        self.pushButton_close.clicked.connect(lambda: self.close())
        self.pushButton_close_2.clicked.connect(lambda: self.close())
        self.pushButton_upload.clicked.connect(lambda: self._upload_user_name())

    def _upload_user_name(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Получаем путь к рабочему столу
        # Открываем диалог выбора папки, начнем с рабочего стола
        # если пользователь выбрал папку, то вернётся путь иначе None
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите путь", desktop_path)

        if folder_path:  # если пользователь выбрал папку (хранит выбранный путь)
            counts = 1
            file_name = '/User_name созданных ботов'

            while True:
                try:
                    with open(f"{folder_path}{file_name}.txt", "x", encoding="utf-8") as file:
                        file.write(self.textEdit_user_name_list.toPlainText())

                    info = DialogInfo('Успешно!', f'Файл успешно выгружен по пути:\n{folder_path}{file_name}.txt',
                                       'notification.mp3')  # Создаем экземпляр
                    info.exec_()  # Открываем
                    break
                except FileExistsError:
                    file_name = f'/User_name созданных каналов ({counts}).txt'
                    counts += 1
                except FileNotFoundError:
                    error_info = DialogInfo('Ошибка!', 'Указанный путь не найден!',
                                             'notification.mp3')  # Создаем экземпляр
                    error_info.exec_()  # Открываем
                    break