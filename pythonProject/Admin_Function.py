

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import mysql.connector

class AdminFunctionWindow(QMainWindow):
    def __init__(self, username=None, currentPW=None, parent=None):
        super(AdminFunctionWindow, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.db = self.connect_database()
        self.setWindowTitle("매니저 창")
        self.username = username
        print("Received username:", self.username)
        self.currentPW = currentPW
        self.setGeometry(0, 0, 480, 830)
        self.setFixedSize(480,830)
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.setCentralWidget(self.central_widget)
        managerLabel = QLabel("관리자 메뉴",self)
        managerLabel.setFont(QFont("Noto Sans CJK KR Bold",30))
        managerLabel.setAlignment(Qt.AlignCenter)
        managerLabel.setGeometry(100,40,280,40)
        btnContainer = QFrame(self.central_widget)
        btnContainer.setGeometry(20,90,440,600)
        btnContainer.setFixedSize(440,600)
        btngrid = QGridLayout(btnContainer)
        btngrid.setVerticalSpacing(20)
        btngrid.setHorizontalSpacing(10)

        add_menu_button = self.create_button("ad-menuadd.png")
        add_menu_button.clicked.connect(self.add_menu)
        update_menu_button = self.create_button("ad-menuedit.png")
        update_menu_button.clicked.connect(self.update_menu)
        delete_menu_button = self.create_button("ad-menudel.png")
        delete_menu_button.clicked.connect(self.delete_menu)
        setting_button = self.create_button("ad-set.png")
        setting_button.clicked.connect(self.go_to_settingwindow)

        btngrid.addWidget(add_menu_button,0,0)
        btngrid.addWidget(update_menu_button,0,1)
        btngrid.addWidget(delete_menu_button,1,0)
        btngrid.addWidget(setting_button,1,1)

        exit_button = QPushButton("나       가       기",self)
        exit_button.setGeometry(30,710,420,90)
        exit_button.setStyleSheet("background-color: rgb(255,255,255);border: 4px solid rgb(255,136,0); color: rgb(255,136,0);")
        exit_button.setFont(QFont("Noto Sans CJK KR Black", 40))
        exit_button.clicked.connect(lambda: self.exit_admin_window(username))

    def create_button(self,image_path):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn = QPushButton()
        # 이미지를 버튼의 배경으로 설정하고, 이미지 크기를 버튼 크기에 맞게 조정
        btn.setSizePolicy(sizePolicy)
        btn.setStyleSheet(
            f"QPushButton {{ background-image: url('img/AdminSetup/{image_path}');"
            f"background-position: center;"
            f"background-repeat: no-repeat;"
            f"background-size: cover;"
            f" border-radius: 5px;  "
            f"border : 4px solid rgb(255,126,0)}}")
        btn.setFlat(True)
        return btn

    def exit_admin_window(self,username):
        self.close()  # 현재 창을 닫음
        self.open_main_window(username)  # MainWindow를 엶

    def open_main_window(self, username):
        from MainWindow import MainWindow
        self.main_window = MainWindow(username=username)  # MainWindow 인스턴스 생성
        self.main_window.show()  # MainWindow를 보여줌


    def connect_database(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="kiosk"
            )
            QMessageBox.information(self, "연결 성공", "MySQL 데이터베이스에 성공적으로 연결되었습니다.")
            return db
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "연결 실패", f"MySQL 데이터베이스 연결 중 오류 발생: {str(e)}")
            return None
    def add_menu(self):
        if self.db:
            add_menu_window = AddMenuWindow(self.username,self.db)
            add_menu_window.exec_()

    def delete_menu(self):
        if self.db:
            try:
                cursor = self.db.cursor()
                sql = "SELECT name, category FROM menu WHERE username = %s"
                cursor.execute(sql, (self.username,))
                menus = cursor.fetchall()
                delete_menu_window = DeleteMenuWindow(self.db, self.username, menus)
                delete_menu_window.exec_()
            except mysql.connector.Error as e:
                QMessageBox.warning(self, "오류", f"메뉴 목록을 가져오는 도중 오류가 발생했습니다: {str(e)}")
            finally:
                cursor.close()

    def update_menu(self):
        if self.db:
            update_menu_window = UpdateMenuWindow(self.db,self.username)
            update_menu_window.exec_()

    def go_to_settingwindow(self):
        from adminwindow.SettingWindow import SettingWindow
        setting_window = SettingWindow(self.username)
        setting_window.exec_()
