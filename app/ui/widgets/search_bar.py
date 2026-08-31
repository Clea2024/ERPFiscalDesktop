from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)


class SearchBar(QWidget):

    searchRequested = Signal(str)
    clearRequested = Signal()

    def __init__(
        self,
        placeholder="Pesquisar...",
        parent=None,
    ):

        super().__init__(parent)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel("Pesquisar:")

        self.txtPesquisa = QLineEdit()

        self.txtPesquisa.setPlaceholderText(
            placeholder
        )

        self.btPesquisar = QPushButton("Pesquisar")

        self.btLimpar = QPushButton("Limpar")

        layout.addWidget(lbl)
        layout.addWidget(self.txtPesquisa, 1)
        layout.addWidget(self.btPesquisar)
        layout.addWidget(self.btLimpar)

        ############################################################

        self.btPesquisar.clicked.connect(
            self.emitir_pesquisa
        )

        self.btLimpar.clicked.connect(
            self.limpar
        )

        self.txtPesquisa.returnPressed.connect(
            self.emitir_pesquisa
        )

    ############################################################

    def texto(self):

        return self.txtPesquisa.text().strip()

    ############################################################

    def emitir_pesquisa(self):

        self.searchRequested.emit(
            self.texto()
        )

    ############################################################

    def limpar(self):

        self.txtPesquisa.clear()

        self.clearRequested.emit()