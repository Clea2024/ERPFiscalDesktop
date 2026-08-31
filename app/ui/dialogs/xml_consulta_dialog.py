from collections import Counter

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from app.database.database import get_session

from app.repositories.fiscal_document_repository import (
    FiscalDocumentRepository,
)

from app.services.external_export_service import (
    ExternalExportService,
)

from app.ui.dialogs.xml_detail_dialog import (
    XMLDetailDialog,
)

from app.ui.widgets.search_bar import (
    SearchBar,
)


class XMLConsultaDialog(QDialog):

    def __init__(
        self,
        parent=None,
    ):

        super().__init__(parent)

        self.setWindowTitle(
            "Consulta de Documentos Fiscais"
        )

        self.resize(
            1200,
            700,
        )

        self.db = get_session()

        self.repository = FiscalDocumentRepository(
            self.db
        )

        self.documentos = []

        layout = QVBoxLayout(
            self
        )

        ########################################################
        # TÍTULO
        ########################################################

        titulo = QLabel(
            "Documentos Fiscais Importados"
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )

        titulo.setStyleSheet(
            """
            QLabel {
                font-size: 22px;
                font-weight: bold;
                padding: 8px;
            }
            """
        )

        layout.addWidget(
            titulo
        )

        ########################################################
        # CONTADORES
        ########################################################

        painel_contadores = QHBoxLayout()

        self.lblTotalTitulo = QLabel(
            "XML importados:"
        )

        self.lblTotalXML = QLabel(
            "0"
        )

        self.lblExibidosTitulo = QLabel(
            "Exibidos:"
        )

        self.lblExibidos = QLabel(
            "0"
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

        self.lblNFSe = QLabel(
            "NFS-e: 0"
        )
        self.lblNFe.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.lblNFCe.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.lblCTe.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.lblNFSe.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.lblTotalTitulo.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.lblExibidosTitulo.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.lblTotalXML.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            padding: 4px 12px;
            """
        )

        self.lblExibidos.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            padding: 4px 12px;
            """
        )

        painel_contadores.addWidget(
            self.lblTotalTitulo
        )

        painel_contadores.addWidget(
            self.lblTotalXML
        )

        painel_contadores.addSpacing(
            30
        )

        painel_contadores.addWidget(
            self.lblExibidosTitulo
        )

        painel_contadores.addWidget(
            self.lblExibidos
        )

        painel_contadores.addSpacing(
            30
        )

        painel_contadores.addWidget(
            self.lblNFe
        )

        painel_contadores.addSpacing(
            20
        )

        painel_contadores.addWidget(
            self.lblNFCe
        )

        painel_contadores.addSpacing(
            20
        )

        painel_contadores.addWidget(
            self.lblCTe
        )

        painel_contadores.addSpacing(
            20
        )

        painel_contadores.addWidget(
            self.lblNFSe
        )

        painel_contadores.addStretch()

        layout.addLayout(
            painel_contadores
        )

        ########################################################
        # COMPETÊNCIAS
        ########################################################

        self.lblCompetencias = QLabel(
            "Competências: Nenhum XML importado"
        )

        self.lblCompetencias.setWordWrap(
            True
        )

        self.lblCompetencias.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
            """
        )

        layout.addWidget(
            self.lblCompetencias
        )

        ########################################################
        # PESQUISA
        ########################################################

        self.searchBar = SearchBar(
            "Chave, número, emitente ou destinatário..."
        )

        layout.addWidget(
            self.searchBar
        )

        ########################################################
        # TABELA
        ########################################################

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(
            9
        )

        self.tabela.setHorizontalHeaderLabels(
            [
                "Tipo",
                "Chave",
                "Modelo",
                "Número",
                "Série",
                "Emitente",
                "Destinatário",
                "Valor",
                "Emissão",
            ]
        )

        self.tabela.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.tabela.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        layout.addWidget(
            self.tabela
        )

        ########################################################
        # BOTÕES
        ########################################################

        botoes = QHBoxLayout()

        self.btAtualizar = QPushButton(
            "Atualizar"
        )

        self.btExportar = QPushButton(
            "Salvar XMLs em Pasta"
        )

        self.btFechar = QPushButton(
            "Fechar"
        )

        botoes.addWidget(
            self.btAtualizar
        )

        botoes.addWidget(
            self.btExportar
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

        self.btAtualizar.clicked.connect(
            self.carregar_dados
        )

        self.btExportar.clicked.connect(
            self.exportar_xmls
        )

        self.btFechar.clicked.connect(
            self.close
        )

        self.tabela.cellDoubleClicked.connect(
            self.abrir_documento
        )

        self.searchBar.searchRequested.connect(
            self.pesquisar
        )

        self.searchBar.clearRequested.connect(
            self.carregar_dados
        )

        ########################################################
        # PRIMEIRA CARGA
        ########################################################

        self.carregar_dados()
    ############################################################
    # CARREGAR DADOS
    ############################################################

    def carregar_dados(self):

        documentos = (
            self.repository.listar()
        )

        total_nfe = 0
        total_nfce = 0
        total_cte = 0
        total_nfse = 0

        for documento in documentos:

            tipo = self.identificar_tipo(
                documento
            )

            if tipo == "NF-e":
                total_nfe += 1

            elif tipo == "NFC-e":
                total_nfce += 1

            elif tipo in (
                "CT-e",
                "CT-e OS",
            ):
                total_cte += 1

            elif tipo == "NFS-e":
                total_nfse += 1

        self.lblTotalXML.setText(
            str(len(documentos))
        )

        self.lblNFe.setText(
            f"NF-e: {total_nfe}"
        )

        self.lblNFCe.setText(
            f"NFC-e: {total_nfce}"
        )

        self.lblCTe.setText(
            f"CT-e: {total_cte}"
        )

        self.lblNFSe.setText(
            f"NFS-e: {total_nfse}"
        )

        self.atualizar_competencias(
            documentos
        )

        self.preencher_tabela(
            documentos
        )

    ############################################################
    # COMPETÊNCIAS
    ############################################################

    def atualizar_competencias(
        self,
        documentos,
    ):

        contador = Counter()

        for doc in documentos:

            if not doc.data_emissao:
                continue

            competencia = (
                doc.data_emissao.strftime(
                    "%m/%Y"
                )
            )

            contador[
                competencia
            ] += 1

        if not contador:

            self.lblCompetencias.setText(
                "Competências: Nenhum XML importado"
            )

            return

        def ordenar_competencia(
            competencia,
        ):

            mes, ano = competencia.split(
                "/"
            )

            return (
                int(ano),
                int(mes),
            )

        competencias = sorted(
            contador.keys(),
            key=ordenar_competencia,
        )

        textos = []

        for competencia in competencias:

            quantidade = contador[
                competencia
            ]

            textos.append(
                f"{competencia}: {quantidade} XML"
            )

        self.lblCompetencias.setText(
            "Competências: "
            + "   |   ".join(textos)
        )

    ############################################################
    # IDENTIFICAR TIPO
    ############################################################

    @staticmethod
    def identificar_tipo(
        doc,
    ):

        modelo = str(
            doc.modelo or ""
        )

        origem = str(
            getattr(
                doc,
                "origem",
                "",
            )
            or ""
        ).upper()

        if modelo == "55":
            return "NF-e"

        if modelo == "65":
            return "NFC-e"

        if modelo == "57":
            return "CT-e"

        if modelo == "67":
            return "CT-e OS"

        if modelo.upper() == "NFSE":
            return "NFS-e"

        if origem == "CTE":
            return "CT-e"

        if origem == "NFSE":
            return "NFS-e"

        return (
            origem
            or "DF-e"
        )

    ############################################################
    # PREENCHER TABELA
    ############################################################

    def preencher_tabela(
        self,
        documentos,
    ):

        self.documentos = documentos

        self.lblExibidos.setText(
            str(len(documentos))
        )

        self.tabela.setRowCount(
            len(documentos)
        )

        for linha, doc in enumerate(
            documentos
        ):

            tipo = self.identificar_tipo(
                doc
            )

            self.tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    tipo
                ),
            )

            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    doc.chave or ""
                ),
            )

            self.tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    doc.modelo or ""
                ),
            )

            self.tabela.setItem(
                linha,
                3,
                QTableWidgetItem(
                    doc.numero or ""
                ),
            )

            self.tabela.setItem(
                linha,
                4,
                QTableWidgetItem(
                    doc.serie or ""
                ),
            )

            self.tabela.setItem(
                linha,
                5,
                QTableWidgetItem(
                    doc.emitente_nome or ""
                ),
            )

            self.tabela.setItem(
                linha,
                6,
                QTableWidgetItem(
                    doc.destinatario_nome or ""
                ),
            )

            try:

                valor = (
                    f"R$ {float(doc.valor_total):,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )

            except Exception:

                valor = "R$ 0,00"

            self.tabela.setItem(
                linha,
                7,
                QTableWidgetItem(
                    valor
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
                8,
                QTableWidgetItem(
                    data
                ),
            )

        self.tabela.resizeColumnsToContents()

    ############################################################
    # PESQUISAR
    ############################################################

    def pesquisar(
        self,
        texto,
    ):

        texto = (
            texto.lower()
            .strip()
        )

        if not texto:

            self.carregar_dados()

            return

        documentos = (
            self.repository.listar()
        )

        resultado = []

        for doc in documentos:

            chave = (
                doc.chave or ""
            ).lower()

            numero = (
                doc.numero or ""
            ).lower()

            emitente = (
                doc.emitente_nome or ""
            ).lower()

            destinatario = (
                doc.destinatario_nome or ""
            ).lower()

            tipo = (
                self.identificar_tipo(
                    doc
                )
                .lower()
            )

            if (
                texto in chave
                or texto in numero
                or texto in emitente
                or texto in destinatario
                or texto in tipo
            ):

                resultado.append(
                    doc
                )

        self.preencher_tabela(
            resultado
        )

    ############################################################
    # ABRIR DOCUMENTO
    ############################################################

    def abrir_documento(
        self,
        linha,
        coluna,
    ):

        try:

            if (
                linha < 0
                or linha >= len(
                    self.documentos
                )
            ):

                return

            documento = (
                self.documentos[
                    linha
                ]
            )

            print(
                "[XML] Abrindo documento:",
                documento.id,
                documento.numero,
            )

            tela = XMLDetailDialog(
                documento,
                self,
            )

            tela.exec()

        except Exception as erro:

            print(
                "[XML] ERRO AO ABRIR DOCUMENTO:",
                erro,
            )

            raise

    ############################################################
    # EXPORTAR XMLs
    ############################################################

    def exportar_xmls(self):

        if not self.documentos:

            QMessageBox.information(
                self,
                "Exportar XML",
                "Não existem documentos para exportar.",
            )

            return

        pasta = QFileDialog.getExistingDirectory(
            self,
            "Escolha a pasta de destino",
        )

        if not pasta:
            return

        exportador = (
            ExternalExportService()
        )

        exportados = 0
        ignorados = 0
        erros = []

        for documento in self.documentos:

            cnpj_empresa = ""

            empresa = getattr(
                documento,
                "empresa",
                None,
            )

            if empresa is not None:

                cnpj_empresa = getattr(
                    empresa,
                    "cnpj",
                    "",
                )

            resultado = (
                exportador.exportar_documento(
                    documento=documento,
                    pasta_destino=pasta,
                    cnpj_empresa=cnpj_empresa,
                )
            )

            if resultado.get(
                "sucesso"
            ):

                exportados += 1

            else:

                ignorados += 1

                mensagem = resultado.get(
                    "mensagem",
                    "",
                )

                if mensagem:
                    erros.append(
                        mensagem
                    )

        mensagem_final = (
            f"XMLs exportados: {exportados}\n"
            f"Ignorados: {ignorados}"
        )

        if erros:

            mensagem_final += (
                "\n\nAlguns documentos não possuem "
                "arquivo XML disponível no caminho salvo."
            )

        QMessageBox.information(
            self,
            "Exportação concluída",
            mensagem_final,
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

