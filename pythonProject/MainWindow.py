import json
import sys
import time


import mysql.connector
import pyttsx3
import speech_recognition as sr
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Normal import NormalWindow, get_menu_data_from_database  # Normal.py 파일에서 NormalWindow 클래스 import


class MainWindow(QMainWindow):
    def go_manager(self):
        from adminwindow.Admin_Main import AdminMainWindow
        self.manager_window = AdminMainWindow(username=self.username)
        self.manager_window.show()

    def __init__(self, username=None):
        super(MainWindow, self).__init__()
        self.setStyleSheet(u"Background-color:rgb(255, 255, 255);")
        self.setFixedSize(480, 830)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.username = username
        self.font = QFont()
        self.font.setFamily(u"Cafe24 Ssurround Bold")
        self.font.setPointSize(22)

        # 바탕이 되는 위젯 생성
        self.MainDisplay = QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(
            self.MainDisplay.sizePolicy().hasHeightForWidth())
        self.MainDisplay.setFixedSize(480, 830)
        self.setCentralWidget(self.MainDisplay)

        self.MainStackWidget = QStackedWidget(self.MainDisplay)
        self.MainStackWidget.setGeometry(QRect(0, 140, 480, 690))
        self.eat_where = None

        # 관리자 버튼 범위 시작##############################################
        def btnSetNHome(w, h, img):
            btn = QPushButton(self.MainDisplay)
            btn.setStyleSheet(
                f"QPushButton {{ background-image: url('{img}');"
                f"background-position: center;"
                f"background-repeat: no-repeat;"
                f"background-size: cover;}}")
            btn.setFixedSize(w, h)
            btn.setFlat(1)
            return btn

        self.SettingButton = btnSetNHome(40, 40, "img/UI/set.png")
        self.ButtonHome = btnSetNHome(60, 60, "img/UI/left.png")
        self.SettingButton.setGeometry(QRect(15, 75, 40, 40))
        self.ButtonHome.setGeometry(QRect(5, 60, 60, 60))

        self.SettingButton.clicked.connect(self.go_manager)
        self.ButtonHome.clicked.connect(self.go_home)
        self.ButtonHome.setHidden(True)
        # 관리자 버튼 범위 끝###############################################

        self.LabelWelcome = QLabel(self.MainDisplay)
        self.LabelWelcome.setFont(self.font)
        self.LabelWelcome.setAlignment(Qt.AlignCenter)
        self.LabelWelcome.setGeometry(QRect(70, 35, 250, 110))
        self.LabelWelcome.setText("쉽고 간편하게\n주문하세요")

        self.mixFrame = QFrame(self.MainDisplay)
        self.mixFrame.setGeometry(QRect(330, 70, 150, 70))
        self.LabelTextsize = QLabel(self.MainDisplay)
        self.LabelTextsize.setFont(QFont("Cafe24 Ssurround Bold", 20))
        self.LabelTextsize.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.LabelTextsize.setText("글씨 크기")
        self.LabelTextsize.setGeometry(QRect(330, 35, 150, 30))

        HlayoutTextsize = QHBoxLayout(self.mixFrame)

        def makezoom(text):
            btn = QPushButton(self.mixFrame)
            btn.setFixedSize(60, 60)
            btn.setSizePolicy(sizePolicy)
            btn.setStyleSheet(
                u"border: 1px solid rgba(0,0,0,0); border-radius: 16px; Background-color: rgb(255,126,0);font-weight:Bold; color: white; font-size: 90px;")
            btn.setText(text)
            return btn

        self.ButtonBig = makezoom("+")
        self.ButtonSmall = makezoom("-")

        HlayoutTextsize.addWidget(self.ButtonSmall)
        HlayoutTextsize.addWidget(self.ButtonBig)

        self.ButtonBig.clicked.connect(self.increase_font_size)
        self.ButtonSmall.clicked.connect(self.decrease_font_size)

        self.PageSelectWhere = QWidget(self.MainStackWidget)
        self.PageSelectWhere.setGeometry(QRect(0, 0, 480, 690))

        self.LabelSelectWhere = QLabel(self.PageSelectWhere)
        self.LabelSelectWhere.setFont(self.font)
        self.LabelSelectWhere.setGeometry(0, 30, 480, 90)
        self.LabelSelectWhere.setAlignment(Qt.AlignCenter)
        self.LabelSelectWhere.setText("식사 장소를 선택하세요")

        def BtnWhere(filename, text, eat_where=None):
            btn = QPushButton(self.PageSelectWhere)
            btn.setStyleSheet(f"QPushButton {{ background-image: url('img/Here&ToGo/{filename}');"
                              f"background-position: center; background-repeat: no-repeat; background-size: 50% 50% ; color: rgba(0,0,0,0); "
                              f"border-radius: 21px; border: 16px rgba(0,0,0,0);}}")
            btn.setMaximumSize(220, 500)
            btn.setFlat(True)
            btn.setText(text)
            btn.clicked.connect(lambda _, eat_where=eat_where: self.go_method(eat_where))
            return btn

        self.BtnHere = BtnWhere("Eat_Here.png", "먹고가기", "매장")
        self.BtnHere.setGeometry(20, 140, 210, 570)
        self.BtnTake = BtnWhere("Take_Out.png", "포장하기", "포장")
        self.BtnTake.setGeometry(250, 140, 210, 570)

        self.PageOrdermethod = QWidget(self.MainStackWidget)
        self.PageOrdermethod.setGeometry(0, 0, 480, 690)
        self.gridFrame = QFrame(self.PageOrdermethod)
        self.gridFrame.setGeometry(QRect(0, 100, 480, 590))
        self.LayoutOrdermethod = QGridLayout(self.gridFrame)
        self.LayoutOrdermethod.setVerticalSpacing(40)

        def makeOrderBtn(text, wid, hei, img):
            btn = QPushButton()
            btn.setFont(self.font)
            btn.setIcon(QIcon(f"img/UI/{img}"))
            btn.setIconSize(QSize(100, 100))
            btn.setStyleSheet(f"""
                QPushButton {{
                    border-radius: 16px; border: 2px solid rgba(0, 0, 0, 0);background-color: rgb(255, 126, 0);
                    color: rgb(255, 255, 255); padding-left: 30px;  /* 텍스트 위치 조정 */
                    text-align: left;  /* 텍스트를 왼쪽으로 정렬 */
                }}
                QPushButton::icon {{
                    position: absolute;
                    left: 10px;  /* 아이콘 위치 조정

                      }}
                QPushButton::icon {{
                    position: absolute;
                    left: 10px;  /* 아이콘 위치 조정 */
                }}
            """)
            btn.setText(text)
            btn.setFixedSize(wid, hei)
            return btn

        self.BtnChoboOdr = makeOrderBtn("쉬운 주문하기", 450, 130, "menu-easy.png")
        self.BtnRecOdr = makeOrderBtn("메뉴 추천", 450, 130, "menu-rec.png")
        self.BtnVoiceOdr = makeOrderBtn("음성 주문", 450, 130, "menu-voice.png")

        self.LayoutOrdermethod.addWidget(self.BtnChoboOdr, 0, 0)
        self.LayoutOrdermethod.addWidget(self.BtnVoiceOdr, 1, 0)
        self.LayoutOrdermethod.addWidget(self.BtnRecOdr, 2, 0)

        self.BtnChoboOdr.clicked.connect(self.go_normal_order)
        self.BtnVoiceOdr.clicked.connect(self.go_voice)
        self.BtnRecOdr.clicked.connect(self.go_recommend)

        self.LabelMethodSelect = QLabel(self.PageOrdermethod)
        self.LabelMethodSelect.setFont(self.font)
        self.LabelMethodSelect.setAlignment(Qt.AlignCenter)
        self.LabelMethodSelect.setText("주문 방법을 선택하세요")
        self.LabelMethodSelect.setGeometry(0, 15, 480, 90)

        self.MainStackWidget.addWidget(self.PageSelectWhere)
        self.MainStackWidget.addWidget(self.PageOrdermethod)
        self.MainStackWidget.setCurrentIndex(0)

        self.font_size = 22

    def increase_font_size(self):
        if self.font_size < 32:
            self.font_size += 1
            self.update_font()

    def decrease_font_size(self):
        if self.font_size > 16:
            self.font_size -= 1
            self.update_font()

    def update_font(self):
        self.font.setPointSize(self.font_size)
        self.LabelWelcome.setFont(self.font)
        self.LabelSelectWhere.setFont(self.font)
        self.LabelMethodSelect.setFont(self.font)
        self.BtnVoiceOdr.setFont(self.font)
        self.BtnRecOdr.setFont(self.font)
        self.BtnChoboOdr.setFont(self.font)

    def go_method(self, eat_where):
        self.eat_where = eat_where
        self.MainStackWidget.setCurrentWidget(self.PageOrdermethod)
        self.ButtonHome.setHidden(False)
        self.SettingButton.setHidden(True)
        print(f"선택된 식사 장소: {self.eat_where}")

    def go_home(self):
        self.MainStackWidget.setCurrentIndex(0)
        self.ButtonHome.setHidden(True)
        self.SettingButton.setHidden(False)
        self.EatWhere = ""

    def go_normal_order(self):
        menu_data = get_menu_data_from_database(self.username)
        self.normal_window = NormalWindow(username=self.username, menu_data=menu_data, EatWhere=self.eat_where)
        self.normal_window.show()

    def go_voice(self):
        menu_data = get_menu_data_from_database(self.username)
        self.voice_window = VoiceKiosk(username=self.username, menu_data=menu_data, EatWhere=self.eat_where)
        self.voice_window.show()

    def go_recommend(self):
        from Recommend import RecommandOrder
        menu_data = get_menu_data_from_database(self.username)
        self.recommend = RecommandOrder(username=self.username, menu_data=menu_data, EatWhere=self.eat_where)
        self.recommend.show()

