#메인 첫 화면
import importlib
import sys
import time

import mysql.connector
import pyttsx3
import speech_recognition as sr
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Normal import NormalWindow, get_menu_data_from_database  # Normal.py 파일에서 NormalWindow 클래스 import
# from Recommend import MenuWidget

class MainWindow(QMainWindow):


    def go_manager(self):
        from adminwindow.Admin_Main import AdminMainWindow
        self.manager_window = AdminMainWindow()
        self.manager_window.show()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setStyleSheet(u"Background-color:rgb(255, 255, 255);")
        self.setFixedSize(480, 800)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.MainDisplay = QWidget()
        self.MainDisplay.setObjectName(u"MainDisplay")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainDisplay.sizePolicy().hasHeightForWidth())
        self.MainDisplay.setSizePolicy(sizePolicy)
        self.MainDisplay.setFixedSize(480, 800)
        self.MainStackWidget = QStackedWidget(self.MainDisplay)
        self.MainStackWidget.setObjectName(u"MainStackWidget")
        self.MainStackWidget.setGeometry(QRect(0, 0, 480, 800))
        self.EatWhere = ""

        # 전체 큰 화면 위젯(메인)
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

        # 세팅버튼 및 홈버튼 정의
        self.SettingButton = QPushButton(self.verticalLayoutWidget)
        icon = QIcon()
        icon.addFile(u":/AdminSetup/settings.png", QSize(), QIcon.Normal, QIcon.On)
        self.SettingButton.setIcon(icon)
        self.SettingButton.setIconSize(QSize(20, 20))
        self.SettingButton.setFixedSize(30, 30)
        self.SettingButton.setFlat(1)

        self.ButtonHome = QPushButton(self.verticalLayoutWidget)
        iconBack = QIcon()
        iconBack.addFile(u":img/AdminSetup/left.png", QSize(), QIcon.Normal, QIcon.On)
        self.ButtonHome.setIcon(iconBack)
        self.ButtonHome.setFixedSize(50, 30)

        # 관리자 설정 진입하는 버튼 배치
        self.LayoutSetting.addWidget(self.SettingButton)
        self.LayoutSetting.addWidget(self.ButtonHome)

        # 세팅버튼 클릭시 관리자 페이지 호출
        self.SettingButton.clicked.connect(self.go_manager)
        # 홈버튼 클릭시 홈화면으로 복귀
        self.ButtonHome.clicked.connect(self.go_home)

        self.LabelWelcome = QLabel(self.verticalLayoutWidget)
        self.LabelWelcome.setObjectName(u"LabelWelcome")
        font = QFont()
        font.setFamily(u"학교안심 우주 R")
        font.setPointSize(25)
        self.LabelWelcome.setFont(font)
        self.LabelWelcome.setAlignment(Qt.AlignCenter)
        self.LabelWelcome.setMaximumSize(320, 100)
        self.LabelWelcome.setText("쉽고 간편하게\n주문하세요")

        self.VlayoutTextsize = QVBoxLayout()
        self.LabelTextsize = QLabel(self.verticalLayoutWidget)
        self.LabelTextsize.setFont(font)
        self.LabelTextsize.setAlignment(Qt.AlignCenter)
        self.LabelTextsize.setText("글씨 크기")

        self.VlayoutTextsize.addWidget(self.LabelTextsize)

        self.LayoutSizebutton = QHBoxLayout()
        self.LayoutSizebutton.setObjectName(u"LayoutSizebutton")
        self.ButtonBig = QPushButton(self.verticalLayoutWidget)
        self.ButtonBig.setObjectName(u"ButtonBig")
        self.ButtonBig.setFixedSize(62, 62)
        sizemodifyfont = QFont()
        sizemodifyfont.setFamily(u"Noto Sans CJK KR Bold")
        sizemodifyfont.setPointSize(40)
        self.ButtonBig.setFont(sizemodifyfont)
        self.ButtonBig.setStyleSheet(u"border-radius:15px;\n"
                                     "border: 2px solid rgb(45, 45, 45);\n""color: rgb(255,127,0)")

        self.LayoutSizebutton.addWidget(self.ButtonBig)

        self.ButtonSmall = QPushButton(self.verticalLayoutWidget)
        self.ButtonSmall.setObjectName(u"ButtonSmall")
        self.ButtonSmall.setFont(sizemodifyfont)
        self.ButtonSmall.setStyleSheet(u"border-radius:15px;\n"
                                       "border: 2px solid rgb(45, 45, 45);\n""color: rgb(255,127,0)")
        self.ButtonSmall.setFixedSize(62, 62)
        self.ButtonBig.setText("+")
        self.ButtonSmall.setText("−")
        # 레이아웃 중첩배치 및 레이아웃 사이 공간 추가
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
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 0, 480, 690))
        self.VLayoutSelectWhere = QVBoxLayout(self.verticalLayoutWidget_2)
        self.VLayoutSelectWhere.setObjectName(u"VLayoutSelectWhere")
        self.VLayoutSelectWhere.setContentsMargins(0, 0, 0, 0)
        self.LabelSelectWhere = QLabel(self.verticalLayoutWidget_2)
        self.LabelSelectWhere.setObjectName(u"LabelSelectWhere")
        self.LabelSelectWhere.setFont(font)
        self.LabelSelectWhere.setMaximumSize(480, 40)
        self.LabelSelectWhere.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.LabelSelectWhere.setText("식사 장소를 선택하세요")
        self.VLayoutSelectWhere.addWidget(self.LabelSelectWhere)

        self.LayoutWhereButton = QHBoxLayout()
        self.LayoutWhereButton.setObjectName(u"LayoutWhereButton")

        def BtnWhere(filename, text):
            btn = QPushButton()
            btn.setStyleSheet(f"QPushButton {{ background-image: url('img/Here&ToGo/{filename}');"
                              f"background-position: center; background-repeat: no-repeat; background-size: contain; }}")
            btn.setMaximumSize(220, 600)
            btn.setFlat(True)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setText(text)
            btn.clicked.connect(self.go_method)
            return btn

        self.BtnHere = BtnWhere("Eat_Here.png", "먹고가기")  # 먹고가기 버튼 디자인 정의
        self.BtnTake = BtnWhere("Take_Out.png", "포장하기")  # 테이크아웃 버튼 디자인 정의

        # 버튼을 배치
        self.LayoutWhereButton.addWidget(self.BtnHere)
        self.LayoutWhereButton.addWidget(self.BtnTake)

        self.VLayoutSelectWhere.addLayout(self.LayoutWhereButton)

        self.SWidgetPlaceNMethod.addWidget(self.PageSelectWhere)
        self.PageOrdermethod = QWidget()
        self.gridLayoutWidget = QWidget(self.PageOrdermethod)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 480, 690))
        self.LayoutOrdermethod = QGridLayout(self.gridLayoutWidget)
        self.LayoutOrdermethod.setObjectName(u"LayoutOrdermethod")
        self.LayoutOrdermethod.setContentsMargins(0, 0, 0, 0)

        def makeOrderBtn(text, wid, hei):
            # 버튼 생성을 함수로 정의(생성될 레이아웃,가로,세로 크기)
            btn = QPushButton()
            btn.setFont(font)
            btn.setStyleSheet(u"border-radius:15px; border: 2px solid rgb(45, 45, 45);")
            btn.setText(text)
            btn.setFixedSize(wid, hei)
            return btn

        self.BtnChoboOdr = makeOrderBtn("쉬운 주문하기", 470, 180)  # 초보용 주문 버튼 설정
        self.BtnRecOdr = makeOrderBtn("메뉴 추천", 470, 180)  # 메뉴 추천 버튼 설정
        self.BtnVoiceOdr = makeOrderBtn("음성 주문", 470, 180)  # 음성 주문 버튼 설정

        # 주문 버튼 배치
        self.LayoutOrdermethod.addWidget(self.BtnChoboOdr, 1, 0)
        self.LayoutOrdermethod.addWidget(self.BtnVoiceOdr, 2, 0)
        self.LayoutOrdermethod.addWidget(self.BtnRecOdr, 3, 0)

        # 각 주문별 버튼입력 시 페이지 전환
        self.BtnChoboOdr.clicked.connect(self.go_normal_order)
        self.BtnVoiceOdr.clicked.connect(self.go_voice)
        self.BtnRecOdr.clicked.connect(self.go_recommend)

        self.LabelMethodSelect = QLabel(self.gridLayoutWidget)
        self.LabelMethodSelect.setObjectName(u"LabelMethodSelect")
        self.LabelMethodSelect.setFont(font)
        self.LabelMethodSelect.setAlignment(Qt.AlignCenter)
        self.LabelMethodSelect.setText("주문 방법을 선택하세요")

        self.LayoutOrdermethod.addWidget(self.LabelMethodSelect, 0, 0)
        self.SWidgetPlaceNMethod.addWidget(self.PageOrdermethod)
        self.LayoutPlaceNMethod.addWidget(self.SWidgetPlaceNMethod)


        self.MainStackWidget.addWidget(self.PagePlaceNMethod)



        self.setCentralWidget(self.MainDisplay)

        self.SWidgetPlaceNMethod.setCurrentIndex(0)
        # 버튼에 기능 연결
        self.ButtonBig.clicked.connect(self.increase_font_size)
        self.ButtonSmall.clicked.connect(self.decrease_font_size)

        # 글꼴 크기 초기값 설정
        self.font_size = 25