class AddMenuWindow(QDialog):
    def __init__(self, username, db):
        super().__init__()
        self.db = db
        self.username = username
        self.setWindowTitle("메뉴 추가")
        self.setGeometry(100, 100, 600, 400)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        menu_name_label = QLabel("메뉴명:", self)
        main_layout.addWidget(menu_name_label)
        self.menu_name_entry = QLineEdit(self)
        main_layout.addWidget(self.menu_name_entry)
        menu_price_label = QLabel("메뉴 가격:", self)
        main_layout.addWidget(menu_price_label)
        self.menu_price_entry = QLineEdit(self)
        main_layout.addWidget(self.menu_price_entry)
        category_label = QLabel("카테고리 선택:", self)
        main_layout.addWidget(category_label)
        self.category_combo = QComboBox(self)
        self.populate_categories()
        main_layout.addWidget(self.category_combo)
        self.new_category_entry = QLineEdit(self)
        self.new_category_entry.setPlaceholderText("새 카테고리 입력")
        main_layout.addWidget(self.new_category_entry)
        self.add_category_button = QPushButton("카테고리 추가", self)
        self.add_category_button.clicked.connect(self.add_new_category)
        main_layout.addWidget(self.add_category_button)
        self.image_preview_label = QLabel("이미지 미리보기", self)
        self.image_preview_label.setAlignment(Qt.AlignCenter)
        self.image_preview_label.setFixedSize(200, 200)
        main_layout.addWidget(self.image_preview_label)
        self.upload_button = QPushButton("이미지 업로드", self)
        self.upload_button.clicked.connect(self.upload_image)
        main_layout.addWidget(self.upload_button)
        self.detail_layout = QVBoxLayout()
        detail_group_box = QGroupBox("디테일 선택", self)
        detail_group_box.setLayout(self.detail_layout)
        main_layout.addWidget(detail_group_box)
        self.detail_buttons = []
        self.populate_details()
        for i in range(3):
            row_layout = QHBoxLayout()
            self.detail_layout.addLayout(row_layout)
            for j in range(3):
                if self.detail_buttons:
                    button = self.detail_buttons.pop(0)
                    row_layout.addWidget(button)
        self.add_detail_button = QPushButton("+", self)
        self.add_detail_button.clicked.connect(self.add_new_detail)
        if row_layout is not None:
            row_layout.addWidget(self.add_detail_button)
        else:
            row_layout = QHBoxLayout()
            row_layout.addWidget(self.add_detail_button)
            self.detail_layout.addLayout(row_layout)
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        cancel_button = QPushButton("취소", self)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)
        add_button = QPushButton("등록", self)
        add_button.clicked.connect(self.add_menu)
        button_layout.addWidget(add_button)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(200, 200)
        main_layout.addWidget(self.image_label)
    def add_new_detail(self):
        detail, ok = QInputDialog.getText(self, "새 디테일 입력", "새로운 디테일을 입력하세요:")
        if ok and detail.strip():
            button = QPushButton(detail.strip(), self)
            button.setCheckable(True)
            self.detail_buttons.append(button)
            self.detail_layout.itemAt(self.detail_layout.count() - 2).layout().addWidget(button)
    def upload_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "이미지 업로드", "", "Image files (*.jpg *.png)")
        if file_path:
            print("Selected image file:", file_path)
            pixmap = QPixmap(file_path)
            self.image_preview_label.setPixmap(pixmap.scaled(200, 200))
    def add_new_category(self):
        new_category = self.new_category_entry.text().strip()
        if new_category:
            self.category_combo.addItem(new_category)
            self.new_category_entry.clear()
        else:
            QMessageBox.warning(self, "입력 오류", "새 카테고리 이름을 입력하세요.", QMessageBox.Ok)
    def add_menu(self):
        menu_name = self.menu_name_entry.text()
        menu_price = self.menu_price_entry.text()
        menu_category = self.category_combo.currentText()
        selected_details = [button.text() for button in self.detail_buttons if button.isChecked()]
        if not (menu_name and menu_price and menu_category and selected_details):
            QMessageBox.warning(self, "입력 오류", "모든 필수 항목을 입력하세요.", QMessageBox.Ok)
            return
        try:
            cursor = self.db.cursor()
            sql = "INSERT INTO menu (username, name, price, category, image, detail1, detail2, detail3, detail4, detail5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (
                self.username, menu_name, float(menu_price), menu_category, None, *selected_details,
                *[None] * (5 - len(selected_details))
            )
            cursor.execute(sql, values)
            self.db.commit()
            QMessageBox.information(self, "추가 완료", "메뉴가 추가되었습니다.", QMessageBox.Ok)
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "추가 실패", f"메뉴 추가 중 오류 발생: {str(e)}")
        finally:
            cursor.close()
            self.close()
    def populate_categories(self):
        try:
            cursor = self.db.cursor()
            sql = "SELECT DISTINCT category FROM menu WHERE username = %s"
            cursor.execute(sql, (self.username,))
            categories = cursor.fetchall()
            for category in categories:
                self.category_combo.addItem(category[0])
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "로드 실패", f"카테고리 목록 로드 중 오류 발생: {str(e)}")
        finally:
            cursor.close()
    def populate_details(self):
        try:
            cursor = self.db.cursor()
            sql = "SELECT detail1, detail2, detail3, detail4, detail5 FROM (SELECT DISTINCT detail1, detail2, detail3, detail4, detail5 FROM menu WHERE username = %s) AS unique_details ORDER BY detail1 ASC, detail2 ASC, detail3 ASC, detail4 ASC, detail5 ASC"
            cursor.execute(sql, (self.username,))
            rows = cursor.fetchall()
            num_columns = 3
            current_column = 0
            current_row_layout = None
            for row in rows:
                for detail in row:
                    if detail:
                        if current_column == 0:
                            current_row_layout = QHBoxLayout()
                            self.detail_layout.addLayout(current_row_layout)
                        button = QPushButton(detail, self)
                        button.setCheckable(True)
                        self.detail_buttons.append(button)
                        current_row_layout.addWidget(button)
                        current_column += 1
                        if current_column == num_columns:
                            current_column = 0
                            current_row_layout = None
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "로드 실패", f"디테일 목록 로드 중 오류 발생: {str(e)}")
        finally:
            cursor.fetchall()
            cursor.close()
