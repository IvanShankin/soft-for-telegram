import os  # это для действия ниже перед запуском функции

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")  # 1. Автоматическое определение пути

if not Path(qt_plugins_path).exists():  # 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path  # 3. Установка пути

# 4. Только после этого импортируем QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator


class WindowProxyUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.root_project_dir = '..'

        self.setObjectName("MainWindow")
        self.resize(1500, 850)
        self.setMinimumSize(QtCore.QSize(1200, 750))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.setFont(font)
        self.setStyleSheet("background-color: rgb(236, 237, 240);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea_3 = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_3.sizePolicy().hasHeightForWidth())
        self.scrollArea_3.setSizePolicy(sizePolicy)
        self.scrollArea_3.setMinimumSize(QtCore.QSize(270, 0))
        self.scrollArea_3.setMaximumSize(QtCore.QSize(270, 16777215))
        self.scrollArea_3.setStyleSheet("background-color: rgb(14, 22, 33);\nborder: none;")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
<<<<<<< HEAD
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 268, 848))
        self.scrollAreaWidgetContents.setStyleSheet("")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_account_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
=======
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 268, 848))
        self.scrollAreaWidgetContents_3.setStyleSheet("")
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_account_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
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
                                                "border: 0;\n"
                                                "text-align: center;\n"
                                                "padding: 10px;")
        self.pushButton_account_2.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/logo.PNG"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.pushButton_account_2.setIcon(icon)
        self.pushButton_account_2.setIconSize(QtCore.QSize(300, 60))
        self.pushButton_account_2.setCheckable(False)
        self.pushButton_account_2.setObjectName("pushButton_account_2")
        self.verticalLayout.addWidget(self.pushButton_account_2)
<<<<<<< HEAD
        self.label_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
=======
        self.label_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(0, 0))
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
<<<<<<< HEAD
        self.pushButton_account = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
=======
        self.pushButton_account = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
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
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/account.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_account.setIcon(icon1)
        self.pushButton_account.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_account.setCheckable(False)
        self.pushButton_account.setObjectName("pushButton_account")
        self.verticalLayout.addWidget(self.pushButton_account)
<<<<<<< HEAD
        self.pushButton_mailing = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
=======
        self.pushButton_mailing = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
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
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/mailing.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_mailing.setIcon(icon2)
        self.pushButton_mailing.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_mailing.setObjectName("pushButton_mailing")
        self.verticalLayout.addWidget(self.pushButton_mailing)
<<<<<<< HEAD
        self.pushButton_mailing_chat = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