# 글씨 크기 늘리는 함수
    def increase_font_size(self):
        self.font_size += 1
        self.update_font()

    # 글씨 크기 줄이는 함수
    def decrease_font_size(self):
        self.font_size -= 1
        self.update_font()

    # 변경된 글씨 크기를 업데이트 시켜주는 함수
    def update_font(self):
        font = QFont()
        font.setFamily("학교안심 우주 R")
        font.setPointSize(self.font_size)
        self.LabelWelcome.setFont(font)
        self.LabelSelectWhere.setFont(font)
        self.LabelMethodSelect.setFont(font)
        self.BtnVoiceOdr.setFont(font)
        self.BtnRecOdr.setFont(font)
        self.BtnChoboOdr.setFont(font)

    def go_method(self):
        # 페이지 넘기는 함수
        self.SWidgetPlaceNMethod.setCurrentWidget(self.PageOrdermethod)

    def go_home(self):
        # 홈으로 보내는 함수
        self.MainStackWidget.setCurrentIndex(0)
        self.SWidgetPlaceNMethod.setCurrentIndex(0)
        self.EatWhere = ""

    def go_normal_order(self):
        self.close()
        menu_data = get_menu_data_from_database()
        self.normal_window = NormalWindow(menu_data)
        self.normal_window.show()

    def go_voice(self):
        self.close()
        self.voice_window = VoiceKiosk()
        self.voice_window.show()

    def go_recommend(self):
        self.close()
        pass


