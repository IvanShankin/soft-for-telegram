import sys
import os

from app.accounts.ui.dialig_info_add_folder_accounts_ui import DialogInfoAddFolder

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtWidgets

class InfoAddFolder(DialogInfoAddFolder):
    def __init__(self):
        super().__init__()
        self.root_project_dir = '..'

        # события
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_close_2.clicked.connect(self.close)
        # события

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = InfoAddFolder()
    ui.show()
    sys.exit(app.exec_())