class OrderNumberManager:
    def __init__(self):
        self.current_order_number = 1

    def generate_order_number(self):
        order_number = self.current_order_number
        self.current_order_number += 1
        return order_number

    def reset_order_number(self):
        self.current_order_number = 1

class VoiceKiosk(QWidget):

    def text_to_speech(self, text):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        engine.say(text)
        engine.runAndWait()

    def imgchange(self):
        if self.img_token == 0:
            self.activate_button.setStyleSheet(
                "QPushButton { background-image: url('img/UI/Voice_Off.png');"
                "background-position: center;"
                "background-repeat: no-repeat;"
                "background-size: cover; }"
            )
        else:
            self.activate_button.setStyleSheet(
                "QPushButton { background-image: url('img/UI/Voice_On.png');"
                "background-position: center;"
                "background-repeat: no-repeat;"
                "background-size: cover; }"
            )

    def activate_microphone(self):
        if not self.listening:
            self.listening = True
            self.LblVinfo.setText("1초 후에 음성 입력을 시작합니다.")
            self.repaint()
            time.sleep(1)
            self.img_token = 1
            self.imgchange()

            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                self.LblVinfo.setText("음성을 입력하세요...")
                self.text_to_speech("음성을 입력하세요.")

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
            self.img_token = 0
            self.imgchange()
            self.LblVinfo.setText("주문할 메뉴를 말씀해주세요.")

    def __init__(self, username, menu_data, EatWhere):
        super().__init__()
        self.listening = False
        self.payment_screen = None

        self.username = username
        self.menu_data = menu_data
        self.EatWhere = EatWhere
        self.setWindowTitle("음성 주문")
        self.setFixedSize(480, 830)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: rgb(255,255,255);")

        self.PageVoice = QWidget()
        self.PageVoice.setGeometry(0, 30, 480, 800)
        self.order_list = []

        self.LblVname = QLabel("음성 주문", self.PageVoice)
        self.LblVname.setGeometry(QRect(90, 40, 240, 60))

        # Add buttons to PageVoice widget
        self.activate_button = QToolButton(self.PageVoice)
        self.activate_button.setGeometry(QRect(180, 360, 120, 120))
        self.activate_button.setIcon(QIcon("img/UI/mic_inactive.png"))  # Set icon image
        self.activate_button.setIconSize(QSize(120, 120))  # Set icon size
        self.activate_button.clicked.connect(self.activate_microphone)

        self.back_button = QToolButton(self.PageVoice)
        self.back_button.setGeometry(10, 40, 60, 60)
        self.back_button.setIcon(QIcon("img/UI/left.png"))  # Set icon image
        self.back_button.setIconSize(QSize(60, 60))  # Set icon size
        self.back_button.clicked.connect(self.close)

        self.LblVinfo = QLabel("버튼을 누르고\n주문할 메뉴를 말씀해주세요.", self.PageVoice)
        self.LblVinfo.setAlignment(Qt.AlignCenter)
        self.LblVinfo.setGeometry(QRect(50, 110, 380, 100))

        self.back_button = QPushButton(self.PageVoice)
        self.back_button.setStyleSheet(
            "QPushButton { background-image: url('img/UI/left.png');"
            "background-position: center;"
            "background-repeat: no-repeat;"
            "background-size: cover; }"
        )
        self.back_button.setGeometry(10, 40, 60, 60)

        self.activate_button = QPushButton(self.PageVoice)
        self.img_token = 0
        self.imgchange()
        self.activate_button.setFlat(1)
        self.activate_button.clicked.connect(self.activate_microphone)
        self.activate_button.setGeometry(QRect(180, 360, 120, 120))

        self.order_label = QLabel("주문 목록:", self.PageVoice)
        self.order_label.setGeometry(QRect(10, 520, 70, 30))

        self.order_frame = QFrame(self.PageVoice)
        self.order_frame.setGeometry(QRect(10, 560, 450, 200))
        self.order_display = QVBoxLayout(self.order_frame)

        self.LblOrderTotal = QLabel("총 합계         0원", self.PageVoice)
        self.LblOrderTotal.setAlignment(Qt.AlignLeft)
        self.LblOrderTotal.setGeometry(QRect(10, 770, 340, 50))

        self.checkout_button = QPushButton("결제하기", self.PageVoice)
        self.checkout_button.setEnabled(False)
        self.checkout_button.clicked.connect(self.open_payment_screen)
        self.checkout_button.setGeometry(QRect(350, 770, 120, 50))

        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = "1234"
        self.db_database = "kiosk"

        self.db_connection = None

        self.connect_to_database()
        self.back_button.clicked.connect(self.close)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.PageVoice)

    def check_menu(self, user_input):
        if self.db_connection is None:
            QMessageBox.warning(self, "Connection Error", "Not connected to the database.")
            return False

        try:
            with self.db_connection.cursor() as cursor:
                sql = "SELECT * FROM menu WHERE name = %s"
                cursor.execute(sql, (user_input,))
                result = cursor.fetchone()
                if result:
                    menu_name = result[2]
                    menu_price_str = result[3]  # Get menu price as string
                    try:
                        menu_price = int(menu_price_str)  # Convert menu price to integer
                    except ValueError:
                        QMessageBox.warning(self, "Conversion Error",
                                            f"Error converting price: '{menu_price_str}' is not a valid integer.")
                        return False
                    self.order_list.append((menu_name, menu_price, 1))
                    print(f"{menu_name} - Price: {menu_price}원")
                    return True
                else:
                    return False
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "Query Error", f"Error executing query: {str(e)}")
            return False

    def update_order_display(self):
        total_amount = 0
        for i in reversed(range(self.order_display.count())):
            widget = self.order_display.itemAt(i).widget()
            if widget is not None:
                self.order_display.removeWidget(widget)
                widget.deleteLater()

        for item in self.order_list:
            menu_name, menu_price, quantity = item
            total_price = menu_price * quantity
            total_amount += total_price  # 항목의 총 가격을 합계에 추가
            menu_widget = QWidget()
            menu_layout = QHBoxLayout()

            menu_label = QLabel(f"{menu_name} ------- {total_price}원", self)
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
        self.LblOrderTotal.setText(f"총 합계         {total_amount}원")

    def adjust_quantity(self, item, quantity):
        index = None
        for i, order_item in enumerate(self.order_list):
            if order_item[0] == item[0]:
                index = i
                break

        if index is not None:
            if quantity == 0:
                del self.order_list[index]  # 수량이 0이면 해당 항목을 주문 목록에서 삭제
            else:
                self.order_list[index] = (item[0], item[1], quantity)  # 수량 업데이트
            self.update_order_display()  # 주문 목록 업데이트

    def open_payment_screen(self):
        from Voice_Payment import PaymentScreen
        self.payment_screen = PaymentScreen(order_number=123)
        self.payment_screen.set_cart(self.order_list)
        self.payment_screen.show()

    def connect_to_database(self):
        try:
            self.db_connection = mysql.connector.connect(host=self.db_host, user=self.db_user,
                                                         password=self.db_password, database=self.db_database)
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "연결 실패", f"데이터베이스 연결 중 오류 발생: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    username = "user"  # 사용자명을 직접 입력하거나 적절히 설정합니다.
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())  # 이벤트 루프 시작