class VoiceKiosk(QMainWindow):
    def backtoMain(self):
        self.close()
        self.mainwindow = MainWindow()
        self.mainwindow.show()

    def activate_microphone(self):
        if not self.listening:
            self.listening = True
            self.activate_button.setText("음성 입력 중지")
            self.label.setText("1초 후에 음성 입력을 시작합니다.")
            self.repaint()
            time.sleep(1)

            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                self.label.setText("음성을 입력하세요...")
                self.repaint()
                audio_data = recognizer.listen(source)
                try:
                    user_input = recognizer.recognize_google(audio_data, language='ko-KR')
                    if self.check_menu(user_input):
                        self.update_order_display()
                        QMessageBox.information(self, "주문 추가", f"{user_input}을(를) 주문에 추가하였습니다.")
                        self.checkout_button.setEnabled(True)
                    else:
                        QMessageBox.warning(self, "주문 실패", "죄송합니다. 해당 메뉴가 없습니다.")
                except sr.UnknownValueError:
                    QMessageBox.warning(self, "음성 인식 실패", "음성을 인식할 수 없습니다.")
            self.listening = False
            self.activate_button.setText("음성 입력 시작")
            self.label.setText("키오스크가 주문할 메뉴를 말씀해주세요.")

    def speak_instruction(self, instruction):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        engine.say(instruction)
        engine.runAndWait()

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(200, self.activate_voice_guide)

    def activate_voice_guide(self):

        self.speak_instruction("키오스크가 주문할 메뉴를 말씀해주세요.")

    def __init__(self):
        super().__init__()
        self.listening = False

        self.setWindowTitle("음성 주문 키오스크")
        self.setGeometry(100, 100, 480, 800)
        self.order_list = []

        layout = QVBoxLayout()

        self.label = QLabel("키오스크가 주문할 메뉴를 말씀해주세요.", self)
        self.label.setFont(QFont("Arial", 14))
        layout.addWidget(self.label)

        self.activate_button = QPushButton("음성 입력 시작", self)
        self.activate_button.clicked.connect(self.activate_microphone)
        layout.addWidget(self.activate_button)

        self.order_label = QLabel("주문 목록:", self)
        self.order_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.order_label)

        self.order_display = QVBoxLayout()
        layout.addLayout(self.order_display)

        self.checkout_button = QPushButton("결제하기", self)
        self.checkout_button.setEnabled(False)
        self.checkout_button.clicked.connect(self.open_payment_screen)
        layout.addWidget(self.checkout_button)

        self.back_button = QPushButton("", self)
        self.back_button.setIcon(QIcon("back_icon.png"))
        self.back_button.setIconSize(self.back_button.sizeHint())
        self.back_button.setMaximumSize(20, 50)
        layout.addWidget(self.back_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = "1234"
        self.db_database = "kiosk"

        self.db_connection = None

        self.connect_to_database()
        self.back_button.clicked.connect(self.backtoMain)

    def check_menu(self, user_input):
        if self.db_connection is None:
            QMessageBox.warning(self, "연결 실패", "데이터베이스에 연결되어 있지 않습니다.")
            return False

        try:
            with self.db_connection.cursor() as cursor:
                sql = "SELECT * FROM menu WHERE name = %s"
                cursor.execute(sql, (user_input,))
                result = cursor.fetchone()
                if result:
                    menu_name = result[1]
                    menu_price = result[2]
                    self.order_list.append((menu_name, menu_price, 1))
                    print(f"{menu_name} - 가격: {menu_price}원")
                    return True
                else:
                    return False
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "쿼리 실패", f"쿼리 실행 중 오류 발생: {str(e)}")
            return False

    def update_order_display(self):

        for i in reversed(range(self.order_display.count())):
            widget = self.order_display.itemAt(i).widget()
            if widget is not None:
                self.order_display.removeWidget(widget)
                widget.deleteLater()

        for item in self.order_list:
            menu_name, menu_price, quantity = item
            total_price = menu_price * quantity
            menu_widget = QWidget()
            menu_layout = QHBoxLayout()

            menu_label = QLabel(f"{menu_name} , 총 가격: {total_price}원", self)
            menu_layout.addWidget(menu_label)

            minus_button = QPushButton("-", self)
            minus_button.clicked.connect(lambda _, q=quantity, i=item: self.adjust_quantity(i, q - 1))
            menu_layout.addWidget(minus_button)

            quantity_label = QLabel(str(quantity), self)
            menu_layout.addWidget(quantity_label)

            plus_button = QPushButton("+", self)
            plus_button.clicked.connect(lambda _, q=quantity, i=item: self.adjust_quantity(i, q + 1))
            menu_layout.addWidget(plus_button)
            menu_widget.setLayout(menu_layout)
            self.order_display.addWidget(menu_widget)

    def adjust_quantity(self, item, new_quantity):
        index = self.order_list.index(item)
        if new_quantity > 0:
            self.order_list[index] = (item[0], item[1], new_quantity)
            self.update_order_display()
        else:
            del self.order_list[index]
            self.update_order_display()

    def open_payment_screen(self):
        import Voice_Payment
        payment_screen = Voice_Payment.PaymentScreen()
        payment_screen.exec_()

    def connect_to_database(self):
        try:
            self.db_connection = mysql.connector.connect(host=self.db_host, user=self.db_user,
                                                         password=self.db_password, database=self.db_database)
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "연결 실패", f"데이터베이스 연결 중 오류 발생: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())  # 이벤트 루프 시작