from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QFileDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)

from app.controllers.company_controller import CompanyController
from app.services.company_service import CompanyService


class CompanyDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.controller = CompanyController()
        self.service = CompanyService()

        self.setWindowTitle("Cadastro de Empresas")
        self.resize(1200, 700)

        self.criar_interface()
        self.carregar_empresas()

    # ==================================================

    def criar_interface(self):

        layout = QVBoxLayout(self)

        pesquisa = QHBoxLayout()

        pesquisa.addWidget(QLabel("Pesquisar"))

        self.txtPesquisa = QLineEdit()

        pesquisa.addWidget(self.txtPesquisa)

        self.btPesquisar = QPushButton("Pesquisar")

        pesquisa.addWidget(self.btPesquisar)

        layout.addLayout(pesquisa)

        #################################################

        linha = QHBoxLayout()

        linha.addWidget(QLabel("Razão Social"))

        self.razao = QLineEdit()

        linha.addWidget(self.razao)

        layout.addLayout(linha)

        #################################################

        linha = QHBoxLayout()

        linha.addWidget(QLabel("Nome Fantasia"))

        self.fantasia = QLineEdit()

        linha.addWidget(self.fantasia)

        layout.addLayout(linha)

        #################################################

        linha = QHBoxLayout()

        linha.addWidget(QLabel("CNPJ"))

        self.cnpj = QLineEdit()

        linha.addWidget(self.cnpj)

        layout.addLayout(linha)

        #################################################

        linha = QHBoxLayout()

        linha.addWidget(QLabel("Inscrição Estadual"))

        self.ie = QLineEdit()

        linha.addWidget(self.ie)

        layout.addLayout(linha)

        #################################################

        linha = QHBoxLayout()

        linha.addWidget(QLabel("Inscrição Municipal"))

        self.im = QLineEdit()

        linha.addWidget(self.im)

        layout.addLayout(linha)

        #################################################

        linha = QHBoxLayout()

        linha.addWidget(QLabel("Regime"))

        self.regime = QComboBox()

        self.regime.addItems([
            "Simples Nacional",
            "Lucro Presumido",
            "Lucro Real"
        ])

        linha.addWidget(self.regime)

        layout.addLayout(linha)

        #################################################

        linha = QHBoxLayout()

        linha.addWidget(QLabel("Certificado"))

        self.certificado = QLineEdit()

        linha.addWidget(self.certificado)

        self.btArquivo = QPushButton("...")

        linha.addWidget(self.btArquivo)

        layout.addLayout(linha)

        #################################################

        botoes = QHBoxLayout()

        self.btNovo = QPushButton("Novo")

        self.btSalvar = QPushButton("Salvar")

        self.btExcluir = QPushButton("Excluir")

        self.btAtualizar = QPushButton("Atualizar")

        botoes.addWidget(self.btNovo)
        botoes.addWidget(self.btSalvar)
        botoes.addWidget(self.btExcluir)
        botoes.addWidget(self.btAtualizar)

        layout.addLayout(botoes)

        #################################################

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(4)

        self.tabela.setHorizontalHeaderLabels(
            [
                "ID",
                "Razão Social",
                "CNPJ",
                "Regime",
            ]
        )

        layout.addWidget(self.tabela)

        #################################################

        self.btSalvar.clicked.connect(self.salvar)

        self.btAtualizar.clicked.connect(
            self.carregar_empresas
        )

        self.btPesquisar.clicked.connect(
            self.pesquisar
        )

        self.btArquivo.clicked.connect(
            self.escolher_certificado
        )

    # ==================================================

    def escolher_certificado(self):

        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar certificado",
            "",
            "Certificados (*.pfx)"
        )

        if arquivo:

            self.certificado.setText(arquivo)

    # ==================================================

    def salvar(self):

        dados = {

            "razao_social": self.razao.text(),

            "cnpj": self.cnpj.text()

        }

        ok, mensagem = self.service.validar(dados)

        if not ok:

            QMessageBox.warning(
                self,
                "ERP",
                mensagem
            )

            return

        self.controller.salvar(

            razao_social=self.razao.text(),

            nome_fantasia=self.fantasia.text(),

            cnpj=self.cnpj.text(),

            inscricao_estadual=self.ie.text(),

            inscricao_municipal=self.im.text(),

            regime=self.regime.currentText(),

            certificado=self.certificado.text()

        )

        QMessageBox.information(
            self,
            "ERP",
            "Empresa cadastrada."
        )

        self.limpar()

        self.carregar_empresas()

    # ==================================================

    def pesquisar(self):

        empresas = self.controller.pesquisar(
            self.txtPesquisa.text()
        )

        self.preencher_tabela(empresas)

    # ==================================================

    def carregar_empresas(self):

        empresas = self.controller.listar()

        self.preencher_tabela(empresas)

    # ==================================================

    def preencher_tabela(self, empresas):

        self.tabela.setRowCount(len(empresas))

        for linha, empresa in enumerate(empresas):

            self.tabela.setItem(
                linha,
                0,
                QTableWidgetItem(str(empresa.id))
            )

            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    empresa.razao_social
                )
            )

            self.tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    empresa.cnpj
                )
            )

            self.tabela.setItem(
                linha,
                3,
                QTableWidgetItem(
                    empresa.regime
                )
            )

    # ==================================================

    def limpar(self):

        self.razao.clear()
        self.fantasia.clear()
        self.cnpj.clear()
        self.ie.clear()
        self.im.clear()
        self.certificado.clear()