class UpdateMenuWindow(QDialog):
    menu_updated = pyqtSignal()
    def __init__(self, db,username, menu_info=None):
        super().__init__()
        self.db = db
        self.username = username
        self.menu_info = menu_info
        self.setWindowTitle("메뉴 수정")
        self.setGeometry(100, 100, 400, 300)
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        self.menu_list_widget = QListWidget(self)
        self.menu_list_widget.itemClicked.connect(self.show_menu_details)
        main_layout.addWidget(self.menu_list_widget)
        self.edit_menu_layout = QVBoxLayout()
        main_layout.addLayout(self.edit_menu_layout)
        self.edit_menu_widget = QWidget(self)
        self.edit_menu_widget.setLayout(self.edit_menu_layout)
        self.edit_menu_widget.hide()
        self.populate_menu_list()

    def populate_menu_list(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT name, price, category FROM menu WHERE username = %s", (self.username,))
            menus = cursor.fetchall()
            for menu in menus:
                item_text = f"{menu[0]} - {menu[1]}원 ({menu[2]})"
                list_item = QListWidgetItem(item_text)
                self.menu_list_widget.addItem(list_item)
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "로드 실패", f"메뉴 목록 로드 중 오류 발생: {str(e)}")
        finally:
            cursor.close()

    def show_menu_details(self, item):
        menu_name = item.text().split(" - ")[0]
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM menu WHERE name = %s", (menu_name,))
            menu_info = cursor.fetchone()
            if menu_info:
                update_menu_dialog = UpdateMenuDialog(self.db, menu_info)
                update_menu_dialog.exec_()
                image_data = menu_info[4]
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                update_menu_dialog.set_image_preview(pixmap)
            else:
                QMessageBox.warning(self, "로드 실패", f"{menu_name} 메뉴 정보를 불러오는 데 실패했습니다.")
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "로드 실패", f"메뉴 정보 로드 중 오류 발생: {str(e)}")
        finally:
            cursor.close()
    def add_menu_ui_elements(self, menu_info=None):
        menu_name_label = QLabel("메뉴명:", self)
        self.edit_menu_layout.addWidget(menu_name_label)
        self.menu_name_entry = QLineEdit(self)
        self.edit_menu_layout.addWidget(self.menu_name_entry)
        menu_price_label = QLabel("메뉴 가격:", self)
        self.edit_menu_layout.addWidget(menu_price_label)
        self.menu_price_entry = QLineEdit(self)
        self.edit_menu_layout.addWidget(self.menu_price_entry)
        category_label = QLabel("카테고리 선택:", self)
        self.edit_menu_layout.addWidget(category_label)
        self.category_combo = QComboBox(self)
        self.populate_categories()
        self.edit_menu_layout.addWidget(self.category_combo)
        self.image_preview_label = QLabel("이미지 미리보기", self)
        self.image_preview_label.setAlignment(Qt.AlignCenter)
        self.image_preview_label.setFixedSize(200, 200)
        self.edit_menu_layout.addWidget(self.image_preview_label)
        self.upload_button = QPushButton("이미지 업로드", self)
        self.upload_button.clicked.connect(self.upload_image)
        self.edit_menu_layout.addWidget(self.upload_button)
        self.detail_layout = QVBoxLayout()
        detail_group_box = QGroupBox("디테일 선택", self)
        detail_group_box.setLayout(self.detail_layout)
        self.edit_menu_layout.addWidget(detail_group_box)
        self.detail_buttons = []
        self.populate_details()
        button_layout = QHBoxLayout()
        self.edit_menu_layout.addLayout(button_layout)
        update_button = QPushButton("수정", self)
        update_button.clicked.connect(self.update_menu)
        button_layout.addWidget(update_button)
        cancel_button = QPushButton("취소", self)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)
        if menu_info:
            self.menu_name_entry.setText(menu_info[1])
            self.menu_price_entry.setText(str(menu_info[2]))
            category_index = self.category_combo.findText(menu_info[3])
            if category_index != -1:
                self.category_combo.setCurrentIndex(category_index)
    def set_image_preview(self, pixmap):
        self.image_preview_label.setPixmap(pixmap)
    def update_menu(self):
        menu_name = self.menu_name_entry.text()
        menu_price = self.menu_price_entry.text()
        menu_category = self.category_combo.currentText()
        if not (menu_name and menu_price and menu_category):
            QMessageBox.warning(self, "입력 오류", "모든 필수 항목을 입력하세요.", QMessageBox.Ok)
            return
        if self.menu_info is None:
            QMessageBox.warning(self, "로드 실패", "메뉴 정보를 불러오는 데 실패했습니다.")
            return
        try:
            cursor = self.db.cursor()
            sql = "UPDATE menu SET name = '%s', price = '%s', category = '%s', image = '%s' WHERE name = '%s' and username = '%s'"
            values = (menu_name, float(menu_price), menu_category, self.menu_info[1],self.username)
            cursor.execute(sql, values)
            self.db.commit()
            QMessageBox.information(self, "수정 완료", "메뉴가 수정되었습니다.", QMessageBox.Ok)
            self.menu_updated.emit()
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "수정 실패", f"메뉴 수정 중 오류 발생: {str(e)}")
        finally:
            cursor.close()
    def populate_categories(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT DISTINCT category FROM menu")
            categories = cursor.fetchall()
            for category in categories:
                self.category_combo.addItem(category[0])
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "로드 실패", f"카테고리 목록 로드 중 오류 발생: {str(e)}")
        finally:
            cursor.close()
    def add_category(self):
        category, ok = QInputDialog.getText(self, "카테고리 추가", "추가할 카테고리 이름:")
        if ok and category.strip():
            self.category_combo.addItem(category.strip())
    def add_detail(self):
        detail, ok = QInputDialog.getText(self, "디테일 추가", "추가할 디테일 이름:")
        if ok and detail.strip():
            button = QPushButton(detail.strip(), self)
            button.setCheckable(True)
            self.detail_buttons.append(button)
            self.detail_layout.addWidget(button)
    def populate_details(self):
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "SELECT detail1, detail2, detail3, detail4, detail5 FROM (SELECT DISTINCT detail1, detail2, detail3, detail4, detail5 FROM menu) AS unique_details ORDER BY detail1 ASC, detail2 ASC, detail3 ASC, detail4 ASC, detail5 ASC")
            rows = cursor.fetchall()
            num_columns = 3
            current_column = 0
            current_row_layout = None
            for row in rows:
                for detail in row:
                    if detail:
                        if current_column == 0:
                            current_row_layout = QHBoxLayout()
                            self.detail_layout.addLayout(current_row_layout)
                        button = QPushButton(detail, self)
                        button.setCheckable(True)
                        self.detail_buttons.append(button)
                        current_row_layout.addWidget(button)
                        current_column += 1
                        if current_column == num_columns:
                            current_column = 0
                            current_row_layout = None
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "로드 실패", f"디테일 목록 로드 중 오류 발생: {str(e)}")
        finally:
            cursor.fetchall()
            cursor.close()
    def upload_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "이미지 업로드", "", "Image files (*.jpg *.png)")
        if file_path:
            print("Selected image file:", file_path)
            pixmap = QPixmap(file_path)
            self.set_image_preview(pixmap)
    def set_image_preview(self, pixmap):
        self.image_preview_label.setPixmap(pixmap)
