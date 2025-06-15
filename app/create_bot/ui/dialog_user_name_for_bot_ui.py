import os

from app.general.ui.draggable_label_ui import DraggableLabel

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")  # 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():  # 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path  # 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QTextEdit
from PyQt5.QtCore import Qt

class RestrictedTextEdit(QTextEdit):
        def __init__(self, parent=None):
                super().__init__(parent)

        def keyPressEvent(self, event):
                # Разрешаем управляющие клавиши (Backspace, Delete, стрелки и т. д.)
                if (
                        event.key() in (
                        Qt.Key_Backspace,
                        Qt.Key_Delete,
                        Qt.Key_Left,
                        Qt.Key_Right,
                        Qt.Key_Up,
                        Qt.Key_Down,
                        Qt.Key_Return,
                        Qt.Key_Enter,
                        Qt.Key_Home,
                        Qt.Key_End,
                        Qt.Key_PageUp,
                        Qt.Key_PageDown,
                        Qt.Key_Escape,
                )
                        or (event.modifiers() & Qt.ControlModifier and event.key() in (
                        Qt.Key_A,  # Выделить всё (Ctrl+A)
                        Qt.Key_C,  # Копировать (Ctrl+C)
                        Qt.Key_V,  # Вставить (Ctrl+V)
                        Qt.Key_X,  # Вырезать (Ctrl+X)
                        Qt.Key_Z,  # Отменить (Ctrl+Z)
                        Qt.Key_Y,  # Повторить (Ctrl+Y)
                ))
                ):
                        super().keyPressEvent(event)
                        return

                        # Получаем введённый символ
                char = event.text()

                # Проверяем, что символ:
                # 1. Латинская буква (A-Z, a-z) ИЛИ
                # 2. Цифра (0-9) ИЛИ
                # 3. Нижнее подчёркивание (_)
                # И НЕ является русской буквой (кириллицей)
                if (char.isalpha() and char.isascii()) or char.isdigit() or char == '_':
                        super().keyPressEvent(event)
                else:
                        # Игнорируем русские буквы и другие запрещённые символы
                        event.ignore()

class DialogUserNameForBotUi(QDialog):
    def __init__(self):
        super().__init__()
        self.root_project_dir = '..'
        self.setWindowFlags(Qt.FramelessWindowHint)  # Убираем рамки окна, включая заголовок

        self.setObjectName("Dialog")
        self.resize(1048, 600)
        self.setMaximumSize(QtCore.QSize(1048, 600))
        self.setStyleSheet("background-color: rgb(236, 237, 240);\n"
"border: 1px solid black;")
        self.gridLayout_5 = QtWidgets.QGridLayout(self)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_title = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"padding: 5px;\n"
"border-bottom: none;\n"
"border-right: none;")
        self.label_title.setObjectName("label_title")
        self.horizontalLayout.addWidget(self.label_title)
        self.pushButton_close = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_close.sizePolicy().hasHeightForWidth())
        self.pushButton_close.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    text-align: center;\n"
