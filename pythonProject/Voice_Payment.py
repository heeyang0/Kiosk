#결제방법 선택화면

import sys
from socket import socket

from PyQt5.QtCore import QTimer, QSize, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QDialog
from PyQt5.QtGui import QIcon
from MainWindow import VoiceKiosk
import pyttsx3


class PaymentScreen(QDialog):
    def __init__(self, *args: object, **kwargs: object) -> object:
        super().__init__(*args, **kwargs)
        self.voice_kiosk = VoiceKiosk()
        self.setWindowTitle("키오스크 결제 화면")
        self.setGeometry(100, 100, 480, 800)
        self.font_size = 16
        self.cart = None
        self.selected_payment = None

        self.initUI()

    def set_cart(self, cart):
        self.cart = cart
    def showEvent(self, event):
        super().showEvent(event)

        QTimer.singleShot(100, self.activate_voice_guide)

    def activate_voice_guide(self):

        self.speak_instruction("결제 방법을 선택하세요.")

    def speak_instruction(self, instruction):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        engine.say(instruction)
        engine.runAndWait()

    def initUI(self):

        self.back_button = QPushButton("이전", self)
        self.back_button.setFixedSize(100, 50)
        self.back_button.setStyleSheet("font-size: 20px;")
        self.back_button.clicked.connect(self.back_button_clicked)


        self.font_increase_button = QPushButton("+", self)
        self.font_increase_button.clicked.connect(self.increase_font_size)
        self.font_increase_button.setFixedSize(50, 50)
        self.font_decrease_button = QPushButton("-", self)
        self.font_decrease_button.clicked.connect(self.decrease_font_size)
        self.font_decrease_button.setFixedSize(50, 50)


        self.menu_info_label = QLabel(self)
        self.menu_info_label.setStyleSheet("font-size: 12pt;")
        self.display_menu_info()


        font_button_layout = QHBoxLayout()
        font_button_layout.addWidget(self.font_increase_button)
        font_button_layout.addWidget(self.font_decrease_button)
        font_button_layout.setAlignment(Qt.AlignRight)


        self.label = QLabel("\n\n결제수단을 선택하세요\n", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: orange; font-family: 'Black Han Sans', sans-serif; font-weight: 400; font-size: {}pt; text-align: center;".format(self.font_size))


        self.card_payment_button = QPushButton("카드결제", self)
        self.card_payment_button.setIcon(QIcon("pic/card_icon.png"))
        self.card_payment_button.setIconSize(QSize(120, 160))
        self.card_payment_button.setStyleSheet("font-size: {}pt; height: 200px; background-color: white;".format(self.font_size))
        self.card_payment_button.clicked.connect(self.select_card_payment)


        self.counter_payment_button = QPushButton("카운터에서 결제", self)
        self.counter_payment_button.setIcon(QIcon("pic/counter_icon.png"))
        self.counter_payment_button.setIconSize(QSize(120, 160))
        self.counter_payment_button.setStyleSheet("font-size: {}pt; height: 200px; background-color: white;".format(self.font_size))
        self.counter_payment_button.clicked.connect(self.select_counter_payment)


        self.select_button = QPushButton("선택", self)
        self.select_button.setStyleSheet("background-color: orange; color: white; font-size: 16pt; border-radius: 20px;")
        self.select_button.clicked.connect(self.process_selection)
        self.select_button.setFixedSize(300, 50)


        button_layout = QHBoxLayout()
        button_layout.addWidget(self.card_payment_button)
        button_layout.addWidget(self.counter_payment_button)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.back_button)
        top_layout.addLayout(font_button_layout)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.label, alignment=Qt.AlignHCenter)
        main_layout.addWidget(self.menu_info_label, alignment=Qt.AlignHCenter)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.select_button, alignment=Qt.AlignHCenter)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

        self.update_font()



    def back_button_clicked(self):
        self.close()
        self.voice_kiosk = VoiceKiosk()
        self.voice_kiosk.show()



    def increase_font_size(self):
        self.font_size += 2
        self.update_font()

    def decrease_font_size(self):
        self.font_size -= 2
        self.update_font()

    def update_font(self):
        self.label.setStyleSheet("color: orange; font-family: 'Black Han Sans', sans-serif; font-weight: 400; font-size: {}pt; text-align: center;".format(self.font_size))
        self.card_payment_button.setStyleSheet("font-size: {}pt; height: 200px; background-color: white;".format(self.font_size))
        self.counter_payment_button.setStyleSheet("font-size: {}pt; height: 200px; background-color: white;".format(self.font_size))
        self.menu_info_label.setStyleSheet("font-size: {}pt;".format(self.font_size))  # 메뉴 정보 라벨의 글꼴 크기도 함께 업데이트

    def select_card_payment(self):
        self.selected_payment = "카드결제"
        self.card_payment_button.setStyleSheet("font-size: {}pt; height: 200px; background-color: orange;".format(self.font_size))
        self.counter_payment_button.setStyleSheet("font-size: {}pt; height: 200px; background-color: white;".format(self.font_size))

    def select_counter_payment(self):
        self.selected_payment = "카운터에서 결제"
        self.card_payment_button.setStyleSheet(
            "font-size: {}pt; height: 200px; background-color: white;".format(self.font_size))
        self.counter_payment_button.setStyleSheet(
            "font-size: {}pt; height: 200px; background-color: orange;".format(self.font_size))

    def process_selection(self):
        if self.selected_payment is None:
            QMessageBox.warning(self, "경고", "결제 방식을 선택해주세요.")
        else:
            if self.selected_payment == "카드결제":
                print("카드결제 화면으로 이동합니다.")
            elif self.selected_payment == "카운터에서 결제":
                print(" /d")
                self.close()

    def show_admin_window(self):
        pass
    def display_menu_info(self):

        menu_info = "메뉴 정보:\n"
        self.menu_info_label.setText(menu_info)  #

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaymentScreen()
    window.show()
    sys.exit(app.exec_())
