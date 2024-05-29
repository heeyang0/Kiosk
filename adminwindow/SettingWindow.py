import sys

import mysql
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QApplication


class SettingWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("환경 설정")
        self.setGeometry(100, 100, 400, 300)
        main_layout = QVBoxLayout()
        self.sales_aggregate_button = QPushButton("판매집계", self)
        self.sales_aggregate_button.clicked.connect(self.show_sales_aggregate)

        self.change_manager_key_button = QPushButton("관리자비밀번호\n 변경", self)
        self.change_manager_key_button.clicked.connect(self.change_manager_key)

        self.prepare_for_business_button = QPushButton("영업 준비", self)
        self.prepare_for_business_button.clicked.connect(self.prepare_for_business)

        self.close_sales_button = QPushButton("판매 마감", self)
        self.close_sales_button.clicked.connect(self.close_sales)

        self.exit_button = QPushButton("나가기", self)
        self.exit_button.clicked.connect(self.go_close)

        main_layout.addWidget(self.sales_aggregate_button)
        main_layout.addWidget(self.change_manager_key_button)
        main_layout.addWidget(self.prepare_for_business_button)
        main_layout.addWidget(self.close_sales_button)
        main_layout.addWidget(self.exit_button)  # Add the exit button
        self.setLayout(main_layout)

    def go_close(self):
        from Admin_Main import AdminMainWindow
        AdminMain_Window = AdminMainWindow()
        AdminMain_Window.show()

    def show_sales_aggregate(self):
        # Implement functionality to show sales aggregate by date
        pass
    def prepare_for_business(self):
        pass
    def change_manager_key(self):
        new_key = self.new_manager_key_input.text()
        if not new_key:
            QMessageBox.warning(self, "경고", "새로운 관리자 비밀번호를 입력하세요.")
            return

        # 데이터베이스 연결
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="kiosk"
        )
        cursor = db_connection.cursor()

        # 새로운 관리자 키를 데이터베이스에 업데이트
        try:
            query = "UPDATE users SET managerkey = %s WHERE id = %s"
            cursor.execute(query, (new_key, self.user_id))
            db_connection.commit()
            QMessageBox.information(self, "성공", "새로운 관리자 비밀번호가 업데이트 되었습니다.")
        except mysql.connector.Error as err:
            print("에러:", err)
            QMessageBox.critical(self, "에러", "데이터베이스 업데이트 중 오류 발생.")
        finally:
            cursor.close()
            db_connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingWindow()
    window.show()
    sys.exit(app.exec_())
