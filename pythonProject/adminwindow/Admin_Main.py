import sys

import mysql
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import mysql.connector


def get_manager_key(username):
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="kiosk"
    )
    cursor = db_connection.cursor()

    # 사용자 이름을 기반으로 관리자 키 조회
    query = "SELECT managerkey FROM users WHERE username = %s"
    cursor.execute(query, (username,))

    result = cursor.fetchone()  # 하나의 레코드 가져오기
    manager_key = result[0] if result else None

    cursor.close()
    db_connection.close()

    return manager_key

class AdminMainWindow(QMainWindow):
    def __init__(self, username=None, parent=None):
        super(AdminMainWindow, self).__init__(parent)
        self.username = username
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)
        # 메인 텍스트 폰트
        self.mainlabelfont = QFont()
        self.mainlabelfont.setFamily(u"학교안심 우주 R")
        self.mainlabelfont.setPointSize(28)
        self.mainlabelfont.setWeight(50)

        # 버튼 폰트rmflrh
        self.pwNumfont = QFont()
        self.pwNumfont.setFamily(u"Noto Sans CJK KR Bold")
        self.pwNumfont.setPointSize(28)
        self.pwNumfont.setBold(True)
        self.pwNumfont.setWeight(75)

        # 비밀번호 폰트
        self.pwKeyfont = QFont()
        self.pwKeyfont.setFamily(u"Noto Sans CJK KR Medium")
        self.pwKeyfont.setPointSize(24)

        # 경고문 폰트
        self.warningfont = QFont()
        self.warningfont.setFamily(u"학교안심 우주 R")
        self.warningfont.setPointSize(13)
        self.warningfont.setBold(True)
        self.warningfont.setWeight(75)

        self.setWindowTitle("어드민 윈도우")
        self.setFixedSize(400, 600)
        self.currentPW = ""
        self.setupUI()
        self.AdminStackWidget.addWidget(self.PagePW)

        self.db = mysql.connector.connect(host='localhost', user='root', password='1234', database="kiosk")
        self.cursor = self.db.cursor()  # 커서 생성

        # 이 부분에서 self.manager_key를 초기화해야 합니다.
        self.manager_key = None  # manager_key 속성 초기화

    def setupUI(self)  :
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("Background-color: rgb(255, 255, 255);")
        self.centralwidget.setGeometry(QRect(0,0,400,600))
        self.AdminStackWidget = QStackedWidget(self.centralwidget)
        self.AdminStackWidget.setGeometry(QRect(0, 0, 400, 600))
        self.AdminStackWidget.setCurrentIndex(0)
        self.setupPWPage()

    def setupPWPage(self):
        self.PagePW = QWidget()
        self.PagePW.setObjectName(u"PagePW")
        self.verticalLayoutWidget_5 = QWidget(self.PagePW)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(0, 0, 400, 600))
        self.LayoutPW = QVBoxLayout(self.verticalLayoutWidget_5)
        self.LayoutPW.setSpacing(10)
        self.LayoutPW.setObjectName(u"LayoutPW")
        self.LayoutPW.setContentsMargins(0, 0, 0, 0)
        self.FramePW = QFrame(self.verticalLayoutWidget_5)
        self.FramePW.setObjectName(u"FramePW")
        self.FramePW.setStyleSheet(u"")
        self.FramePW.setFrameShape(QFrame.StyledPanel)
        self.FramePW.setFrameShadow(QFrame.Raised)

        self.LabelAdmin = QLabel(self.FramePW)
        self.LabelAdmin.setObjectName(u"LabelAdmin")
        self.LabelAdmin.setGeometry(QRect(0, 40, 400, 70))
        self.LabelAdmin.setFont(self.mainlabelfont)
        self.LabelAdmin.setAlignment(Qt.AlignCenter)
        self.LabelAdmin.setText("관리자 인증")

        self.setupGridLayout()
        self.setupQuitLabel()
        self.setupPWLabelButtons()

        self.LayoutPW.addWidget(self.FramePW)

    def setupGridLayout(self):
        self.gridLayoutWidget_5 = QWidget(self.FramePW)
        self.gridLayoutWidget_5.setObjectName(u"gridLayoutWidget_5")
        self.gridLayoutWidget_5.setGeometry(QRect(20, 240, 361, 341))
        self.GridPW = QGridLayout(self.gridLayoutWidget_5)
        self.GridPW.setSpacing(10)
        self.GridPW.setObjectName(u"GridPW")
        self.GridPW.setContentsMargins(5, 5, 5, 5)

    def setupQuitLabel(self):
        self.LabelQuit = QPushButton(self.FramePW)
        self.LabelQuit.setText("✕")
        self.LabelQuit.setObjectName(u"LabelQuit")
        self.LabelQuit.setGeometry(QRect(10, 10, 40, 30))
        self.LabelQuit.setFont(self.mainlabelfont)
        self.LabelQuit.setFlat(True)
        self.LabelQuit.clicked.connect(self.close)

    def setupPWLabelButtons(self):
        self.LabelWrongPW = QLabel(self.FramePW)
        self.LabelWrongPW.setObjectName(u"LabelWrongPW")
        self.LabelWrongPW.setGeometry(QRect(0, 110, 391, 20))
        self.LabelWrongPW.setFont(self.warningfont)
        self.LabelWrongPW.setStyleSheet(u"color:red;")
        self.LabelWrongPW.setAlignment(Qt.AlignCenter)
        self.LabelWrongPW.setText("잘못된 비밀번호입니다. 초기 비밀번호:1234")
        self.LabelWrongPW.setHidden(True)

        self.horizontalLayoutWidget_3 = QWidget(self.FramePW)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(29, 140, 340, 80))
        self.LayoutPWForm = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.LayoutPWForm.setSpacing(0)
        self.LayoutPWForm.setObjectName(u"LayoutPWForm")
        self.LayoutPWForm.setContentsMargins(10, 0, 10, 0)

        self.PWLabels = []
        for _ in range(4):
            pw_label = QLabel(self.FramePW)
            pw_label.setText("○")
            pw_label.setFont(self.pwKeyfont)
            pw_label.setAlignment(Qt.AlignCenter)
            self.PWLabels.append(pw_label)
            self.LayoutPWForm.addWidget(pw_label)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ButtonSubmit = QPushButton(self.FramePW)
        self.ButtonSubmit.setFont(self.mainlabelfont)
        self.ButtonSubmit.setStyleSheet(u"background-color:rgb(255, 255, 255);border: 2px solid rgb(0, 0, 0);")
        self.ButtonSubmit.setText("입력")

        self.ButtonDel = QPushButton(self.FramePW)
        self.ButtonDel.setObjectName(u"ButtonDel")
        self.ButtonDel.setFont(self.mainlabelfont)
        self.ButtonDel.setStyleSheet(u"background-color:rgb(255,255,255);border: 2px solid rgb(255, 0, 0);color: red;")
        self.ButtonDel.setText("삭제")

        sizePolicy.setHeightForWidth(self.ButtonDel.sizePolicy().hasHeightForWidth())
        sizePolicy.setHeightForWidth(self.ButtonSubmit.sizePolicy().hasHeightForWidth())
        self.ButtonDel.setSizePolicy(sizePolicy)
        self.ButtonSubmit.setSizePolicy(sizePolicy)

        self.ButtonDel.clicked.connect(self.clearPassword)
        self.ButtonSubmit.clicked.connect(self.checkPassword)

        button_texts = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.buttons = []
        for text in button_texts:
            button = QPushButton(text)
            self.buttons.append(button)
        for i, button in enumerate(self.buttons):
            setattr(self, f"Num{i}", button)
            button.setFont(self.pwNumfont)
            sizePolicy.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
            button.setSizePolicy(sizePolicy)
            button.setStyleSheet("background-color:rgb(255,255,255);border: 2px solid rgb(0, 0, 0);")
            button.setFlat(True)
        positions = [(3, 1), (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), (3, 2), (3, 0)]
        for i, button in enumerate(self.buttons):
            button.clicked.connect(lambda _, digit=i: self.addDigit(str(digit)))
        for widget, (row, col) in zip(self.buttons + [self.ButtonSubmit, self.ButtonDel], positions):
            self.GridPW.addWidget(widget, row, col, 1, 1)

    def addDigit(self, digit):
        if len(self.currentPW) < 4:  # 비밀번호 길이 제한
            self.currentPW += digit
            self.updatePWDisplay()

    def updatePWDisplay(self):
        for i, _ in enumerate(self.currentPW):
            self.PWLabels[i].setText("●")  # 입력된 길이만큼 ● 표시
        for i in range(len(self.currentPW), 4):
            self.PWLabels[i].setText("○")  # 남은 부분은 ○ 표시

    def checkPassword(self):
        manager_key = get_manager_key(self.username)

        print("Received username:", self.username)
        print("Received current password:", self.currentPW)
        if self.currentPW == manager_key:  # 사용자가 입력한 비밀번호와 데이터베이스에서 가져온 관리자 키 비교
            self.LabelWrongPW.setHidden(True)
            self.clearPassword()
            from Admin_Function import AdminFunctionWindow
            self.admin_function_window = AdminFunctionWindow(username=self.username, currentPW=self.currentPW)
            self.admin_function_window.show()
            self.close()
        else:
            self.LabelWrongPW.setHidden(False)
    def clearPassword(self):
        self.currentPW = ""  # 현재 입력된 비밀번호 초기화
        self.updatePWDisplay()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AdminMainWindow()
    window.show()
    sys.exit(app.exec_())
