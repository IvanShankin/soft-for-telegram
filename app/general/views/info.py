import sys
import os
import pygame

from app.general.ui.dialog_info import DialogInfoUi

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtWidgets

class DialogInfo(DialogInfoUi):
    def __init__(self,title: str,text: str,file_sound: str = None, button_text: str = 'ОК'):
        super().__init__()
        self.root_project_dir = '..'
        self.button_text = button_text

        self.label_titel.setText(title)
        self.pushButton_ok.setText(button_text)

        # события
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_ok.clicked.connect(self.close)
        # события

        self.label_titel.setText(title)
        self.label_info.setText(text)

        if file_sound:
            try:
                sound_file = (self.root_project_dir + f"/resources/sounds/{file_sound}")
                pygame.mixer.init()
                pygame.mixer.music.load(sound_file)  # Загрузка звукового файла
                pygame.mixer.music.play()  # Проигрывание звука
            except Exception:
                pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = DialogInfo('Внимание!','test','notification.mp3')
    ui.show()
    sys.exit(app.exec_())