class UpdateMenuDialog(QDialog):
    menu_updated = pyqtSignal()
    def __init__(self, db, menu_info=None):
        super().__init__()
        self.db = db
        self.menu_info = menu_info
        self.setWindowTitle("메뉴 수정")
        self.setGeometry(100, 100, 400, 300)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        menu_name_label = QLabel("메뉴명:", self)
        self.main_layout.addWidget(menu_name_label)
        self.menu_name_entry = QLineEdit(self)
        self.main_layout.addWidget(self.menu_name_entry)
        menu_price_label = QLabel("메뉴 가격:", self)
        self.main_layout.addWidget(menu_price_label)
        self.menu_price_entry = QLineEdit(self)
        self.main_layout.addWidget(self.menu_price_entry)
        category_label = QLabel("카테고리 선택:", self)
        self.main_layout.addWidget(category_label)
        self.category_combo = QComboBox(self)
        self.populate_categories()
        self.main_layout.addWidget(self.category_combo)
        self.add_category_button = QPushButton("카테고리 추가", self)
        self.add_category_button.clicked.connect(self.add_category)
        self.main_layout.addWidget(self.add_category_button)
        self.image_preview_label = QLabel(self)
        self.image_preview_label.setAlignment(Qt.AlignCenter)
        self.image_preview_label.setFixedSize(200, 200)
        self.main_layout.addWidget(self.image_preview_label)
        self.upload_button = QPushButton("이미지 업로드", self)
        self.upload_button.clicked.connect(self.upload_image)
        self.main_layout.addWidget(self.upload_button)
        self.detail_layout = QVBoxLayout()
        detail_group_box = QGroupBox("디테일 선택", self)
        detail_group_box.setLayout(self.detail_layout)
        self.main_layout.addWidget(detail_group_box)
        self.detail_buttons = []
        self.populate_details()
        self.add_detail_button = QPushButton("디테일 추가", self)
        self.add_detail_button.clicked.connect(self.add_detail)
        self.detail_layout.addWidget(self.add_detail_button)
        button_layout = QHBoxLayout()
        self.main_layout.addLayout(button_layout)
        update_button = QPushButton("수정", self)
        update_button.clicked.connect(self.update_menu)
        button_layout.addWidget(update_button)
        cancel_button = QPushButton("취소", self)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)
        if menu_info:
            self.menu_name_entry.setText(menu_info[2])
            self.menu_price_entry.setText(str(menu_info[2]))
            category_index = self.category_combo.findText(str(menu_info[3]))
            if category_index != -1:
                self.category_combo.setCurrentIndex(category_index)
    def update_menu(self):
        update_menu_dialog = UpdateMenuDialog(self.db, self.menu_info)
        update_menu_dialog.exec_()
    def populate_categories(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT DISTINCT category FROM menu")
            categories = cursor.fetchall()
            for category in categories:
                self.category_combo.addItem(category[0])
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "로드 실패", f"카테고리 목록 로드 중 오류 발생: {str(e)}")
        finally:
            cursor.close()
    def add_category(self):
        category, ok = QInputDialog.getText(self, "카테고리 추가", "추가할 카테고리 이름:")
        if ok and category.strip():
            self.category_combo.addItem(category.strip())
    def add_detail(self):
        detail, ok = QInputDialog.getText(self, "디테일 추가", "추가할 디테일 이름:")
        if ok and detail.strip():
            button = QPushButton(detail.strip(), self)
            button.setCheckable(True)
            self.detail_buttons.append(button)
            self.detail_layout.addWidget(button)
    def populate_details(self):
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "SELECT detail1, detail2, detail3, detail4, detail5 FROM (SELECT DISTINCT detail1, detail2, detail3, detail4, detail5 FROM menu) AS unique_details ORDER BY detail1 ASC, detail2 ASC, detail3 ASC, detail4 ASC, detail5 ASC")
            rows = cursor.fetchall()
            num_columns = 3
            current_column = 0
            current_row_layout = None
            for row in rows:
                for detail in row:
                    if detail:
                        if current_column == 0:
                            current_row_layout = QHBoxLayout()
                            self.detail_layout.addLayout(current_row_layout)
                        button = QPushButton(detail, self)
                        button.setCheckable(True)
                        self.detail_buttons.append(button)
                        current_row_layout.addWidget(button)
                        current_column += 1
                        if current_column == num_columns:
                            current_column = 0
                            current_row_layout = None
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "로드 실패", f"디테일 목록 로드 중 오류 발생: {str(e)}")
        finally:
            cursor.fetchall()
            cursor.close()
    def upload_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "이미지 업로드", "", "Image files (*.jpg *.png)")
        if file_path:
            print("Selected image file:", file_path)
    def set_image_preview(self, pixmap):
        self.image_preview_label.setPixmap(pixmap)
