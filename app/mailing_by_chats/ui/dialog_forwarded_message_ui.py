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


class DialogForwardedMessageUi(QDialog):
    def __init__(self):
        super().__init__()
        self.root_project_dir = '..'
        self.setWindowFlags(Qt.FramelessWindowHint)  # Убираем рамки окна, включая заголовок

        self.setObjectName("Dialog")
        self.resize(394, 280)
        self.setStyleSheet("background-color: rgb(236, 237, 240);\n"
                             "border: 1px solid black;")
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
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
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_19 = QtWidgets.QGridLayout()
        self.gridLayout_19.setContentsMargins(9, -1, 9, -1)
        self.gridLayout_19.setVerticalSpacing(11)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.groupBox_4 = QtWidgets.QGroupBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 20px;\n"
                                      "border: none;\n"
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
        self.lineEdit_user_name_group.setMaxLength(20)
        validator = QRegExpValidator(QRegExp(r"^[a-zA-Z0-9_]*$"))  # Разрешаем только цифры (целые числа любой длины)
        self.lineEdit_user_name_group.setValidator(validator)
        self.lineEdit_user_name_group.setObjectName("lineEdit_user_name_group")
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
        self.lineEdit_ID_message.setMaxLength(20)
        validator = QRegExpValidator(QRegExp(r"[0-9]*"))  # Разрешаем только цифры (целые числа любой длины)
        self.lineEdit_ID_message.setValidator(validator)
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
        self.pushButton_info = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_info.sizePolicy().hasHeightForWidth())
        self.pushButton_info.setSizePolicy(sizePolicy)
        self.pushButton_info.setStyleSheet("background-color: none;\n"
                                           "border: none;")
        self.pushButton_info.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/question.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_info.setIcon(icon)
        self.pushButton_info.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_info.setObjectName("pushButton_info")
        self.gridLayout_19.addWidget(self.pushButton_info, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setStyleSheet("border: none;\n"
                                 "margin-left: 3px; ")
        self.label.setObjectName("label")
        self.gridLayout_19.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_19, 1, 0, 1, 1)
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
        self.gridLayout.addLayout(self.horizontalLayout_13, 2, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_title.setText(_translate("Dialog", "Сообщение для пересылки"))
        self.pushButton_close.setText(_translate("Dialog", "✕"))
        self.label_27.setText(_translate("Dialog", "ID сообщения:"))
        self.label_28.setText(_translate("Dialog", "User_name чата/канала:"))
        self.label.setText(_translate("Dialog", "Данные сообщения:"))
        self.pushButton_save.setText(_translate("Dialog", "Сохранить"))