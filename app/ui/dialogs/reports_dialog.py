from collections import Counter
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from app.database.database import get_session
from app.models.company import Company
from app.models.fiscal_document import FiscalDocumentModel


class ReportsDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle(
            "Relatórios Fiscais"
        )

        self.resize(
            1200,
            750,
        )

        self.db = get_session()

        layout = QVBoxLayout(self)

        ########################################################
        # TÍTULO
        ########################################################

        titulo = QLabel(
            "Central de Relatórios Fiscais"
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

        layout.addWidget(
            titulo
        )

        ########################################################
        # FILTROS
        ########################################################

        filtros = QHBoxLayout()

        self.comboEmpresa = QComboBox()

        self.comboTipo = QComboBox()

        self.comboMes = QComboBox()

        self.comboAno = QComboBox()

        filtros.addWidget(
            QLabel("Empresa:")
        )

        filtros.addWidget(
            self.comboEmpresa
        )

        filtros.addWidget(
            QLabel("Tipo:")
        )

        filtros.addWidget(
            self.comboTipo
        )

        filtros.addWidget(
            QLabel("Mês:")
        )

        filtros.addWidget(
            self.comboMes
        )

        filtros.addWidget(
            QLabel("Ano:")
        )

        filtros.addWidget(
            self.comboAno
        )

        self.btGerar = QPushButton(
            "Gerar Relatório"
        )

        filtros.addWidget(
            self.btGerar
        )

        layout.addLayout(
            filtros
        )

        ########################################################
        # CONTADORES
        ########################################################

        resumo = QHBoxLayout()

        self.lblTotal = QLabel(
            "Total DF-e: 0"
        )

        self.lblNFe = QLabel(
            "NF-e: 0"
        )

        self.lblNFCe = QLabel(
            "NFC-e: 0"
        )

        self.lblCTe = QLabel(
            "CT-e: 0"
        )

        self.lblCTeOS = QLabel(
            "CT-e OS: 0"
        )

        self.lblValor = QLabel(
            "Valor total: R$ 0,00"
        )

        resumo.addWidget(
            self.lblTotal
        )

        resumo.addWidget(
            self.lblNFe
        )

        resumo.addWidget(
            self.lblNFCe
        )

        resumo.addWidget(
            self.lblCTe
        )

        resumo.addWidget(
            self.lblCTeOS
        )

        resumo.addWidget(
            self.lblValor
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
                "Tipo",
                "Número",
                "Série",
                "Emissão",
                "Emitente",
                "Destinatário",
                "Valor",
                "Chave",
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

        self.btExcel = QPushButton(
            "Exportar Excel"
        )

        self.btPDF = QPushButton(
            "Exportar PDF"
        )

        self.btFechar = QPushButton(
            "Fechar"
        )

        botoes.addWidget(
            self.btExcel
        )

        botoes.addWidget(
            self.btPDF
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

        self.btGerar.clicked.connect(
            self.gerar_relatorio
        )

        self.btFechar.clicked.connect(
            self.close
        )

        ########################################################
        # CARREGAR FILTROS
        ########################################################

        self.carregar_filtros()

    ############################################################
    # CARREGAR FILTROS
    ############################################################

    def carregar_filtros(self):

        ########################################################
        # EMPRESAS
        ########################################################

        self.comboEmpresa.clear()

        self.comboEmpresa.addItem(
            "Todas",
            None,
        )

        empresas = (
            self.db.query(Company)
            .order_by(
                Company.razao_social
            )
            .all()
        )

        for empresa in empresas:

            self.comboEmpresa.addItem(
                empresa.razao_social,
                empresa.id,
            )

        ########################################################
        # TIPOS DE DOCUMENTOS
        ########################################################

        self.comboTipo.clear()

        self.comboTipo.addItem(
            "Todos",
            ""
        )

        self.comboTipo.addItem(
            "NF-e",
            "55"
        )

        self.comboTipo.addItem(
            "NFC-e",
            "65"
        )

        self.comboTipo.addItem(
            "CT-e",
            "57"
        )

        self.comboTipo.addItem(
            "CT-e OS",
            "67"
        )

        ########################################################
        # MESES
        ########################################################

        self.comboMes.clear()

        meses = [
            ("Todos", 0),
            ("Janeiro", 1),
            ("Fevereiro", 2),
            ("Março", 3),
            ("Abril", 4),
            ("Maio", 5),
            ("Junho", 6),
            ("Julho", 7),
            ("Agosto", 8),
            ("Setembro", 9),
            ("Outubro", 10),
            ("Novembro", 11),
            ("Dezembro", 12),
        ]

        for nome, numero in meses:

            self.comboMes.addItem(
                nome,
                numero,
            )

        ########################################################
        # ANOS
        ########################################################

        self.comboAno.clear()

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

        self.comboMes.clear()

        self.comboMes.addItem(
            "Todos",
            0,
        )

        for mes in range(
            1,
            13,
        ):

            self.comboMes.addItem(
                f"{mes:02d}",
                mes,
            )

        ########################################################

        self.comboAno.clear()

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

    ############################################################
    # GERAR RELATÓRIO
    ############################################################

    def gerar_relatorio(self):

        documentos = (
            self.db.query(
                FiscalDocumentModel
            )
            .all()
        )

        empresa_id = (
            self.comboEmpresa.currentData()
        )

        modelo = (
            self.comboTipo.currentData()
        )

        mes = (
            self.comboMes.currentData()
        )

        ano = (
            self.comboAno.currentData()
        )

        resultado = []

        for documento in documentos:

            if (
                empresa_id is not None
                and documento.company_id
                != empresa_id
            ):
                continue

            if (
                modelo
                and documento.modelo
                != modelo
            ):
                continue

            if documento.data_emissao:

                if (
                    mes
                    and documento.data_emissao.month
                    != mes
                ):
                    continue

                if (
                    ano
                    and documento.data_emissao.year
                    != ano
                ):
                    continue

            resultado.append(
                documento
            )

        self.preencher_resultado(
            resultado
        )

    ############################################################
    # PREENCHER RESULTADO
    ############################################################

    def preencher_resultado(
        self,
        documentos,
    ):

        contador = Counter()

        valor_total = 0

        self.tabela.setRowCount(
            len(documentos)
        )

        for linha, documento in enumerate(
            documentos
        ):

            modelo = str(
                documento.modelo or ""
            )

            if modelo == "55":
                tipo = "NF-e"

            elif modelo == "65":
                tipo = "NFC-e"

            elif modelo == "57":
                tipo = "CT-e"

            elif modelo == "67":
                tipo = "CT-e OS"

            else:
                tipo = "DF-e"

            contador[tipo] += 1

            try:

                valor = float(
                    documento.valor_total
                    or 0
                )

            except Exception:

                valor = 0

            valor_total += valor

            data = ""

            if documento.data_emissao:

                data = (
                    documento.data_emissao.strftime(
                        "%d/%m/%Y"
                    )
                )

            valores = [
                tipo,
                documento.numero or "",
                documento.serie or "",
                data,
                documento.emitente_nome or "",
                documento.destinatario_nome or "",
                self.formatar_moeda(valor),
                documento.chave or "",
            ]

            for coluna, valor_coluna in enumerate(
                valores
            ):

                self.tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(
                        str(valor_coluna)
                    ),
                )

        ########################################################
        # RESUMO
        ########################################################

        self.lblTotal.setText(
            f"Total DF-e: {len(documentos)}"
        )

        self.lblNFe.setText(
            f"NF-e: {contador['NF-e']}"
        )

        self.lblNFCe.setText(
            f"NFC-e: {contador['NFC-e']}"
        )

        self.lblCTe.setText(
            f"CT-e: {contador['CT-e']}"
        )

        self.lblCTeOS.setText(
            f"CT-e OS: {contador['CT-e OS']}"
        )

        self.lblValor.setText(
            "Valor total: "
            + self.formatar_moeda(
                valor_total
            )
        )

        self.tabela.resizeColumnsToContents()

    ############################################################
    # MOEDA
    ############################################################

    @staticmethod
    def formatar_moeda(
        valor,
    ):

        return (
            f"R$ {valor:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

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