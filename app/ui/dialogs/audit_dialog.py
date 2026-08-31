from collections import Counter
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from app.database.database import get_session
from app.models.fiscal_document import FiscalDocumentModel
from app.services.audit_service import AuditService


class AuditDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle(
            "Auditoria Fiscal"
        )

        self.resize(
            1200,
            750,
        )

        self.db = get_session()

        self.service = AuditService()

        self.resultados = []

        layout = QVBoxLayout(self)

        ########################################################
        # TÍTULO
        ########################################################

        titulo = QLabel(
            "Central de Auditoria Fiscal"
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )

        titulo.setStyleSheet(
            """
            QLabel {
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
            """
        )

        layout.addWidget(titulo)

        ########################################################
        # FILTROS
        ########################################################

        filtros = QHBoxLayout()

        filtros.addWidget(
            QLabel("Mês:")
        )

        self.comboMes = QComboBox()

        self.comboMes.addItem(
            "Todos",
            0,
        )

        for mes in range(1, 13):

            self.comboMes.addItem(
                f"{mes:02d}",
                mes,
            )

        filtros.addWidget(
            self.comboMes
        )

        filtros.addWidget(
            QLabel("Ano:")
        )

        self.comboAno = QComboBox()

        self.comboAno.addItem(
            "Todos",
            0,
        )

        ano_atual = datetime.now().year

        for ano in range(
            ano_atual - 5,
            ano_atual + 2,
        ):

            self.comboAno.addItem(
                str(ano),
                ano,
            )

        filtros.addWidget(
            self.comboAno
        )

        self.btExecutar = QPushButton(
            "Executar Auditoria"
        )

        filtros.addWidget(
            self.btExecutar
        )

        filtros.addStretch()

        layout.addLayout(
            filtros
        )

        ########################################################
        # RESUMO
        ########################################################

        resumo = QHBoxLayout()

        self.lblDocumentos = QLabel(
            "Documentos: 0"
        )

        self.lblSucesso = QLabel(
            "Sucesso: 0"
        )

        self.lblAlertas = QLabel(
            "Alertas: 0"
        )

        self.lblErros = QLabel(
            "Erros: 0"
        )

        self.lblCriticos = QLabel(
            "Críticos: 0"
        )

        resumo.addWidget(
            self.lblDocumentos
        )

        resumo.addWidget(
            self.lblSucesso
        )

        resumo.addWidget(
            self.lblAlertas
        )

        resumo.addWidget(
            self.lblErros
        )

        resumo.addWidget(
            self.lblCriticos
        )

        resumo.addStretch()

        layout.addLayout(
            resumo
        )

        ########################################################
        # TABELA
        ########################################################

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(
            8
        )

        self.tabela.setHorizontalHeaderLabels(
            [
                "Regra",
                "Severidade",
                "Item",
                "Código",
                "Mensagem",
                "Encontrado",
                "Correto",
                "Sugestão",
            ]
        )

        self.tabela.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.tabela.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        layout.addWidget(
            self.tabela
        )

        ########################################################
        # BOTÕES
        ########################################################

        botoes = QHBoxLayout()

        self.btFechar = QPushButton(
            "Fechar"
        )

        botoes.addStretch()

        botoes.addWidget(
            self.btFechar
        )

        layout.addLayout(
            botoes
        )

        ########################################################
        # EVENTOS
        ########################################################

        self.btExecutar.clicked.connect(
            self.executar_auditoria
        )

        self.btFechar.clicked.connect(
            self.close
        )

    ############################################################
    # BUSCAR DOCUMENTOS
    ############################################################

    def buscar_documentos(self):

        consulta = self.db.query(
            FiscalDocumentModel
        )

        mes = self.comboMes.currentData()

        ano = self.comboAno.currentData()

        documentos = consulta.all()

        resultado = []

        for documento in documentos:

            if documento.data_emissao is None:
                continue

            if (
                mes
                and documento.data_emissao.month != mes
            ):
                continue

            if (
                ano
                and documento.data_emissao.year != ano
            ):
                continue

            resultado.append(
                documento
            )

        return resultado

    ############################################################
    # EXECUTAR
    ############################################################

    def executar_auditoria(self):

        try:

            documentos = (
                self.buscar_documentos()
            )

            if not documentos:

                QMessageBox.information(
                    self,
                    "Auditoria",
                    (
                        "Nenhum documento encontrado "
                        "para a competência selecionada."
                    ),
                )

                self.preencher_resultados(
                    [],
                    0,
                )

                return

            resultados = (
                self.service
                .auditar_documentos(
                    documentos
                )
            )

            self.preencher_resultados(
                resultados,
                len(documentos),
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro na Auditoria",
                str(erro),
            )

    ############################################################
    # PREENCHER RESULTADOS
    ############################################################

    def preencher_resultados(
        self,
        resultados,
        total_documentos,
    ):

        self.resultados = resultados

        contador = Counter(
            resultado.severidade
            for resultado in resultados
        )

        self.lblDocumentos.setText(
            f"Documentos: {total_documentos}"
        )

        self.lblSucesso.setText(
            f"Sucesso: {contador['SUCESSO']}"
        )

        self.lblAlertas.setText(
            f"Alertas: {contador['ALERTA']}"
        )

        self.lblErros.setText(
            f"Erros: {contador['ERRO']}"
        )

        self.lblCriticos.setText(
            f"Críticos: {contador['CRITICO']}"
        )

        self.tabela.setRowCount(
            len(resultados)
        )

        for linha, resultado in enumerate(
            resultados
        ):

            item = ""

            if resultado.item is not None:

                item = str(
                    resultado.item
                )

            valores = [
                resultado.regra or "",
                resultado.severidade or "",
                item,
                resultado.codigo or "",
                resultado.mensagem or "",
                resultado.valor_encontrado or "",
                resultado.valor_correto or "",
                resultado.sugestao or "",
            ]

            for coluna, valor in enumerate(
                valores
            ):

                self.tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(
                        str(valor)
                    ),
                )

        self.tabela.resizeColumnsToContents()

    ############################################################
    # FECHAR
    ############################################################

    def closeEvent(
        self,
        event,
    ):

        try:

            self.db.close()

        except Exception:

            pass

        event.accept()