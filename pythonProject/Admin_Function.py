

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QIODevice, QByteArray, pyqtSignal, QBuffer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QLineEdit, QFileDialog, QMessageBox, QScrollArea, QGroupBox,
    QFormLayout, QListWidget, QDialog, QComboBox, QGridLayout, QListWidgetItem, QDialogButtonBox, QInputDialog
)
import sys
import mysql.connector

class AdminFunctionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = self.connect_database()  # 데이터베이스 연결
        self.setWindowTitle("매니저 창")
        self.setGeometry(100, 100, 800, 480)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)
        add_menu_button = QPushButton("메뉴 추가")
        add_menu_button.clicked.connect(self.add_menu)
        main_layout.addWidget(add_menu_button)
        delete_menu_button = QPushButton("메뉴 삭제")
        delete_menu_button.clicked.connect(self.delete_menu)
        main_layout.addWidget(delete_menu_button)
        update_menu_button = QPushButton("메뉴 수정")
        update_menu_button.clicked.connect(self.update_menu)
        main_layout.addWidget(update_menu_button)
        setting_button = QPushButton("환경 설정")
        setting_button.clicked.connect(self.go_to_settingwindow)
        main_layout.addWidget(setting_button)
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
            add_menu_window = AddMenuWindow(self.db)
            add_menu_window.exec_()
    def delete_menu(self):
        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute("SELECT name, category FROM menu")
                menus = cursor.fetchall()
                if menus:
                    delete_menu_window = DeleteMenuWindow(menus, self.db)
                    delete_menu_window.exec_()
                else:
                    QMessageBox.warning(self, "데이터 없음", "삭제할 메뉴가 없습니다.", QMessageBox.Ok)
            except mysql.connector.Error as e:
                QMessageBox.warning(self, "로드 실패", f"메뉴 목록 로드 중 오류 발생: {str(e)}")
            finally:
                cursor.close()

    def update_menu(self):
        if self.db:
            update_menu_window = UpdateMenuWindow(self.db)
            update_menu_window.exec_()

    def go_to_settingwindow(self):
        from adminwindow.SettingWindow import SettingWindow
        setting_window = SettingWindow()
        setting_window.exec_()


