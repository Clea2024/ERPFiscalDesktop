from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class DashboardCard(QFrame):

    def __init__(
        self,
        titulo,
        valor="0",
        cor="#7B1E3A",
        fundo="#FFFFFF",
        parent=None,
    ):

        super().__init__(parent)

        self.setFrameShape(
            QFrame.StyledPanel
        )

        self.setMinimumHeight(
            125
        )

        self.setMaximumHeight(
            145
        )
        
        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: {fundo};
                border: 2px solid #2E7D32;
                border-radius: 12px;
            }}

            QLabel#titulo {{
                font-size: 15px;
                font-weight: bold;
                color: #444444;
                border: none;
                background: transparent;
            }}

            QLabel#valor {{
                font-size: 26px;
                font-weight: bold;
                color: #1F3A5F;
                border: none;
                background: transparent;
            }}
            """
        )
        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            14,
            8,
            14,
            8,
        )

        layout.setSpacing(
            4
        )

        self.lblTitulo = QLabel(
            titulo
        )

        self.lblTitulo.setObjectName(
            "titulo"
        )

        self.lblTitulo.setAlignment(
            Qt.AlignCenter
        )

        self.lblValor = QLabel(
            valor
        )

        self.lblValor.setObjectName(
            "valor"
        )

        self.lblValor.setAlignment(
            Qt.AlignCenter
        )

        self.lblStatus = QLabel("")

        self.lblStatus.setAlignment(
            Qt.AlignCenter
        )

        self.lblStatus.setStyleSheet(
            """
            font-size: 12px;
            font-weight: bold;
            border: none;
            background: transparent;
            """
        )

        self.lblUltimaConsulta = QLabel("")

        self.lblUltimaConsulta.setAlignment(
            Qt.AlignCenter
        )

        self.lblUltimaConsulta.setStyleSheet(
            """
            font-size: 10px;
            color: #666666;
            border: none;
            background: transparent;
            """
        )

        layout.addWidget(
            self.lblTitulo
        )

        layout.addWidget(
            self.lblValor
        )

        layout.addWidget(
            self.lblStatus
        )

        layout.addWidget(
            self.lblUltimaConsulta
        )

    ############################################################

    def setUltimaConsulta(
        self,
        data,
    ):

        if not data or data == "-":

            self.lblUltimaConsulta.setText(
                "Última consulta: -"
            )

        else:

            self.lblUltimaConsulta.setText(
                f"Última consulta: {data}"
            )

    ############################################################

    def setValor(
        self,
        valor,
    ):

        self.lblValor.setText(
            str(valor)
        )

    ############################################################

    def setStatus(
        self,
        status,
        cor="#2E7D32",
    ):

        self.lblStatus.setText(
            f"● {status}"
        )

        self.lblStatus.setStyleSheet(
            f"""
            font-size: 12px;
            font-weight: bold;
            color: {cor};
            border: none;
            background: transparent;
            """
        )