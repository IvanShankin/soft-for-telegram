import pygame
import sys
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
from PyQt5.QtWidgets import  QDialog, QLabel
from PyQt5.QtCore import Qt

class DialogYesOrCancelUi(QDialog):
    def __init__(self):
        super().__init__()
        self.root_project_dir = '..'

        self.setWindowFlags(Qt.FramelessWindowHint)# Убираем рамки окна, включая заголовок
        self.setObjectName("Dialog")
        self.resize(277, 116)
        self.setStyleSheet("border: 1px solid black;")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 3)
        self.verticalLayout.setObjectName("verticalLayout")
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
                                       "    padding-left: 5px;"
                                        "border-right: none;\n"
                                        "border-bottom: none;")
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
"    background-color: rgb(255, 1, 1); /* Цвет фона при наведении  */\n"
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
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.label_info = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_info.sizePolicy().hasHeightForWidth())
        self.label_info.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_info.setFont(font)
        self.label_info.setStyleSheet("border-top: none;\n"
                                    "border-bottom: none;\n"
                                    "    padding-left: 5px;\n"
                                    "    padding-top: 3px;\n"
                                    "    padding-bottom: 5px;\n"
                                    "    padding-right: 5px;\n")
        self.label_info.setObjectName("label_info")
        self.verticalLayout.addWidget(self.label_info)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0,0,0,5)
        self.label_5 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setStyleSheet("border-right: none;\n"
"border-bottom: none;\n"
"border-top: none;")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.pushButton_ok = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_ok.setFont(font)
        self.pushButton_ok.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    text-align: center;\n"
"    border: none;\n"
"    border-radius: 12px;\n"
"    padding-top:     3px;\n"
"    padding-bottom: 3px;    \n"
"    padding-left:     7px;\n"
"    padding-right: 7px;    \n"
"   }\n"
"QPushButton:hover {\n"
"    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
"}")
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout_4.addWidget(self.pushButton_ok)
        self.pushButton_cancel = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_cancel.setFont(font)
        self.pushButton_cancel.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    text-align: center;\n"
"    border: none;\n"
"    border-radius: 12px;\n"
"    padding-top:     3px;\n"
"    padding-bottom: 3px;    \n"
"    padding-left:     7px;\n"
"    padding-right: 7px;    \n"
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
"border-left: none;\n"
"")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_title.setText(_translate("Dialog", " Внимание!"))
        self.pushButton_close.setText(_translate("Dialog", "✕"))
        self.label_info.setText(_translate("Dialog", "info"))
        self.pushButton_ok.setText(_translate("Dialog", "Да"))
        self.pushButton_cancel.setText(_translate("Dialog", "Отмена"))
