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
from PyQt5.QtWidgets import  QDialog
from PyQt5.QtCore import Qt

class DialogAddAccountsUi(QDialog):
    def __init__(self):
        super().__init__()
        self.root_project_dir = '..'
        self.setWindowFlags(Qt.FramelessWindowHint)  # Убираем рамки окна, включая заголовок
        self.setObjectName("Dialog")
        self.setStyleSheet("border: 1px solid black;")  # Обводка по всему периметру окна
        self.resize(460, 127) # длинна изначально была 190
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 15)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_title = DraggableLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy)
        self.label_title.setMaximumSize(QtCore.QSize(16777215, 33))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("background-color: rgb(255, 255, 255);"
                                       "padding-left: 7px;"
                                       "border-bottom: none;"
                                       "border-right: none;")
        self.label_title.setObjectName("label_title")
        self.horizontalLayout_3.addWidget(self.label_title)
        self.pushButton_close = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
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
"    border-bottom: none;"
"    border-left: none;"
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
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, -1, 10, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_progress_bar = QtWidgets.QGroupBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_progress_bar.sizePolicy().hasHeightForWidth())
        self.groupBox_progress_bar.setSizePolicy(sizePolicy)
        self.groupBox_progress_bar.setMinimumSize(QtCore.QSize(0, 66))
        self.groupBox_progress_bar.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBox_progress_bar.setFont(font)
        self.groupBox_progress_bar.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 17px;\n"
"    border: none;"
"\n"
"")
        self.groupBox_progress_bar.setTitle("")
        self.groupBox_progress_bar.setObjectName("groupBox_progress_bar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_progress_bar)
        self.horizontalLayout.setContentsMargins(11, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar = QtWidgets.QProgressBar(self.groupBox_progress_bar)
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet("QProgressBar {\n"
"                border: 2px solid  rgb(255, 255, 255); /* Цвет рамки */\n"
"                border-radius: 5px; /* Закругленные углы */\n"
"                background-color: #f3f3f3; /* Цвет фона */\n"
"\n"
"            }\n"
"\n"
"QProgressBar::chunk {\n"
"                background: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:1, \n"
"                    stop:1 #4CAF50, stop:1 #81C784); /* Градиент зеленого цвета */\n"
"                border-radius: 5px; /* Закругленные углы заполненной части */\n"
"            }\n"
"")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.pushButton_info = QtWidgets.QPushButton(self.groupBox_progress_bar)
        self.pushButton_info.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/success.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_info.setIcon(icon)
        self.pushButton_info.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_info.setObjectName("pushButton_info")
        self.pushButton_info.hide()
        self.pushButton_info.setStyleSheet(" border: none;")
        self.horizontalLayout.addWidget(self.pushButton_info)
        self.label_info = QtWidgets.QLabel(self.groupBox_progress_bar)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_info.setFont(font)
        self.label_info.setObjectName("label_info")
        self.label_info.hide()
        self.label_info.setStyleSheet('border: none;')
        self.horizontalLayout.addWidget(self.label_info)
        self.horizontalLayout_2.addWidget(self.groupBox_progress_bar)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 15, -1, 7)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_5.setStyleSheet("    border-bottom: none;"
                                   "    border-right: none;"
                                   "    border-top: none;")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.pushButton_close_bottom = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_close_bottom.setFont(font)
        self.pushButton_close_bottom.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    text-align: center;\n"
"    border: none;"
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
        self.pushButton_close_bottom.setObjectName("pushButton_close_bottom")
        self.pushButton_close_bottom.hide()
        self.horizontalLayout_4.addWidget(self.pushButton_close_bottom)
        self.pushButton_chooes = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_chooes.setFont(font)
        self.pushButton_chooes.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    text-align: center;\n"
"    border: none;"
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
        self.pushButton_chooes.setObjectName("pushButton_chooes")
        self.pushButton_chooes.hide() # скрыли
        self.horizontalLayout_4.addWidget(self.pushButton_chooes)
        self.pushButton_report = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_report.setFont(font)
        self.pushButton_report.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    text-align: center;\n"
"    border: none;"
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
        self.pushButton_report.setObjectName("pushButton_report")
        self.pushButton_report.hide()  # скрыли
        self.horizontalLayout_4.addWidget(self.pushButton_report)
        self.label_6 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setStyleSheet("border-left: none;"
                                   "border-top: none;"
                                   "border-bottom: none;")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_title.setText(_translate("Dialog", "В процессе..."))
        self.pushButton_close.setText(_translate("Dialog", "✕"))
        self.label_info.setText(_translate("Dialog", "TextLabel"))
        self.pushButton_close_bottom.setText(_translate("Dialog", "Закрыть"))
        self.pushButton_chooes.setText(_translate("Dialog", "Выбрать"))
        self.pushButton_report.setText(_translate("Dialog", "Отчёт"))


