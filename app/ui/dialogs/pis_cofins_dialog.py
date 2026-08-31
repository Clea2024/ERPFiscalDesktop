from decimal import Decimal, InvalidOperation

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from app.database.database import get_session
from app.models.company import Company
from app.models.tributacao_pis_cofins import TributacaoPisCofins
from app.services.apuracao_pis_cofins_service import ApuracaoPisCofinsService


class PisCofinsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Apuração PIS / COFINS")
        self.resize(1250, 700)
        self.service = ApuracaoPisCofinsService()

        self.montar_tela()
        self.carregar_empresas()
        self.atualizar_regime()
        self.carregar()

    @staticmethod
    def decimal_texto(texto):
        texto = str(texto or "").strip().replace(".", "").replace(",", ".")
        if not texto:
            return Decimal("0.00")
        try:
            return Decimal(texto)
        except InvalidOperation as erro:
            raise ValueError("Valor inválido.") from erro

    @staticmethod
    def moeda(valor):
        valor = Decimal(str(valor or 0))
        formatado = f"{valor:,.2f}"
        formatado = (
            formatado
            .replace(",", "#")
            .replace(".", ",")
            .replace("#", ".")
        )
        return f"R$ {formatado}"

    def montar_tela(self):
        layout = QVBoxLayout(self)

        titulo = QLabel("APURAÇÃO PIS / COFINS")
        titulo.setStyleSheet(
            "font-size: 22px; font-weight: bold; padding: 10px;"
        )
        layout.addWidget(titulo)

        self.formulario = QFormLayout()

        self.cmbEmpresa = QComboBox()

        self.cmbRegime = QComboBox()
        self.cmbRegime.addItems(["CUMULATIVO", "NAO_CUMULATIVO"])
        self.cmbRegime.currentTextChanged.connect(self.atualizar_regime)

        self.txtCompetencia = QLineEdit()
        self.txtCompetencia.setPlaceholderText("MM/AAAA")

        self.txtReceita = QLineEdit()
        self.txtReceita.setPlaceholderText("Ex.: 100.000,00")

        self.txtExclusoes = QLineEdit()
        self.txtExclusoes.setPlaceholderText("Ex.: 0,00")

        self.txtCreditoPis = QLineEdit()
        self.txtCreditoPis.setPlaceholderText("Ex.: 1.000,00")

        self.txtCreditoCofins = QLineEdit()
        self.txtCreditoCofins.setPlaceholderText("Ex.: 4.000,00")

        self.formulario.addRow("Empresa:", self.cmbEmpresa)
        self.formulario.addRow("Regime PIS/COFINS:", self.cmbRegime)
        self.formulario.addRow("Competência:", self.txtCompetencia)
        self.formulario.addRow("Receita tributável:", self.txtReceita)
        self.formulario.addRow("Exclusões da base:", self.txtExclusoes)
        self.formulario.addRow("Crédito PIS:", self.txtCreditoPis)
        self.formulario.addRow("Crédito COFINS:", self.txtCreditoCofins)

        layout.addLayout(self.formulario)

        self.btnCalcular = QPushButton("Calcular PIS / COFINS")
        self.btnCalcular.clicked.connect(self.calcular)
        layout.addWidget(self.btnCalcular)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(12)
        self.tabela.setHorizontalHeaderLabels(
            [
                "Empresa",
                "Competência",
                "Regime",
                "Receita",
                "Base PIS",
                "Débito PIS",
                "Crédito PIS",
                "Saldo PIS",
                "Base COFINS",
                "Débito COFINS",
                "Crédito COFINS",
                "Saldo COFINS",
            ]
        )
        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.tabela.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tabela)

        btn_atualizar = QPushButton("Atualizar")
        btn_atualizar.clicked.connect(self.carregar)
        layout.addWidget(btn_atualizar)

    def atualizar_regime(self):
        nao_cumulativo = self.cmbRegime.currentText() == "NAO_CUMULATIVO"
        self.formulario.setRowVisible(self.txtCreditoPis, nao_cumulativo)
        self.formulario.setRowVisible(self.txtCreditoCofins, nao_cumulativo)

    def carregar_empresas(self):
        db = get_session()
        try:
            empresas = db.query(Company).order_by(Company.razao_social).all()
            self.cmbEmpresa.clear()
            for empresa in empresas:
                self.cmbEmpresa.addItem(
                    f"{empresa.razao_social} - {empresa.cnpj}",
                    empresa.id,
                )
        finally:
            db.close()

    def calcular(self):
        company_id = self.cmbEmpresa.currentData()
        if not company_id:
            QMessageBox.warning(self, "PIS / COFINS", "Selecione uma empresa.")
            return

        competencia_tela = self.txtCompetencia.text().strip()

        try:
            mes, ano = competencia_tela.split("/")
            if (
                len(mes) != 2
                or len(ano) != 4
                or not mes.isdigit()
                or not ano.isdigit()
                or not 1 <= int(mes) <= 12
            ):
                raise ValueError
            competencia = f"{ano}-{mes}"
        except ValueError:
            QMessageBox.warning(
                self,
                "PIS / COFINS",
                "Informe a competência no formato MM/AAAA.",
            )
            return

        try:
            receita = self.decimal_texto(self.txtReceita.text())
            exclusoes = self.decimal_texto(self.txtExclusoes.text())
            credito_pis = self.decimal_texto(self.txtCreditoPis.text())
            credito_cofins = self.decimal_texto(self.txtCreditoCofins.text())
        except ValueError:
            QMessageBox.warning(
                self,
                "PIS / COFINS",
                "Verifique os valores informados.",
            )
            return

        try:
            resultado = self.service.apurar_e_salvar(
                company_id=company_id,
                competencia=competencia,
                regime_apuracao=self.cmbRegime.currentText(),
                receita_tributavel=receita,
                exclusoes_base=exclusoes,
                credito_pis=credito_pis,
                credito_cofins=credito_cofins,
            )

            QMessageBox.information(
                self,
                "PIS / COFINS",
                (
                    "Apuração salva com sucesso.\n\n"
                    f"Saldo PIS: {self.moeda(resultado['saldo_pis'])}\n"
                    f"Saldo COFINS: {self.moeda(resultado['saldo_cofins'])}"
                ),
            )
            self.carregar()
        except Exception as erro:
            QMessageBox.critical(self, "Erro", str(erro))

    def carregar(self):
        db = get_session()

        try:
            registros = (
                db.query(TributacaoPisCofins)
                .order_by(TributacaoPisCofins.competencia.desc())
                .all()
            )

            self.tabela.setRowCount(len(registros))

            for linha, registro in enumerate(registros):
                empresa = (
                    db.query(Company)
                    .filter(Company.id == registro.company_id)
                    .first()
                )
                nome_empresa = (
                    empresa.razao_social if empresa else str(registro.company_id)
                )

                competencia = registro.competencia
                if competencia and len(competencia) == 7 and "-" in competencia:
                    ano, mes = competencia.split("-")
                    competencia = f"{mes}/{ano}"

                valores = [
                    nome_empresa,
                    competencia,
                    registro.regime_apuracao,
                    self.moeda(registro.receita_tributavel),
                    self.moeda(registro.base_pis),
                    self.moeda(registro.debito_pis),
                    self.moeda(registro.credito_pis),
                    self.moeda(registro.saldo_pis),
                    self.moeda(registro.base_cofins),
                    self.moeda(registro.debito_cofins),
                    self.moeda(registro.credito_cofins),
                    self.moeda(registro.saldo_cofins),
                ]

                for coluna, valor in enumerate(valores):
                    self.tabela.setItem(
                        linha,
                        coluna,
                        QTableWidgetItem(str(valor)),
                    )
        finally:
            db.close()