class AddMenuWindow(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("메뉴 추가")
        self.setGeometry(100, 100, 600, 400)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # 메뉴명 입력
        menu_name_label = QLabel("메뉴명:", self)
        main_layout.addWidget(menu_name_label)
        self.menu_name_entry = QLineEdit(self)
        main_layout.addWidget(self.menu_name_entry)

        # 메뉴 가격 입력
        menu_price_label = QLabel("메뉴 가격:", self)
        main_layout.addWidget(menu_price_label)
        self.menu_price_entry = QLineEdit(self)
        main_layout.addWidget(self.menu_price_entry)

        # 카테고리 선택
        category_label = QLabel("카테고리 선택:", self)
        main_layout.addWidget(category_label)
        self.category_combo = QComboBox(self)
        self.populate_categories()  # 데이터베이스에서 카테고리 가져오기
        main_layout.addWidget(self.category_combo)
        self.new_category_entry = QLineEdit(self)
        self.new_category_entry.setPlaceholderText("새 카테고리 입력")
        main_layout.addWidget(self.new_category_entry)

        self.add_category_button = QPushButton("카테고리 추가", self)
        self.add_category_button.clicked.connect(self.add_new_category)
        main_layout.addWidget(self.add_category_button)

        # 이미지 업로드
        self.image_preview_label = QLabel("이미지 미리보기", self)
        self.image_preview_label.setAlignment(Qt.AlignCenter)
        self.image_preview_label.setFixedSize(200, 200)
        main_layout.addWidget(self.image_preview_label)


        self.upload_button = QPushButton("이미지 업로드", self)
        self.upload_button.clicked.connect(self.upload_image)
        main_layout.addWidget(self.upload_button)

        # 디테일 입력
        self.detail_layout = QVBoxLayout()  # 디테일 레이아웃 초기화
        detail_group_box = QGroupBox("디테일 선택", self)
        detail_group_box.setLayout(self.detail_layout)
        main_layout.addWidget(detail_group_box)
        self.detail_buttons = []
        self.populate_details()  # 디테일 선택 버튼 생성
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

        # 추가 및 취소 버튼
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        cancel_button = QPushButton("취소", self)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)
        add_button = QPushButton("등록", self)
        add_button.clicked.connect(self.add_menu)
        button_layout.addWidget(add_button)

        # 이미지 업로드에 대한 미리보기 추가
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(200, 200)
        main_layout.addWidget(self.image_label)

    def add_new_detail(self):
        detail, ok = QInputDialog.getText(self, "새 디테일 입력", "새로운 디테일을 입력하세요:")
        if ok and detail.strip():
            # 입력된 디테일을 버튼으로 추가
            button = QPushButton(detail.strip(), self)
            button.setCheckable(True)
            self.detail_buttons.append(button)
            self.detail_layout.itemAt(self.detail_layout.count() - 2).layout().addWidget(button)  # + 버튼 이전에 추가

    def upload_image(self):
        # 파일 대화상자를 열어 이미지 파일 선택
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "이미지 업로드", "", "Image files (*.jpg *.png)")
        if file_path:
            # 선택한 이미지 파일 경로를 출력
            print("Selected image file:", file_path)
            # QPixmap으로 이미지 불러오기
            pixmap = QPixmap(file_path)
            # 이미지 미리보기 QLabel에 표시
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

        if not (menu_name and menu_price and menu_category and selected_details and self.image_label.pixmap()):
            QMessageBox.warning(self, "입력 오류", "모든 필수 항목을 입력하세요.", QMessageBox.Ok)
            return

        try:
            cursor = self.db.cursor()
            sql = "INSERT INTO menu (name, price, category, image, detail1, detail2, detail3, detail4, detail5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (
            menu_name, float(menu_price), menu_category, *selected_details, *[None] * (5 - len(selected_details)))
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
            cursor.execute("SELECT DISTINCT category FROM menu")
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
            cursor.execute(
                "SELECT detail1, detail2, detail3, detail4, detail5 FROM (SELECT DISTINCT detail1, detail2, detail3, detail4, detail5 FROM menu) AS unique_details ORDER BY detail1 ASC, detail2 ASC, detail3 ASC, detail4 ASC, detail5 ASC")
            rows = cursor.fetchall()  # 모든 행을 가져옴

            num_columns = 3  # 열의 수
            current_column = 0  # 현재 열 카운터
            current_row_layout = None  # 현재 행 레이아웃

            for row in rows:
                for detail in row:
                    if detail:
                        if current_column == 0:
                            # 새로운 행 레이아웃 생성
                            current_row_layout = QHBoxLayout()
                            self.detail_layout.addLayout(current_row_layout)

                        button = QPushButton(detail, self)
                        button.setCheckable(True)
                        self.detail_buttons.append(button)
                        current_row_layout.addWidget(button)  # 디테일 버튼을 현재 행에 추가

                        current_column += 1
                        if current_column == num_columns:
                            current_column = 0  # 열 카운터 초기화
                            current_row_layout = None  # 현재 행 레이아웃 초기화
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "로드 실패", f"디테일 목록 로드 중 오류 발생: {str(e)}")
        finally:
            cursor.fetchall()  # 모든 결과를 가져옴
            cursor.close()  # 커서를 닫음


