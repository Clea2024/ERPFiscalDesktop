from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHeaderView,
)

from app.controllers.company_controller import CompanyController
from app.controllers.xml_import_controller import XMLImportController


class XMLImportDialog(QDialog):

    def __init__(self):

        super().__init__()

        self.company_controller = CompanyController()
        self.controller = XMLImportController()

        self.setWindowTitle("Importação de XML")
        self.resize(1100, 700)

        self.montar_interface()

        self.carregar_empresas()

        self.atualizar_tabela()

    #################################################################

    def montar_interface(self):

        layout = QVBoxLayout(self)

        #############################################################

        titulo = QLabel("Importação de Documentos Fiscais")

        titulo.setAlignment(Qt.AlignCenter)

        titulo.setStyleSheet("""
            QLabel{
                font-size:22px;
                font-weight:bold;
                color:#1565C0;
                padding:8px;
            }
        """)

        layout.addWidget(titulo)

        #############################################################

        linha_empresa = QHBoxLayout()

        lbl_empresa = QLabel("Empresa")

        self.combo_empresa = QComboBox()

        linha_empresa.addWidget(lbl_empresa)

        linha_empresa.addWidget(self.combo_empresa)

        layout.addLayout(linha_empresa)

        #############################################################

        linha_botoes = QHBoxLayout()

        self.bt_importar = QPushButton(
            "Selecionar XML(s)"
        )

        self.bt_atualizar = QPushButton(
            "Atualizar"
        )

        linha_botoes.addWidget(self.bt_importar)

        linha_botoes.addWidget(self.bt_atualizar)

        layout.addLayout(linha_botoes)

        #############################################################

        self.progress = QProgressBar()

        self.progress.setValue(0)

        layout.addWidget(self.progress)

        #############################################################

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(6)

        self.tabela.setHorizontalHeaderLabels([
            "Chave",
            "Modelo",
            "Número",
            "Emitente",
            "Valor",
            "Status",
        ])

        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.tabela)

        #############################################################

        self.bt_importar.clicked.connect(
            self.importar_xml
        )

        self.bt_atualizar.clicked.connect(
            self.atualizar_tabela
        )
            #################################################################

    def carregar_empresas(self):

        self.combo_empresa.clear()

        try:

            empresas = self.company_controller.listar()

            for empresa in empresas:

                self.combo_empresa.addItem(
                    empresa.razao_social,
                    empresa.id,
                )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                f"Erro ao carregar empresas.\n\n{erro}",
            )

    #################################################################

    def importar_xml(self):

        arquivos, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecionar XML",
            "",
            "Arquivos XML (*.xml)",
        )

        if not arquivos:
            return

        company_id = self.combo_empresa.currentData()

        if company_id is None:

            QMessageBox.warning(
                self,
                "Empresa",
                "Selecione uma empresa antes de importar.",
            )

            return

        total = len(arquivos)

        self.progress.setValue(0)

        erros = []

        sucesso = 0

        for indice, arquivo in enumerate(arquivos):

            try:

                ok, retorno = self.controller.importar(
                    company_id,
                    arquivo,
                )

                if ok:

                    sucesso += 1

                else:

                    if isinstance(retorno, list):

                        erros.extend(retorno)

                    else:

                        erros.append(str(retorno))

            except Exception as e:

                erros.append(str(e))

            percentual = int(
                ((indice + 1) / total) * 100
            )

            self.progress.setValue(percentual)

        self.atualizar_tabela()

        if erros:

            QMessageBox.warning(
                self,
                "Importação finalizada",
                f"{sucesso} documento(s) importado(s).\n\n"
                + "\n".join(erros),
            )

        else:

            QMessageBox.information(
                self,
                "Importação",
                f"{sucesso} documento(s) importado(s) com sucesso.",
            )
                #################################################################

    def atualizar_tabela(self):

        try:

            documentos = self.controller.listar()

            self.tabela.setRowCount(len(documentos))

            for linha, doc in enumerate(documentos):

                self.tabela.setItem(
                    linha,
                    0,
                    QTableWidgetItem(str(doc.chave)),
                )

                self.tabela.setItem(
                    linha,
                    1,
                    QTableWidgetItem(str(doc.modelo)),
                )

                self.tabela.setItem(
                    linha,
                    2,
                    QTableWidgetItem(str(doc.numero)),
                )

                self.tabela.setItem(
                    linha,
                    3,
                    QTableWidgetItem(str(doc.emitente_nome)),
                )

                self.tabela.setItem(
                    linha,
                    4,
                    QTableWidgetItem(
                        f"{float(doc.valor_total):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    ),
                )

                self.tabela.setItem(
                    linha,
                    5,
                    QTableWidgetItem(str(doc.status)),
                )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                f"Erro ao carregar documentos.\n\n{erro}",
            )