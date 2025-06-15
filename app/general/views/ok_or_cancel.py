import pygame
import sys
import os

from app.general.ui.dialog_ok_or_canel_ui import DialogOkOrCancelUi

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal  # Импортируем pyqtSignal


class DialogOkOrCancel(DialogOkOrCancelUi):
    data_returned = pyqtSignal(bool)  # Сигнал для возврата данных в главное окно

    def __init__(self,title: str,text: str,sound_file: str = None):
        super().__init__()
        self.title = title
        self.text = text
        self.sound_file = sound_file
        self.root_project_dir = '..'

        # события
        self.pushButton_close.clicked.connect(lambda: self.result_false())
        self.pushButton_cancel.clicked.connect(lambda: self.result_false())
        self.pushButton_ok.clicked.connect(lambda: self.result_true())
        # события

        self.label_title.setText(self.title)
        self.label_info.setText(self.text)

        if self.sound_file:
            try:
                sound_file_path = (self.root_project_dir + f"/sounds/{self.file}")
                pygame.mixer.init()
                pygame.mixer.music.load(sound_file_path)  # Загрузка звукового файла
                pygame.mixer.music.play()  # Проигрывание звука
            except Exception:
                pass

    def result_true(self):
        self.data_returned.emit(True)
        self.close()
    def result_false(self):
        self.data_returned.emit(False)
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = DialogOkOrCancel('Внимание!','test','notification.mp3')
    ui.show()
    sys.exit(app.exec_())
