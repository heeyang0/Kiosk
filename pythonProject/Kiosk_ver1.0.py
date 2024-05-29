import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Ui_MainWindow(object):
    #세팅 버튼 클릭하면 관리자 메뉴 호출하고 기존 창은 그대로 냅둠
    def go_manager(self):
        from adminwindow import Manager
        self.manager_window = Manager.AdminWindow()
        self.manager_window.show()

    def setupUi(self, MainWindow):

        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setStyleSheet(u"Background-color:rgb(253, 255, 240);")
        MainWindow.setFixedSize(480,800)
        self.MainDisplay = QWidget(MainWindow)
        self.MainDisplay.setObjectName(u"MainDisplay")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainDisplay.sizePolicy().hasHeightForWidth())
        self.MainDisplay.setSizePolicy(sizePolicy)
        self.MainDisplay.setFixedSize(480,800)
        self.MainStackWidget = QStackedWidget(self.MainDisplay)
        self.MainStackWidget.setObjectName(u"MainStackWidget")
        self.MainStackWidget.setGeometry(QRect(0, 0, 480, 800))
        self.PagePlaceNMethod = QWidget()
        self.PagePlaceNMethod.setObjectName(u"PagePlaceNMethod")
        self.verticalLayoutWidget = QWidget(self.PagePlaceNMethod)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 480, 800))
        self.LayoutPlaceNMethod = QVBoxLayout(self.verticalLayoutWidget)
        self.LayoutPlaceNMethod.setObjectName(u"LayoutPlaceNMethod")
        self.LayoutPlaceNMethod.setContentsMargins(0, 0, 0, 0)
        self.LayoutWelcomeNSize = QHBoxLayout()
        self.LayoutWelcomeNSize.setObjectName(u"LayoutWelcomeNSize")
        self.LayoutSetting = QVBoxLayout()
        self.LayoutSetting.setObjectName(u"LayoutSetting")
        self.SettingButton = QPushButton(self.verticalLayoutWidget)
        self.SettingButton.setObjectName(u"SettingButton")
        icon = QIcon()
        icon.addFile(u":/AdminSetup/settings.png", QSize(), QIcon.Normal, QIcon.On)
        self.SettingButton.setIcon(icon)
        self.SettingButton.setIconSize(QSize(20, 20))

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        #관리자 설정 진입하는 버튼 배치
        self.LayoutSetting.addWidget(self.SettingButton)
        self.LayoutSetting.addItem(self.verticalSpacer)
        #세팅버튼 클릭시 관리자 페이지 호출
        self.SettingButton.clicked.connect(self.go_manager)



        self.LabelWelcome = QLabel(self.verticalLayoutWidget)
        self.LabelWelcome.setObjectName(u"LabelWelcome")
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(20)
        self.LabelWelcome.setFont(font)
        self.LabelWelcome.setAlignment(Qt.AlignCenter)


        self.VlayoutTextsize = QVBoxLayout()
        self.VlayoutTextsize.setObjectName(u"VlayoutTextsize")
        self.LabelTextsize = QLabel(self.verticalLayoutWidget)
        self.LabelTextsize.setObjectName(u"LabelTextsize")
        self.LabelTextsize.setFont(font)
        self.LabelTextsize.setAlignment(Qt.AlignCenter)

        self.VlayoutTextsize.addWidget(self.LabelTextsize)

        self.LayoutSizebutton = QHBoxLayout()
        self.LayoutSizebutton.setObjectName(u"LayoutSizebutton")
        self.ButtonBig = QPushButton(self.verticalLayoutWidget)
        self.ButtonBig.setObjectName(u"ButtonBig")
        palette = QPalette()
        brush = QBrush(QColor(253, 255, 240, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.ButtonBig.setPalette(palette)
        font1 = QFont()
        font1.setPointSize(35)
        self.ButtonBig.setFont(font1)
        self.ButtonBig.setStyleSheet(u"border-radius:15px;\n"
"border: 2px solid rgb(45, 45, 45);\n")

        self.LayoutSizebutton.addWidget(self.ButtonBig)

        self.ButtonSmall = QPushButton(self.verticalLayoutWidget)
        self.ButtonSmall.setObjectName(u"ButtonSmall")
        self.ButtonSmall.setFont(font1)
        self.ButtonSmall.setStyleSheet(u"border-radius:15px;\n"
"border: 2px solid rgb(45, 45, 45);\n")

        #레이아웃 중첩배치 및 레이아웃 사이 공간 추가
        self.LayoutSizebutton.addWidget(self.ButtonSmall)
        self.VlayoutTextsize.addLayout(self.LayoutSizebutton)
        self.LayoutWelcomeNSize.addLayout(self.LayoutSetting)
        self.LayoutWelcomeNSize.addStretch(1)
        self.LayoutWelcomeNSize.addWidget(self.LabelWelcome)
        self.LayoutWelcomeNSize.addStretch(1)
        self.LayoutWelcomeNSize.addLayout(self.VlayoutTextsize)


        self.LayoutPlaceNMethod.addLayout(self.LayoutWelcomeNSize)

        self.SWidgetPlaceNMethod = QStackedWidget(self.verticalLayoutWidget)
        self.SWidgetPlaceNMethod.setObjectName(u"SWidgetPlaceNMethod")
        self.PageSelectWhere = QWidget()
        self.PageSelectWhere.setObjectName(u"PageSelectWhere")
        self.verticalLayoutWidget_2 = QWidget(self.PageSelectWhere)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(-1, -1, 481, 691))
        self.VLayoutSelectWhere = QVBoxLayout(self.verticalLayoutWidget_2)
        self.VLayoutSelectWhere.setObjectName(u"VLayoutSelectWhere")
        self.VLayoutSelectWhere.setContentsMargins(0, 0, 0, 0)
        self.LabelSelectWhere = QLabel(self.verticalLayoutWidget_2)
        self.LabelSelectWhere.setObjectName(u"LabelSelectWhere")
        self.LabelSelectWhere.setFont(font)
        self.LabelSelectWhere.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.VLayoutSelectWhere.addWidget(self.LabelSelectWhere)

        self.LayoutWhereButton = QHBoxLayout()
        self.LayoutWhereButton.setObjectName(u"LayoutWhereButton")
        self.ButtonHere = QPushButton(self.verticalLayoutWidget_2)
        self.ButtonHere.setObjectName(u"ButtonHere")
        font2 = QFont()
        font2.setKerning(True)

        #먹고가기 버튼 디자인 정의
        self.ButtonHere.setFont(font2)
        self.ButtonHere.setCursor(QCursor(Qt.PointingHandCursor))
        self.ButtonHere.setStyleSheet(u"border-radius:15px;\n"
"border: 2px solid rgb(45, 45, 45);")
        icon1 = QIcon()
        icon1.addFile(u":/Here&ToGo/Eat_Here.png", QSize(), QIcon.Normal, QIcon.On)
        self.ButtonHere.setIcon(icon1)
        self.ButtonHere.setIconSize(QSize(190, 500))
        self.ButtonHere.setFixedSize(220,600)

        #테이크아웃 버튼 디자인 정의
        self.ButtonTakeout = QPushButton(self.verticalLayoutWidget_2)
        self.ButtonTakeout.setObjectName(u"ButtonTakeout")
        self.ButtonTakeout.setCursor(QCursor(Qt.PointingHandCursor))
        self.ButtonTakeout.setStyleSheet(u"border-radius:15px;\n"
"border: 2px solid rgb(45, 45, 45);\n")
        icon2 = QIcon()
        icon2.addFile(u":/Here&ToGo/Take_Out.png", QSize(), QIcon.Normal, QIcon.On)
        self.ButtonTakeout.setIcon(icon2)
        self.ButtonTakeout.setIconSize(QSize(190, 500))
        self.ButtonTakeout.setFixedSize(220,600)


        #버튼을 배치
        self.LayoutWhereButton.addWidget(self.ButtonHere)
        self.LayoutWhereButton.addWidget(self.ButtonTakeout)
        self.ButtonHere.clicked.connect(self.go_method)
        self.ButtonTakeout.clicked.connect(self.go_method)


        self.VLayoutSelectWhere.addLayout(self.LayoutWhereButton)

        self.SWidgetPlaceNMethod.addWidget(self.PageSelectWhere)
        self.PageOrdermethod = QWidget()
        self.PageOrdermethod.setObjectName(u"PageOrdermethod")
        self.gridLayoutWidget = QWidget(self.PageOrdermethod)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 480, 690))
        self.LayoutOrdermethod = QGridLayout(self.gridLayoutWidget)
        self.LayoutOrdermethod.setObjectName(u"LayoutOrdermethod")
        self.LayoutOrdermethod.setContentsMargins(0, 0, 0, 0)

        #초보용 주문 버튼 설정
        self.ButtonChoboOrder = QPushButton(self.gridLayoutWidget)
        self.ButtonChoboOrder.setObjectName(u"ButtonChoboOrder")
        font3 = QFont()
        font3.setFamily(u"Arial")
        font3.setPointSize(25)
        self.ButtonChoboOrder.setFont(font3)
        self.ButtonChoboOrder.setFixedSize(478,200)
        self.ButtonChoboOrder.setStyleSheet(u"border-radius:15px;\n"
"border: 2px solid rgb(45, 45, 45);\n")

        #메뉴 추천 버튼 설정
        self.ButtonReccomandOrder = QPushButton(self.gridLayoutWidget)
        self.ButtonReccomandOrder.setObjectName(u"ButtonReccomandOrder")
        self.ButtonReccomandOrder.setFont(font3)
        self.ButtonReccomandOrder.setFixedSize(478,200)
        self.ButtonReccomandOrder.setStyleSheet(u"border-radius:15px;\n"
"border: 2px solid rgb(45, 45, 45);\n")

        #음성 주문 버튼 설정
        self.ButtonVoiceOrder = QPushButton(self.gridLayoutWidget)
        self.ButtonVoiceOrder.setObjectName(u"ButtonVoiceOrder")
        self.ButtonVoiceOrder.setFont(font3)
        self.ButtonVoiceOrder.setFixedSize(478, 200)
        self.ButtonVoiceOrder.setStyleSheet(u"border-radius:15px;\n"
"border: 2px solid rgb(45, 45, 45);\n")

        #주문 버튼 배치
        self.LayoutOrdermethod.addWidget(self.ButtonChoboOrder, 1, 0, 1, 1)
        self.LayoutOrdermethod.addWidget(self.ButtonVoiceOrder, 2, 0, 1, 1)
        self.LayoutOrdermethod.addWidget(self.ButtonReccomandOrder, 3, 0, 1, 1)

        self.LabelMethodSelect = QLabel(self.gridLayoutWidget)
        self.LabelMethodSelect.setObjectName(u"LabelMethodSelect")
        font4 = QFont()
        font4.setPointSize(20)
        self.LabelMethodSelect.setFont(font4)
        self.LabelMethodSelect.setAlignment(Qt.AlignCenter)

        self.LayoutOrdermethod.addWidget(self.LabelMethodSelect, 0, 0, 1, 1)

        self.SWidgetPlaceNMethod.addWidget(self.PageOrdermethod)

        self.LayoutPlaceNMethod.addWidget(self.SWidgetPlaceNMethod)

        self.MainStackWidget.addWidget(self.PagePlaceNMethod)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.MainStackWidget.addWidget(self.page_2)
        MainWindow.setCentralWidget(self.MainDisplay)

        self.retranslateUi(MainWindow)

        self.SWidgetPlaceNMethod.setCurrentIndex(0)
        # 버튼에 기능 연결
        self.ButtonBig.clicked.connect(self.increase_font_size)
        self.ButtonSmall.clicked.connect(self.decrease_font_size)

        # 글꼴 크기 초기값 설정
        self.font_size = 20


    # 글씨 크기 늘리는 함수
    def increase_font_size(self):
        self.font_size += 2
        self.update_font()

    # 글씨 크기 줄이는 함수
    def decrease_font_size(self):
        self.font_size -= 2
        self.update_font()

    # 변경된 글씨 크기를 업데이트 시켜주는 함수
    def update_font(self):
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(self.font_size)
        self.LabelWelcome.setFont(font)
        self.LabelSelectWhere.setFont(font)
        self.LabelMethodSelect.setFont(font)
        self.ButtonBig.setFont(font)
        self.ButtonSmall.setFont(font)



        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.SettingButton.setText("")
        self.LabelWelcome.setText(QCoreApplication.translate("MainWindow", u"\ucd08\ubcf4\uc790\ub3c4\n"
"\uc27d\uace0 \uac04\ud3b8\ud558\uac8c\n"
"\uc8fc\ubb38\ud558\uc138\uc694", None))
        self.LabelTextsize.setText(QCoreApplication.translate("MainWindow", u"\uae00\uc528 \ud06c\uae30", None))
        self.ButtonBig.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.ButtonSmall.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.LabelSelectWhere.setText(QCoreApplication.translate("MainWindow", u"\uc2dd\uc0ac \ubc29\ubc95\uc744 \uc120\ud0dd\ud558\uc138\uc694", None))
        self.ButtonHere.setText("")
        self.ButtonTakeout.setText("")
        self.ButtonChoboOrder.setText(QCoreApplication.translate("MainWindow", u"\ucd08\ubcf4\uc6a9 \uc8fc\ubb38", None))
        self.ButtonReccomandOrder.setText(QCoreApplication.translate("MainWindow", u"\uba54\ub274 \ucd94\ucc9c", None))
        self.ButtonVoiceOrder.setText(QCoreApplication.translate("MainWindow", u"\uc74c\uc131 \uc8fc\ubb38", None))
        self.LabelMethodSelect.setText(QCoreApplication.translate("MainWindow", u"\uc8fc\ubb38 \ubc29\ubc95\uc744 \uc120\ud0dd\ud558\uc138\uc694", None))

    #페이지 넘기는 함수
    def go_method(self):
        currentpage = self.SWidgetPlaceNMethod.currentIndex()
        self.SWidgetPlaceNMethod.setCurrentIndex(currentpage+1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())