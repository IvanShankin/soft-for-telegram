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


class DialogListUsedChatsUi(QDialog):
    def __init__(self):
        super().__init__()
        self.root_project_dir = '..'
        self.setWindowFlags(Qt.FramelessWindowHint)  # Убираем рамки окна, включая заголовок

        self.setObjectName("Dialog")
        self.resize(465, 526)
        self.setStyleSheet("background-color: rgb(236, 237, 240);\n"
"border: 1px solid black;")
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_title = DraggableLabel(self)
        self.label_title.setText('Список')
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
        self.label_title_2 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_title_2.sizePolicy().hasHeightForWidth())
        self.label_title_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_title_2.setFont(font)
        self.label_title_2.setStyleSheet("padding-left: 5px;\n"
"border-top: none;\n"
"border-bottom: none;\n"
"")
        self.label_title_2.setObjectName("label_title_2")
        self.gridLayout.addWidget(self.label_title_2, 1, 0, 1, 1)
        self.scrollArea_7 = QtWidgets.QScrollArea(self)
        self.scrollArea_7.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea_7.setStyleSheet("border: 0; "
                                        "margin: 1px;")
        self.scrollArea_7.setWidgetResizable(True)
        self.scrollArea_7.setObjectName("scrollArea_7")
        self.scrollAreaWidgetContents_8 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_8.setGeometry(QtCore.QRect(0, 0, 465, 460))
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
        self.gridLayout_19 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_8)
        self.gridLayout_19.setContentsMargins(20, -1, 20, 10)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.gridLayout_20 = QtWidgets.QGridLayout()
        self.gridLayout_20.setContentsMargins(0, -1, -1, -1)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.textEdit_user_name_list = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_8)
        self.textEdit_user_name_list.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit_user_name_list.setFont(font)
        self.textEdit_user_name_list.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"padding-top: 15px; /* Отступ только слева */   \n"
" padding-bottom: 15px; /* Отступ только снизу */\n"
"")
        self.textEdit_user_name_list.setReadOnly(False)
        self.textEdit_user_name_list.setObjectName("textEdit_user_name_list")
        self.textEdit_user_name_list.setReadOnly(True)
        self.gridLayout_20.addWidget(self.textEdit_user_name_list, 0, 0, 1, 1)
        self.gridLayout_19.addLayout(self.gridLayout_20, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents_8)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.pushButton_close_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_close_2.sizePolicy().hasHeightForWidth())
        self.pushButton_close_2.setSizePolicy(sizePolicy)
        self.pushButton_close_2.setMinimumSize(QtCore.QSize(111, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_close_2.setFont(font)
        self.pushButton_close_2.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    text-align: center;\n"
"    border-radius: 10px;\n"
"border: none;\n"
"    padding-left:10px;\n"
"    padding-right: 10px;\n"
"   }\n"
"QPushButton:hover {\n"
"    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
"}")
        self.pushButton_close_2.setObjectName("pushButton_close_2")
        self.horizontalLayout_2.addWidget(self.pushButton_close_2)
        self.pushButton_upload = QtWidgets.QPushButton(self.scrollAreaWidgetContents_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_upload.sizePolicy().hasHeightForWidth())
        self.pushButton_upload.setSizePolicy(sizePolicy)
        self.pushButton_upload.setMinimumSize(QtCore.QSize(111, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_upload.setFont(font)
        self.pushButton_upload.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    text-align: center;\n"
"    border-radius: 10px;\n"
"    border: none;\n"
"    padding-left:10px;\n"
"    padding-right: 10px;\n"
"   }\n"
"QPushButton:hover {\n"
"    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
"}")
        self.pushButton_upload.setObjectName("pushButton_upload")
        self.horizontalLayout_2.addWidget(self.pushButton_upload)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_8)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.gridLayout_19.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.scrollArea_7.setWidget(self.scrollAreaWidgetContents_8)
        self.gridLayout.addWidget(self.scrollArea_7, 2, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_title.setText(_translate("Dialog", "Список"))
        self.pushButton_close.setText(_translate("Dialog", "✕"))
        self.label_title_2.setText(_translate("Dialog", "Список чатов по которым производили рассылку"))
        self.textEdit_user_name_list.setHtml(_translate("Dialog", ""))
        self.pushButton_close_2.setText(_translate("Dialog", "Закрыть"))
        self.pushButton_upload.setText(_translate("Dialog", "Выгрузить"))