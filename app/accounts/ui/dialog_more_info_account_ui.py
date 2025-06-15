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
from PyQt5.QtCore import Qt, QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator

class DialogMoreInfoAccountUi(QDialog):
    def __init__(self):
        super().__init__()
        self.root_project_dir = '..'
        self.setWindowFlags(Qt.FramelessWindowHint)  # Убираем рамки окна, включая заголовок
        self.setObjectName("Dialog")
        self.resize(679, 555)
        self.setStyleSheet("background-color: rgb(236, 237, 240);\n"
                             "border: 1px solid black;")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(143, 41, 21, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("border: none;")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(139, 80, 27, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("border: none;")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(67, 189, 99, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("border: none;")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(125, 224, 41, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("border: none;")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(82, 264, 84, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("border: none;")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(83, 338, 83, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("border: none;")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self)
        self.label_7.setGeometry(QtCore.QRect(26, 377, 140, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("border: none;")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self)
        self.label_8.setGeometry(QtCore.QRect(50, 456, 116, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("border: none;")
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self)
        self.label_9.setGeometry(QtCore.QRect(126, 416, 40, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("border: none;")
        self.label_9.setObjectName("label_9")
        self.label_erro_info = QtWidgets.QLabel(self)
        self.label_erro_info.setGeometry(QtCore.QRect(91, 441, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_erro_info.setFont(font)
        self.label_erro_info.setStyleSheet("border: none;")
        self.label_erro_info.setObjectName("label_erro_info")
        self.label_erro_info.hide()
        self.label_solution_error_info = QtWidgets.QLabel(self)
        self.label_solution_error_info.setGeometry(QtCore.QRect(10, 481, 156, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_solution_error_info.setFont(font)
        self.label_solution_error_info.setStyleSheet("border: none;")
        self.label_solution_error_info.setObjectName("label_solution_error_info")
        self.label_solution_error_info.hide()
        self.label_12 = QtWidgets.QLabel(self)
        self.label_12.setGeometry(QtCore.QRect(124, 119, 42, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("border: none;")
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self)
        self.label_13.setGeometry(QtCore.QRect(80, 154, 86, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("border: none;")
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self)
        self.label_14.setGeometry(QtCore.QRect(101, 303, 65, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("border: none;")
        self.label_14.setObjectName("label_14")
        self.label_geo = QtWidgets.QLabel(self)
        self.label_geo.setGeometry(QtCore.QRect(185, 226, 40, 26))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_geo.setFont(font)
        self.label_geo.setStyleSheet("border: none;\n"
                                     "text-align: center;\n")
        self.label_geo.setText("")
        self.label_geo.setScaledContents(True)
        self.label_geo.setObjectName("label_geo")
        self.label_phone = QtWidgets.QLabel(self)
        self.label_phone.setGeometry(QtCore.QRect(180, 264, 141, 27))
        font = QtGui.QFont()
        font.setPointSize(12)

        self.label_phone.setFont(font)
        self.label_phone.setStyleSheet("border: none;\n"
                                       "  background-color: rgb(255, 255, 255);\n"
                                       "    text-align: center;\n"
                                       "    border-radius: 10px;\n"
                                       "padding: 4px;"
                                       "padding-left: 6px;"
                                       "padding-right: 6px;")
        self.label_phone.setText("")
        self.label_phone.setScaledContents(True)
        self.label_phone.setObjectName("label_phone")
        self.label_tg_id = QtWidgets.QLabel(self)
        self.label_tg_id.setGeometry(QtCore.QRect(180, 80, 141, 27))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_tg_id.setFont(font)
        self.label_tg_id.setStyleSheet("border: none;\n"
                                       "  background-color: rgb(255, 255, 255);\n"
                                       "    text-align: center;\n"
                                       "    border-radius: 10px;\n"
                                       "padding: 4px;"
                                       "padding-left: 6px;"
                                       "padding-right: 6px;")
        self.label_tg_id.setText("")
        self.label_tg_id.setScaledContents(True)
        self.label_tg_id.setObjectName("label_tg_id")
        self.label_id = QtWidgets.QLabel(self)
        self.label_id.setGeometry(QtCore.QRect(180, 41, 141, 27))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_id.setFont(font)
        self.label_id.setStyleSheet("border: none;\n"
                                    "  background-color: rgb(255, 255, 255);\n"
                                    "    text-align: center;\n"
                                    "    border-radius: 10px;\n"
                                    "padding: 4px;"
                                    "padding-left: 6px;"
                                    "padding-right: 6px;")
        self.label_id.setText("")
        self.label_id.setScaledContents(True)
        self.label_id.setObjectName("label_id")
        self.label_recuperation = QtWidgets.QLabel(self)
        self.label_recuperation.setGeometry(QtCore.QRect(180, 338, 141, 27))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_recuperation.setFont(font)
        self.label_recuperation.setStyleSheet("border: none;\n"
                                              "  background-color: rgb(255, 255, 255);\n"
                                              "    text-align: center;\n"
                                              "    border-radius: 10px;\n"
                                              "padding: 4px;"
                                              "padding-left: 6px;"
                                              "padding-right: 6px;"
                                              )
        self.label_recuperation.setText("")
        self.label_recuperation.setScaledContents(True)
        self.label_recuperation.setObjectName("label_recuperation")
        self.label_last_used = QtWidgets.QLabel(self)
        self.label_last_used.setGeometry(QtCore.QRect(180, 377, 141, 27))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_last_used.setFont(font)
        self.label_last_used.setStyleSheet("border: none;\n"
                                           "  background-color: rgb(255, 255, 255);\n"
                                           "    text-align: center;\n"
                                           "    border-radius: 10px;\n"
                                           "padding: 4px;"
                                           "padding-left: 6px;"
                                           "padding-right: 6px;"
                                           )
        self.label_last_used.setText("")
        self.label_last_used.setScaledContents(True)
        self.label_last_used.setObjectName("label_last_used")
        self.label_type = QtWidgets.QLabel(self)
        self.label_type.setGeometry(QtCore.QRect(180, 416, 141, 27))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_type.setFont(font)
        self.label_type.setStyleSheet("border: none;\n"
                                      "  background-color: rgb(255, 255, 255);\n"
                                      "    text-align: center;\n"
                                      "    border-radius: 10px;\n"
                                      "padding: 4px;"
                                      "padding-left: 6px;"
                                      "padding-right: 6px;"
                                      )
        self.label_type.setText("")
        self.label_type.setScaledContents(True)
        self.label_type.setObjectName("label_type")
        self.label_error = QtWidgets.QLabel(self)
        self.label_error.setGeometry(QtCore.QRect(180, 441, 141, 27))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_error.setFont(font)
        self.label_error.setStyleSheet("border: none;\n"
                                       "  background-color: rgb(255, 255, 255);\n"
                                       "    text-align: center;\n"
                                       "    border-radius: 10px;\n"
                                       "padding: 4px;"
                                       "padding-left: 6px;"
                                       "padding-right: 6px;"
                                       )
        self.label_error.setText("")
        self.label_error.setScaledContents(True)
        self.label_error.setObjectName("label_error")
        self.label_error.hide()
        self.label_solution_error = QtWidgets.QLabel(self)
        self.label_solution_error.setGeometry(QtCore.QRect(180, 481, 141, 27))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_solution_error.setFont(font)
        self.label_solution_error.setStyleSheet("border: none;\n"
                                                "  background-color: rgb(255, 255, 255);\n"
                                                "    text-align: center;\n"
                                                "    border-radius: 10px;\n"
                                                "padding: 7px;"
                                                "padding-left: 5px;"
                                                "padding-right: 5px;")
        self.label_solution_error.setText("")
        self.label_solution_error.setScaledContents(True)
        self.label_solution_error.setObjectName("label_solution_error")
        self.label_solution_error.hide()
        self.lineEdit_bio = QtWidgets.QLineEdit(self)
        self.lineEdit_bio.setGeometry(QtCore.QRect(180, 303, 471, 29))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_bio.setFont(font)
        self.lineEdit_bio.setStyleSheet("QLineEdit {\n"
                                        "    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
                                        "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
                                        "    border-radius: 10px; /* Закругление углов */\n"
                                        "    padding: 2px; /* Отступы внутри текстового поля */\n"
                                        "padding-left: 6px;"
                                       "padding-right: 6px;"
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
        self.lineEdit_bio.setMaxLength(69)
        self.lineEdit_bio.setObjectName("lineEdit_bio")
        self.lineEdit_notes = QtWidgets.QLineEdit(self)
        self.lineEdit_notes.setGeometry(QtCore.QRect(180, 456, 471, 29))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_notes.setFont(font)
        self.lineEdit_notes.setStyleSheet("QLineEdit {\n"
                                          "    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
                                          "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
                                          "    border-radius: 10px; /* Закругление углов */\n"
                                          "    padding: 2px; /* Отступы внутри текстового поля */\n"
                                          "padding-left: 6px;"
                                       "padding-right: 6px;"
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
        self.lineEdit_notes.setText("")
        self.lineEdit_notes.setMaxLength(100)
        self.lineEdit_notes.setObjectName("lineEdit_notes")
        self.lineEdit_user_name = QtWidgets.QLineEdit(self)
        self.lineEdit_user_name.setGeometry(QtCore.QRect(180, 189, 471, 29))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_user_name.setFont(font)
        self.lineEdit_user_name.setStyleSheet("QLineEdit {\n"
                                              "    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
                                              "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
                                              "    border-radius: 10px; /* Закругление углов */\n"
                                              "    padding: 2px; /* Отступы внутри текстового поля */\n"
                                              "padding-left: 6px;"
                                       "padding-right: 6px;"
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
        self.lineEdit_user_name.setMaxLength(32)
        self.lineEdit_user_name.setObjectName("lineEdit_user_name")
        regex = QRegularExpression("^[a-zA-Z0-9_]*$")  # Разрешаем только буквы и цифры
        validator = QRegularExpressionValidator(regex)
        self.lineEdit_user_name.setValidator(validator)
        self.lineEdit_surname = QtWidgets.QLineEdit(self)
        self.lineEdit_surname.setGeometry(QtCore.QRect(180, 154, 471, 29))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_surname.setFont(font)
        self.lineEdit_surname.setStyleSheet("QLineEdit {\n"
                                            "    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
                                            "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
                                            "    border-radius: 10px; /* Закругление углов */\n"
                                            "    padding: 2px; /* Отступы внутри текстового поля */\n"
                                            "    padding-left: 6px;"
                                            "    padding-right: 6px;"
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
        self.lineEdit_surname.setMaxLength(64)
        self.lineEdit_surname.setObjectName("lineEdit_surname")
        self.lineEdit_name = QtWidgets.QLineEdit(self)
        self.lineEdit_name.setGeometry(QtCore.QRect(180, 119, 471, 29))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_name.setFont(font)
        self.lineEdit_name.setStyleSheet("QLineEdit {\n"
                                         "    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
                                         "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
                                         "    border-radius: 10px; /* Закругление углов */\n"
                                         "    padding: 2px; /* Отступы внутри текстового поля */\n"
                                         "    padding-left: 6px;"
                                         "    padding-right: 6px;"
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
        self.lineEdit_name.setText("")
        self.lineEdit_name.setMaxLength(64)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.label_title = DraggableLabel(self)
        self.label_title.setGeometry(QtCore.QRect(1, 1, 636, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                       "border: none;\n"
                                       "\n"
                                       "padding-left: 7px;")
        self.label_title.setObjectName("label_title")
        self.pushButton_close = QtWidgets.QPushButton(self)
        self.pushButton_close.setGeometry(QtCore.QRect(637, 1, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setStyleSheet("\n"
                                            "QPushButton {\n"
                                            "    background-color: rgb(255, 255, 255);\n"
                                            "    text-align: center;\n"
                                            "    border: none;\n"
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
        self.pushButton_save = QtWidgets.QPushButton(self)
        self.pushButton_save.setGeometry(QtCore.QRect(163, 500, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_save.setFont(font)
        self.pushButton_save.setStyleSheet("QPushButton {\n"
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
        self.pushButton_save.setObjectName("pushButton_save")
        self.pushButton_close_2 = QtWidgets.QPushButton(self)
        self.pushButton_close_2.setGeometry(QtCore.QRect(390, 500, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_close_2.setFont(font)
        self.pushButton_close_2.setStyleSheet("QPushButton {\n"
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
        self.pushButton_close_2.setObjectName("pushButton_close_2")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">#</span>:</p></body></html>"))
        self.label_2.setText(_translate("Dialog", "ID:"))
        self.label_3.setText(_translate("Dialog", "Юзернейм:"))
        self.label_4.setText(_translate("Dialog", "ГЕО:"))
        self.label_5.setText(_translate("Dialog", "Телефон:"))
        self.label_6.setText(_translate("Dialog", "Отлёжка:"))
        self.label_7.setText(_translate("Dialog", "Использовался:"))
        self.label_8.setText(_translate("Dialog", "Примечание:"))
        self.label_9.setText(_translate("Dialog", "Тип:"))
        self.label_erro_info.setText(_translate("Dialog", "Ошибка:"))
        self.label_solution_error_info.setText(_translate("Dialog", "Решение ошибки:"))
        self.label_12.setText(_translate("Dialog", "Имя:"))
        self.label_13.setText(_translate("Dialog", "Фамилия:"))
        self.label_14.setText(_translate("Dialog", "О себе:"))
        self.label_title.setText(_translate("Dialog", "Данные об аккаунте"))
        self.pushButton_close.setText(_translate("Dialog", "✕"))
        self.pushButton_save.setText(_translate("Dialog", "сохранить изменения"))
        self.pushButton_close_2.setText(_translate("Dialog", "Закрыть"))