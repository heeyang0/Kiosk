import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QListWidget, QListWidgetItem, QLabel, \
    QMessageBox, QLineEdit, QPushButton, QComboBox, QHBoxLayout


def get_menu_data_from_database():
    menu_data = {}
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="kiosk"
        )
        if db:
            print("데이터베이스 연결 성공!")
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT name, price, category, detail1, detail2, detail3, detail4, detail5 FROM menu")
            rows = cursor.fetchall()
            print("데이터를 가져왔습니다:")
            for row in rows:
                print(row)
                name = row["name"]
                price = row["price"]
                category = row["category"]
                detail1 = row["detail1"]
                detail2 = row["detail2"]
                detail3 = row["detail3"]
                detail4 = row["detail4"]
                detail5 = row["detail5"]
                if category not in menu_data:
                    menu_data[category] = []
                menu_data[category].append({"name": name, "price": price, "detail1": detail1, "detail2": detail2, "detail3": detail3, "detail4": detail4, "detail5": detail5})
            cursor.close()
            db.close()
    except mysql.connector.Error as e:
        print(f"데이터베이스 연결 실패: {str(e)}")
    return menu_data

class MenuWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("키오스크 추천 메뉴")
        self.layout = QVBoxLayout()

        # 데이터베이스에서 메뉴 데이터 가져오기
        self.menu_data = get_menu_data_from_database()

        # 필터링을 위한 검색 입력창과 버튼 추가
        self.filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("검색어 입력")
        self.filter_layout.addWidget(self.search_input)
        self.filter_button = QPushButton("검색")
        self.filter_button.clicked.connect(self.filter_menu)
        self.filter_layout.addWidget(self.filter_button)
        self.layout.addLayout(self.filter_layout)

        # 카테고리 필터링을 위한 콤보 박스 추가
        self.category_combo = QComboBox()
        self.category_combo.addItem("전체 카테고리")
        self.category_combo.addItems(self.menu_data.keys())
        self.category_combo.currentTextChanged.connect(self.filter_menu)
        self.filter_layout.addWidget(self.category_combo)

        # 탭 위젯 생성
        self.tab_widget = QTabWidget(self)
        for category, items in self.menu_data.items():
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)
            list_widget = QListWidget(tab)
            for item in items:
                list_item = QListWidgetItem(f"{item['name']} - 가격: {item['price']}원", list_widget)
                list_widget.addItem(list_item)
            list_widget.itemClicked.connect(self.show_item_detail)  # 아이템 클릭 시 세부 정보 표시
            tab_layout.addWidget(list_widget)
            self.tab_widget.addTab(tab, category)

        self.layout.addWidget(self.tab_widget)
        self.setLayout(self.layout)

    def show_item_detail(self, item):
        # 클릭된 아이템의 세부 정보 표시
        detail = ""
        for key, value in item.detail.items():
            detail += f"{key}: {value}\n"
        QMessageBox.information(self, "아이템 세부 정보", detail)

    def filter_menu(self):
        # 검색어, 카테고리로 메뉴 필터링
        search_text = self.search_input.text().strip()
        category_text = self.category_combo.currentText()

        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            list_widget = tab.layout().itemAt(0).widget()
            for j in range(list_widget.count()):
                list_item = list_widget.item(j)
                item_text = list_item.text()
                if (search_text.lower() not in item_text.lower() and search_text) or \
                        (category_text != "전체 카테고리" and category_text not in item_text):
                    list_item.setHidden(True)
                else:
                    list_item.setHidden(False)


if __name__ == "__main__":
    app = QApplication([])
    menu_widget = MenuWidget()
    menu_widget.show()
    app.exec_()