"    border-bottom: none;\n"
"    border-left: none;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 3px;\n"
"   }\n"
"QPushButton:hover {\n"
"    background-color: rgb(255, 0, 0); /* Цвет фона при наведении  */\n"
"    color: rgb(255,255,255)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"     background: rgb(255, 100, 100); /* Цвет фона при нажатии (еще серее) */\n"
"     color: rgb(255,255,255)\n"
"}\n"
"")
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout.addWidget(self.pushButton_close)
        self.gridLayout_5.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(9, -1, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_11 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("margin-left: 10px;\n"
"border:none;")
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_3.addWidget(self.label_11)
        self.pushButton_info = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_info.sizePolicy().hasHeightForWidth())
        self.pushButton_info.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.pushButton_info.setFont(font)
        self.pushButton_info.setStyleSheet("border: none;\n"
"background: none;")
        self.pushButton_info.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/question.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_info.setIcon(icon)
        self.pushButton_info.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_info.setFlat(False)
        self.pushButton_info.setObjectName("pushButton_info")
        self.horizontalLayout_3.addWidget(self.pushButton_info)
        self.label = QtWidgets.QLabel(self)
        self.label.setStyleSheet("border:none;\n"
"margin-right:1px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.gridLayout_5.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setContentsMargins(1, 9, 1, 20)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.scrollArea_6 = QtWidgets.QScrollArea(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_6.sizePolicy().hasHeightForWidth())
        self.scrollArea_6.setSizePolicy(sizePolicy)
        self.scrollArea_6.setMinimumSize(QtCore.QSize(310, 280))
        self.scrollArea_6.setStyleSheet("border: 0;")
        self.scrollArea_6.setWidgetResizable(True)
        self.scrollArea_6.setObjectName("scrollArea_6")
        self.scrollAreaWidgetContents_6 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_6.setGeometry(QtCore.QRect(0, 0, 345, 397))
        self.scrollAreaWidgetContents_6.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents_6.setStyleSheet("/* СТИЛЬ ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */\n"
"QScrollBar:vertical {\n"
"    border-radius: 8px;\n"
"    background: rgb(210, 210, 213);\n"
"    width: 14px;\n"
"    margin: 0px 0 0px 0;\n"
"}\n"
"\n"
"/* HANDLE BAR ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */\n"
"QScrollBar::handle:vertical {  \n"
"    background-color: rgb(210, 210, 213);\n"
"    min-height: 30px;\n"
"    border-radius: 0px;\n"
"    transition: background-color 0.2s ease;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {  \n"
"    background-color: rgb(180, 180, 184);\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:pressed {  \n"
"    background-color: rgb(150, 150, 153);\n"
"}\n"
"\n"
"/* КНОПКА ВВЕРХУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */\n"
"QScrollBar::sub-line:vertical {\n"
"    border: none;  \n"
"    background-color: rgb(190, 190, 193);  /* Более темный серый */\n"
"    height: 15px;\n"
"    border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical:hover {  \n"
"    background-color: rgb(170, 170, 174);  /* Темнее при наведении */\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical:pressed {  \n"
"    background-color: rgb(140, 140, 143);  /* Еще темнее при нажатии */\n"
"}\n"
"\n"
"/* КНОПКА ВНИЗУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */\n"
"QScrollBar::add-line:vertical {\n"
"    border: none;  \n"
"    background-color: rgb(190, 190, 193);  /* Более темный серый */\n"
"    height: 15px;\n"
"    border-bottom-left-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical:hover {  \n"
"    background-color: rgb(170, 170, 174);  /* Темнее при наведении */\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical:pressed {  \n"
"    background-color: rgb(140, 140, 143);  /* Еще темнее при нажатии */\n"
"}\n"
"\n"
"/* УБРАТЬ СТРЕЛКИ */\n"
"QScrollBar::up-arrow:vertical, \n"
"QScrollBar::down-arrow:vertical {\n"
"    background: none;\n"
"}\n"
"\n"
"/* УБРАТЬ ФОН */\n"
"QScrollBar::add-page:vertical, \n"
"QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}")
        self.scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.checkBox_use_list_1 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_6)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_use_list_1.setFont(font)
        self.checkBox_use_list_1.setStyleSheet("\n"
"QCheckBox {\n"
"color: rgb(0, 0, 0);\n"
"    spacing: 5px; /* Отступ между иконкой и текстом */\n"
"\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 15px; /* Ширина индикатора (чекбокса) */\n"
"    height: 15px; /* Высота индикатора (чекбокса) */\n"
"    border: 2px solid rgb(150, 150, 150); /* Обводка чекбокса */\n"
"    border-radius: 4px; /* Закругление углов */\n"
"    background-color: white; /* Цвет фона чекбокса */\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background-color: rgb(150, 200, 150); \n"
"    border: 2px solid rgb(150, 150, 150); \n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked:hover {\n"
"    border: 2px solid rgb(100, 100, 100);\n"
"}\n"
"\n"
"QCheckBox::indicator:checked:hover {\n"
"    background-color: rgb(180, 230, 180); \n"
"}")
        self.checkBox_use_list_1.setObjectName("checkBox_use_list_1")
        self.gridLayout_2.addWidget(self.checkBox_use_list_1, 1, 0, 1, 1)
        self.textEdit_list_1 = RestrictedTextEdit(self.scrollAreaWidgetContents_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_list_1.sizePolicy().hasHeightForWidth())
        self.textEdit_list_1.setSizePolicy(sizePolicy)
        self.textEdit_list_1.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.textEdit_list_1.setFont(font)
        self.textEdit_list_1.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"padding-top: 15px; /* Отступ только слева */   \n"
