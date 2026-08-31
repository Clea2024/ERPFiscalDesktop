from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QFrame,
    QGridLayout,
    QVBoxLayout,
    QWidget,
)


class Card(QFrame):

    def __init__(self, titulo, valor):
        super().__init__()

        self.setStyleSheet("""
            QFrame{
                background:white;
                border:1px solid #DDDDDD;
                border-radius:10px;
            }
        """)

        layout = QVBoxLayout(self)

        lblTitulo = QLabel(titulo)
        lblTitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lblValor = QLabel(valor)
        lblValor.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lblValor.setStyleSheet("""
            font-size:32px;
            font-weight:bold;
            color:#1565C0;
        """)

        layout.addWidget(lblTitulo)
        layout.addWidget(lblValor)


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        layout = QGridLayout(self)

        layout.addWidget(Card("Empresas", "0"), 0, 0)
        layout.addWidget(Card("Usuários", "1"), 0, 1)
        layout.addWidget(Card("XML", "0"), 1, 0)
        layout.addWidget(Card("Certificados", "0"), 1, 1)