class DeleteMenuWindow(QDialog):
    def __init__(self, db, username, menus):
        super().__init__()
        self.setWindowTitle("메뉴 삭제")
        self.setGeometry(100, 100, 400, 300)
        self.db = db
        self.username = username
        self.menus = menus
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        self.menu_list_widget = QListWidget(self)
        for menu in menus:
            menu_name = menu[0]
            category = menu[1]
            item_text = f"{menu_name} ({category})"
            list_item = QListWidgetItem(item_text)
            self.menu_list_widget.addItem(list_item)
        main_layout.addWidget(self.menu_list_widget)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.confirm_delete)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

    def confirm_delete(self):
        selected_items = self.menu_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "선택 필요", "삭제할 메뉴를 선택해주세요.", QMessageBox.Ok)
            return
        confirm_message = "정말로 선택한 메뉴를 삭제하시겠습니까?"
        reply = QMessageBox.question(self, "삭제 확인", confirm_message, QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.delete_selected_menus()

    def delete_selected_menus(self):
        for selected_item in self.menu_list_widget.selectedItems():
            menu_info = selected_item.text()
            menu_name, category = menu_info.split(" (")
            category = category[:-1]
            try:
                cursor = self.db.cursor()
                sql = "DELETE FROM menu WHERE name = %s AND category = %s AND username = %s"
                cursor.execute(sql, (menu_name, category, self.username,))
                self.db.commit()
            except mysql.connector.Error as e:
                QMessageBox.warning(self, "삭제 실패", f"메뉴 삭제 중 오류 발생: {str(e)}")
            finally:
                cursor.close()
        QMessageBox.information(self, "삭제 완료", "선택한 메뉴가 삭제되었습니다.", QMessageBox.Ok)
        self.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    username = "user"
    admin_window = AdminFunctionWindow(username=username)
    admin_window.show()
    sys.exit(app.exec_())
