import os
import sys
from app.general.info import Dialog_info

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QTableWidgetItem
from PyQt5.QtWidgets import  QDialog, QLabel
class DraggableLabel(QLabel): # спец класс для Label

    def __init__(self, parent=None):
        super().__init__( parent)
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

class Dialog_error_open_accounts(QDialog):

    def __init__(self,accounts: list):
        super().__init__()
        self.accounts = accounts


        self.setObjectName("Dialog")
        self.resize(1200, 500)
        self.setMinimumSize(1200, 500)
        self.setMaximumSize(1200, 500)
        self.setStyleSheet("background-color: rgb(236, 237, 240);\n"
"border: 1px solid black;")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Убираем рамки окна, включая заголовок
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
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
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout.addWidget(self.pushButton_close)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("border-top: none;\n"
"border-bottom: none;\n"
"")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.scrollArea_2 = QtWidgets.QScrollArea(self)
        self.scrollArea_2.setStyleSheet("border: none;\n"
"\n"
"")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 760, 429))
        self.scrollAreaWidgetContents_2.setStyleSheet("/* Убираем вертикальную полосу прокрутки */\n"
"QScrollBar:vertical {\n"
"    width: 0px; /* Установка ширины на 0 пикселей */\n"
"    background: transparent; /* Делаем фон прозрачным */\n"
"    border: none; \n"
"\n"
"\n"
"}\n"
"\n"
"/* Убираем ползунок вертикального скроллбара */\n"
"QScrollBar::handle:vertical {\n"
"    background: none; /* Делаем ползунок невидимым */\n"
"}\n"
"\n"
"/* Убираем кнопки сверху и снизу */\n"
"QScrollBar::sub-line:vertical,\n"
"QScrollBar::add-line:vertical {\n"
"    background: none; /* Убираем кнопки */\n"
"}\n"
"\n"
"/* Убираем стрелки */\n"
"QScrollBar::up-arrow:vertical,\n"
"QScrollBar::down-arrow:vertical {\n"
"    background: none; /* Убираем стрелки */\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWidget_account = QtWidgets.QTableWidget(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_account.sizePolicy().hasHeightForWidth())
        self.tableWidget_account.setSizePolicy(sizePolicy)
        self.tableWidget_account.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8) # размер элементов внутри ячейки
        self.tableWidget_account.setFont(font)
        self.tableWidget_account.setStyleSheet("\n"
"QTableWidget {\n"
"background-color: rgb(255, 255, 255);\n"
"outline: 0;\n"
"border: 1px solid black;\n"
"border-top: none;\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    border: none;/*  Убираем границу у ячеек */\n"
"    padding: 5px; /* Устанавливаем отступы (по желанию) */\n"
"    border-bottom: 1px solid rgb(210, 210, 213); /* Добавляем нижнюю границу */\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    border: none; /* Убираем границу у заголовков */\n"
"     background-color: rgb(230, 230, 230); /* цвет фона заголовка  ячейки */\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    color: rgb(0,0,0);   "
"    background-color:  rgb(210, 210, 213); /* цвет фона для выделенной ячейки */\n"
"}")
        self.tableWidget_account.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget_account.setAlternatingRowColors(False)
        self.tableWidget_account.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_account.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_account.setShowGrid(False)
        self.tableWidget_account.setGridStyle(QtCore.Qt.NoPen)
        self.tableWidget_account.setRowCount(0)
        self.tableWidget_account.setObjectName("tableWidget_account")
        self.tableWidget_account.setColumnCount(5)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_account.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_account.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_account.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_account.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_account.setHorizontalHeaderItem(4, item)
        self.tableWidget_account.horizontalHeader().setVisible(True)
        self.tableWidget_account.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_account.horizontalHeader().setDefaultSectionSize(120)
        self.tableWidget_account.horizontalHeader().setHighlightSections(True)
        self.tableWidget_account.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget_account.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_account.verticalHeader().setVisible(False)
        self.tableWidget_account.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget_account.verticalHeader().setHighlightSections(True)
        self.tableWidget_account.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget_account.verticalHeader().setStretchLastSection(False)

        self.tableWidget_account.setColumnWidth(0, 30)
        self.tableWidget_account.setColumnWidth(1, 100)
        self.tableWidget_account.setColumnWidth(2, 150)
        self.tableWidget_account.setColumnWidth(3, 340)

        self.gridLayout_3.addWidget(self.tableWidget_account, 0, 0, 1, 1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.scrollArea_2)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.show_accounts()
        self.show_info()

        self.pushButton_close.clicked.connect(self.close)

    def show_accounts(self):
        self.tableWidget_account.setRowCount(0)
        counter = 0
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignCenter)  # Центрируем текст в ячейке
        for one_account in self.accounts:
            col = 1
            self.tableWidget_account.insertRow(counter)
            item = QTableWidgetItem(str(counter))
            item.setTextAlignment(Qt.AlignCenter)  # Центрируем текст в ячейке
            self.tableWidget_account.setItem(counter, 0, item)

            for info in one_account:
                item = QTableWidgetItem(str(info))
                item.setTextAlignment(Qt.AlignCenter)  # Центрируем текст в ячейке
                if col == self.tableWidget_account.columnCount() - 1:  # Если это последняя строка
                    item.setFlags(item.flags() | Qt.ItemIsEditable)  # Разрешаем редактирование
                else:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Запрещаем редактирование
                self.tableWidget_account.setItem(counter, col, item)
                col += 1
            counter += 1

    def show_info(self):
        error_info = Dialog_info('Внимание!','При попытке загрузки данных\nпроизошла ошибка входа в аккаунт','notification.mp3')  # Создаем экземпляр
        error_info.exec_()  # Открываем

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_title.setText(_translate("Dialog", "Аккаунты с ошибкой входа:"))
        self.pushButton_close.setText(_translate("Dialog", "✕"))
        self.label.setText(_translate("Dialog", "Отчёт:"))
        self.tableWidget_account.setSortingEnabled(False)
        item = self.tableWidget_account.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "#"))
        item = self.tableWidget_account.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "ID"))
        item = self.tableWidget_account.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Юзернейм"))
        item = self.tableWidget_account.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Ошибка"))
        item = self.tableWidget_account.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Решение"))


if __name__ == "__main__":
    accounts = [[432432,'user_name','У аккаунта установленна двухфакторная аутентификация','если аккаунт не заблокирован, то войдите в tg аккаунт и добавьте новую tdata в программу'],
                [432432,'user_name','Неизвестная ошибка входа','если аккаунт не заблокирован, то войдите в tg аккаунт и добавьте новую tdata в программу'],
                [872432,'user_name','Неизвестная ошибка входа','если аккаунт не заблокирован, то войдите в tg аккаунт и добавьте новую tdata в программу'],
                [432432,'user_name','Неизвестная ошибка входа','если аккаунт не заблокирован, то войдите в tg аккаунт и добавьте новую tdata в программу']]
    app = QtWidgets.QApplication(sys.argv)
    ui = Dialog_error_open_accounts(accounts)
    ui.show()
    ui.show_info()
    sys.exit(app.exec_())
