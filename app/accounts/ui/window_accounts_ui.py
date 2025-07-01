import os
from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtCore import QSize

class WindowAccountsUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.root_project_dir = '..'
        self.setObjectName("MainWindow")
        self.setWindowModality(QtCore.Qt.NonModal)
        self.resize(1500, 850)
        self.setMinimumSize(QtCore.QSize(1200, 750))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.setFont(font)
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.setStyleSheet("background-color: rgb(236, 237, 240);")
        self.setIconSize(QtCore.QSize(24, 24))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, -1, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(25, 10, 20, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_5.addWidget(self.label_13)
        self.pushButton_info = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_info.setStyleSheet("border: none;\n")
        self.pushButton_info.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_info.setIcon(icon)
        self.pushButton_info.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_info.setObjectName("pushButton_info")
        self.horizontalLayout_5.addWidget(self.pushButton_info)
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setText("")
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_5.addWidget(self.label_15)

        self.groupBox_progress = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_progress.sizePolicy().hasHeightForWidth())
        self.groupBox_progress.setSizePolicy(sizePolicy)
        self.groupBox_progress.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 13px;\n"
                                      "")
        self.groupBox_progress.setTitle("")
        self.groupBox_progress.setObjectName("groupBox_progress")
        self.groupBox_progress.setMinimumSize(0,0)
        self.groupBox_progress.setMaximumSize(20000, 40)
        self.horizontalLayout_5.addWidget(self.groupBox_progress)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_progress)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(10, 0, 10, 0)  # Отступы в 10px со всех сторон

        self.label_gif_load = QtWidgets.QLabel(self.groupBox_progress)
        self.label_gif_load.setScaledContents(True)# Установка свойства для масштабирования содержимого
        self.label_gif_load.setMaximumSize(30,30)
        movie = QtGui.QMovie(self.root_project_dir + '/resources/icon/load.gif')# Загрузка GIF с использованием QMovie
        self.label_gif_load.setMovie(movie)
        movie.start() # Запуск анимации
        self.horizontalLayout_6.addWidget(self.label_gif_load)

        self.groupBox_progress.hide()

        self.button_info_open_account = QtWidgets.QPushButton(self.groupBox_progress)
        self.button_info_open_account.setText('')
        icon0 = QtGui.QIcon()
        icon0.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/success.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_info_open_account.setIcon(icon0)
        size = QSize(20,20)
        self.button_info_open_account.setIconSize(size)
        self.horizontalLayout_6.addWidget(self.button_info_open_account)
        self.button_info_open_account.hide()

        self.label_result_open_account = QtWidgets.QLabel(self.groupBox_progress)
        self.label_result_open_account.setText('')
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_result_open_account.setFont(font)
        self.horizontalLayout_6.addWidget(self.label_result_open_account)
        self.label_result_open_account.hide()

        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_2.setStyleSheet("border: none;\n"
                                        "")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 1205, 481))
        self.scrollAreaWidgetContents_2.setStyleSheet("/* Убираем вертикальную полосу прокрутки */\n"
                                                      "QScrollBar:vertical {\n"
                                                      "    width: 0px; /* Установка ширины на 1 пикселей */\n"
                                                      "    background: transparent; /* Делаем фон прозрачным */\n"
                                                      "    border: none; /* Убираем рамку */\n"
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
                                                      "/* СТИЛЬ ГОРИЗОНТАЛЬНОГО СКРОЛЛБАРА */\n"
                                                      "QScrollBar:horizontal {\n"
                                                      "    border-radius: 8px;\n"
                                                      "    background: rgb(255, 255, 255); /* Стандартный цвет фона */\n"
                                                      "    height: 14px;\n"
                                                      "    margin: 1 15px 1 15px; /* Отступы по горизонтали */\n"
                                                      "}\n"
                                                      "\n"
                                                      "/* HANDLE BAR ГОРИЗОНТАЛЬНОГО СКРОЛЛБАРА */\n"
                                                      "QScrollBar::handle:horizontal {\n"
                                                      "    background-color: rgb(210, 210, 213); /* Стандартный цвет фона для ползунка */\n"
                                                      "    min-width: 30px; /* Минимальная ширина ползунка */\n"
                                                      "    border-radius: 7px;\n"
                                                      "    transition: background-color 1.2s ease, min-width 1.2s ease; /* Плавный переход цвета и ширины */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QScrollBar::handle:horizontal:hover {\n"
                                                      "    background-color: rgb(180, 180, 184); /* Цвет ползунка при наведении */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QScrollBar::handle:horizontal:pressed {\n"
                                                      "    background-color: rgb(150, 150, 153); /* Цвет ползунка при нажатии */\n"
                                                      "}\n"
                                                      "\n"
                                                      "/* КНОПКА СЛЕВА - ГОРИЗОНТАЛЬНЫЙ СКРОЛЛБАР */\n"
                                                      "QScrollBar::sub-line:horizontal {\n"
                                                      "    border: none;\n"
                                                      "    background-color: rgb(210, 210, 213); /* Стандартный цвет фона для кнопки влево */\n"
                                                      "    width: 15px;\n"
                                                      "    border-top-left-radius: 7px;\n"
                                                      "    border-bottom-left-radius: 7px;\n"
                                                      "    subcontrol-position: left;\n"
                                                      "    subcontrol-origin: margin;\n"
                                                      "    transition: background-color 1.2s ease; /* Плавный переход цвета */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QScrollBar::sub-line:horizontal:hover {\n"
                                                      "    background-color: rgb(180, 180, 184); /* Цвет кнопки влево при наведении */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QScrollBar::sub-line:horizontal:pressed {\n"
                                                      "    background-color: rgb(150, 150, 153); /* Цвет кнопки влево при нажатии */\n"
                                                      "}\n"
                                                      "\n"
                                                      "/* КНОПКА СПРАВА - ГОРИЗОНТАЛЬНЫЙ СКРОЛЛБАР */\n"
                                                      "QScrollBar::add-line:horizontal {\n"
                                                      "    border: none;\n"
                                                      "    background-color: rgb(210, 210, 213); /* Стандартный цвет фона для кнопки вправо */\n"
                                                      "    width: 15px;\n"
                                                      "    border-top-right-radius: 7px;\n"
                                                      "    border-bottom-right-radius: 7px;\n"
                                                      "    subcontrol-position: right;\n"
                                                      "    subcontrol-origin: margin;\n"
                                                      "    transition: background-color 1.2s ease; /* Плавный переход цвета */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QScrollBar::add-line:horizontal:hover {\n"
                                                      "    background-color: rgb(180, 180, 184); /* Цвет кнопки вправо при наведении */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QScrollBar::add-line:horizontal:pressed {\n"
                                                      "    background-color: rgb(150, 150, 153); /* Цвет кнопки вправо при нажатии */\n"
                                                      "}\n"
                                                      "\n"
                                                      "/* УБРАТЬ СТРЕЛКИ */\n"
                                                      "QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {\n"
                                                      "    background: none; /* Убираем стрелки */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
                                                      "    background: none; /* Убираем фоновую страницу */\n"
                                                      "}")
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWidget_account = QtWidgets.QTableWidget(self.scrollAreaWidgetContents_2)
        self.tableWidget_account.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tableWidget_account.setFont(font)
        self.tableWidget_account.setStyleSheet("\n"
                                               "QTableWidget {\n"
                                               "background-color: rgb(255, 255, 255);\n"
                                               "outline: 1;\n"
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
                                               "	color: rgb(1,1,1);\n"
                                               "    background-color:  rgb(210, 210, 213); /* цвет фона для выделенной ячейки */\n"
                                               "}")
        self.tableWidget_account.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget_account.setAlternatingRowColors(False)
        self.tableWidget_account.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableWidget_account.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_account.setShowGrid(False)
        self.tableWidget_account.setGridStyle(QtCore.Qt.NoPen)
        self.tableWidget_account.setRowCount(0)
        self.tableWidget_account.setObjectName("tableWidget_account")
        self.tableWidget_account.setColumnCount(9)

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_account.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QtGui.QColor(255, 255, 255))
        self.tableWidget_account.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_account.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_account.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setTextAlignment(0)
        self.tableWidget_account.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_account.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_account.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)

        self.tableWidget_account.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)

        self.tableWidget_account.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)



        self.tableWidget_account.setHorizontalHeaderItem(7, item)
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
        self.tableWidget_account.setIconSize(QSize(25,15))

        self.tableWidget_account.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed) # запрет на изменения ширины колонки

        # задаём ширину колонок
        self.tableWidget_account.setColumnWidth(0, 60)
        self.tableWidget_account.setColumnWidth(1, 110)
        self.tableWidget_account.setColumnWidth(2, 170)
        self.tableWidget_account.setColumnWidth(3, 150)
        self.tableWidget_account.setColumnWidth(4, 60)
        self.tableWidget_account.setColumnWidth(5, 150)
        self.tableWidget_account.setColumnWidth(6, 100)
        self.tableWidget_account.setColumnWidth(7, 160)

        self.gridLayout_3.addWidget(self.tableWidget_account, 0, 0, 1, 1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout.addWidget(self.scrollArea_2, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "border-radius: 8px;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_account = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_account.setFont(font)
        self.label_account.setStyleSheet("")
        self.label_account.setObjectName("label_account")
        self.horizontalLayout_3.addWidget(self.label_account)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)

        self.pushButton_move_active = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_move_active.sizePolicy().hasHeightForWidth())
        self.pushButton_move_active.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_move_active.setFont(font)
        self.pushButton_move_active.setStyleSheet("QPushButton {\n"
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
        self.pushButton_move_active.setObjectName("pushButton_move_active")
        self.horizontalLayout_3.addWidget(self.pushButton_move_active)

        self.pushButton_move_archive = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_move_archive.sizePolicy().hasHeightForWidth())
        self.pushButton_move_archive.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_move_archive.setFont(font)
        self.pushButton_move_archive.setStyleSheet("QPushButton {\n"
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
        self.pushButton_move_archive.setObjectName("pushButton_move_archive")
        self.horizontalLayout_3.addWidget(self.pushButton_move_archive)

        self.pushButton_move_main_account = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_move_main_account.sizePolicy().hasHeightForWidth())

        self.pushButton_move_main_account.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_move_main_account.setFont(font)
        self.pushButton_move_main_account.setStyleSheet("QPushButton {\n"
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
        self.pushButton_move_main_account.setObjectName("pushButton_move_main_account")
        self.horizontalLayout_3.addWidget(self.pushButton_move_main_account)

        self.pushButton_update = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_update.setSizePolicy(sizePolicy)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_update.sizePolicy().hasHeightForWidth())
        self.pushButton_update.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_update.setFont(font)
        self.pushButton_update.setStyleSheet("QPushButton {\n"
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
        self.pushButton_update.setObjectName("pushButton_update")
        self.pushButton_update.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/update.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_update.setIcon(icon1)
        self.pushButton_update.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_update.setCheckable(False)
        self.pushButton_update.setMinimumSize(QtCore.QSize(42, 42))
        self.horizontalLayout_3.addWidget(self.pushButton_update)

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_7 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_7.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 8px;")
        self.groupBox_7.setTitle("")
        self.groupBox_7.setObjectName("groupBox_7")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_open_active_accounts = QtWidgets.QPushButton(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_open_active_accounts.sizePolicy().hasHeightForWidth())
        self.pushButton_open_active_accounts.setSizePolicy(sizePolicy)
        self.pushButton_open_active_accounts.setMinimumSize(QtCore.QSize(0, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_open_active_accounts.setFont(font)
        self.pushButton_open_active_accounts.setStyleSheet("QPushButton {\n"
                                                                    "  background: rgb(150, 150, 153);\n"
                                                                    "text-align: center;\n"
                                                                    "border-radius: 10px;\n"
                                                                    "   }")
        self.pushButton_open_active_accounts.setObjectName("pushButton_open_active_accounts")
        self.horizontalLayout_4.addWidget(self.pushButton_open_active_accounts)
        self.pushButton_open_arxive_accounts = QtWidgets.QPushButton(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_open_arxive_accounts.sizePolicy().hasHeightForWidth())
        self.pushButton_open_arxive_accounts.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_open_arxive_accounts.setFont(font)
        self.pushButton_open_arxive_accounts.setStyleSheet("QPushButton {\n"
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
        self.pushButton_open_arxive_accounts.setObjectName("pushButton_open_arxive_accounts")
        self.horizontalLayout_4.addWidget(self.pushButton_open_arxive_accounts)
        self.pushButton_open_main_account = QtWidgets.QPushButton(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_open_main_account.sizePolicy().hasHeightForWidth())
        self.pushButton_open_main_account.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_open_main_account.setFont(font)
        self.pushButton_open_main_account.setStyleSheet("QPushButton {\n"
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
        self.pushButton_open_main_account.setObjectName("pushButton_open_main_account")
        self.horizontalLayout_4.addWidget(self.pushButton_open_main_account)
        self.pushButton_open_temporary_ban_accounts = QtWidgets.QPushButton(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_open_temporary_ban_accounts.sizePolicy().hasHeightForWidth())
        self.pushButton_open_temporary_ban_accounts.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_open_temporary_ban_accounts.setFont(font)
        self.pushButton_open_temporary_ban_accounts.setStyleSheet("QPushButton {\n"
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
        self.pushButton_open_temporary_ban_accounts.setObjectName("pushButton_open_temporary_ban_accounts")
        self.horizontalLayout_4.addWidget(self.pushButton_open_temporary_ban_accounts)
        self.pushButton_open_login_error = QtWidgets.QPushButton(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_open_login_error.sizePolicy().hasHeightForWidth())
        self.pushButton_open_login_error.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_open_login_error.setFont(font)
        self.pushButton_open_login_error.setStyleSheet("QPushButton {\n"
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
        self.pushButton_open_login_error.setObjectName("pushButton_open_login_error")
        self.horizontalLayout_4.addWidget(self.pushButton_open_login_error)
        self.gridLayout.addWidget(self.groupBox_7, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(20, 0, 20, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_add = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_add.sizePolicy().hasHeightForWidth())
        self.pushButton_add.setSizePolicy(sizePolicy)
        self.pushButton_add.setMinimumSize(QtCore.QSize(185, 55))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_add.setFont(font)
        self.pushButton_add.setStyleSheet("\n"
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
        self.pushButton_add.setIconSize(QtCore.QSize(120, 120))
        self.pushButton_add.setObjectName("pushButton_add")
        self.horizontalLayout.addWidget(self.pushButton_add)
        self.pushButton_show_data_account = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_show_data_account.sizePolicy().hasHeightForWidth())
        self.pushButton_show_data_account.setSizePolicy(sizePolicy)
        self.pushButton_show_data_account.setMinimumSize(QtCore.QSize(185, 55))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_show_data_account.setFont(font)
        self.pushButton_show_data_account.setStyleSheet("\n"
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
        self.pushButton_show_data_account.setIconSize(QtCore.QSize(120, 120))
        self.pushButton_show_data_account.setObjectName("pushButton_show_data_account")
        self.horizontalLayout.addWidget(self.pushButton_show_data_account)
        self.pushButton_enter = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_enter.sizePolicy().hasHeightForWidth())
        self.pushButton_enter.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
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
        self.pushButton_upload_tdata = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_upload_tdata.sizePolicy().hasHeightForWidth())
        self.pushButton_upload_tdata.setSizePolicy(sizePolicy)
        self.pushButton_upload_tdata.setMinimumSize(QtCore.QSize(185, 55))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_upload_tdata.setFont(font)
        self.pushButton_upload_tdata.setStyleSheet("\n"
                                                   "QPushButton {\n"
                                                   "    background-color: rgb(255, 255, 255);\n"
                                                   "    text-align: center;\n"
                                                   "    border-radius: 17px;\n"
                                                   "    padding-left: 5px;\n"
                                                   "    padding-right: 5px;\n"
                                                   "   }\n"
                                                   "QPushButton:hover {\n"
                                                   "    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
                                                   "}\n"
                                                   "\n"
                                                   "QPushButton:pressed {\n"
                                                   "     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
                                                   "}")
        self.pushButton_upload_tdata.setObjectName("pushButton_upload_tdata")
        self.horizontalLayout.addWidget(self.pushButton_upload_tdata)
        self.pushButton_delete = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_delete.sizePolicy().hasHeightForWidth())
        self.pushButton_delete.setSizePolicy(sizePolicy)
        self.pushButton_delete.setMinimumSize(QtCore.QSize(185, 55))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_delete.setFont(font)
        self.pushButton_delete.setStyleSheet("\n"
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
        self.pushButton_delete.setIconSize(QtCore.QSize(120, 120))
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.horizontalLayout.addWidget(self.pushButton_delete)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(20, 0, 20, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 13px;")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_count_all_account = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_count_all_account.sizePolicy().hasHeightForWidth())
        self.label_count_all_account.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_count_all_account.setFont(font)
        self.label_count_all_account.setStyleSheet("")
        self.label_count_all_account.setObjectName("label_count_all_account")
        self.verticalLayout_2.addWidget(self.label_count_all_account)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 13px;")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_count_active_account = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_count_active_account.sizePolicy().hasHeightForWidth())
        self.label_count_active_account.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_count_active_account.setFont(font)
        self.label_count_active_account.setStyleSheet("")
        self.label_count_active_account.setObjectName("label_count_active_account")
        self.verticalLayout_3.addWidget(self.label_count_active_account)
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.horizontalLayout_2.addWidget(self.groupBox_3)

        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 13px;")
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_count_archive_account = QtWidgets.QLabel(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_count_archive_account.sizePolicy().hasHeightForWidth())
        self.label_count_archive_account.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_count_archive_account.setFont(font)
        self.label_count_archive_account.setStyleSheet("")
        self.label_count_archive_account.setObjectName("label_count_archive_account")
        self.verticalLayout_4.addWidget(self.label_count_archive_account)
        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.horizontalLayout_2.addWidget(self.groupBox_4)



        self.groupBox_8 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_8.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 13px;")
        self.groupBox_8.setTitle("")
        self.groupBox_8.setObjectName("groupBox_8")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_8)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_count_main_account = QtWidgets.QLabel(self.groupBox_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_count_main_account.sizePolicy().hasHeightForWidth())
        self.label_count_main_account.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_count_main_account.setFont(font)
        self.label_count_main_account.setStyleSheet("")
        self.label_count_main_account.setObjectName("label_count_main_account")
        self.verticalLayout_8.addWidget(self.label_count_main_account)
        self.label_10 = QtWidgets.QLabel(self.groupBox_8)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("")
        self.label_10.setObjectName("label_10")
        self.verticalLayout_8.addWidget(self.label_10)
        self.horizontalLayout_2.addWidget(self.groupBox_8)



        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 13px;\n"
                                      "")
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_count_temporary_banned_account = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_count_temporary_banned_account.sizePolicy().hasHeightForWidth())
        self.label_count_temporary_banned_account.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_count_temporary_banned_account.setFont(font)
        self.label_count_temporary_banned_account.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_count_temporary_banned_account.setStyleSheet("")
        self.label_count_temporary_banned_account.setObjectName("label_count_temporary_banned_account")
        self.verticalLayout_5.addWidget(self.label_count_temporary_banned_account)
        self.label_6 = QtWidgets.QLabel(self.groupBox_5)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("")
        self.label_6.setObjectName("label_6")
        self.verticalLayout_5.addWidget(self.label_6)
        self.horizontalLayout_2.addWidget(self.groupBox_5)
        self.groupBox_6 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_6.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 13px;\n"
                                      "")
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_count_login_error = QtWidgets.QLabel(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_count_login_error.sizePolicy().hasHeightForWidth())
        self.label_count_login_error.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_count_login_error.setFont(font)
        self.label_count_login_error.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_count_login_error.setStyleSheet("border: 0px ;\n"
                                                   "border-radius: 1;\n"
                                                   "")
        self.label_count_login_error.setObjectName("label_count_login_error")
        self.verticalLayout_6.addWidget(self.label_count_login_error)
        self.label_7 = QtWidgets.QLabel(self.groupBox_6)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("border: 0px ;\n"
                                   "border-radius: 1;\n"
                                   "")
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7)
        self.horizontalLayout_2.addWidget(self.groupBox_6)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(270, 0))
        self.scrollArea.setMaximumSize(QtCore.QSize(270, 16777215))
        self.scrollArea.setStyleSheet("background-color: rgb(14, 22, 33);\n"
                                      "border: none;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 238, 848))
        self.scrollAreaWidgetContents.setStyleSheet("")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_account_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_account_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_account_2.sizePolicy().hasHeightForWidth())
        self.pushButton_account_2.setSizePolicy(sizePolicy)
        self.pushButton_account_2.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_account_2.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_account_2.setFont(font)
        self.pushButton_account_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                                "border: 1;\n"
                                                "text-align: center;\n"
                                                "padding: 10px;")
        self.pushButton_account_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/logo.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_account_2.setIcon(icon1)
        self.pushButton_account_2.setIconSize(QtCore.QSize(300, 60))
        self.pushButton_account_2.setCheckable(False)
        self.pushButton_account_2.setObjectName("pushButton_account_2")
        self.verticalLayout.addWidget(self.pushButton_account_2)
        self.label_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(0, 0))
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.pushButton_account = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_account.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_account.sizePolicy().hasHeightForWidth())
        self.pushButton_account.setSizePolicy(sizePolicy)
        self.pushButton_account.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_account.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_account.setFont(font)
        self.pushButton_account.setStyleSheet("QPushButton {\n"
                                              "color: rgb(255, 255, 255);\n"
                                              "border: 1;\n"
                                              "text-align: left;\n"
                                              "padding: 10px;\n"
                                              "   }\n"
                                              "   QPushButton:hover {\n"
                                              "       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
                                              "   }\n"
                                              "\n"
                                              "QPushButton:pressed {\n"
                                              "                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
                                              "            }")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/account.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_account.setIcon(icon2)
        self.pushButton_account.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_account.setCheckable(False)
        self.pushButton_account.setObjectName("pushButton_account")
        self.verticalLayout.addWidget(self.pushButton_account)
        self.pushButton_mailing = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_mailing.sizePolicy().hasHeightForWidth())
        self.pushButton_mailing.setSizePolicy(sizePolicy)
        self.pushButton_mailing.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_mailing.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_mailing.setFont(font)
        self.pushButton_mailing.setStyleSheet("QPushButton {\n"
                                              "color: rgb(143, 145, 165);\n"
                                              "border: 1;\n"
                                              "text-align: left;\n"
                                              "padding: 10px;\n"
                                              "   }\n"
                                              "   QPushButton:hover {\n"
                                              "       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
                                              "   }\n"
                                              "\n"
                                              "QPushButton:pressed {\n"
                                              "                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
                                              "            }")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/mailing.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_mailing.setIcon(icon3)
        self.pushButton_mailing.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_mailing.setObjectName("pushButton_mailing")
        self.verticalLayout.addWidget(self.pushButton_mailing)
        self.pushButton_mailing_chat = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_mailing_chat.setFont(font)
        self.pushButton_mailing_chat.setStyleSheet("QPushButton {\n"
                                                   "color: rgb(143, 145, 165);\n"
                                                   "border: 1;\n"
                                                   "text-align: left;\n"
                                                   "padding: 10px;\n"
                                                   "   }\n"
                                                   "   QPushButton:hover {\n"
                                                   "       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
                                                   "   }\n"
                                                   "\n"
                                                   "QPushButton:pressed {\n"
                                                   "                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
                                                   "            }")
        self.pushButton_mailing_chat.setIcon(icon3)
        self.pushButton_mailing_chat.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_mailing_chat.setObjectName("pushButton_mailing_chat")
        self.verticalLayout.addWidget(self.pushButton_mailing_chat)
        self.pushButton_invite = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_invite.sizePolicy().hasHeightForWidth())
        self.pushButton_invite.setSizePolicy(sizePolicy)
        self.pushButton_invite.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_invite.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_invite.setFont(font)
        self.pushButton_invite.setStyleSheet("QPushButton {\n"
                                             "color: rgb(143, 145, 165);\n"
                                             "border: 1;\n"
                                             "text-align: left;\n"
                                             "padding: 10px;\n"
                                             "   }\n"
                                             "   QPushButton:hover {\n"
                                             "       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
                                             "   }\n"
                                             "\n"
                                             "QPushButton:pressed {\n"
                                             "                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
                                             "            }")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/invaite.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_invite.setIcon(icon4)
        self.pushButton_invite.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_invite.setObjectName("pushButton_invite")
        self.verticalLayout.addWidget(self.pushButton_invite)
        self.pushButton_parser = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_parser.sizePolicy().hasHeightForWidth())
        self.pushButton_parser.setSizePolicy(sizePolicy)
        self.pushButton_parser.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_parser.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_parser.setFont(font)
        self.pushButton_parser.setStyleSheet("QPushButton {\n"
                                             "color: rgb(143, 145, 165);\n"
                                             "border: 1;\n"
                                             "text-align: left;\n"
                                             "padding: 10px;\n"
                                             "   }\n"
                                             "   QPushButton:hover {\n"
                                             "       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
                                             "   }\n"
                                             "\n"
                                             "QPushButton:pressed {\n"
                                             "                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
                                             "            }")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/parser.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_parser.setIcon(icon5)
        self.pushButton_parser.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_parser.setObjectName("pushButton_parser")
        self.verticalLayout.addWidget(self.pushButton_parser)
        self.pushButton_proxy = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_proxy.sizePolicy().hasHeightForWidth())
        self.pushButton_proxy.setSizePolicy(sizePolicy)
        self.pushButton_proxy.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_proxy.setMaximumSize(QtCore.QSize(16777215, 57))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_proxy.setFont(font)
        self.pushButton_proxy.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_proxy.setStyleSheet("QPushButton {\n"
                                            "color: rgb(143, 145, 165);\n"
                                            "border: 1;\n"
                                            "text-align: left;\n"
                                            "padding: 10px;\n"
                                            "   }\n"
                                            "   QPushButton:hover {\n"
                                            "       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
                                            "   }\n"
                                            "\n"
                                            "QPushButton:pressed {\n"
                                            "                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
                                            "            }")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/proxy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_proxy.setIcon(icon6)
        self.pushButton_proxy.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_proxy.setObjectName("pushButton_proxy")
        self.verticalLayout.addWidget(self.pushButton_proxy)
        self.pushButton_bomber = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_bomber.setMinimumSize(QtCore.QSize(185, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_bomber.setFont(font)
        self.pushButton_bomber.setStyleSheet("QPushButton {\n"
                                             "color: rgb(143, 145, 165);\n"
                                             "border: 1;\n"
                                             "text-align: left;\n"
                                             "padding: 10px;\n"
                                             "   }\n"
                                             "   QPushButton:hover {\n"
                                             "       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
                                             "   }\n"
                                             "\n"
                                             "QPushButton:pressed {\n"
                                             "                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
                                             "            }")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/bomber.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_bomber.setIcon(icon7)
        self.pushButton_bomber.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_bomber.setObjectName("pushButton_bomber")
        self.verticalLayout.addWidget(self.pushButton_bomber)

        self.pushButton_create_channel = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_create_channel.setFont(font)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/channel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_create_channel.setIcon(icon8)
        self.pushButton_create_channel.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_create_channel.setStyleSheet("QPushButton {\n"
                                                     "color: rgb(143, 145, 165);\n"
                                                     "border: 0;\n"
                                                     "text-align: left;\n"
                                                     "padding: 10px;\n"
                                                     "   }\n"
                                                     "   QPushButton:hover {\n"
                                                     "       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
                                                     "   }\n"
                                                     "\n"
                                                     "QPushButton:pressed {\n"
                                                     "                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
                                                     "            }")
        self.pushButton_create_channel.setObjectName("pushButton_create_channel")
<<<<<<< HEAD
        self.verticalLayout.addWidget(self.pushButton_create_channel)

        self.pushButton_create_bot = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_create_bot.setFont(font)
        self.pushButton_create_bot.setStyleSheet("QPushButton {\n"
                                      "color: rgb(143, 145, 165);"
                                      "border: 0;\n"
                                      "text-align: left;\n"
                                      "padding: 10px;\n"
                                      "   }\n"
                                      "   QPushButton:hover {\n"
                                      "       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
                                      "   }\n"
                                      "\n"
                                      "QPushButton:pressed {\n"
                                      "                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
                                      "            }")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/creating_bots.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_create_bot.setIcon(icon7)
        self.pushButton_create_bot.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_create_bot.setObjectName("pushButton_create_bot")
        self.verticalLayout.addWidget(self.pushButton_create_bot)

=======
        self.pushButton_create_channel.setText('   Массовое создание каналов')
        self.verticalLayout.addWidget(self.pushButton_create_channel)

>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
        self.pushButton_enter_group = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_enter_group.setFont(font)
        self.pushButton_enter_group.setStyleSheet("QPushButton {\n"
                                                  "color: rgb(143, 145, 165);\n"
                                                  "border: 1;\n"
                                                  "text-align: left;\n"
                                                  "padding: 10px;\n"
                                                  "   }\n"
                                                  "   QPushButton:hover {\n"
                                                  "       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
                                                  "   }\n"
                                                  "\n"
                                                  "QPushButton:pressed {\n"
                                                  "                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
                                                  "            }")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/enter_the_group.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_enter_group.setIcon(icon8)
        self.pushButton_enter_group.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_enter_group.setObjectName("pushButton_enter_group")
        self.verticalLayout.addWidget(self.pushButton_enter_group)
        self.pushButton_reactions = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_reactions.setFont(font)
        self.pushButton_reactions.setStyleSheet("QPushButton {\n"
                                                "color: rgb(143, 145, 165);\n"
                                                "border: 1;\n"
                                                "text-align: left;\n"
                                                "padding: 10px;\n"
                                                "   }\n"
                                                "   QPushButton:hover {\n"
                                                "       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
                                                "   }\n"
                                                "\n"
                                                "QPushButton:pressed {\n"
                                                "                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
                                                "            }")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/like.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_reactions.setIcon(icon9)
        self.pushButton_reactions.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_reactions.setObjectName("pushButton_reactions")
        self.verticalLayout.addWidget(self.pushButton_reactions)
        self.pushButton_comment = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_comment.setFont(font)
        self.pushButton_comment.setStyleSheet("QPushButton {\n"
                                              "color: rgb(143, 145, 165);\n"
                                              "border: 1;\n"
                                              "text-align: left;\n"
                                              "padding: 10px;\n"
                                              "   }\n"
                                              "   QPushButton:hover {\n"
                                              "       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
                                              "   }\n"
                                              "\n"
                                              "QPushButton:pressed {\n"
                                              "                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
                                              "            }")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/coment.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_comment.setIcon(icon10)
        self.pushButton_comment.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_comment.setObjectName("pushButton_comment")
        self.verticalLayout.addWidget(self.pushButton_comment)
        self.pushButton_convert = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_convert.sizePolicy().hasHeightForWidth())
        self.pushButton_convert.setSizePolicy(sizePolicy)
        self.pushButton_convert.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_convert.setMaximumSize(QtCore.QSize(16777215, 57))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_convert.setFont(font)
        self.pushButton_convert.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_convert.setStyleSheet("QPushButton {\n"
                                              "color: rgb(143, 145, 165);\n"
                                              "border: 1;\n"
                                              "text-align: left;\n"
                                              "padding: 10px;\n"
                                              "   }\n"
                                              "   QPushButton:hover {\n"
                                              "       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
                                              "   }\n"
                                              "\n"
                                              "QPushButton:pressed {\n"
                                              "                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
                                              "            }")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/convert.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_convert.setIcon(icon11)
        self.pushButton_convert.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_convert.setObjectName("pushButton_convert")
        self.verticalLayout.addWidget(self.pushButton_convert)

        self.pushButton_doc = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_doc.sizePolicy().hasHeightForWidth())
        self.pushButton_doc.setSizePolicy(sizePolicy)
        self.pushButton_doc.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_doc.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_doc.setFont(font)
        self.pushButton_doc.setStyleSheet("QPushButton {\n"
                                          "color: rgb(143, 145, 165);\n"
                                          "border: 1;\n"
                                          "text-align: left;\n"
                                          "padding: 10px;\n"
                                          "   }\n"
                                          "   QPushButton:hover {\n"
                                          "       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
                                          "   }\n"
                                          "\n"
                                          "QPushButton:pressed {\n"
                                          "                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
                                          "            }")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/doc.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_doc.setIcon(icon12)
        self.pushButton_doc.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_doc.setObjectName("pushButton_doc")
        self.verticalLayout.addWidget(self.pushButton_doc)

        self.label_8 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(0, 0))
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 4, 1)
        self.setCentralWidget(self.centralwidget)
        self.action = QtWidgets.QAction(self)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(self)
        self.action_2.setObjectName("action_2")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_13.setText(_translate("MainWindow", "Аккаунты"))
        self.tableWidget_account.setSortingEnabled(True)

        item = self.tableWidget_account.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "#"))
        item = self.tableWidget_account.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget_account.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Юзернейм"))
        item = self.tableWidget_account.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Имя"))
        item = self.tableWidget_account.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", " Гео"))
        item = self.tableWidget_account.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Телефон"))
        item = self.tableWidget_account.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Отлёжка"))
        item = self.tableWidget_account.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Использован"))
        item = self.tableWidget_account.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Примечания"))
        self.label_account.setText(_translate("MainWindow", "Активные:"))

        self.pushButton_move_active.setText(_translate("MainWindow", "Переместить к \nактивным"))
        self.pushButton_move_main_account.setText(_translate("MainWindow", "Переместить в \nглавные аккаунты"))
        self.pushButton_move_archive.setText(_translate("MainWindow", "Переместить в \nархив"))

        self.pushButton_open_active_accounts.setText(_translate("MainWindow", "Активные аккаунты"))
        self.pushButton_open_arxive_accounts.setText(_translate("MainWindow", "Аккаунты в архиве"))
        self.pushButton_open_main_account.setText(_translate("MainWindow", "Главные аккаунты"))
        self.pushButton_open_temporary_ban_accounts.setText(_translate("MainWindow", "Аккаунты во \nвременном бане"))
        self.pushButton_open_login_error.setText(_translate("MainWindow", "Аккаунты с\nошибкой входа"))
        self.pushButton_add.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_show_data_account.setText(_translate("MainWindow", "Просмотр данных"))
        self.pushButton_enter.setText(_translate("MainWindow", "Войти"))
        self.pushButton_upload_tdata.setText(_translate("MainWindow", "Выгрузить Tdata"))
        self.pushButton_delete.setText(_translate("MainWindow", "Удалить"))
        self.label_count_all_account.setToolTip(
            _translate("MainWindow", "<html><head/><body><p align=\"justify\"><br/></p></body></html>"))
        self.label_count_all_account.setText(_translate("MainWindow", "<html><head/><body><p>1</p></body></html>"))
        self.label.setText(_translate("MainWindow", "Аккаунтов всего"))
        self.label_count_active_account.setText(_translate("MainWindow", "<html><head/><body><p>0</p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "Активных"))
        self.label_count_archive_account.setText(_translate("MainWindow", "<html><head/><body><p>0</p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "В архиве"))
        self.label_count_temporary_banned_account.setText(
            _translate("MainWindow", "<html><head/><body><p>0</p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "Во временном бане"))
        self.label_count_login_error.setText(_translate("MainWindow", "<html><head/><body><p>0</p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "С ошибкой входа"))
        self.label_count_main_account.setText(_translate("MainWindow", "<html><head/><body><p>0</p></body></html>"))
        self.label_10.setText(_translate("MainWindow", "Главные аккаунты"))

        self.pushButton_account.setText(_translate("MainWindow", "   Аккаунты"))
        self.pushButton_mailing.setText(_translate("MainWindow", "   Рассылка по юзерам"))
        self.pushButton_mailing_chat.setText(_translate("MainWindow", "   Рассылка по чатам"))
        self.pushButton_invite.setText(_translate("MainWindow", "   Инвайт"))
        self.pushButton_parser.setText(_translate("MainWindow", "   Парсер"))
        self.pushButton_proxy.setText(_translate("MainWindow", "   Прокси"))
        self.pushButton_bomber.setText(_translate("MainWindow", "   Бомбер на аккаунт"))
<<<<<<< HEAD
        self.pushButton_create_channel.setText(_translate("MainWindow", "   Массовое создание каналов"))
        self.pushButton_create_bot.setText(_translate("MainWindow", "   Массовое создание ботов"))
=======
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
        self.pushButton_enter_group.setText(_translate("MainWindow", "   Массовый заход в группу"))
        self.pushButton_reactions.setText(_translate("MainWindow", "   Накрутка реакций"))
        self.pushButton_comment.setText(_translate("MainWindow", "   Накрутка комментариев"))
        self.pushButton_convert.setText(_translate("MainWindow", "   Конвертер tdata и session"))
        self.pushButton_doc.setText(_translate("MainWindow", "   Документация"))
        self.action.setText(_translate("MainWindow", "сохранить"))
        self.action_2.setText(_translate("MainWindow", "добавить"))