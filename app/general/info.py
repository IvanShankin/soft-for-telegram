import sys
import os
import pygame

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


class DraggableLabel(QLabel): # спец класс для Label
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.oldPos = None  # Переменная для хранения позиции мыши

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  # Проверка на левую кнопку мыши
            self.oldPos = event.globalPos() - self.parent().frameGeometry().topLeft()  # Запоминаем позицию мыши
            event.accept()  # Принять событие

    def mouseMoveEvent(self, event):
        if self.oldPos is not None and event.buttons() == Qt.LeftButton:  # Проверка, что кнопка мыши удерживается
            self.parent().move(event.globalPos() - self.oldPos)  # Перемещения окна
            event.accept()  # Принять событие

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:  # Проверка на отпускание кнопки мыши
            self.oldPos = None  # Обнуляем позицию
            event.accept()  # Принять событие

class Dialog_info(QDialog):
    root_project_dir = '..'

    text = ''
    file = ''
    title = ''
    def __init__(self,title: str,text: str,file_sound: str = None, button_text: str = 'ОК'):
        super().__init__()

        self.title = title
        self.text = text
        self.file = file_sound
        self.button_text = button_text

        self.setWindowFlags(Qt.FramelessWindowHint)# Убираем рамки окна, включая заголовок
        self.setStyleSheet("border: 1px solid black;")  # Обводка по всему периметру окна

        self.setObjectName("MainWindow")
        self.resize(213, 93)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_titel = DraggableLabel(self.title,self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_titel.sizePolicy().hasHeightForWidth())
        self.label_titel.setSizePolicy(sizePolicy)
        self.label_titel.setStyleSheet("background-color: rgb(255, 255, 255);"
                                       "    padding-left: 5px;"
                                       "    border-right: none;"
                                       "    border-bottom: none;"
                                       )
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_titel.setFont(font)
        self.label_titel.setObjectName("label_titel")
        self.horizontalLayout_3.addWidget(self.label_titel)
        self.pushButton_close = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    color: rgb(1, 1, 1);\n"
"    text-align: center;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 3px;\n"                                            
"    border-left: none;"
"    border-bottom: none;"                                            
"   }\n"
"QPushButton:hover {\n"
"    background-color: rgb(255, 1, 1); /* Цвет фона при наведении (немного серый) */\n"
"    color: rgb(255, 255, 255);"
"}\n"
"\n"
"QPushButton:pressed {\n"
"     background: rgb(255, 100, 100); /* Цвет фона при нажатии (еще серее) */\n"
        "color: rgb(255, 255, 255);\n"
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
        self.label_info.setStyleSheet("padding-bottom: 7px")
        self.label_info.setObjectName("label_info")
        self.label_info.setStyleSheet("    border-top: none;\n"
                                            "    border-bottom: none;\n"
                                            "    padding-left: 5px;\n"
                                            "    padding-top: 3px;\n"
                                            "    padding-bottom: 3px;\n"
                                            "    padding-right: 5px;\n")
        self.verticalLayout.addWidget(self.label_info)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_5.setStyleSheet("    border-top: none;  border-bottom: none;    border-right: none;")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.pushButton_ok = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_ok.setFont(font)
        self.pushButton_ok.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    text-align: center;\n"
"    border-radius: 9px;\n"
"    padding: 1px;\n"
"    margin-bottom: 5px;\n"
"    border: none;"
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
        self.label_6 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setStyleSheet("")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.label_6.setStyleSheet("    border-top: none; border-bottom: none;  border-left: none;")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # события
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_ok.clicked.connect(self.close)
        # события

        self.label_titel.setText(self.title)
        self.label_info.setText(self.text)

        if self.file:
            try:
                sound_file = (self.root_project_dir + f"/resources/sounds/{self.file}")
                pygame.mixer.init()
                pygame.mixer.music.load(sound_file)  # Загрузка звукового файла
                pygame.mixer.music.play()  # Проигрывание звука
            except Exception:
                pass



    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_titel.setText(_translate("Dialog", " Внимание!"))
        self.pushButton_close.setText(_translate("Dialog", "✕"))
        self.label_info.setText(_translate("Dialog", "error_info"))
        self.pushButton_ok.setText(_translate("Dialog", self.button_text))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Dialog_info('Внимание!','test','notification.mp3')
    ui.show()
    sys.exit(app.exec_())
