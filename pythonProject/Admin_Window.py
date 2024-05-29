import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QGridLayout, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QThread
import requests
import json

class OrderManager(QWidget):
    def __init__(self, orders):
        super().__init__()
        self.orders = orders
        self.current_page = 0
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.nav_layout = QHBoxLayout()
        self.layout.addLayout(self.nav_layout)

        self.prev_button = QPushButton('이전')
        self.prev_button.clicked.connect(self.prev_page)
        self.nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton('다음')
        self.next_button.clicked.connect(self.next_page)
        self.nav_layout.addWidget(self.next_button)

        self.update_order_view()

    def update_order_view(self):
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)

        start_index = self.current_page * 6
        end_index = start_index + 6
        for i, order in enumerate(self.orders[start_index:end_index]):
            order_widget = self.create_order_widget(order)
            self.grid_layout.addWidget(order_widget, i // 3, i % 3)

    def create_order_widget(self, order):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        order_number_label = QLabel(f"주문 번호: {order['order_number']}")
        order_number_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(order_number_label)

        for item in order['cart']:
            item_label = QLabel(f"{item['name']} - {item['quantity']}개")
            layout.addWidget(item_label)

        total_price_label = QLabel(f"총 가격: {order['total_price']}원")
        layout.addWidget(total_price_label)

        call_button = QPushButton('호출')
        layout.addWidget(call_button)

        return widget

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_order_view()

    def next_page(self):
        if (self.current_page + 1) * 6 < len(self.orders):
            self.current_page += 1
            self.update_order_view()

class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('관리자 키오스크')
        self.setFixedSize(800, 600)

        self.orders = []

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.order_manager = OrderManager(self.orders)
        self.layout.addWidget(self.order_manager)

        self.load_orders()

    def load_orders(self):
        try:
            response = requests.get('http://localhost:5001/get_orders')
            if response.status_code == 200:
                self.orders = response.json()
                self.order_manager.orders = self.orders
                self.order_manager.update_order_view()
        except requests.RequestException as e:
            print(f"Error loading orders: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec_())