class UpdateMenuWindow(QDialog):
    menu_updated = pyqtSignal()

    def __init__(self, db, menu_info=None):
        super().__init__()
        self.db = db
        self.menu_info = menu_info
        self.setWindowTitle("메뉴 수정")
        self.setGeometry(100, 100, 400, 300)

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # 전체 메뉴 목록 표시
        self.menu_list_widget = QListWidget(self)
        self.menu_list_widget.itemClicked.connect(self.show_menu_details)
        main_layout.addWidget(self.menu_list_widget)

        # 메뉴 디테일 편집용 레이아웃
        self.edit_menu_layout = QVBoxLayout()
        main_layout.addLayout(self.edit_menu_layout)

        self.edit_menu_widget = QWidget(self)
        self.edit_menu_widget.setLayout(self.edit_menu_layout)
        self.edit_menu_widget.hide()

        # 메뉴 목록 업데이트
        self.populate_menu_list()

    def populate_menu_list(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT name, price, category FROM menu")
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
        # 선택된 메뉴 정보 가져오기
        menu_name = item.text().split(" - ")[0]
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM menu WHERE name = %s", (menu_name,))
            menu_info = cursor.fetchone()
            if menu_info:
                # 메뉴 수정 UI 요소 생성
                update_menu_dialog = UpdateMenuDialog(self.db, menu_info)
                update_menu_dialog.exec_()  # 레이아웃을 활성화합니다.

                # 이미지 데이터 가져와서 미리보기 표시
                image_data = menu_info[4]  # 예시로 4번째 컬럼에 이미지 데이터가 있다고 가정합니다.
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
        # 메뉴명 입력
        menu_name_label = QLabel("메뉴명:", self)
        self.edit_menu_layout.addWidget(menu_name_label)
        self.menu_name_entry = QLineEdit(self)
        self.edit_menu_layout.addWidget(self.menu_name_entry)

        # 메뉴 가격 입력
        menu_price_label = QLabel("메뉴 가격:", self)
        self.edit_menu_layout.addWidget(menu_price_label)
        self.menu_price_entry = QLineEdit(self)
        self.edit_menu_layout.addWidget(self.menu_price_entry)

        # 카테고리 선택
        category_label = QLabel("카테고리 선택:", self)
        self.edit_menu_layout.addWidget(category_label)
        self.category_combo = QComboBox(self)
        self.populate_categories()  # 데이터베이스에서 카테고리 가져오기
        self.edit_menu_layout.addWidget(self.category_combo)

        # 이미지 업로드
        self.image_preview_label = QLabel("이미지 미리보기", self)
        self.image_preview_label.setAlignment(Qt.AlignCenter)
        self.image_preview_label.setFixedSize(200, 200)
        self.edit_menu_layout.addWidget(self.image_preview_label)
        self.upload_button = QPushButton("이미지 업로드", self)
        self.upload_button.clicked.connect(self.upload_image)  # 이 부분은 추가해야 할 부분입니다.
        self.edit_menu_layout.addWidget(self.upload_button)

        # 디테일 입력
        self.detail_layout = QVBoxLayout()  # 디테일 레이아웃 초기화
        detail_group_box = QGroupBox("디테일 선택", self)
        detail_group_box.setLayout(self.detail_layout)
        self.edit_menu_layout.addWidget(detail_group_box)
        self.detail_buttons = []
        self.populate_details()  # 디테일 선택 버튼 생성
        # 추가 및 수정 버튼
        button_layout = QHBoxLayout()
        self.edit_menu_layout.addLayout(button_layout)

        # 수정 버튼
        update_button = QPushButton("수정", self)
        update_button.clicked.connect(self.update_menu)
        button_layout.addWidget(update_button)

        # 취소 버튼
        cancel_button = QPushButton("취소", self)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        if menu_info:
            # 메뉴 정보가 주어진 경우 기존 정보를 UI에 표시
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
            sql = "UPDATE menu SET name = %s, price = %s, category = %s, image = %s WHERE name = %s"
            values = (menu_name, float(menu_price), menu_category, self.menu_info[1])
            cursor.execute(sql, values)
            self.db.commit()
            QMessageBox.information(self, "수정 완료", "메뉴가 수정되었습니다.", QMessageBox.Ok)
            self.menu_updated.emit()  # 메뉴가 수정되었음을 신호로 알림
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
            # 새로운 디테일 버튼 생성 및 레이아웃에 추가
            button = QPushButton(detail.strip(), self)
            button.setCheckable(True)
            self.detail_buttons.append(button)
            self.detail_layout.addWidget(button)

    def populate_details(self):
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "SELECT detail1, detail2, detail3, detail4, detail5 FROM (SELECT DISTINCT detail1, detail2, detail3, detail4, detail5 FROM menu) AS unique_details ORDER BY detail1 ASC, detail2 ASC, detail3 ASC, detail4 ASC, detail5 ASC")
            rows = cursor.fetchall()  # 모든 행을 가져옴

            num_columns = 3  # 열의 수
            current_column = 0  # 현재 열 카운터
            current_row_layout = None  # 현재 행 레이아웃

            for row in rows:
                for detail in row:
                    if detail:
                        if current_column == 0:
                            # 새로운 행 레이아웃 생성
                            current_row_layout = QHBoxLayout()
                            self.detail_layout.addLayout(current_row_layout)

                        button = QPushButton(detail, self)
                        button.setCheckable(True)
                        self.detail_buttons.append(button)
                        current_row_layout.addWidget(button)  # 디테일 버튼을 현재 행에 추가
                        current_column += 1
                        if current_column == num_columns:
                            current_column = 0  # 열 카운터 초기화
                            current_row_layout = None  # 현재 행 레이아웃 초기화
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "로드 실패", f"디테일 목록 로드 중 오류 발생: {str(e)}")
        finally:
            cursor.fetchall()  # 모든 결과를 가져옴
            cursor.close()  # 커서를 닫음

    def upload_image(self):
        # 이미지를 업로드하는 로직을 여기에 추가합니다.
        # 예를 들어, 파일 대화상자를 열어 사용자로부터 이미지 파일을 선택하고,
        # 선택한 이미지 파일의 경로를 얻어올 수 있습니다.
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "이미지 업로드", "", "Image files (*.jpg *.png)")
        if file_path:
            print("Selected image file:", file_path)
            pixmap = QPixmap(file_path)
            self.set_image_preview(pixmap)

    def set_image_preview(self, pixmap):
        # QPixmap 객체를 QLabel에 표시하기 위해 setPixmap 메서드를 사용합니다.
        self.image_preview_label.setPixmap(pixmap)

