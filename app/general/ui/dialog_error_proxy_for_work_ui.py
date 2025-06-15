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

class DialogErrorProxyUi(QDialog):
    def __init__(self):
        super().__init__()
        self.root_project_dir = '..'
        self.setWindowFlags(Qt.FramelessWindowHint) # Убираем рамки окна, включая заголовок

        self.setObjectName("Dialog")
        self.resize(480, 300)
        self.setStyleSheet("background-color: rgb(236, 237, 240);")
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_info = DraggableLabel(self)
        self.label_info.setText('  Введите корректные данные!')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_info.sizePolicy().hasHeightForWidth())
        self.label_info.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_info.setFont(font)
        self.label_info.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_info.setObjectName("label_info")
        self.horizontalLayout_3.addWidget(self.label_info)
        self.pushButton_close = QtWidgets.QPushButton(self)
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
"    padding-bottom: 3px;                                 \n"
"    border: none;\n"
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
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(10, 0, 10, 5)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.groupBox_2 = QtWidgets.QGroupBox(self)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 190))
        self.groupBox_2.setMaximumSize(QtCore.QSize(7657, 16777215))
        self.groupBox_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 13px;")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setVerticalSpacing(10)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineEdit_port = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_port.setMaximumSize(QtCore.QSize(432, 423))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEdit_port.setFont(font)
        self.lineEdit_port.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
"    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
"    border-radius: 10px; /* Закругление углов */\n"
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
"    border: 2px solid rgb(1, 1, 1); /* Цвет рамки при фокусировке */\n"
"    background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */\n"
"}\n"
"\n"
"/* Состояние для отключенного текстового поля */\n"
"QLineEdit:disabled {\n"
"    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */\n"
"    color: rgb(170, 170, 170); /* Цвет текста для отключенного */\n"
"    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */\n"
"}")
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.gridLayout_2.addWidget(self.lineEdit_port, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("")
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_login = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_login.setMaximumSize(QtCore.QSize(432, 433324))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEdit_login.setFont(font)
        self.lineEdit_login.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
"    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
"    border-radius: 10px; /* Закругление углов */\n"
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
"    border: 2px solid rgb(1, 1, 1); /* Цвет рамки при фокусировке */\n"
"    background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */\n"
"}\n"
"\n"
"/* Состояние для отключенного текстового поля */\n"
"QLineEdit:disabled {\n"
"    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */\n"
"    color: rgb(170, 170, 170); /* Цвет текста для отключенного */\n"
"    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */\n"
"}")
        self.lineEdit_login.setObjectName("lineEdit_login")
        self.gridLayout_2.addWidget(self.lineEdit_login, 2, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_11.setFont(font)
        self.label_11.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_11.setStyleSheet("")
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 3, 0, 1, 1)
        self.lineEdit_password = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_password.setMaximumSize(QtCore.QSize(432, 342432))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEdit_password.setFont(font)
        self.lineEdit_password.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
"    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
"    border-radius: 10px; /* Закругление углов */\n"
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
"    border: 2px solid rgb(1, 1, 1); /* Цвет рамки при фокусировке */\n"
"    background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */\n"
"}\n"
"\n"
"/* Состояние для отключенного текстового поля */\n"
"QLineEdit:disabled {\n"
"    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */\n"
"    color: rgb(170, 170, 170); /* Цвет текста для отключенного */\n"
"    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */\n"
"}")
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.gridLayout_2.addWidget(self.lineEdit_password, 3, 1, 1, 1)
        self.lineEdit_ip = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_ip.setMaximumSize(QtCore.QSize(432423, 342432))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEdit_ip.setFont(font)
        self.lineEdit_ip.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
"    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
"    border-radius: 10px; /* Закругление углов */\n"
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
"    border: 2px solid rgb(1, 1, 1); /* Цвет рамки при фокусировке */\n"
"    background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */\n"
"}\n"
"\n"
"/* Состояние для отключенного текстового поля */\n"
"QLineEdit:disabled {\n"
"    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */\n"
"    color: rgb(170, 170, 170); /* Цвет текста для отключенного */\n"
"    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */\n"
"}")
        self.lineEdit_ip.setObjectName("lineEdit_ip")
        self.gridLayout_2.addWidget(self.lineEdit_ip, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("")
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.gridLayout.addLayout(self.verticalLayout_3, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 0, 10, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_enter = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_enter.sizePolicy().hasHeightForWidth())
        self.pushButton_enter.setSizePolicy(sizePolicy)
        self.pushButton_enter.setMinimumSize(QtCore.QSize(0, 46))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_enter.setFont(font)
        self.pushButton_enter.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    text-align: center;\n"
"    border-radius: 17px;\n"
"   }\n"
"QPushButton:hover {\n"
"    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
"}")
        self.pushButton_enter.setObjectName("pushButton_enter")
        self.horizontalLayout.addWidget(self.pushButton_enter)
        self.pushButton_not_use_proxy = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_not_use_proxy.sizePolicy().hasHeightForWidth())
        self.pushButton_not_use_proxy.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_not_use_proxy.setFont(font)
        self.pushButton_not_use_proxy.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    text-align: center;\n"
"    border-radius: 17px;\n"
"   }\n"
"QPushButton:hover {\n"
"    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
"}")
        self.pushButton_not_use_proxy.setObjectName("pushButton_not_use_proxy")
        self.horizontalLayout.addWidget(self.pushButton_not_use_proxy)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_info.setText(_translate("Dialog", "  Введите корректные данные!"))
        self.pushButton_close.setText(_translate("Dialog", "✕"))
        self.label.setText(_translate("Dialog", "SOCKS5:"))
        self.label_2.setText(_translate("Dialog", "IP:"))
        self.label_3.setText(_translate("Dialog", "Login:"))
        self.label_11.setText(_translate("Dialog", "Password:"))
        self.label_4.setText(_translate("Dialog", "Port:"))
        self.pushButton_enter.setText(_translate("Dialog", "Войти"))
        self.pushButton_not_use_proxy.setText(_translate("Dialog", "Закрыть"))