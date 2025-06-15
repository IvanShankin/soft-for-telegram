import os

from app.general.ui.draggable_label_ui import DraggableLabel

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

class DialogInfoAddAccountsUi(QDialog):
    def __init__(self):
        self.root_project_dir = '..'
        super().__init__()
        self.setObjectName("Dialog")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Убираем рамки окна, включая заголовок
        self.resize(486, 170)
        self.setStyleSheet("border: 1px solid black;\n"
                             "background-color: rgb(236, 237, 240);")
        self.gridLayout_2 = QtWidgets.QGridLayout(self)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_title = DraggableLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                       "    border-right: none;\n"
                                       "    border-bottom: none;")
        self.label_title.setObjectName("label_title")
        self.horizontalLayout_3.addWidget(self.label_title)
        self.pushButton_close = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setStyleSheet("\n"
                                            "QPushButton {\n"
                                            "    background-color: rgb(255, 255, 255);\n"
                                            "    text-align: center;\n"
                                            "    border-left: none;\n"
                                            "    border-bottom: none;\n"
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
        self.horizontalLayout_3.addWidget(self.pushButton_close)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setStyleSheet("padding-left: 14px;\n"
                                 "border-top: none;\n"
                                 "border-bottom: none;\n"
                                 "border-right: none;")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.pushButton_info_folder = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_info_folder.sizePolicy().hasHeightForWidth())
        self.pushButton_info_folder.setSizePolicy(sizePolicy)
        self.pushButton_info_folder.setStyleSheet("margin-top: 8px;\n"
                                                  "border: none;\n"
                                                  "")
        self.pushButton_info_folder.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/question.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_info_folder.setIcon(icon)
        self.pushButton_info_folder.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_info_folder.setObjectName("pushButton_info_folder")
        self.horizontalLayout.addWidget(self.pushButton_info_folder)
        self.label_8 = QtWidgets.QLabel(self)
        self.label_8.setStyleSheet("border-top: none;\n"
                                   "border-bottom: none;\n"
                                   "border-left: none;\n"
                                   "")
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.horizontalLayout.addWidget(self.label_8)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(15, 10, 15, 5)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox_use_autofill = QtWidgets.QCheckBox(self)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.checkBox_use_autofill.setFont(font)
        self.checkBox_use_autofill.setStyleSheet("\n"
                                                 "QCheckBox {\n"
                                                 "color: rgb(0, 0, 0);\n"
                                                 "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                                 "    border: none;\n"
                                                 "    margin-left: 4px;\n"
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
                                                 "    border: 2px solid rgb(150, 150, 150);\n"
                                                 "}\n"
                                                 "\n"
                                                 "QCheckBox::indicator:checked:hover {\n"
                                                 "    background-color: rgb(180, 230, 180); \n"
                                                 "}")
        self.checkBox_use_autofill.setObjectName("checkBox_use_autofill")
        self.verticalLayout.addWidget(self.checkBox_use_autofill)
        self.groupBox = QtWidgets.QGroupBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "border-radius: 20px;\n"
                                    "border: none;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.groupBox.hide()
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(12, -1, 12, -1)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.checkBox_avatar_man = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_avatar_man.setFont(font)
        self.checkBox_avatar_man.setStyleSheet("QCheckBox {\n"
                                               "color: rgb(0, 0, 0);\n"
                                               "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                               "    border: none;\n"
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
                                               "    border: 2px solid rgb(150, 150, 150);\n"
                                               "}\n"
                                               "\n"
                                               "QCheckBox::indicator:checked:hover {\n"
                                               "    background-color: rgb(180, 230, 180); \n"
                                               "}")
        self.checkBox_avatar_man.setObjectName("checkBox_avatar_man")
        self.gridLayout.addWidget(self.checkBox_avatar_man, 0, 1, 1, 2)
        self.checkBox_avatar_neutral = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_avatar_neutral.setFont(font)
        self.checkBox_avatar_neutral.setStyleSheet("QCheckBox {\n"
                                                   "color: rgb(0, 0, 0);\n"
                                                   "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                                   "    border: none;\n"
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
                                                   "    border: 2px solid rgb(150, 150, 150);\n"
                                                   "}\n"
                                                   "\n"
                                                   "QCheckBox::indicator:checked:hover {\n"
                                                   "    background-color: rgb(180, 230, 180); \n"
                                                   "}")
        self.checkBox_avatar_neutral.setObjectName("checkBox_avatar_neutral")
        self.gridLayout.addWidget(self.checkBox_avatar_neutral, 0, 3, 1, 1)
        self.checkBox_avatar_woman = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_avatar_woman.setFont(font)
        self.checkBox_avatar_woman.setStyleSheet("QCheckBox {\n"
                                                 "color: rgb(0, 0, 0);\n"
                                                 "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                                 "    border: none;\n"
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
                                                 "    border: 2px solid rgb(150, 150, 150);\n"
                                                 "}\n"
                                                 "\n"
                                                 "QCheckBox::indicator:checked:hover {\n"
                                                 "    background-color: rgb(180, 230, 180); \n"
                                                 "}\n"
                                                 "")
        self.checkBox_avatar_woman.setObjectName("checkBox_avatar_woman")
        self.gridLayout.addWidget(self.checkBox_avatar_woman, 0, 4, 1, 1)


        self.label_3 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.checkBox_name_man = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_name_man.setFont(font)
        self.checkBox_name_man.setStyleSheet("QCheckBox {\n"
                                           "color: rgb(0, 0, 0);\n"
                                           "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                           "    border: none;\n"
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
                                           "    border: 2px solid rgb(150, 150, 150);\n"
                                           "}\n"
                                           "\n"
                                           "QCheckBox::indicator:checked:hover {\n"
                                           "    background-color: rgb(180, 230, 180); \n"
                                           "}")
        self.checkBox_name_man.setObjectName("checkBox_name_man")
        self.gridLayout.addWidget(self.checkBox_name_man, 2, 1, 1, 2)
        self.checkBox_name_neutral = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_name_neutral.setFont(font)
        self.checkBox_name_neutral.setStyleSheet("QCheckBox {\n"
                                               "color: rgb(0, 0, 0);\n"
                                               "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                               "    border: none;\n"
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
                                               "    border: 2px solid rgb(150, 150, 150);\n"
                                               "}\n"
                                               "\n"
                                               "QCheckBox::indicator:checked:hover {\n"
                                               "    background-color: rgb(180, 230, 180); \n"
                                               "}")
        self.checkBox_name_neutral.setObjectName("checkBox_name_neutral")
        self.gridLayout.addWidget(self.checkBox_name_neutral, 2, 3, 1, 1)
        self.checkBox_name_woman = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_name_woman.setFont(font)
        self.checkBox_name_woman.setStyleSheet("QCheckBox {\n"
                                             "color: rgb(0, 0, 0);\n"
                                             "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                             "    border: none;\n"
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
                                             "    border: 2px solid rgb(150, 150, 150);\n"
                                             "}\n"
                                             "\n"
                                             "QCheckBox::indicator:checked:hover {\n"
                                             "    background-color: rgb(180, 230, 180); \n"
                                             "}")
        self.checkBox_name_woman.setObjectName("checkBox_name_woman")
        self.gridLayout.addWidget(self.checkBox_name_woman, 2, 4, 1, 1)




        self.label_9 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)
        self.checkBox_surname_man = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_surname_man.setFont(font)
        self.checkBox_surname_man.setStyleSheet("QCheckBox {\n"
                                           "color: rgb(0, 0, 0);\n"
                                           "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                           "    border: none;\n"
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
                                           "    border: 2px solid rgb(150, 150, 150);\n"
                                           "}\n"
                                           "\n"
                                           "QCheckBox::indicator:checked:hover {\n"
                                           "    background-color: rgb(180, 230, 180); \n"
                                           "}")
        self.checkBox_surname_man.setObjectName("checkBox_surname_man")
        self.gridLayout.addWidget(self.checkBox_surname_man, 3, 1, 1, 2)
        self.checkBox_surname_neutral = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_surname_neutral.setFont(font)
        self.checkBox_surname_neutral.setStyleSheet("QCheckBox {\n"
                                               "color: rgb(0, 0, 0);\n"
                                               "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                               "    border: none;\n"
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
                                               "    border: 2px solid rgb(150, 150, 150);\n"
                                               "}\n"
                                               "\n"
                                               "QCheckBox::indicator:checked:hover {\n"
                                               "    background-color: rgb(180, 230, 180); \n"
                                               "}")
        self.checkBox_surname_neutral.setObjectName("checkBox_surname_neutral")
        self.gridLayout.addWidget(self.checkBox_surname_neutral, 3, 3, 1, 1)
        self.checkBox_surname_woman = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_surname_woman.setFont(font)
        self.checkBox_surname_woman.setStyleSheet("QCheckBox {\n"
                                             "color: rgb(0, 0, 0);\n"
                                             "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                             "    border: none;\n"
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
                                             "    border: 2px solid rgb(150, 150, 150);\n"
                                             "}\n"
                                             "\n"
                                             "QCheckBox::indicator:checked:hover {\n"
                                             "    background-color: rgb(180, 230, 180); \n"
                                             "}")
        self.checkBox_surname_woman.setObjectName("checkBox_surname_woman")
        self.gridLayout.addWidget(self.checkBox_surname_woman, 3, 4, 1, 1)






        self.label_7 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1)
        self.checkBox_user_name = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_user_name.setFont(font)
        self.checkBox_user_name.setStyleSheet("QCheckBox {\n"
                                              "color: rgb(0, 0, 0);\n"
                                              "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                              "    border: none;\n"
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
                                              "    border: 2px solid rgb(150, 150, 150);\n"
                                              "}\n"
                                              "\n"
                                              "QCheckBox::indicator:checked:hover {\n"
                                              "    background-color: rgb(180, 230, 180); \n"
                                              "}")
        self.checkBox_user_name.setObjectName("checkBox_user_name")
        self.gridLayout.addWidget(self.checkBox_user_name, 4, 1, 1, 2)

        self.label_4 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 2)
        self.checkBox_description = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_description.setFont(font)
        self.checkBox_description.setStyleSheet("QCheckBox {\n"
                                                "color: rgb(0, 0, 0);\n"
                                                "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                                "    border: none;\n"
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
                                                "    border: 2px solid rgb(150, 150, 150);\n"
                                                "}\n"
                                                "\n"
                                                "QCheckBox::indicator:checked:hover {\n"
                                                "    background-color: rgb(180, 230, 180); \n"
                                                "}")
        self.checkBox_description.setObjectName("checkBox_description")
        self.gridLayout.addWidget(self.checkBox_description, 5, 1, 1, 2)
        self.verticalLayout.addWidget(self.groupBox)
        self.gridLayout_2.addLayout(self.verticalLayout, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, -1, -1, 7)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setStyleSheet("border-top: none;\n"
                                   "border-bottom: none;\n"
                                   "border-right: none;")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.pushButton_choose = QtWidgets.QPushButton(self)
        self.pushButton_choose.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_choose.setFont(font)
        self.pushButton_choose.setStyleSheet("\n"
                                             "QPushButton {\n"
                                             "    background-color: rgb(255, 255, 255);\n"
                                             "    text-align: center;\n"
                                             "    border-radius: 12px;\n"
                                             "    padding-top:     3px;\n"
                                             "    padding-bottom: 3px;    \n"
                                             "    padding-left:     7px;\n"
                                             "    padding-right: 7px;    \n"
                                             "    border: none;\n"
                                             "   }\n"
                                             "QPushButton:hover {\n"
                                             "    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
                                             "}\n"
                                             "\n"
                                             "QPushButton:pressed {\n"
                                             "     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
                                             "}")
        self.pushButton_choose.setObjectName("pushButton_choose")
        self.horizontalLayout_4.addWidget(self.pushButton_choose)
        self.pushButton_cancel = QtWidgets.QPushButton(self)
        self.pushButton_cancel.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_cancel.setFont(font)
        self.pushButton_cancel.setStyleSheet("\n"
                                             "QPushButton {\n"
                                             "    background-color: rgb(255, 255, 255);\n"
                                             "    text-align: center;\n"
                                             "    border-radius: 12px;\n"
                                             "    padding: 3px;\n"
                                             "    border: none;\n"
                                             "   }\n"
                                             "QPushButton:hover {\n"
                                             "    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
                                             "}\n"
                                             "\n"
                                             "QPushButton:pressed {\n"
                                             "     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
                                             "}")
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout_4.addWidget(self.pushButton_cancel)
        self.label_6 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setStyleSheet("border-top: none;\n"
                                   "border-bottom: none;\n"
                                   "border-left: none;")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)



    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_title.setText(_translate("Dialog", " Внимание!"))
        self.pushButton_close.setText(_translate("Dialog", "✕"))
        self.label.setText(_translate("Dialog", "Необходимо выбрать папку\n"
                                                "и соблюсти такую иерархию папок:"))
        self.checkBox_use_autofill.setText(_translate("Dialog", "Использовать автозаполнение аккаунта"))
        self.label_2.setText(_translate("Dialog", "Аватар:"))
        self.checkBox_avatar_man.setText(_translate("Dialog", "Мужской"))
        self.checkBox_avatar_neutral.setText(_translate("Dialog", "Нейтральный"))
        self.checkBox_avatar_woman.setText(_translate("Dialog", "Женский"))
        self.label_7.setText(_translate("Dialog", "User name:"))
        self.checkBox_user_name.setText(_translate("Dialog", "Установить"))
        self.label_3.setText(_translate("Dialog", "Имя:"))
        self.checkBox_name_man.setText(_translate("Dialog", "Мужское"))
        self.checkBox_name_neutral.setText(_translate("Dialog", "Нейтральное"))
        self.checkBox_name_woman.setText(_translate("Dialog", "Женское"))
        self.label_9.setText(_translate("Dialog", "Фамилия:"))
        self.checkBox_surname_man.setText(_translate("Dialog", "Мужская"))
        self.checkBox_surname_neutral.setText(_translate("Dialog", "Нейтральная"))
        self.checkBox_surname_woman.setText(_translate("Dialog", "Женская"))
        self.label_4.setText(_translate("Dialog", "БИО:"))
        self.checkBox_description.setText(_translate("Dialog", "Установить"))
        self.pushButton_choose.setText(_translate("Dialog", "Выбрать"))
        self.pushButton_cancel.setText(_translate("Dialog", "Отмена"))

