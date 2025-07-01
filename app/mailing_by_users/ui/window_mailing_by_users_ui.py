import os  # это для действия ниже перед запуском функции

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator  # для разрешения ввода только цифр в LineEdit
from PyQt5.QtWidgets import QSizePolicy


class WindowMailingByUsersUi(QtWidgets.QMainWindow):
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
        self.gridLayout_12 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_12.setContentsMargins(0, 0, 20, 0)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.scrollArea_3 = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_3.sizePolicy().hasHeightForWidth())
        self.scrollArea_3.setSizePolicy(sizePolicy)
        self.scrollArea_3.setMinimumSize(QtCore.QSize(270, 0))
        self.scrollArea_3.setMaximumSize(QtCore.QSize(270, 16777215))
        self.scrollArea_3.setStyleSheet("background-color: rgb(14, 22, 33);\n"
                                        "border: none;")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 268, 848))
        self.scrollAreaWidgetContents_3.setStyleSheet("")
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_account_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
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
        self.label_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(0, 0))
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.pushButton_account = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
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
        self.pushButton_mailing = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
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
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/mailing.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_mailing.setIcon(icon2)
        self.pushButton_mailing.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_mailing.setObjectName("pushButton_mailing")
        self.verticalLayout.addWidget(self.pushButton_mailing)
        self.pushButton_mailing_chat = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
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
        self.pushButton_invite = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
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
        self.pushButton_parser = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
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
        self.pushButton_proxy = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
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
        self.pushButton_bomber = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
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

        self.pushButton_create_channel = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
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

        self.pushButton_create_bot = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
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

=======
        self.pushButton_create_channel.setText('   Массовое создание каналов')
        self.verticalLayout.addWidget(self.pushButton_create_channel)

