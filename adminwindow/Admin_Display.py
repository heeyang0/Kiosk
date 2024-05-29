# Admin_Display.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel
from PyQt5.QtCore import Qt

class AdminDisplay(QMainWindow):
    def __init__(self, username=None, orders=None, parent=None):  # username을 추가합니다.
        super().__init__(parent)
        self.username = username  # 전달받은 username을 인스턴스 변수로 저장합니다.
        self.setWindowTitle('Admin Display')
        self.setGeometry(100, 100, 600, 400)

        # Central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)

        # Order grid layout
        self.order_grid = QGridLayout()
        main_layout.addLayout(self.order_grid)

        # Display orders if provided
        if orders:
            self.display_orders(orders)

    def display_orders(self, orders):
        for i, order in enumerate(orders):
            order_number = order.get('order_number', 'N/A')
            cart = order.get('cart', [])
            total_price = order.get('total_price', 'N/A')
            eat_where = order.get('EatWhere', 'N/A')

            # Create a widget for each order
            order_widget = QWidget()
            order_layout = QVBoxLayout()
            order_widget.setLayout(order_layout)

            # Add order details to the layout
            order_layout.addWidget(QLabel(f"Order Number: {order_number}"))
            for item in cart:
                order_layout.addWidget(QLabel(f"{item['name']} x {item['quantity']} - {item['price']}원"))
            order_layout.addWidget(QLabel(f"Total Price: {total_price}원"))
            order_layout.addWidget(QLabel(f"Eat Where: {eat_where}"))

            # Add order widget to the grid
            row = i // 2
            col = i % 2
            self.order_grid.addWidget(order_widget, row, col)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AdminDisplay()
    window.show()
    sys.exit(app.exec_())
