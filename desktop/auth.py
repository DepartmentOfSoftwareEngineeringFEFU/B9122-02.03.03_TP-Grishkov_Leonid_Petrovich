from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from api_client import APIClient


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.setWindowTitle("Вход в систему")
        self.setFixedSize(380, 260)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(12)

        title = QLabel("ERP Система")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #0067B8;")
        layout.addWidget(title)

        subtitle = QLabel("ООО «Экструзионное оборудование»")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 12px; color: #666;")
        layout.addWidget(subtitle)

        layout.addSpacerItem(QSpacerItem(0, 8, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        self.username_input.setStyleSheet("padding: 8px; font-size: 13px;")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 8px; font-size: 13px;")
        layout.addWidget(self.password_input)

        self.login_btn = QPushButton("Войти")
        self.login_btn.setStyleSheet(
            "QPushButton { background-color: #0067B8; color: white; padding: 10px; "
            "font-size: 14px; border-radius: 4px; } "
            "QPushButton:hover { background-color: #005299; }"
        )
        self.login_btn.clicked.connect(self.do_login)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

    def do_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        success, error = self.api_client.login(username, password)
        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка входа", error or "Неверный логин или пароль")

    def get_client(self):
        return self.api_client