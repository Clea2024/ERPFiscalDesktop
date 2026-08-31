from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from app.controllers.company_controller import (
    CompanyController,
)

from app.controllers.certificate_controller import (
    CertificateController,
)


class CertificateDialog(QDialog):

    def __init__(self):

        super().__init__()

        self.company_controller = CompanyController()

        self.certificate_controller = (
            CertificateController()
        )

        self.setWindowTitle(
            "Certificados Digitais"
        )

        self.resize(1100, 700)

        self.montar_interface()

        self.carregar_empresas()

        self.atualizar_tabela()

        self.conectar_eventos()

    ####################################################################

    def montar_interface(self):

        layout = QVBoxLayout(self)

        titulo = QLabel(
            "Gerenciamento de Certificados Digitais"
        )

        titulo.setStyleSheet("""
            QLabel{
                font-size:22px;
                font-weight:bold;
                color:#1565C0;
            }
        """)

        layout.addWidget(titulo)

        ###############################################################

        linha = QHBoxLayout()

        linha.addWidget(
            QLabel("Empresa")
        )

        self.empresa = QComboBox()

        linha.addWidget(
            self.empresa
        )

        layout.addLayout(linha)

        ###############################################################

        linha = QHBoxLayout()

        linha.addWidget(
            QLabel("Descrição")
        )

        self.descricao = QLineEdit()

        linha.addWidget(
            self.descricao
        )

        layout.addLayout(linha)

        ###############################################################

        linha = QHBoxLayout()

        linha.addWidget(
            QLabel("Arquivo")
        )

        self.arquivo = QLineEdit()

        linha.addWidget(
            self.arquivo
        )

        self.btArquivo = QPushButton(
            "Selecionar..."
        )

        linha.addWidget(
            self.btArquivo
        )

        layout.addLayout(linha)

        ###############################################################

        linha = QHBoxLayout()

        linha.addWidget(
            QLabel("Senha")
        )

        self.senha = QLineEdit()

        self.senha.setEchoMode(
            QLineEdit.Password
        )

        linha.addWidget(
            self.senha
        )

        layout.addLayout(linha)
                ###############################################################

        barra = QHBoxLayout()

        self.btNovo = QPushButton("Novo")
        self.btSalvar = QPushButton("Salvar")
        self.btAlterar = QPushButton("Alterar")
        self.btExcluir = QPushButton("Excluir")
        self.btAtualizar = QPushButton("Atualizar")

        barra.addWidget(self.btNovo)
        barra.addWidget(self.btSalvar)
        barra.addWidget(self.btAlterar)
        barra.addWidget(self.btExcluir)
        barra.addWidget(self.btAtualizar)

        layout.addLayout(barra)

        ###############################################################

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(5)

        self.tabela.setHorizontalHeaderLabels(
            [
                "ID",
                "Empresa",
                "Descrição",
                "Arquivo",
                "Validade",
            ]
        )

        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.tabela)

    ####################################################################

    def conectar_eventos(self):

        self.btArquivo.clicked.connect(
            self.abrir_arquivo
        )

        self.btNovo.clicked.connect(
            self.novo
        )

        self.btSalvar.clicked.connect(
            self.salvar
        )

        self.btAlterar.clicked.connect(
            self.alterar
        )

        self.btExcluir.clicked.connect(
            self.excluir
        )

        self.btAtualizar.clicked.connect(
            self.atualizar_tabela
        )

    ####################################################################

    def abrir_arquivo(self):

        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Certificado",
            "",
            "Certificados (*.pfx)"
        )

        if arquivo:

            self.arquivo.setText(arquivo)

    ####################################################################

    def carregar_empresas(self):

        self.empresa.clear()

        empresas = (
            self.company_controller.listar()
        )

        for empresa in empresas:

            self.empresa.addItem(
                empresa.razao_social,
                empresa.id,
            )

    ####################################################################

    def limpar_campos(self):

        self.descricao.clear()

        self.arquivo.clear()

        self.senha.clear()

    ####################################################################

    def novo(self):

        self.limpar_campos()
            ####################################################################

    def salvar(self):

        if self.empresa.currentIndex() == -1:

            QMessageBox.warning(
                self,
                "ERP Fiscal",
                "Cadastre uma empresa primeiro."
            )

            return

        dados = {

            "company_id": self.empresa.currentData(),

            "descricao": self.descricao.text().strip(),

            "arquivo": self.arquivo.text().strip(),

            "senha": self.senha.text().strip(),

        }

        ok, mensagem = (
            self.certificate_controller.salvar(
                **dados
            )
        )

        if ok:

            QMessageBox.information(
                self,
                "ERP Fiscal Desktop",
                mensagem
            )

            self.limpar_campos()

            self.atualizar_tabela()

        else:

            QMessageBox.warning(
                self,
                "ERP Fiscal Desktop",
                mensagem
            )

    ####################################################################

    def atualizar_tabela(self):

        certificados = (
            self.certificate_controller.listar()
        )

        self.tabela.setRowCount(
            len(certificados)
        )

        for linha, certificado in enumerate(
            certificados
        ):

            self.tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    str(certificado.id)
                )
            )

            empresa = ""

            if certificado.empresa:

                empresa = (
                    certificado.empresa.razao_social
                )

            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    empresa
                )
            )

            self.tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    certificado.descricao
                )
            )

            self.tabela.setItem(
                linha,
                3,
                QTableWidgetItem(
                    certificado.arquivo
                )
            )

            validade = ""

            if certificado.validade:

                validade = (
                    certificado.validade.strftime(
                        "%d/%m/%Y"
                    )
                )

            self.tabela.setItem(
                linha,
                4,
                QTableWidgetItem(
                    validade
                )
            )
                ####################################################################

    def alterar(self):

        QMessageBox.information(
            self,
            "ERP Fiscal",
            (
                "A função de alteração será "
                "implementada na próxima Sprint."
            ),
        )

    ####################################################################

    def excluir(self):

        QMessageBox.information(
            self,
            "ERP Fiscal",
            (
                "A função de exclusão será "
                "implementada na próxima Sprint."
            ),
        )