=======
        self.pushButton_mailing_chat = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_mailing_chat.setFont(font)
        self.pushButton_mailing_chat.setStyleSheet("QPushButton {\n"
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
        self.pushButton_mailing_chat.setIcon(icon2)
        self.pushButton_mailing_chat.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_mailing_chat.setObjectName("pushButton_mailing_chat")
        self.verticalLayout.addWidget(self.pushButton_mailing_chat)
<<<<<<< HEAD
        self.pushButton_invite = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
=======
        self.pushButton_invite = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
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
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/invaite.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_invite.setIcon(icon3)
        self.pushButton_invite.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_invite.setObjectName("pushButton_invite")
        self.verticalLayout.addWidget(self.pushButton_invite)
<<<<<<< HEAD
        self.pushButton_parser = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
=======
        self.pushButton_parser = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
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
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/parser.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_parser.setIcon(icon4)
        self.pushButton_parser.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_parser.setObjectName("pushButton_parser")
        self.verticalLayout.addWidget(self.pushButton_parser)
<<<<<<< HEAD
        self.pushButton_proxy = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
=======
        self.pushButton_proxy = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
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
                                            "color: rgb(255, 255, 255);\n"
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
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/proxy.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_proxy.setIcon(icon5)
        self.pushButton_proxy.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_proxy.setObjectName("pushButton_proxy")
        self.verticalLayout.addWidget(self.pushButton_proxy)
<<<<<<< HEAD
        self.pushButton_bomber = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
=======
        self.pushButton_bomber = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
        self.pushButton_bomber.setMinimumSize(QtCore.QSize(185, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_bomber.setFont(font)
        self.pushButton_bomber.setStyleSheet("QPushButton {\n"
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
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/bomber.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_bomber.setIcon(icon6)
        self.pushButton_bomber.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_bomber.setObjectName("pushButton_bomber")
        self.verticalLayout.addWidget(self.pushButton_bomber)

<<<<<<< HEAD
        self.pushButton_create_channel = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
=======
        self.pushButton_create_channel = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
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
        icon7.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/creating_bots.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_create_bot.setIcon(icon7)
        self.pushButton_create_bot.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_create_bot.setObjectName("pushButton_create_bot")
        self.verticalLayout.addWidget(self.pushButton_create_bot)

        self.pushButton_enter_group = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
=======
        self.pushButton_create_channel.setText('   Массовое создание каналов')
        self.verticalLayout.addWidget(self.pushButton_create_channel)

        self.pushButton_enter_group = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_enter_group.setFont(font)
        self.pushButton_enter_group.setStyleSheet("QPushButton {\n"
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
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/enter_the_group.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_enter_group.setIcon(icon7)
        self.pushButton_enter_group.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_enter_group.setObjectName("pushButton_enter_group")
        self.verticalLayout.addWidget(self.pushButton_enter_group)
<<<<<<< HEAD
        self.pushButton_reactions = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
=======
        self.pushButton_reactions = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_reactions.setFont(font)
        self.pushButton_reactions.setStyleSheet("QPushButton {\n"
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
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/like.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_reactions.setIcon(icon8)
        self.pushButton_reactions.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_reactions.setObjectName("pushButton_reactions")
        self.verticalLayout.addWidget(self.pushButton_reactions)
<<<<<<< HEAD
        self.pushButton_comment = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
=======
        self.pushButton_comment = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_comment.setFont(font)
        self.pushButton_comment.setStyleSheet("QPushButton {\n"
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
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/coment.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_comment.setIcon(icon9)
        self.pushButton_comment.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_comment.setObjectName("pushButton_comment")
        self.verticalLayout.addWidget(self.pushButton_comment)
<<<<<<< HEAD
        self.pushButton_convert = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
=======
        self.pushButton_convert = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
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
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/convert.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.pushButton_convert.setIcon(icon10)
        self.pushButton_convert.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_convert.setObjectName("pushButton_convert")
        self.verticalLayout.addWidget(self.pushButton_convert)
<<<<<<< HEAD
        self.pushButton_doc = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
=======
        self.pushButton_doc = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
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
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/doc.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.pushButton_doc.setIcon(icon11)
        self.pushButton_doc.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_doc.setObjectName("pushButton_doc")
        self.verticalLayout.addWidget(self.pushButton_doc)
<<<<<<< HEAD
        self.label_10 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
=======
        self.label_10 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QtCore.QSize(0, 0))
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
<<<<<<< HEAD
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents)
=======
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
        self.gridLayout.addWidget(self.scrollArea_3, 0, 0, 4, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(20, 10, -1, 10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_2.addWidget(self.label_18)
        self.pushButton_info = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_info.setStyleSheet("border: none;\n"
                                           "")
        self.pushButton_info.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/info.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.pushButton_info.setIcon(icon12)
        self.pushButton_info.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_info.setObjectName("pushButton_info")
        self.horizontalLayout_2.addWidget(self.pushButton_info)
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setText("")
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_2.addWidget(self.label_19)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(20, 10, 20, -1)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("")
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setMaximumSize(QtCore.QSize(400, 16777215))
        self.groupBox_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 13px;")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox_2)
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
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_port_socks5 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_port_socks5.setMaximumSize(QtCore.QSize(250, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_port_socks5.setFont(font)
        self.lineEdit_port_socks5.setStyleSheet("QLineEdit {\n"
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
        self.lineEdit_port_socks5.setObjectName("lineEdit_port_socks5")
        self.lineEdit_port_socks5.setPlaceholderText("58306")  # Подсказка
        self.lineEdit_port_socks5.setValidator(QIntValidator())
        self.gridLayout_2.addWidget(self.lineEdit_port_socks5, 1, 1, 1, 1)
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
        self.lineEdit_login_socks5 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_login_socks5.setMaximumSize(QtCore.QSize(250, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_login_socks5.setFont(font)
        self.lineEdit_login_socks5.setStyleSheet("QLineEdit {\n"
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
        self.lineEdit_login_socks5.setObjectName("lineEdit_login_socks5")
        self.lineEdit_login_socks5.setPlaceholderText("HB3fdn0fsVz")  # Подсказка
        self.gridLayout_2.addWidget(self.lineEdit_login_socks5, 2, 1, 1, 1)
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
        self.lineEdit_password_socks5 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_password_socks5.setMaximumSize(QtCore.QSize(250, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_password_socks5.setFont(font)
        self.lineEdit_password_socks5.setStyleSheet("QLineEdit {\n"
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
        self.lineEdit_password_socks5.setObjectName("lineEdit_password_socks5")
        self.lineEdit_password_socks5.setPlaceholderText("ljPrDld4N")  # Подсказка
        self.gridLayout_2.addWidget(self.lineEdit_password_socks5, 3, 1, 1, 1)
        self.lineEdit_ip_socks5 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_ip_socks5.setMaximumSize(QtCore.QSize(250, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_ip_socks5.setFont(font)
        self.lineEdit_ip_socks5.setStyleSheet("QLineEdit {\n"
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
        self.lineEdit_ip_socks5.setObjectName("lineEdit_ip_socks5")
        self.lineEdit_ip_socks5.setPlaceholderText("114.122.806.470")  # Подсказка
        self.gridLayout_2.addWidget(self.lineEdit_ip_socks5, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pushButton_check_proxy = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_check_proxy.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_check_proxy.setMaximumSize(QtCore.QSize(400, 16777215))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_check_proxy.setFont(font)
        self.pushButton_check_proxy.setStyleSheet("\n"
                                                  "QPushButton {\n"
                                                  "    background-color: rgb(255, 255, 255);\n"
                                                  "    text-align: center;\n"
                                                  "    border-radius: 12px;\n"
                                                  "    padding: 7px;\n"
                                                  "    border: none;\n"
                                                  "    margin-left: 100px;\n"
                                                  "    margin-right: 100px;\n"
                                                  "   }\n"
                                                  "QPushButton:hover {\n"
                                                  "    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:pressed {\n"
                                                  "     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
                                                  "}")
        self.pushButton_check_proxy.setObjectName("pushButton_check_proxy")
        self.verticalLayout_3.addWidget(self.pushButton_check_proxy)

        self.checkBox_use_proxy_for_loading = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.checkBox_use_proxy_for_loading.setFont(font)
        self.checkBox_use_proxy_for_loading.setMaximumSize(470, 213)
        self.checkBox_use_proxy_for_loading.setStyleSheet("QCheckBox {\n"
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
        self.checkBox_use_proxy_for_loading.setObjectName("checkBox_use_proxy_for_loading")
        self.horizontalLayout.addWidget(self.checkBox_use_proxy_for_loading)
        self.pushButton_icon_info = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_icon_info.sizePolicy().hasHeightForWidth())
        self.pushButton_icon_info.setSizePolicy(sizePolicy)
        self.pushButton_icon_info.setStyleSheet("border: none;\n"
                                                "background-color: rgb(236, 237, 240);")
        self.pushButton_icon_info.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/free-icon-idea-149200.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_icon_info.setIcon(icon13)
        self.pushButton_icon_info.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_icon_info.setObjectName("pushButton_icon_info")
        self.horizontalLayout.addWidget(self.pushButton_icon_info)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_3, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setText("")
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 3, 1, 1, 1)
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
        self.label_18.setText(_translate("MainWindow", "Прокси"))
        self.label_5.setText(_translate("MainWindow", "SOCKS5:"))
        self.label.setText(_translate("MainWindow", "IP:"))
        self.label_3.setText(_translate("MainWindow", "Login:"))
        self.label_11.setText(_translate("MainWindow", "Password:"))
        self.label_2.setText(_translate("MainWindow", "Port:"))
        self.pushButton_check_proxy.setText(_translate("MainWindow", "Проверить"))
        self.checkBox_use_proxy_for_loading.setText(
            _translate("MainWindow", "Использовать прокси при загрузке аккаунтов"))
        self.action.setText(_translate("MainWindow", "сохранить"))
        self.action_2.setText(_translate("MainWindow", "добавить"))