>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
        self.pushButton_enter_group = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
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
        icon7.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/enter_the_group.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_enter_group.setIcon(icon7)
        self.pushButton_enter_group.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_enter_group.setObjectName("pushButton_enter_group")
        self.verticalLayout.addWidget(self.pushButton_enter_group)
        self.pushButton_reactions = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
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
        self.pushButton_comment = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
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
        self.pushButton_convert = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
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

        self.pushButton_doc = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
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

        self.label_8 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(0, 0))
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout_12.addWidget(self.scrollArea_3, 0, 0, 4, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(27, 10, -1, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout.addWidget(self.label_18)
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
        self.horizontalLayout.addWidget(self.pushButton_info)
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setText("")
        self.label_19.setObjectName("label_19")
        self.horizontalLayout.addWidget(self.label_19)
        self.gridLayout_12.addLayout(self.horizontalLayout, 0, 1, 1, 3)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_2.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea_2.setStyleSheet("border: 0;")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 572, 385))
        self.scrollAreaWidgetContents_2.setStyleSheet("/* СТИЛЬ ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */"
                                                        "QScrollBar:vertical {"
                                                        "    border-radius: 8px;"
                                                        "    background: rgb(210, 210, 213);"
                                                        "    width: 14px;"
                                                        "    margin: 0px 0 0px 0;"
                                                        "}"
                                                        ""
                                                        "/* HANDLE BAR ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */"
                                                        "QScrollBar::handle:vertical {"
                                                        "    background-color: rgb(210, 210, 213);"
                                                        "    min-height: 30px;"
                                                        "    border-radius: 0px;"
                                                        "    transition: background-color 0.2s ease;"
                                                        "}"
                                                        ""
                                                        "QScrollBar::handle:vertical:hover {"
                                                        "    background-color: rgb(180, 180, 184);"
                                                        "}"
                                                        ""
                                                        "QScrollBar::handle:vertical:pressed {"
                                                        "    background-color: rgb(150, 150, 153);"
                                                        "}"
                                                        ""
                                                        "/* КНОПКА ВВЕРХУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */"
                                                        "QScrollBar::sub-line:vertical {"
                                                        "    border: none;"
                                                        "    background-color: rgb(190, 190, 193);"
                                                        "    height: 15px;"
                                                        "    border-top-left-radius: 7px;"
                                                        "    border-top-right-radius: 7px;"
                                                        "    subcontrol-position: top;"
                                                        "    subcontrol-origin: margin;"
                                                        "}"
                                                        ""
                                                        "QScrollBar::sub-line:vertical:hover {"
                                                        "    background-color: rgb(170, 170, 174);"
                                                        "}"
                                                        ""
                                                        "QScrollBar::sub-line:vertical:pressed {"
                                                        "    background-color: rgb(140, 140, 143);"
                                                        "}"
                                                        ""
                                                        "/* КНОПКА ВНИЗУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */"
                                                        "QScrollBar::add-line:vertical {"
                                                        "    border: none;"
                                                        "    background-color: rgb(190, 190, 193);"
                                                        "    height: 15px;"
                                                        "    border-bottom-left-radius: 7px;"
                                                        "    border-bottom-right-radius: 7px;"
                                                        "    subcontrol-position: bottom;"
                                                        "    subcontrol-origin: margin;"
                                                        "}"
                                                        ""
                                                        "QScrollBar::add-line:vertical:hover {"
                                                        "    background-color: rgb(170, 170, 174);"
                                                        "}"
                                                        ""
                                                        "QScrollBar::add-line:vertical:pressed {"
                                                        "    background-color: rgb(140, 140, 143);"
                                                        "}"
                                                        ""
                                                        "/* УБРАТЬ СТРЕЛКИ */"
                                                        "QScrollBar::up-arrow:vertical,"
                                                        "QScrollBar::down-arrow:vertical {"
                                                        "    background: none;"
                                                        "}"
                                                        ""
                                                        "/* УБРАТЬ ФОН */"
                                                        "QScrollBar::add-page:vertical,"
                                                        "QScrollBar::sub-page:vertical {"
                                                        "    background: none;"
                                                        "}")
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setContentsMargins(20, -1, 40, -1)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("")
        self.label_6.setObjectName("label_6")
        self.gridLayout_7.addWidget(self.label_6, 0, 0, 1, 1)
        self.scrollArea_4 = QtWidgets.QScrollArea(self.scrollAreaWidgetContents_2)
        self.scrollArea_4.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea_4.setStyleSheet("border: 0;")
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 532, 343))
        self.scrollAreaWidgetContents_4.setStyleSheet("/* СТИЛЬ ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */"
                                                        "QScrollBar:vertical {"
                                                        "    border-radius: 8px;"
                                                        "    background: rgb(210, 210, 213);"
                                                        "    width: 14px;"
                                                        "    margin: 0px 0 0px 0;"
                                                        "}"
                                                        ""
                                                        "/* HANDLE BAR ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */"
                                                        "QScrollBar::handle:vertical {"
                                                        "    background-color: rgb(210, 210, 213);"
                                                        "    min-height: 30px;"
                                                        "    border-radius: 0px;"
                                                        "    transition: background-color 0.2s ease;"
                                                        "}"
                                                        ""
                                                        "QScrollBar::handle:vertical:hover {"
                                                        "    background-color: rgb(180, 180, 184);"
                                                        "}"
                                                        ""
                                                        "QScrollBar::handle:vertical:pressed {"
                                                        "    background-color: rgb(150, 150, 153);"
                                                        "}"
                                                        ""
                                                        "/* КНОПКА ВВЕРХУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */"
                                                        "QScrollBar::sub-line:vertical {"
                                                        "    border: none;"
                                                        "    background-color: rgb(190, 190, 193);"
                                                        "    height: 15px;"
                                                        "    border-top-left-radius: 7px;"
                                                        "    border-top-right-radius: 7px;"
                                                        "    subcontrol-position: top;"
                                                        "    subcontrol-origin: margin;"
                                                        "}"
                                                        ""
                                                        "QScrollBar::sub-line:vertical:hover {"
                                                        "    background-color: rgb(170, 170, 174);"
                                                        "}"
                                                        ""
                                                        "QScrollBar::sub-line:vertical:pressed {"
                                                        "    background-color: rgb(140, 140, 143);"
                                                        "}"
                                                        ""
                                                        "/* КНОПКА ВНИЗУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */"
                                                        "QScrollBar::add-line:vertical {"
                                                        "    border: none;"
                                                        "    background-color: rgb(190, 190, 193);"
                                                        "    height: 15px;"
                                                        "    border-bottom-left-radius: 7px;"
                                                        "    border-bottom-right-radius: 7px;"
                                                        "    subcontrol-position: bottom;"
                                                        "    subcontrol-origin: margin;"
                                                        "}"
                                                        ""
                                                        "QScrollBar::add-line:vertical:hover {"
                                                        "    background-color: rgb(170, 170, 174);"
                                                        "}"
                                                        ""
                                                        "QScrollBar::add-line:vertical:pressed {"
                                                        "    background-color: rgb(140, 140, 143);"
                                                        "}"
                                                        ""
                                                        "/* УБРАТЬ СТРЕЛКИ */"
                                                        "QScrollBar::up-arrow:vertical,"
                                                        "QScrollBar::down-arrow:vertical {"
                                                        "    background: none;"
                                                        "}"
                                                        ""
                                                        "/* УБРАТЬ ФОН */"
                                                        "QScrollBar::add-page:vertical,"
                                                        "QScrollBar::sub-page:vertical {"
                                                        "    background: none;"
                                                        "}")
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_4)
        self.gridLayout_5.setContentsMargins(-1, -1, -1, 10)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setContentsMargins(0, -1, -1, -1)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.textEdit_message = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_4)
        self.textEdit_message.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit_message.setFont(font)
        self.textEdit_message.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                            "border-radius: 20px;\n"
                                            "padding-top: 15px; /* Отступ только слева */   \n"
                                            " padding-bottom: 15px; /* Отступ только снизу */\n"
                                            "")
        self.textEdit_message.setReadOnly(False)
        self.textEdit_message.setObjectName("textEdit_message")
        self.gridLayout_10.addWidget(self.textEdit_message, 0, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_10, 1, 0, 1, 1)
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.gridLayout_7.addWidget(self.scrollArea_4, 1, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_7, 2, 0, 1, 1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_12.addWidget(self.scrollArea_2, 1, 1, 1, 1)
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setContentsMargins(-1, 40, -1, 10)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 20px;")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setContentsMargins(25, 10, -1, 20)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_choose_file_for_mailing = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_choose_file_for_mailing.setMaximumSize(QtCore.QSize(70, 35))
        self.pushButton_choose_file_for_mailing.setMinimumSize(QtCore.QSize(0, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setPointSize(10)
        self.pushButton_choose_file_for_mailing.setFont(font)
        self.pushButton_choose_file_for_mailing.setStyleSheet("QPushButton {\n"
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
        self.pushButton_choose_file_for_mailing.setObjectName("pushButton_choose_file_for_mailing")
        self.gridLayout.addWidget(self.pushButton_choose_file_for_mailing, 5, 1, 1, 1)
        self.checkBox_use_file_for_message = QtWidgets.QCheckBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.checkBox_use_file_for_message.setFont(font)
        self.checkBox_use_file_for_message.setStyleSheet("\n"
                                                         "QCheckBox {\n"
                                                         "color: rgb(0, 0, 0);\n"
                                                         "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                                         "\n"
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
                                                         "QCheckBox::indicator:checked:hover {\n"
                                                         "    background-color: rgb(180, 230, 180); \n"
                                                         "}")
        self.checkBox_use_file_for_message.setObjectName("checkBox_use_file_for_message")
        self.gridLayout.addWidget(self.checkBox_use_file_for_message, 5, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.lineEdit_delay = QtWidgets.QLineEdit(self.groupBox_2)
        validator = QIntValidator(0, 99999)  # Минимум 0, максимум большое число
        self.lineEdit_delay.setValidator(validator)
        self.lineEdit_delay.setMaximumSize(QtCore.QSize(70, 16777215))
        self.lineEdit_delay.setMaxLength(5)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_delay.setFont(font)
        self.lineEdit_delay.setStyleSheet("QLineEdit {\n"
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
                                          "/* Состояние для отключенного текстового поля */\n"
                                          "QLineEdit:disabled {\n"
                                          "    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */\n"
                                          "    color: rgb(170, 170, 170); /* Цвет текста для отключенного */\n"
                                          "    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */\n"
                                          "}")
        self.lineEdit_delay.setObjectName("lineEdit_delay")
        self.gridLayout.addWidget(self.lineEdit_delay, 2, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setMouseTracking(True)
        self.label_7.setStyleSheet("")
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)
        self.lineEdit_max_message = QtWidgets.QLineEdit(self.groupBox_2)
        validator = QIntValidator(1, 99999)  # Минимум 0, максимум большое число
        self.lineEdit_max_message.setValidator(validator)
        self.lineEdit_max_message.setMaximumSize(QtCore.QSize(70, 16777215))
        self.lineEdit_max_message.setMaxLength(5)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_max_message.setFont(font)
        self.lineEdit_max_message.setStyleSheet("QLineEdit {\n"
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
                                                "/* Состояние при фокусировке */\n"
                                                "QLineEdit:focus {\n"
                                                "    border: 2px solid rgb(0, 0, 0); /* Цвет рамки при фокусировке */\n"
                                                "    background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */\n"
                                                "}\n"
                                                "/* Состояние для отключенного текстового поля */\n"
                                                "QLineEdit:disabled {\n"
                                                "    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */\n"
                                                "    color: rgb(170, 170, 170); /* Цвет текста для отключенного */\n"
                                                "    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */\n"
                                                "}")
        self.lineEdit_max_message.setObjectName("lineEdit_max_message")
        self.gridLayout.addWidget(self.lineEdit_max_message, 3, 1, 1, 1)
        self.checkBox_use_proxy = QtWidgets.QCheckBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.checkBox_use_proxy.setFont(font)
        self.checkBox_use_proxy.setStyleSheet("\n"
                                              "QCheckBox {\n"
                                              "color: rgb(0, 0, 0);\n"
                                              "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                              "\n"
                                              "}\n"
                                              "QCheckBox::indicator {\n"
                                              "    width: 15px; /* Ширина индикатора (чекбокса) */\n"
                                              "    height: 15px; /* Высота индикатора (чекбокса) */\n"
                                              "    border: 2px solid rgb(150, 150, 150); /* Обводка чекбокса */\n"
                                              "    border-radius: 4px; /* Закругление углов */\n"
                                              "    background-color: white; /* Цвет фона чекбокса */\n"
                                              "}\n"
                                              "QCheckBox::indicator:checked {\n"
                                              "    background-color: rgb(150, 200, 150); \n"
                                              "    border: 2px solid rgb(150, 150, 150); \n"
                                              "}\n"
                                              "\n"
                                              "\n"
                                              "QCheckBox::indicator:checked:hover {\n"
                                              "    background-color: rgb(180, 230, 180); \n"
                                              "}")
        self.checkBox_use_proxy.setObjectName("checkBox_use_proxy")
        self.gridLayout.addWidget(self.checkBox_use_proxy, 7, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_12.setFont(font)
        self.label_12.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_12.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 4, 0, 1, 1)
        self.lineEdit_max_message_from_one_account = QtWidgets.QLineEdit(self.groupBox_2)
        validator = QIntValidator(1, 99999)  # Минимум 0, максимум большое число
        self.lineEdit_max_message_from_one_account.setValidator(validator)
        self.lineEdit_max_message_from_one_account.setMaximumSize(QtCore.QSize(70, 16777215))
        self.lineEdit_max_message_from_one_account.setMaxLength(5)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_max_message_from_one_account.setFont(font)
        self.lineEdit_max_message_from_one_account.setStyleSheet("QLineEdit {\n"
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
        self.lineEdit_max_message_from_one_account.setObjectName("lineEdit_max_message_from_one_account")
        self.gridLayout.addWidget(self.lineEdit_max_message_from_one_account, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.pushButton_check_user_name = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_check_user_name.sizePolicy().hasHeightForWidth())
        self.pushButton_check_user_name.setSizePolicy(sizePolicy)
        self.pushButton_check_user_name.setMinimumSize(QtCore.QSize(0, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_check_user_name.setFont(font)
        self.pushButton_check_user_name.setStyleSheet("QPushButton {\n"
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
                                                     "            }\n"
                                                     "")
        self.pushButton_check_user_name.setObjectName("pushButton_check_user_name")
        self.gridLayout.addWidget(self.pushButton_check_user_name, 1, 1, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_11, 1, 2, 1, 2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(20, 10, 10, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setStyleSheet("border: 0;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 818, 384))
        self.scrollAreaWidgetContents.setStyleSheet("/* СТИЛЬ ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */\n"
                                                    "QScrollBar:vertical {\n"
                                                    "    border-radius: 8px; /* Закругление углов */\n"
                                                    "    background: rgb(210, 210, 213); /* Стандартный цвет фона */\n"
                                                    "    width: 14px; /* Ширина скроллбара */\n"
                                                    "    margin: 0px 0 0px 0;\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* HANDLE BAR ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */\n"
                                                    "QScrollBar::handle:vertical {  \n"
                                                    "    background-color: rgb(210, 210, 213); /* Стандартный цвет фона для ползунка */\n"
                                                    "    min-height: 30px; /* Минимальная высота ползунка */\n"
                                                    "    border-radius: 7px; /* Закругление углов ползунка */\n"
                                                    "    transition: background-color 0.2s ease; /* Плавный переход цвета */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::handle:vertical:hover {  \n"
                                                    "    background-color: rgb(180, 180, 184); /* Цвет ползунка при наведении */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::handle:vertical:pressed {  \n"
                                                    "    background-color: rgb(150, 150, 153); /* Цвет ползунка при нажатии */\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* КНОПКА ВВЕРХУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */\n"
                                                    "QScrollBar::sub-line:vertical {\n"
                                                    "    border: none;  \n"
                                                    "    background-color: rgb(210, 210, 213); /* Стандартный цвет фона для кнопки вверх */\n"
                                                    "    height: 15px; /* Высота кнопки */\n"
                                                    "    border-top-left-radius: 7px; /* Закругление верхних углов */\n"
                                                    "    border-top-right-radius: 7px; /* Закругление верхних углов */\n"
                                                    "    subcontrol-position: top; /* Позиция кнопки */\n"
                                                    "    subcontrol-origin: margin; /* Происхождение позиции кнопки */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::sub-line:vertical:hover {  \n"
                                                    "    background-color: rgb(180, 180, 184); /* Цвет кнопки вверх при наведении */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::sub-line:vertical:pressed {  \n"
                                                    "    background-color: rgb(150, 150, 153); /* Цвет кнопки вверх при нажатии */\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* КНОПКА ВНИЗУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */\n"
                                                    "QScrollBar::add-line:vertical {\n"
                                                    "    border: none;  \n"
                                                    "    background-color: rgb(210, 210, 213); /* Стандартный цвет фона для кнопки вниз */\n"
                                                    "    height: 15px; /* Высота кнопки */\n"
                                                    "    border-bottom-left-radius: 7px; /* Закругление нижних углов */\n"
                                                    "    border-bottom-right-radius: 7px; /* Закругление нижних углов */\n"
                                                    "    subcontrol-position: bottom; /* Позиция кнопки */\n"
                                                    "    subcontrol-origin: margin; /* Происхождение позиции кнопки */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::add-line:vertical:hover {  \n"
                                                    "    background-color: rgb(180, 180, 184); /* Цвет кнопки вниз при наведении */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::add-line:vertical:pressed {  \n"
                                                    "    background-color: rgb(150, 150, 153); /* Цвет кнопки вниз при нажатии */\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* УБРАТЬ СТРЕЛКИ */\n"
                                                    "QScrollBar::up-arrow:vertical, \n"
                                                    "QScrollBar::down-arrow:vertical {\n"
                                                    "    background: none; /* Убираем стрелки */\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* УБРАТЬ ФОН */\n"
                                                    "QScrollBar::add-page:vertical, \n"
                                                    "QScrollBar::sub-page:vertical {\n"
                                                    "    background: none; /* Убираем фоновую страницу */\n"
                                                    "}")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_4.setContentsMargins(-1, -1, -1, 10)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("")
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 1, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textEdit_conclusion = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit_conclusion.setMinimumSize(QtCore.QSize(350, 320))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit_conclusion.setFont(font)
        self.textEdit_conclusion.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                               "border-radius: 20px;\n"
                                               "padding-top: 15px; /* Отступ только слева */   \n"
                                               " padding-bottom: 15px; /* Отступ только снизу */\n"
                                               "")
        self.textEdit_conclusion.setReadOnly(True)
        self.textEdit_conclusion.setObjectName("textEdit_conclusion")
        self.gridLayout_3.addWidget(self.textEdit_conclusion, 1, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 2, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.gridLayout_12.addLayout(self.verticalLayout_2, 2, 1, 2, 2)
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setContentsMargins(-1, 50, -1, 15)
        self.gridLayout_9.setVerticalSpacing(25)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "border-radius: 20px;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setMinimumSize(310,160)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_count_attempts = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_count_attempts.setFont(font)
        self.label_count_attempts.setStyleSheet("")
        self.label_count_attempts.setObjectName("label_count_attempts")
        self.gridLayout_2.addWidget(self.label_count_attempts, 3, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_13.setStyleSheet("")
        self.label_13.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 3, 0, 1, 1)
        self.label_banned_account = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_banned_account.setFont(font)
        self.label_banned_account.setStyleSheet("")
        self.label_banned_account.setObjectName("label_banned_account")
        self.gridLayout_2.addWidget(self.label_banned_account, 4, 1, 1, 1)
        self.label_sent_message = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_sent_message.setFont(font)
        self.label_sent_message.setStyleSheet("")
        self.label_sent_message.setObjectName("label_sent_message")
        self.gridLayout_2.addWidget(self.label_sent_message, 0, 1, 1, 1)
        self.label_unsuccessful = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_unsuccessful.setFont(font)
        self.label_unsuccessful.setStyleSheet("")
        self.label_unsuccessful.setObjectName("label_unsuccessful")
        self.gridLayout_2.addWidget(self.label_unsuccessful, 2, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("")
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 4, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_15.setFont(font)
        self.label_15.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_15.setStyleSheet("")
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 0, 0, 1, 1)

        self.label_remaining_message = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_remaining_message.setFont(font)
        self.label_remaining_message.setStyleSheet("")
        self.label_remaining_message.setObjectName("label_remaining_message")
        self.gridLayout_2.addWidget(self.label_remaining_message, 1, 1, 1, 1)

        self.label_10 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_10.setStyleSheet("")
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 1, 0, 1, 1)

        self.label_16 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_16.setFont(font)
        self.label_16.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_16.setStyleSheet("")
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 2, 0, 1, 1)
        self.gridLayout_9.addWidget(self.groupBox, 1, 1, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "border-radius: 20px;")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox")
        self.groupBox_3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.groupBox_3.setMinimumSize(319, 108)
        self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.checkBox_use_streams = QtWidgets.QCheckBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_use_streams.setFont(font)
        self.checkBox_use_streams.setStyleSheet("\n"
                                              "QCheckBox {\n"
                                              "color: rgb(0, 0, 0);\n"
                                              "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                              "\n"
                                              "}\n"
                                              "QCheckBox::indicator {\n"
                                              "    width: 15px; /* Ширина индикатора (чекбокса) */\n"
                                              "    height: 15px; /* Высота индикатора (чекбокса) */\n"
                                              "    border: 2px solid rgb(150, 150, 150); /* Обводка чекбокса */\n"
                                              "    border-radius: 4px; /* Закругление углов */\n"
                                              "    background-color: white; /* Цвет фона чекбокса */\n"
                                              "}\n"
                                              "QCheckBox::indicator:checked {\n"
                                              "    background-color: rgb(150, 200, 150); \n"
                                              "    border: 2px solid rgb(150, 150, 150); \n"
                                              "}\n"
                                              "\n"
                                              "\n"
                                              "QCheckBox::indicator:checked:hover {\n"
                                              "    background-color: rgb(180, 230, 180); \n"
                                              "}")
        self.checkBox_use_streams.setObjectName("checkBox_use_streams")
        self.gridLayout_10.addWidget(self.checkBox_use_streams, 0, 0, 1, 4)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.gridLayout_10.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_quantity_streams = QtWidgets.QLineEdit(self.groupBox_2)
        validator = QIntValidator(1, 99999)  # Минимум 0, максимум большое число
        self.lineEdit_quantity_streams.setValidator(validator)
        self.lineEdit_quantity_streams.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_quantity_streams.setFont(font)
        self.lineEdit_quantity_streams.setMaxLength(5)
        self.lineEdit_quantity_streams.setStyleSheet("QLineEdit {\n"
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
        self.lineEdit_quantity_streams.setObjectName("lineEdit_quantity_streams")
        self.gridLayout_10.addWidget(self.lineEdit_quantity_streams, 1, 1, 1, 1)
        self.pushButton_info_streams = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_info_streams.setStyleSheet("border: none;\n")
        self.pushButton_info_streams.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/question.png"), QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.pushButton_info_streams.setIcon(icon13)
        self.pushButton_info_streams.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_info_streams.setObjectName("pushButton_info_streams")
        self.gridLayout_10.addWidget(self.pushButton_info_streams, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_3.setStyleSheet("")
        self.label_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.label_3.setObjectName("label_3")
        self.gridLayout_10.addWidget(self.label_3, 1, 3, 1, 1)
        self.gridLayout_9.addWidget(self.groupBox_3, 0, 1, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_9, 2, 3, 1, 1)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setContentsMargins(-1, -1, -1, 10)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setMinimumSize(QtCore.QSize(185, 80))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_start.setFont(font)
        self.pushButton_start.setStyleSheet("\n"
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
        self.pushButton_start.setIconSize(QtCore.QSize(120, 120))
        self.pushButton_start.setObjectName("pushButton_start")
        self.gridLayout_8.addWidget(self.pushButton_start, 0, 0, 2, 1)
        self.pushButton_clear_conclusion = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clear_conclusion.setMinimumSize(QtCore.QSize(100, 50))
        self.pushButton_clear_conclusion.setMaximumSize(QtCore.QSize(200, 76))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_clear_conclusion.setFont(font)
        self.pushButton_clear_conclusion.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.pushButton_clear_conclusion.setStyleSheet("\n"
                                                       "QPushButton {\n"
                                                       "    background-color: rgb(255, 255, 255);\n"
                                                       "    text-align: center;\n"
                                                       "    border-radius: 17px;\n"
<<<<<<< HEAD
                                                       "	 padding: 10px;"
                                                        "    padding-left: 20px;"
                                                        "    padding-right: 20px;"
=======
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
                                                       "   }\n"
                                                       "QPushButton:hover {\n"
                                                       "    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
                                                       "}\n"
                                                       "\n"
                                                       "QPushButton:pressed {\n"
                                                       "     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
                                                       "}")
<<<<<<< HEAD
=======
        self.pushButton_clear_conclusion.setIconSize(QtCore.QSize(60, 60))
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
        self.pushButton_clear_conclusion.setObjectName("pushButton_clear_conclusion")
        self.gridLayout_8.addWidget(self.pushButton_clear_conclusion, 1, 1, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_8, 3, 3, 1, 1)
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
        self.label_18.setText(_translate("MainWindow", "Рассылка"))
        self.label_6.setText(_translate("MainWindow", " Сообщение для отправки:"))
        self.textEdit_message.setHtml(_translate("MainWindow",
                                                 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                 "p, li { white-space: pre-wrap; }\n"
                                                 "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                                 "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; -qt-user-state:65536;\"><br /></p></body></html>"))
        self.pushButton_choose_file_for_mailing.setText(_translate("MainWindow", "Выбрать"))
        self.checkBox_use_file_for_message.setText(_translate("MainWindow", "Использоват файл для сообщения "))
        self.label_5.setText(
            _translate("MainWindow", "<html><head/><body><p>Необходимое колличество сообщений:</p></body></html>"))
        self.label_7.setText(
            _translate("MainWindow", "<html><head/><body><p>Задержка между отправкой в секундах:</p></body></html>"))
        self.checkBox_use_proxy.setText(_translate("MainWindow", "Использоват прокси"))
        self.checkBox_use_streams.setText(_translate("MainWindow", "Использовать несколько потоков"))
        self.label_12.setText(_translate("MainWindow", "Максимум сообщений с одного аккаунта: "))
        self.label.setText(_translate("MainWindow", "Файл с @user_name для рассылки:"))
        self.pushButton_check_user_name.setText(_translate("MainWindow", "Просмотр"))
        self.label_4.setText(_translate("MainWindow", "Консоль вывода:"))
        self.textEdit_conclusion.setHtml(_translate("MainWindow",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                                    "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_count_attempts.setText(_translate("MainWindow", "0"))
        self.label_13.setText(_translate("MainWindow", "количество попыток: "))
        self.label_banned_account.setText(_translate("MainWindow", "0"))
        self.label_sent_message.setText(_translate("MainWindow", "0"))
        self.label_unsuccessful.setText(_translate("MainWindow", "0"))
        self.label_remaining_message.setText(_translate("MainWindow", "0"))
        self.label_14.setText(_translate("MainWindow", "Забаненных аккаунтов:"))
        self.label_15.setText(_translate("MainWindow", "Отправленных сообщений: "))
        self.label_10.setText(_translate("MainWindow", "Осталось пользователей: "))
        self.label_16.setText(_translate("MainWindow", "Неудачных попыток: "))
        self.pushButton_start.setText(_translate("MainWindow", "ЗАПУСТИТЬ"))
        self.pushButton_clear_conclusion.setText(_translate("MainWindow", "Очистить\nконсоль"))
        self.action.setText(_translate("MainWindow", "сохранить"))
        self.action_2.setText(_translate("MainWindow", "добавить"))
        self.label_2.setText(_translate("MainWindow", "Количество:"))