" padding-bottom: 15px; /* Отступ только снизу */\n"
"")
        self.textEdit_list_1.setReadOnly(False)
        self.textEdit_list_1.setObjectName("textEdit_list_1")
        self.gridLayout_2.addWidget(self.textEdit_list_1, 0, 0, 1, 1)
        self.scrollArea_6.setWidget(self.scrollAreaWidgetContents_6)
        self.gridLayout_4.addWidget(self.scrollArea_6, 0, 0, 1, 1)
        self.scrollArea_7 = QtWidgets.QScrollArea(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_7.sizePolicy().hasHeightForWidth())
        self.scrollArea_7.setSizePolicy(sizePolicy)
        self.scrollArea_7.setMinimumSize(QtCore.QSize(310, 280))
        self.scrollArea_7.setStyleSheet("border: 0;")
        self.scrollArea_7.setWidgetResizable(True)
        self.scrollArea_7.setObjectName("scrollArea_7")
        self.scrollAreaWidgetContents_7 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_7.setGeometry(QtCore.QRect(0, 0, 344, 397))
        self.scrollAreaWidgetContents_7.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents_7.setStyleSheet("/* СТИЛЬ ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */\n"
"QScrollBar:vertical {\n"
"    border-radius: 8px;\n"
"    background: rgb(210, 210, 213);\n"
"    width: 14px;\n"
"    margin: 0px 0 0px 0;\n"
"}\n"
"\n"
"/* HANDLE BAR ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */\n"
"QScrollBar::handle:vertical {  \n"
"    background-color: rgb(210, 210, 213);\n"
"    min-height: 30px;\n"
"    border-radius: 0px;\n"
"    transition: background-color 0.2s ease;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {  \n"
"    background-color: rgb(180, 180, 184);\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:pressed {  \n"
"    background-color: rgb(150, 150, 153);\n"
"}\n"
"\n"
"/* КНОПКА ВВЕРХУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */\n"
"QScrollBar::sub-line:vertical {\n"
"    border: none;  \n"
"    background-color: rgb(190, 190, 193);  /* Более темный серый */\n"
"    height: 15px;\n"
"    border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical:hover {  \n"
"    background-color: rgb(170, 170, 174);  /* Темнее при наведении */\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical:pressed {  \n"
"    background-color: rgb(140, 140, 143);  /* Еще темнее при нажатии */\n"
"}\n"
"\n"
"/* КНОПКА ВНИЗУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */\n"
"QScrollBar::add-line:vertical {\n"
"    border: none;  \n"
"    background-color: rgb(190, 190, 193);  /* Более темный серый */\n"
"    height: 15px;\n"
"    border-bottom-left-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical:hover {  \n"
"    background-color: rgb(170, 170, 174);  /* Темнее при наведении */\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical:pressed {  \n"
"    background-color: rgb(140, 140, 143);  /* Еще темнее при нажатии */\n"
"}\n"
"\n"
"/* УБРАТЬ СТРЕЛКИ */\n"
"QScrollBar::up-arrow:vertical, \n"
"QScrollBar::down-arrow:vertical {\n"
"    background: none;\n"
"}\n"
"\n"
"/* УБРАТЬ ФОН */\n"
"QScrollBar::add-page:vertical, \n"
"QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}")
        self.scrollAreaWidgetContents_7.setObjectName("scrollAreaWidgetContents_7")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_7)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit_list_2 = RestrictedTextEdit(self.scrollAreaWidgetContents_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_list_2.sizePolicy().hasHeightForWidth())
        self.textEdit_list_2.setSizePolicy(sizePolicy)
        self.textEdit_list_2.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.textEdit_list_2.setFont(font)
        self.textEdit_list_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"padding-top: 15px; /* Отступ только слева */   \n"
