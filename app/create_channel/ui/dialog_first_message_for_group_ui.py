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
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp

class DialogFirstMessageUi(QDialog):
    def __init__(self):
        super().__init__()
        self.root_project_dir = '..'
        self.setWindowFlags(Qt.FramelessWindowHint)  # Убираем рамки окна, включая заголовок

        self.setObjectName("Dialog")
        self.resize(1000, 600)
        self.setStyleSheet("background-color: rgb(236, 237, 240);\n"
                           "border: 1px solid black;")
        self.gridLayout_21 = QtWidgets.QGridLayout(self)
        self.gridLayout_21.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_title = DraggableLabel(self)
        self.label_title.setText('Сообщение для отправки')
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
        self.pushButton_close.setFlat(False)
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout.addWidget(self.pushButton_close)
        self.gridLayout_21.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_16.setContentsMargins(9, -1, 0, -1)
        self.gridLayout_16.setVerticalSpacing(6)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.scrollArea_7 = QtWidgets.QScrollArea(self)
        self.scrollArea_7.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea_7.setStyleSheet("border: 0;")
        self.scrollArea_7.setWidgetResizable(True)
        self.scrollArea_7.setObjectName("scrollArea_7")
        self.scrollAreaWidgetContents_7 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_7.setGeometry(QtCore.QRect(0, 0, 609, 431))
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
        self.gridLayout_17 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_7)
        self.gridLayout_17.setContentsMargins(-1, -1, -1, 10)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.gridLayout_18 = QtWidgets.QGridLayout()
        self.gridLayout_18.setContentsMargins(0, -1, -1, -1)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.textEdit_message = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_7)
        self.textEdit_message.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textEdit_message.setFont(font)
        self.textEdit_message.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                            "border-radius: 20px;\n"
                                            "padding-top: 15px; /* Отступ только слева */   \n"
                                            " padding-bottom: 15px; /* Отступ только снизу */\n"
                                            "")
        self.textEdit_message.setReadOnly(False)
        self.textEdit_message.setObjectName("textEdit_message")
        self.gridLayout_18.addWidget(self.textEdit_message, 0, 0, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_18, 1, 0, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.checkBox_use_file_for_message = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_7)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.checkBox_use_file_for_message.setFont(font)
        self.checkBox_use_file_for_message.setStyleSheet("\n"
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
        self.checkBox_use_file_for_message.setObjectName("checkBox_use_file_for_message")
        self.horizontalLayout_11.addWidget(self.checkBox_use_file_for_message)
        self.pushButton_choose_file_for_message = QtWidgets.QPushButton(self.scrollAreaWidgetContents_7)
        self.pushButton_choose_file_for_message.setMinimumSize(QtCore.QSize(0, 31))
        self.pushButton_choose_file_for_message.setMaximumSize(QtCore.QSize(70, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_choose_file_for_message.setFont(font)
        self.pushButton_choose_file_for_message.setStyleSheet("QPushButton {\n"
                                                              "  background: rgb(210, 210, 213);\n"
                                                              "text-align: center;\n"
                                                              "border-radius: 10px;\n"
                                                              "   }\n"
                                                              "   QPushButton:hover {\n"
                                                              "          background-color: rgb(180, 180, 184); /* Цвет при наведении */\n"
                                                              "   }\n"
                                                              "\n"
                                                              "QPushButton:pressed {\n"
                                                              "                   background-color: rgb(150, 150, 153); /* Цвет фона при нажатии */\n"
                                                              "            }")
        self.pushButton_choose_file_for_message.setObjectName("pushButton_choose_file_for_message")
        self.horizontalLayout_11.addWidget(self.pushButton_choose_file_for_message)
        self.gridLayout_17.addLayout(self.horizontalLayout_11, 2, 0, 1, 1)
        self.scrollArea_7.setWidget(self.scrollAreaWidgetContents_7)
        self.gridLayout_16.addWidget(self.scrollArea_7, 1, 0, 1, 1)
        self.label_25 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_25.setFont(font)
        self.label_25.setStyleSheet("border: none;")
        self.label_25.setObjectName("label_25")
        self.gridLayout_16.addWidget(self.label_25, 0, 0, 1, 1)
        self.gridLayout_21.addLayout(self.gridLayout_16, 1, 0, 1, 1)
        self.gridLayout_19 = QtWidgets.QGridLayout()
        self.gridLayout_19.setContentsMargins(-1, -1, 9, -1)
        self.gridLayout_19.setVerticalSpacing(11)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.groupBox_4 = QtWidgets.QGroupBox(self)
        self.groupBox_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 20px;\n"
                                      "border: none;"
                                      "margin-top: 4px;")
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_20 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.label_27 = QtWidgets.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_27.setFont(font)
        self.label_27.setStyleSheet("border: none;")
        self.label_27.setObjectName("label_27")
        self.gridLayout_20.addWidget(self.label_27, 1, 0, 1, 1)
        self.lineEdit_user_name_group = QtWidgets.QLineEdit(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_user_name_group.sizePolicy().hasHeightForWidth())
        self.lineEdit_user_name_group.setSizePolicy(sizePolicy)
        self.lineEdit_user_name_group.setMaximumSize(QtCore.QSize(643543, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_user_name_group.setFont(font)
        self.lineEdit_user_name_group.setStyleSheet("QLineEdit {\n"
                                                    "    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
                                                    "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
                                                    "    border-radius: 6px; /* Закругление углов */\n"
                                                    "    padding: 2px; /* Отступы внутри текстового поля */\n"
                                                    "    color: rgb(50, 50, 50); /* Цвет текста */\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* Состояние при наведении */\n"
                                                    "QLineEdit:hover {\n"
                                                    "    border: 2px solid rgb(160, 160, 160); /* Цвет рамки при наведении */\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* Состояние при фокусировке */\n"
                                                    "QLineEdit:focus {\n"
                                                    "    border: 2px solid rgb(0, 0, 0); /* Цвет рамки при фокусировке */\n"
                                                    "    background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* Состояние для отключенного текстового поля */\n"
                                                    "QLineEdit:disabled {\n"
                                                    "    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */\n"
                                                    "    color: rgb(170, 170, 170); /* Цвет текста для отключенного */\n"
                                                    "    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */\n"
                                                    "}")
        self.lineEdit_user_name_group.setMaxLength(32)
        self.lineEdit_user_name_group.setObjectName("lineEdit_user_name_group")
        validator = QRegExpValidator(QRegExp(r"^[a-zA-Z0-9_]*$"))  # Разрешаем только цифры и английские буквы (целые числа любой длины)
        self.lineEdit_user_name_group.setValidator(validator)
        self.gridLayout_20.addWidget(self.lineEdit_user_name_group, 0, 1, 1, 1)
        self.lineEdit_ID_message = QtWidgets.QLineEdit(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ID_message.sizePolicy().hasHeightForWidth())
        self.lineEdit_ID_message.setSizePolicy(sizePolicy)
        self.lineEdit_ID_message.setMaximumSize(QtCore.QSize(643543, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_ID_message.setFont(font)
        validator = QRegExpValidator(QRegExp(r"[0-9]*"))  # Разрешаем только цифры (целые числа любой длины)
        self.lineEdit_ID_message.setValidator(validator)
        self.lineEdit_ID_message.setStyleSheet("QLineEdit {\n"
                                               "    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
                                               "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
                                               "    border-radius: 6px; /* Закругление углов */\n"
                                               "    padding: 2px; /* Отступы внутри текстового поля */\n"
                                               "    color: rgb(50, 50, 50); /* Цвет текста */\n"
                                               "}\n"
                                               "\n"
                                               "/* Состояние при наведении */\n"
                                               "QLineEdit:hover {\n"
                                               "    border: 2px solid rgb(160, 160, 160); /* Цвет рамки при наведении */\n"
                                               "}\n"
                                               "\n"
                                               "/* Состояние при фокусировке */\n"
                                               "QLineEdit:focus {\n"
                                               "    border: 2px solid rgb(0, 0, 0); /* Цвет рамки при фокусировке */\n"
                                               "    background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */\n"
                                               "}\n"
                                               "\n"
                                               "/* Состояние для отключенного текстового поля */\n"
                                               "QLineEdit:disabled {\n"
                                               "    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */\n"
                                               "    color: rgb(170, 170, 170); /* Цвет текста для отключенного */\n"
                                               "    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */\n"
                                               "}")
        self.lineEdit_ID_message.setMaxLength(40)
        self.lineEdit_ID_message.setObjectName("lineEdit_ID_message")
        self.gridLayout_20.addWidget(self.lineEdit_ID_message, 1, 1, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_28.setFont(font)
        self.label_28.setStyleSheet("border: none;")
        self.label_28.setObjectName("label_28")
        self.gridLayout_20.addWidget(self.label_28, 0, 0, 1, 1)
        self.gridLayout_19.addWidget(self.groupBox_4, 1, 0, 1, 2)
        self.pushButton_info_forwarded_message = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_info_forwarded_message.sizePolicy().hasHeightForWidth())
        self.pushButton_info_forwarded_message.setSizePolicy(sizePolicy)
        self.pushButton_info_forwarded_message.setStyleSheet("background-color: none;\n"
                                                             "border: none;")
        self.pushButton_info_forwarded_message.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/question.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_info_forwarded_message.setIcon(icon)
        self.pushButton_info_forwarded_message.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_info_forwarded_message.setObjectName("pushButton_info_forwarded_message")
        self.gridLayout_19.addWidget(self.pushButton_info_forwarded_message, 0, 1, 1, 1)
        self.label_29 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy)
        self.label_29.setStyleSheet("border: none;")
        self.label_29.setText("")
        self.label_29.setObjectName("label_29")
        self.gridLayout_19.addWidget(self.label_29, 2, 0, 1, 1)
        self.label_26 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_26.setFont(font)
        self.label_26.setStyleSheet("border: none;\n"
                                    "margin-left: 10px; ")
        self.label_26.setObjectName("label_26")
        self.gridLayout_19.addWidget(self.label_26, 0, 0, 1, 1)
        self.gridLayout_21.addLayout(self.gridLayout_19, 1, 1, 1, 1)
        self.checkBox_use_the_forwarded_message = QtWidgets.QCheckBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_use_the_forwarded_message.sizePolicy().hasHeightForWidth())
        self.checkBox_use_the_forwarded_message.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_use_the_forwarded_message.setFont(font)
        self.checkBox_use_the_forwarded_message.setStyleSheet("\n"
                                                              "QCheckBox {\n"
                                                              "color: rgb(0, 0, 0);\n"
                                                              "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                                              "border: none;\n"
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
        self.checkBox_use_the_forwarded_message.setObjectName("checkBox_use_the_forwarded_message")
        self.gridLayout_21.addWidget(self.checkBox_use_the_forwarded_message, 2, 1, 1, 1)
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
        self.gridLayout_21.addLayout(self.horizontalLayout_13, 4, 0, 1, 2)
        self.checkBox_use_new_message = QtWidgets.QCheckBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_use_new_message.sizePolicy().hasHeightForWidth())
        self.checkBox_use_new_message.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_use_new_message.setFont(font)
        self.checkBox_use_new_message.setStyleSheet("\n"
                                                    "QCheckBox {\n"
                                                    "color: rgb(0, 0, 0);\n"
                                                    "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                                    "margin-left: 18px;\n"
                                                    "border: none;\n"
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
        self.checkBox_use_new_message.setObjectName("checkBox_use_new_message")
        self.gridLayout_21.addWidget(self.checkBox_use_new_message, 2, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_title.setText(_translate("Dialog", "Сообщение для отправки"))
        self.pushButton_close.setText(_translate("Dialog", "✕"))
        self.textEdit_message.setHtml(_translate("Dialog", ""))
        self.checkBox_use_file_for_message.setText(_translate("Dialog", "Использовать файл для сообщения "))
        self.pushButton_choose_file_for_message.setText(_translate("Dialog", "Выбрать"))
        self.label_25.setText(_translate("Dialog", "Новое сообщение:"))
        self.label_27.setText(_translate("Dialog", "ID сообщения:"))
        self.label_28.setText(_translate("Dialog", "User_name чата/канала:"))
        self.label_26.setText(_translate("Dialog", "Переслать сообщение:"))
        self.checkBox_use_the_forwarded_message.setText(_translate("Dialog", "Использовать пересланное сообщение "))
        self.pushButton_save.setText(_translate("Dialog", "Сохранить"))
        self.checkBox_use_new_message.setText(_translate("Dialog", "Использовать новое сообщение "))

