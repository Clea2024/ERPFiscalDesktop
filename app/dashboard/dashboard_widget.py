from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QGridLayout,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.config.user_settings import UserSettings
from app.dashboard.dashboard_card import DashboardCard
from app.dashboard.dashboard_controller import (
    DashboardController,
)


class DashboardWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.controller = DashboardController()

        layout = QVBoxLayout(self)

        ##########################################################
        # TÍTULO
        ##########################################################

        titulo = QLabel(
            "Dashboard Executivo"
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )

        titulo.setStyleSheet("""
            QLabel{
                font-size:24px;
                font-weight:bold;
            }
        """)

        layout.addWidget(titulo)

        ##########################################################
        # SELETOR DE EMPRESA
        ##########################################################

        self.cmbEmpresa = QComboBox()

        self.cmbEmpresa.setMinimumHeight(
            36
        )

        self.cmbEmpresa.setStyleSheet(
            """
            QComboBox {
                font-size: 14px;
                font-weight: bold;
                padding: 6px 10px;
                border: 1px solid #2E7D32;
                border-radius: 6px;
                background: white;
            }
            """
        )

        layout.addWidget(
            self.cmbEmpresa
        )

        ##########################################################
        # CARDS
        ##########################################################

        grid = QGridLayout()

        layout.addLayout(grid)

        self.cardDocumentos = DashboardCard(
            "Documentos",
            cor="#1565C0",
            fundo="#EAF2FD",
        )

        self.cardValor = DashboardCard(
            "Valor Total",
            cor="#2E7D32",
            fundo="#EDF7EE",
        )

        self.cardEmpresas = DashboardCard(
            "Empresas",
            cor="#6A1B9A",
            fundo="#F5ECFA",
        )

        self.cardUltimo = DashboardCard(
            "Última Importação",
            cor="#EF6C00",
            fundo="#FFF3E5",
        )

        self.cardNFe = DashboardCard(
            "NF-e",
            cor="#1565C0",
            fundo="#EAF2FD",
        )

        self.cardNFCe = DashboardCard(
            "NFC-e",
            cor="#0288D1",
            fundo="#EAF7FC",
        )

        self.cardCTe = DashboardCard(
            "CT-e",
            cor="#6A1B9A",
            fundo="#F5ECFA",
        )

        self.cardNFSe = DashboardCard(
            "NFS-e",
            cor="#2E7D32",
            fundo="#EDF7EE",
        )

        ##########################################################
        # ORGANIZAÇÃO DOS CARDS
        ##########################################################

        grid.addWidget(
            self.cardDocumentos,
            0,
            0,
        )

        grid.addWidget(
            self.cardValor,
            0,
            1,
        )

        grid.addWidget(
            self.cardEmpresas,
            0,
            2,
        )

        grid.addWidget(
            self.cardUltimo,
            0,
            3,
        )

        grid.addWidget(
            self.cardNFe,
            1,
            0,
        )

        grid.addWidget(
            self.cardNFCe,
            1,
            1,
        )

        grid.addWidget(
            self.cardCTe,
            1,
            2,
        )

        grid.addWidget(
            self.cardNFSe,
            1,
            3,
        )

        grid.setHorizontalSpacing(
            12
        )

        grid.setVerticalSpacing(
            12
        )

        for coluna in range(4):

            grid.setColumnStretch(
                coluna,
                1,
            )
        ##########################################################
        # STATUS DOS SERVIÇOS AUTOMÁTICOS
        ##########################################################

        self.lblStatusServicos = QLabel()

        self.lblStatusServicos.setAlignment(
            Qt.AlignCenter
        )

        self.lblStatusServicos.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                background-color: #F5F5F5;
                border: 1px solid #DADADA;
                border-radius: 8px;
            }
            """
        )

        layout.addWidget(
            self.lblStatusServicos
        )
        ##########################################################
        # ÚLTIMOS DOCUMENTOS
        ##########################################################

        subtitulo = QLabel(
            "Últimos Documentos Importados"
        )

        subtitulo.setStyleSheet("""
            QLabel{
                font-size:18px;
                font-weight:bold;
            }
        """)

        layout.addWidget(subtitulo)

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(4)

        self.tabela.setHorizontalHeaderLabels(
            [
                "Número",
                "Emitente",
                "Valor",
                "Data",
            ]
        )

        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.tabela)

        ##########################################################

        self.atualizar()

        ########################################################
        # ATUALIZAÇÃO AUTOMÁTICA DO DASHBOARD
        ########################################################

        self.timerAtualizacao = QTimer(
            self
        )

        self.timerAtualizacao.timeout.connect(
            self.atualizar
        )

        self.timerAtualizacao.start(
            60000
        )

        ##########################################################
        # CARREGAR EMPRESAS
        ##########################################################

        self.cmbEmpresa.addItem(
            "Todas as empresas",
            None,
        )

        empresas = (
            self.controller.listar_empresas()
        )

        for empresa in empresas:

            texto_empresa = (
                f'{empresa["razao_social"]}'
                f' — {empresa["cnpj"]}'
            )

            self.cmbEmpresa.addItem(
                texto_empresa,
                empresa["id"],
            )
    ##############################################################

    def atualizar(self):

        company_id = (
            self.cmbEmpresa.currentData()
        )

        dados = (
            self.controller.indicadores(
                company_id
            )
        )
        configuracoes = (
            UserSettings.carregar()
        )

        servico = (
            "ATIVO"
            if configuracoes.get(
                "sefaz_24h",
                True,
            )
            else "DESATIVADO"
        )

        nfe = (
            "ATIVA"
            if configuracoes.get(
                "baixar_nfe",
                True,
            )
            else "DESATIVADA"
        )

        nfce = (
            "ATIVA"
            if configuracoes.get(
                "baixar_nfce",
                True,
            )
            else "DESATIVADA"
        )

        cte = (
            "ATIVA"
            if configuracoes.get(
                "baixar_cte",
                True,
            )
            else "DESATIVADA"
        )

        nfse = (
            "ATIVA"
            if configuracoes.get(
                "baixar_nfse",
                True,
            )
            else "DESATIVADA"
        )

        ultima = dados.get(
            "ultima_importacao",
            "-"
        )

        cor_servico = (
            "#2E7D32"
            if servico == "ATIVO"
            else "#C62828"
        )

        cor_nfe = (
            "#2E7D32"
            if nfe == "ATIVA"
            else "#C62828"
        )

        cor_nfce = (
            "#2E7D32"
            if nfce == "ATIVA"
            else "#C62828"
        )

        cor_cte = (
            "#2E7D32"
            if cte == "ATIVA"
            else "#C62828"
        )

        cor_nfse = (
            "#2E7D32"
            if nfse == "ATIVA"
            else "#C62828"
        )

        self.lblStatusServicos.setText(
            f"Serviço 24H: "
            f"<span style='color:{cor_servico};'>"
            f"{servico}</span>"
            f" &nbsp;&nbsp;|&nbsp;&nbsp; "

            f"NF-e: "
            f"<span style='color:{cor_nfe};'>"
            f"{nfe}</span>"
            f" &nbsp;&nbsp;|&nbsp;&nbsp; "

            f"NFC-e: "
            f"<span style='color:{cor_nfce};'>"
            f"{nfce}</span>"
            f" &nbsp;&nbsp;|&nbsp;&nbsp; "

            f"CT-e: "
            f"<span style='color:{cor_cte};'>"
            f"{cte}</span>"
            f" &nbsp;&nbsp;|&nbsp;&nbsp; "

            f"NFS-e: "
            f"<span style='color:{cor_nfse};'>"
            f"{nfse}</span>"
            f" &nbsp;&nbsp;|&nbsp;&nbsp; "

            f"Última atualização: {ultima}"
        )

        self.cardDocumentos.setValor(
            dados["total_documentos"]
        )

        valor = (
            f'R$ {dados["valor_total"]:,.2f}'
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        self.cardValor.setValor(
            valor
        )

        self.cardEmpresas.setValor(
            dados["total_empresas"]
        )

        self.cardUltimo.setValor(
            dados["ultima_importacao"]
        )

        self.cardNFe.setValor(
            dados.get(
                "total_nfe",
                0,
            )
        )

        self.cardNFCe.setValor(
            dados.get(
                "total_nfce",
                0,
            )
        )

        self.cardCTe.setValor(
            dados.get(
                "total_cte",
                0,
            )
        )

        self.cardNFSe.setValor(
            dados.get(
                "total_nfse",
                0,
            )
        )

        ########################################################
        # STATUS REAL DOS DOCUMENTOS FISCAIS
        ########################################################

        sync_nfe = dados.get(
            "sync_nfe",
            {
                "status": "AGUARDANDO",
                "cor": "#F9A825",
            },
        )

        sync_nfce = dados.get(
            "sync_nfce",
            {
                "status": "AGUARDANDO",
                "cor": "#F9A825",
            },
        )

        sync_cte = dados.get(
            "sync_cte",
            {
                "status": "AGUARDANDO",
                "cor": "#F9A825",
            },
        )

        sync_nfse = dados.get(
            "sync_nfse",
            {
                "status": "AGUARDANDO",
                "cor": "#F9A825",
            },
        )

        self.cardNFe.setStatus(
            sync_nfe["status"],
            sync_nfe["cor"],
        )

        self.cardNFCe.setStatus(
            sync_nfce["status"],
            sync_nfce["cor"],
        )

        self.cardCTe.setStatus(
            sync_cte["status"],
            sync_cte["cor"],
        )

        self.cardNFSe.setStatus(
            sync_nfse["status"],
            sync_nfse["cor"],
        )

        ########################################################
        # ÚLTIMA CONSULTA POR TIPO
        ########################################################

        self.cardNFe.setUltimaConsulta(
            sync_nfe.get(
                "ultima_consulta",
                "-",
            )
        )

        self.cardNFCe.setUltimaConsulta(
            sync_nfce.get(
                "ultima_consulta",
                "-",
            )
        )

        self.cardCTe.setUltimaConsulta(
            sync_cte.get(
                "ultima_consulta",
                "-",
            )
        )

        self.cardNFSe.setUltimaConsulta(
            sync_nfse.get(
                "ultima_consulta",
                "-",
            )
        )
        ##########################################################

        documentos = (
            self.controller.ultimos_documentos(
                company_id
            )
        )

        self.tabela.setRowCount(
            len(documentos)
        )

        for linha, doc in enumerate(documentos):

            self.tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    doc.numero
                ),
            )

            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    doc.emitente_nome
                ),
            )

            self.tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    f"{doc.valor_total}"
                ),
            )

            data = ""

            if doc.data_emissao:

                data = (
                    doc.data_emissao.strftime(
                        "%d/%m/%Y"
                    )
                )

            self.tabela.setItem(
                linha,
                3,
                QTableWidgetItem(
                    data
                ),
            )