" padding-bottom: 15px; /* Отступ только снизу */\n"
"")
        self.textEdit_list_2.setReadOnly(False)
        self.textEdit_list_2.setObjectName("textEdit_list_2")
        self.gridLayout.addWidget(self.textEdit_list_2, 0, 0, 1, 1)
        self.checkBox_use_list_2 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_7)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_use_list_2.setFont(font)
        self.checkBox_use_list_2.setStyleSheet("\n"
"QCheckBox {\n"
"color: rgb(0, 0, 0);\n"
"    spacing: 5px; /* Отступ между иконкой и текстом */\n"
"\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 15px; /* Ширина индикатора (чекбокса) */\n"
"    height: 15px; /* Высота индикатора (чекбокса) */\n"
"    border: 2px solid rgb(150, 150, 150); /* Обводка чекбокса */\n"
"    border-radius: 4px; /* Закругление углов */\n"
"    background-color: white; /* Цвет фона чекбокса */\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background-color: rgb(150, 200, 150); \n"
"    border: 2px solid rgb(150, 150, 150); \n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked:hover {\n"
"    border: 2px solid rgb(100, 100, 100);\n"
"}\n"
"\n"
"QCheckBox::indicator:checked:hover {\n"
"    background-color: rgb(180, 230, 180); \n"
"}")
        self.checkBox_use_list_2.setObjectName("checkBox_use_list_2")
        self.gridLayout.addWidget(self.checkBox_use_list_2, 1, 0, 1, 1)
        self.scrollArea_7.setWidget(self.scrollAreaWidgetContents_7)
        self.gridLayout_4.addWidget(self.scrollArea_7, 0, 1, 1, 1)
        self.scrollArea_8 = QtWidgets.QScrollArea(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_8.sizePolicy().hasHeightForWidth())
        self.scrollArea_8.setSizePolicy(sizePolicy)
        self.scrollArea_8.setMinimumSize(QtCore.QSize(310, 280))
        self.scrollArea_8.setStyleSheet("border: 0;")
        self.scrollArea_8.setWidgetResizable(True)
        self.scrollArea_8.setObjectName("scrollArea_8")
        self.scrollAreaWidgetContents_8 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_8.setGeometry(QtCore.QRect(0, 0, 345, 397))
        self.scrollAreaWidgetContents_8.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents_8.setStyleSheet("/* СТИЛЬ ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */\n"
"QScrollBar:vertical {\n"
"    border-radius: 8px;\n"
"    background: rgb(210, 210, 213);\n"
"    width: 14px;\n"
"    margin: 0px 0 0px 0;\n"
"}\n"
"\n"
"/* HANDLE BAR ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */\n"
"QScrollBar::handle:vertical {  \n"
"    background-color: rgb(210, 210, 213);\n"
"    min-height: 30px;\n"
"    border-radius: 0px;\n"
"    transition: background-color 0.2s ease;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {  \n"
"    background-color: rgb(180, 180, 184);\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:pressed {  \n"
"    background-color: rgb(150, 150, 153);\n"
"}\n"
"\n"
"/* КНОПКА ВВЕРХУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */\n"
"QScrollBar::sub-line:vertical {\n"
"    border: none;  \n"
"    background-color: rgb(190, 190, 193);  /* Более темный серый */\n"
"    height: 15px;\n"
"    border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical:hover {  \n"
"    background-color: rgb(170, 170, 174);  /* Темнее при наведении */\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical:pressed {  \n"
"    background-color: rgb(140, 140, 143);  /* Еще темнее при нажатии */\n"
"}\n"
"\n"
"/* КНОПКА ВНИЗУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */\n"
"QScrollBar::add-line:vertical {\n"
"    border: none;  \n"
"    background-color: rgb(190, 190, 193);  /* Более темный серый */\n"
"    height: 15px;\n"
"    border-bottom-left-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical:hover {  \n"
"    background-color: rgb(170, 170, 174);  /* Темнее при наведении */\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical:pressed {  \n"
"    background-color: rgb(140, 140, 143);  /* Еще темнее при нажатии */\n"
"}\n"
"\n"
"/* УБРАТЬ СТРЕЛКИ */\n"
"QScrollBar::up-arrow:vertical, \n"
"QScrollBar::down-arrow:vertical {\n"
"    background: none;\n"
"}\n"
"\n"
"/* УБРАТЬ ФОН */\n"
"QScrollBar::add-page:vertical, \n"
"QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}")
        self.scrollAreaWidgetContents_8.setObjectName("scrollAreaWidgetContents_8")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_8)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textEdit_list_3 = RestrictedTextEdit(self.scrollAreaWidgetContents_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_list_3.sizePolicy().hasHeightForWidth())
        self.textEdit_list_3.setSizePolicy(sizePolicy)
        self.textEdit_list_3.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.textEdit_list_3.setFont(font)
        self.textEdit_list_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"padding-top: 15px; /* Отступ только слева */   \n"
