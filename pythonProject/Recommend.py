import logging
import sys
import mysql.connector
from functools import partial
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

logging.basicConfig(filename='app.log', level=logging.DEBUG)


class RecommandOrder(QMainWindow):
    def __init__(self, username=None,menu_data=None, EatWhere=None,parent=None):
        super(RecommandOrder, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle('메뉴 추천')
        self.selected_details = []
        self.menu_data = menu_data
        self.EatWhere = EatWhere

        self.PageRecommand = QWidget()
        self.username = username
        self.category_pages = None
        self.setup_ui()

        self.db_connection = self.connect_to_db()
        if self.db_connection:
            logging.info("데이터베이스에 성공적으로 연결되었습니다.")
            categories = self.fetch_categories_from_db()
            if categories:
                logging.info("카테고리를 성공적으로 불러왔습니다.")
                self.category_pages = QStackedWidget(self.PageRecommand)
                self.create_category_buttons(categories, self.category_pages)
            else:
                logging.error("카테고리를 불러오는데 실패했습니다.")
        else:
            logging.error("데이터베이스 연결에 실패했습니다.")

    def connect_to_db(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="kiosk"
            )
            logging.info("MySQL 데이터베이스에 성공적으로 연결되었습니다.")
            QMessageBox.information(self, "연결 성공", "MySQL 데이터베이스에 성공적으로 연결되었습니다.")
            return db
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "연결 실패", f"MySQL 데이터베이스 연결 중 오류 발생: {str(e)}")
            logging.error(f"MySQL 데이터베이스 연결 중 오류 발생: {str(e)}")
            return None

    def setup_ui(self):
        self.setFixedSize(480, 830)
        self.BaseWidget = QWidget(self)
        self.BaseWidget.setGeometry(0, 0, 480, 830)
        self.BaseWidget.setStyleSheet("background-color:rgb(255,255,255);")
        self.setCentralWidget(self.BaseWidget)
        self.RCOrderStackWidget = QStackedWidget(self.BaseWidget)
        self.RCOrderStackWidget.setGeometry(QRect(0, 110, 480, 720))
        self.RCOrderStackWidget.setStyleSheet("background-color:rgb(255,255,255);")
        self.Expendingsize = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.FontInfo = QFont()
        self.FontInfo.setFamily(u"Cafe24 Ssurround Bold")
        self.FontInfo.setPointSize(15)
        self.FontName = QFont()
        self.FontName.setFamily(u"Cafe24 Ssurround Bold")
        self.FontName.setPointSize(25)

        self.setup_detail_page()
        self.BtnGoHome = QPushButton(self.BaseWidget)
        self.BtnGoHome.setGeometry(10, 40, 60, 60)
        self.BtnGoHome.setText("집")

        self.LblIntro = QLabel(self.BaseWidget)
        self.LblIntro.setGeometry(QRect(90, 40, 240, 60))
        self.LblIntro.setAlignment(Qt.AlignCenter)
        self.LblIntro.setText("메뉴 추천")
        self.LblIntro.setFont(self.FontInfo)

        self.LblRCResult = QLabel(self.BaseWidget)
        self.LblRCResult.setGeometry(QRect(90, 40, 240, 60))
        self.LblRCResult.setAlignment(Qt.AlignCenter)
        self.LblRCResult.setFont(self.FontInfo)
        self.LblRCResult.setHidden(True)

        self.BtnZoomin = self.make_zoom_btn("-", 340, 40, 60, 60)
        self.BtnZoomout = self.make_zoom_btn("+", 410, 40, 60, 60)

        self.setup_category_page()
        self.setup_result_page()
        self.RCOrderStackWidget.addWidget(self.PageRecommand)
        self.RCOrderStackWidget.addWidget(self.PageDetail)
        self.RCOrderStackWidget.addWidget(self.PageResult)
        self.RCOrderStackWidget.setCurrentWidget(self.PageRecommand)

        self.BtnGoHome.clicked.connect(self.back_logic)

    def setup_detail_page(self):
        self.PageDetail = QWidget()
        self.PageDetail.setGeometry(QRect(0, 0, 480, 700))
        self.make_rec_btn()

        self.BtnCheckResult = QPushButton(self.PageRecommand)
        self.BtnCheckResult.setGeometry(QRect(100, 625, 280, 80))
        self.BtnCheckResult.setText("다        음")
        self.BtnCheckResult.setStyleSheet(
            "border-radius: 40px; border: 2px solid rgba(0,0,0,0); background-color: rgba(240,136,10,150); color: rgba(0,0,0,150)")
        self.BtnCheckResult.clicked.connect(self.go_detail_page)
        self.BtnCheckResult.setEnabled(False)

    def make_rec_btn(self):
        self.FrameRecBtn = QFrame(self.PageRecommand)
        self.FrameRecBtn.setGeometry(QRect(0, 0, 480, 700))

    def make_label(self, text, geometry, Vsize):
        label = QLabel(self.FrameRecBtn)
        label.setText(text)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(self.FontInfo)
        label.setStyleSheet("font-size: 40px;")
        label.setGeometry(0, geometry, 480, Vsize)
        return label

    def make_layout(self, geometry, ysize):
        frame = QFrame(self.FrameRecBtn)
        layout = QGridLayout()
        layout.setSpacing(20)
        frame.setLayout(layout)
        frame.setGeometry(15, geometry, 450, ysize)
        return frame, layout

    def fetch_categories_from_db(self):
        if not self.db_connection:
            print("No database connection available.")
            return []

        try:
            cursor = self.db_connection.cursor()
            sql = "SELECT DISTINCT category FROM menu WHERE username = %s"
            cursor.execute(sql, (self.username,))
            result = cursor.fetchall()
            categories = [row[0] for row in result]
            return categories
        except mysql.connector.Error as e:
            print(f"Failed to fetch categories: {e}")
            return []

    def create_category_buttons(self, categories, category_pages=None):
        if category_pages is None:
            category_pages = QStackedWidget(self.PageRecommand)
            category_pages.setGeometry(15, 200, 450, 410)

        num_pages = (len(categories) + 3) // 4
        pages = []

        for i in range(num_pages):
            page = QWidget()
            layout = QGridLayout()
            layout.setSpacing(20)
            page.setLayout(layout)
            pages.append(page)
            category_pages.addWidget(page)

        navigation_layout = QHBoxLayout()
        btn_prev = QPushButton("이전")
        btn_next = QPushButton("다음")
        btn_prev.clicked.connect(lambda: self.navigate_pages(category_pages, -1))
        btn_next.clicked.connect(lambda: self.navigate_pages(category_pages, 1))

        navigation_layout.addWidget(btn_prev)
        navigation_layout.addWidget(btn_next)

        main_layout = QVBoxLayout()
        main_layout.addWidget(category_pages)
        main_layout.addLayout(navigation_layout)
        self.PageRecommand.setLayout(main_layout)

        for i, category in enumerate(categories):
            btn = self.make_category_btn(category)
            page_index = i // 4
            row = (i % 4) // 2
            col = (i % 4) % 2
            pages[page_index].layout().addWidget(btn, row, col, 1, 1)
    def makeMenuBtn(self, text):
        btn = QPushButton(text)
        btn.setFont(self.FontName)
        btn.setFlat(True)
        btn.setSizePolicy(self.Expendingsize)
        btn.setStyleSheet(
            "border: 1px solid rgba(0,0,0,0); border-radius: 21px; background-color: rgba(255,126,0,200); color: rgb(255,255,255);")
        btn.clicked.connect(partial(self.category_btn_clicked, btn))
        return btn

    def make_category_btn(self, text):
        btn = QPushButton(text)
        btn.setFont(self.FontName)
        btn.setFlat(True)
        btn.setSizePolicy(self.Expendingsize)
        btn.setStyleSheet(
            "border: 1px solid rgba(0,0,0,0); border-radius: 21px; background-color: rgba(255,126,0,200); color: rgb(255,255,255);")
        btn.clicked.connect(partial(self.category_btn_clicked, btn))
        return btn

    def category_btn_clicked(self, btn):
        for button in self.PageRecommand.findChildren(QPushButton):
            if button != self.BtnCheckResult and button != self.BtnZoomin and button != self.BtnZoomout:
                button.setStyleSheet(
                    "border: 1px solid rgba(0,0,0,0); border-radius: 21px; background-color: rgba(255,126,0,200); color: rgb(255,255,255);")
        btn.setStyleSheet('border: 1px solid rgba(0,0,0,0); border-radius: 21px; background-color: rgb(255,126,0);')
        self.BtnCheckResult.setStyleSheet(
            "border-radius: 40px; border: 2px solid rgba(0,0,0,0); background-color: rgba(240,136,10,255); color: rgba(255,255,255,255)")
        self.BtnCheckResult.setEnabled(True)
        self.selectedCategory = btn.text()
        self.selectedDetails = []

    def navigate_pages(self, stacked_widget, direction):
        current_index = stacked_widget.currentIndex()
        new_index = current_index + direction
        if 0 <= new_index < stacked_widget.count():
            stacked_widget.setCurrentIndex(new_index)

    def go_detail_page(self):
        self.RCOrderStackWidget.setCurrentWidget(self.PageDetail)
        self.BtnGoHome.setText("뒤")
        self.LblRCResult.setHidden(True)
        self.LblIntro.setHidden(True)
        self.create_detail_buttons()

    def setup_category_page(self):
        self.PageRecommand = QWidget()
        self.PageRecommand.setGeometry(QRect(0, 0, 480, 700))
        self.BtnCheckResult = QPushButton(self.PageRecommand)
        self.BtnCheckResult.setGeometry(QRect(100, 625, 280, 80))
        self.BtnCheckResult.setText("다        음")
        self.BtnCheckResult.setStyleSheet(
            "border-radius: 40px; border: 2px solid rgba(0,0,0,0); background-color: rgba(240,136,10,150); color: rgba(0,0,0,150)")
        self.BtnCheckResult.setFont(self.FontInfo)
        self.BtnCheckResult.clicked.connect(self.go_detail_page)
        self.BtnCheckResult.setEnabled(False)

    def setup_result_page(self):
        self.PageResult = QWidget()
        self.PageResult.setGeometry(QRect(0, 0, 480, 700))
        self.resultLayout = QVBoxLayout(self.PageResult)
        self.resultLabel = QLabel("선택된 메뉴")
        self.resultLabel.setFont(self.FontInfo)
        self.resultLayout.addWidget(self.resultLabel)
        self.resultMenuLayout = QVBoxLayout()
        self.resultLayout.addLayout(self.resultMenuLayout)

        self.PageDetail = QWidget()
        self.PageDetail.setGeometry(QRect(0, 0, 480, 700))

    def create_detail_buttons(self):
        self.detailLayout = QVBoxLayout(self.PageDetail)
        self.detailTitle = QLabel("세부 사항 선택")
        self.detailTitle.setFont(self.FontInfo)
        self.detailLayout.addWidget(self.detailTitle)

        details = self.fetch_details_from_db(self.selectedCategory)
        self.detailButtons = []

        for detail in details:
            btn = self.make_detail_btn(detail)
            self.detailLayout.addWidget(btn)
            self.detailButtons.append(btn)
        for detail in details:
            btn = self.make_detail_btn(detail)
            self.detailLayout.addWidget(btn)
            self.detailButtons.append(btn)

        self.BtnCheckDetailResult = QPushButton(self.PageDetail)
        self.BtnCheckDetailResult.setGeometry(QRect(100, 625, 280, 80))
        self.BtnCheckDetailResult.setText("메뉴 확인 (0)")
        self.BtnCheckDetailResult.setStyleSheet(
            "border-radius: 40px; border: 2px solid rgba(0,0,0,0); background-color: rgba(240,136,10,150); color: rgba(0,0,0,150)")
        self.BtnCheckDetailResult.setFont(self.FontInfo)
        self.BtnCheckDetailResult.clicked.connect(self.go_result_page)  # 수정된 부분
        self.BtnCheckDetailResult.setEnabled(False)
        self.detailLayout.addWidget(self.BtnCheckDetailResult)
    def make_detail_btn(self, text):
        btn = QPushButton(text)
        btn.setFont(self.FontName)
        btn.setFlat(True)
        btn.setSizePolicy(self.Expendingsize)
        btn.setStyleSheet(
            "border: 1px solid rgba(0,0,0,0); border-radius: 21px; background-color: rgba(255,126,0,200); color: rgb(255,255,255);")
        btn.clicked.connect(partial(self.detail_btn_clicked, btn))
        return btn

    def detail_btn_clicked(self, btn):
        if btn.text() in self.selectedDetails:
            self.selectedDetails.remove(btn.text())
            btn.setStyleSheet(
                "border: 1px solid rgba(0,0,0,0); border-radius: 21px; background-color: rgba(255,126,0,200); color: rgb(255,255,255);")
        else:
            self.selectedDetails.append(btn.text())
            btn.setStyleSheet(
                "border: 1px solid rgba(0,0,0,0); border-radius: 21px; background-color: rgb(255,126,0);")
        filtered_menu_count = self.get_filtered_menu_count()
        self.BtnCheckDetailResult.setText(f"메뉴 확인 ({filtered_menu_count})")
        self.BtnCheckDetailResult.setEnabled(len(self.selectedDetails) > 0)

    def toggle_detail(self, category, detail):
        if detail in self.selected_details:
            self.selected_details.remove(detail)
        else:
            self.selected_details.append(detail)

    def show_filtered_menu(self):
        if not self.selected_category or not self.selected_details:
            print("카테고리와 디테일을 선택해주세요.")
            return

        print(f"카테고리: {self.selected_category}, 선택된 디테일: {self.selected_details}")

    def get_filtered_menu_count(self):
        if not self.db_connection:
            return 0

        try:
            cursor = self.db_connection.cursor()
            placeholders = ','.join(['%s'] * len(self.selectedDetails))
            sql = f"SELECT COUNT(*) FROM menu WHERE category = %s AND name IN ({placeholders})"
            cursor.execute(sql, (self.selectedCategory, *self.selectedDetails))
            result = cursor.fetchone()
            count = result[0] if result else 0
            return count
        except mysql.connector.Error as e:
            print(f"필터링된 메뉴 수를 가져오지 못했습니다: {e}")
            return 0

    def fetch_details_from_db(self, category):
        if not self.db_connection:
            print("No database connection available.")
            return []

        try:
            cursor = self.db_connection.cursor()
            sql = f"SELECT detail1, detail2, detail3, detail4, detail5 FROM menu WHERE category = '{category}' and username = '{self.username}'"
            cursor.execute(sql)
            result = cursor.fetchall()
            details = [detail for row in result for detail in row if detail]
            return details
        except mysql.connector.Error as e:
            print(f"Failed to fetch details: {e}")
            return []

    def go_result_page(self):
        self.RCOrderStackWidget.setCurrentWidget(self.PageResult)
        self.BtnGoHome.setText("뒤")
        self.LblRCResult.setHidden(False)
        self.LblIntro.setHidden(True)
        self.display_filtered_menus()

    def display_filtered_menus(self):
        for i in reversed(range(self.resultMenuLayout.count())):
            widget = self.resultMenuLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        menus = self.fetch_filtered_menus()
        for menu in menus:
            label = QLabel(menu)
            label.setFont(self.FontInfo)
            self.resultMenuLayout.addWidget(label)

    def fetch_filtered_menus(self):
        if not self.db_connection:
            return []

        try:
            cursor = self.db_connection.cursor()
            placeholders = ','.join(['%s'] * len(self.selectedDetails))
            sql = f"SELECT name FROM menu WHERE category = %s AND detail IN ({placeholders})"
            cursor.execute(sql, (self.selectedCategory, *self.selectedDetails))
            result = cursor.fetchall()
            menus = [row[0] for row in result]
            return menus
        except mysql.connector.Error as e:
            print(f"Failed to fetch filtered menus: {e}")
            return []

    def make_zoom_btn(self, text, x, y, w, h):
        btn = QPushButton(self.BaseWidget)
        btn.setGeometry(x, y, w, h)
        btn.setFixedSize(w, h)
        btn.setText(text)
        btn.setStyleSheet(
            "border: 1px solid rgba(0,0,0,0); border-radius: 16px; background-color: rgb(255,126,0); color: white; font-size: 70px;")
        return btn

    def back_logic(self):
        if self.RCOrderStackWidget.currentWidget() == self.PageRecommand:
            from MainWindow import MainWindow
            self.Main = MainWindow()
            self.Main.show()
            self.close()
        elif self.RCOrderStackWidget.currentWidget() == self.PageDetail:
            self.RCOrderStackWidget.setCurrentWidget(self.PageRecommand)
            self.BtnGoHome.setText("집")
            self.LblRCResult.setHidden(True)
            self.LblIntro.setHidden(False)
            self.selectedCategory = ""
            self.selectedDetails = []
        elif self.RCOrderStackWidget.currentWidget() == self.PageResult:
            self.RCOrderStackWidget.setCurrentWidget(self.PageDetail)
            self.BtnGoHome.setText("뒤")
            self.LblRCResult.setHidden(True)
            self.LblIntro.setHidden(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RecommandOrder(username='username')
    window.show()
    sys.exit(app.exec_())