class UpdateMenuDialog(QDialog):
    menu_updated = pyqtSignal()

    def __init__(self, db, menu_info=None):
        super().__init__()
        self.db = db
        self.menu_info = menu_info
        self.setWindowTitle("메뉴 수정")
        self.setGeometry(100, 100, 400, 300)

        self.main_layout = QVBoxLayout(self)  # 여기를 수정했습니다.
        self.setLayout(self.main_layout)  # 여기를 수정했습니다.

        # 메뉴명 입력
        menu_name_label = QLabel("메뉴명:", self)
        self.main_layout.addWidget(menu_name_label)
        self.menu_name_entry = QLineEdit(self)
        self.main_layout.addWidget(self.menu_name_entry)

        # 메뉴 가격 입력
        menu_price_label = QLabel("메뉴 가격:", self)
        self.main_layout.addWidget(menu_price_label)
        self.menu_price_entry = QLineEdit(self)
        self.main_layout.addWidget(self.menu_price_entry)

        category_label = QLabel("카테고리 선택:", self)
        self.main_layout.addWidget(category_label)
        self.category_combo = QComboBox(self)
        self.populate_categories()  # 데이터베이스에서 카테고리 가져오기
        self.main_layout.addWidget(self.category_combo)

        self.add_category_button = QPushButton("카테고리 추가", self)
        self.add_category_button.clicked.connect(self.add_category)
        self.main_layout.addWidget(self.add_category_button)

        self.image_preview_label = QLabel(self)
        self.image_preview_label.setAlignment(Qt.AlignCenter)
        self.image_preview_label.setFixedSize(200, 200)
        self.main_layout.addWidget(self.image_preview_label)  # 여기를 수정했습니다.

        self.upload_button = QPushButton("이미지 업로드", self)
        self.upload_button.clicked.connect(self.upload_image)  # 이 부분은 추가해야 할 부분입니다.
        self.main_layout.addWidget(self.upload_button)

        # 디테일 입력
        self.detail_layout = QVBoxLayout()  # 디테일 레이아웃 초기화
        detail_group_box = QGroupBox("디테일 선택", self)
        detail_group_box.setLayout(self.detail_layout)
        self.main_layout.addWidget(detail_group_box)
        self.detail_buttons = []
        self.populate_details()  # 디테일 선택 버튼 생성

        self.add_detail_button = QPushButton("디테일 추가", self)
        self.add_detail_button.clicked.connect(self.add_detail)
        self.detail_layout.addWidget(self.add_detail_button)  # 디테일 추가 버튼 그룹 박스 안에 추가

        # 추가 및 수정 버튼
        button_layout = QHBoxLayout()
        self.main_layout.addLayout(button_layout)  # 여기를 수정했습니다.

        # 수정 버튼
        update_button = QPushButton("수정", self)
        update_button.clicked.connect(self.update_menu)
        button_layout.addWidget(update_button)

        # 취소 버튼
        cancel_button = QPushButton("취소", self)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        if menu_info:
            # 메뉴 정보가 주어진 경우 기존 정보를 UI에 표시
            self.menu_name_entry.setText(menu_info[1])
            self.menu_price_entry.setText(str(menu_info[2]))
            category_index = self.category_combo.findText(menu_info[3])
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
            # 새로운 디테일 버튼 생성 및 레이아웃에 추가
            button = QPushButton(detail.strip(), self)
            button.setCheckable(True)
            self.detail_buttons.append(button)
            self.detail_layout.addWidget(button)

    def populate_details(self):
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "SELECT detail1, detail2, detail3, detail4, detail5 FROM (SELECT DISTINCT detail1, detail2, detail3, detail4, detail5 FROM menu) AS unique_details ORDER BY detail1 ASC, detail2 ASC, detail3 ASC, detail4 ASC, detail5 ASC")
            rows = cursor.fetchall()  # 모든 행을 가져옴

            num_columns = 3  # 열의 수
            current_column = 0  # 현재 열 카운터
            current_row_layout = None  # 현재 행 레이아웃

            for row in rows:
                for detail in row:
                    if detail:
                        if current_column == 0:
                            # 새로운 행 레이아웃 생성
                            current_row_layout = QHBoxLayout()
                            self.detail_layout.addLayout(current_row_layout)

                        button = QPushButton(detail, self)
                        button.setCheckable(True)
                        self.detail_buttons.append(button)
                        current_row_layout.addWidget(button)  # 디테일 버튼을 현재 행에 추가
                        current_column += 1
                        if current_column == num_columns:
                            current_column = 0  # 열 카운터 초기화
                            current_row_layout = None  # 현재 행 레이아웃 초기화
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "로드 실패", f"디테일 목록 로드 중 오류 발생: {str(e)}")
        finally:
            cursor.fetchall()  # 모든 결과를 가져옴
            cursor.close()  # 커서를 닫음


    def upload_image(self):
        # 이미지를 업로드하는 로직을 여기에 추가합니다.
        # 예를 들어, 파일 대화상자를 열어 사용자로부터 이미지 파일을 선택하고,
        # 선택한 이미지 파일의 경로를 얻어올 수 있습니다.
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "이미지 업로드", "", "Image files (*.jpg *.png)")
        if file_path:
            # 파일 경로가 유효한 경우 이미지를 미리보기에 표시하거나 저장 등의 작업을 수행할 수 있습니다.
            # 여기서는 간단히 이미지 파일 경로를 출력합니다.
            print("Selected image file:", file_path)

    def set_image_preview(self, pixmap):
        self.image_preview_label.setPixmap(pixmap)

class DeleteMenuWindow(QDialog):
    def __init__(self, menus, db):
        super().__init__()
        self.setWindowTitle("메뉴 삭제")
        self.setGeometry(100, 100, 400, 300)
        self.menus = menus
        self.db = db

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
            menu_info = selected_item.text()  # Extracting menu name and category
            menu_name, category = menu_info.split(" (")
            category = category[:-1]  # Remove the closing parenthesis
            try:
                cursor = self.db.cursor()
                sql = "DELETE FROM menu WHERE name = %s AND category = %s"
                cursor.execute(sql, (menu_name, category))
                self.db.commit()
            except mysql.connector.Error as e:
                QMessageBox.warning(self, "삭제 실패", f"메뉴 삭제 중 오류 발생: {str(e)}")
            finally:
                cursor.close()

        QMessageBox.information(self, "삭제 완료", "선택한 메뉴가 삭제되었습니다.", QMessageBox.Ok)
        self.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin_window = AdminFunctionWindow()
    admin_window.show()
    sys.exit(app.exec_())