" padding-bottom: 15px; /* Отступ только снизу */\n"
"")
        self.textEdit_list_3.setReadOnly(False)
        self.textEdit_list_3.setObjectName("textEdit_list_3")
        self.gridLayout_3.addWidget(self.textEdit_list_3, 0, 0, 1, 1)
        self.checkBox_use_list_3 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_use_list_3.sizePolicy().hasHeightForWidth())
        self.checkBox_use_list_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_use_list_3.setFont(font)
        self.checkBox_use_list_3.setStyleSheet("\n"
"QCheckBox {\n"
"color: rgb(0, 0, 0);\n"
"    spacing: 5px; /* Отступ между иконкой и текстом */\n"
"\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 15px; /* Ширина индикатора (чекбокса) */\n"
"    height: 15px; /* Высота индикатора (чекбокса) */\n"
"    border: 2px solid rgb(150, 150, 150); /* Обводка чекбокса */\n"
"    border-radius: 4px; /* Закругление углов */\n"
"    background-color: white; /* Цвет фона чекбокса */\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background-color: rgb(150, 200, 150); \n"
"    border: 2px solid rgb(150, 150, 150); \n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked:hover {\n"
"    border: 2px solid rgb(100, 100, 100);\n"
"}\n"
"\n"
"QCheckBox::indicator:checked:hover {\n"
"    background-color: rgb(180, 230, 180); \n"
"}")
        self.checkBox_use_list_3.setObjectName("checkBox_use_list_3")
        self.gridLayout_3.addWidget(self.checkBox_use_list_3, 1, 0, 1, 1)
        self.scrollArea_8.setWidget(self.scrollAreaWidgetContents_8)
        self.gridLayout_4.addWidget(self.scrollArea_8, 0, 2, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 2, 0, 1, 1)
        self.checkBox_set_numbers_end_user_name = QtWidgets.QCheckBox(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_set_numbers_end_user_name.setFont(font)
        self.checkBox_set_numbers_end_user_name.setStyleSheet("\n"
"QCheckBox {\n"
"color: rgb(0, 0, 0);\n"
"    spacing: 5px; /* Отступ между иконкой и текстом */\n"
"    margin-left: 9px;\n"
"border:none;    \n"
"margin-right: 1px;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 15px; /* Ширина индикатора (чекбокса) */\n"
"    height: 15px; /* Высота индикатора (чекбокса) */\n"
"    border: 2px solid rgb(150, 150, 150); /* Обводка чекбокса */\n"
"    border-radius: 4px; /* Закругление углов */\n"
"    background-color: white; /* Цвет фона чекбокса */\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background-color: rgb(150, 200, 150); \n"
"    border: 2px solid rgb(150, 150, 150); \n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked:hover {\n"
"    border: 2px solid rgb(100, 100, 100);\n"
"}\n"
"\n"
"QCheckBox::indicator:checked:hover {\n"
"    background-color: rgb(180, 230, 180); \n"
"}")
        self.checkBox_set_numbers_end_user_name.setObjectName("checkBox_set_numbers_end_user_name")
        self.gridLayout_5.addWidget(self.checkBox_set_numbers_end_user_name, 3, 0, 1, 1)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setContentsMargins(-1, 15, -1, 10)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_32 = QtWidgets.QLabel(self)
        self.label_32.setStyleSheet("border-right: none;\n"
"border-top: none;\n"
"border-bottom: none;\n"
"")
        self.label_32.setText("")
        self.label_32.setObjectName("label_32")
        self.horizontalLayout_13.addWidget(self.label_32)
        self.pushButton_save = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_save.sizePolicy().hasHeightForWidth())
        self.pushButton_save.setSizePolicy(sizePolicy)
        self.pushButton_save.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_save.setFont(font)
        self.pushButton_save.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    text-align: center;\n"
"    border-radius: 17px;\n"
"border: none;\n"
"   }\n"
"QPushButton:hover {\n"
"    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
"}")
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout_13.addWidget(self.pushButton_save)
        self.label_33 = QtWidgets.QLabel(self)
        self.label_33.setStyleSheet("border-left: none;\n"
"border-top: none;\n"
"border-bottom: none;\n"
"")
        self.label_33.setText("")
        self.label_33.setObjectName("label_33")
        self.horizontalLayout_13.addWidget(self.label_33)
        self.gridLayout_5.addLayout(self.horizontalLayout_13, 4, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_title.setText(_translate("Dialog", "формирование user_name канала"))
        self.pushButton_close.setText(_translate("Dialog", "✕"))
        self.label_11.setText(_translate("Dialog", "формирование user_name канала"))
        self.checkBox_use_list_1.setText(_translate("Dialog", "Использовать этот список "))
        self.textEdit_list_1.setHtml(_translate("Dialog", ""))
        self.textEdit_list_2.setHtml(_translate("Dialog", ""))
        self.checkBox_use_list_2.setText(_translate("Dialog", "Использовать этот список "))
        self.textEdit_list_3.setHtml(_translate("Dialog", ""))
        self.checkBox_use_list_3.setText(_translate("Dialog", "Использовать этот список "))
        self.checkBox_set_numbers_end_user_name.setText(_translate("Dialog", "Если канал по сформированному юзернейму занят, то добавить цифры в конец юзернейма"))
        self.pushButton_save.setText(_translate("Dialog", "Сохранить"))