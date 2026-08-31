from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)

from app.controllers.login_controller import LoginController


class LoginDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.controller = LoginController()

        self.controller.criar_admin()

        self.setWindowTitle("ERP Fiscal Desktop CE")

        self.setFixedSize(350,220)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Usuário"))

        self.txtLogin = QLineEdit()

        layout.addWidget(self.txtLogin)

        layout.addWidget(QLabel("Senha"))

        self.txtSenha = QLineEdit()

        self.txtSenha.setEchoMode(QLineEdit.Password)

        layout.addWidget(self.txtSenha)

        self.btEntrar = QPushButton("Entrar")

        layout.addWidget(self.btEntrar)

        self.btEntrar.clicked.connect(self.login)

    def login(self):

        usuario = self.controller.autenticar(
            self.txtLogin.text(),
            self.txtSenha.text()
        )

        if usuario:

            self.accept()

        else:

            QMessageBox.warning(
                self,
                "Login",
                "Usuário ou senha inválidos."
            )