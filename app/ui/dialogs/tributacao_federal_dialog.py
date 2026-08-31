from datetime import datetime
from decimal import Decimal, InvalidOperation

from PySide6.QtCore import Qt
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
from app.models.tributacao_federal import TributacaoFederal
from app.models.tributacao_lucro_real import TributacaoLucroReal
from app.services.apuracao_lucro_real_service import ApuracaoLucroRealService
from app.services.tributacao_federal_repository_service import (
    TributacaoFederalRepositoryService,
)


class TributacaoFederalDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Apuração Federal - IRPJ e CSLL")
        self.resize(1450, 780)

        self.service_presumido = TributacaoFederalRepositoryService()
        self.service_real = ApuracaoLucroRealService()

        self.montar_tela()
        self.carregar_empresas()
        self.atualizar_campos_regime()
        self.carregar()

    # ==========================================================
    # TELA
    # ==========================================================

    def montar_tela(self):
        layout = QVBoxLayout(self)

        titulo = QLabel("APURAÇÃO FEDERAL - IRPJ / CSLL")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            padding: 12px;
            """
        )
        layout.addWidget(titulo)

        self.formulario = QFormLayout()

        self.cmbEmpresa = QComboBox()

        self.cmbRegime = QComboBox()
        self.cmbRegime.addItems(
            [
                "Lucro Presumido",
                "Lucro Real",
            ]
        )
        self.cmbRegime.currentTextChanged.connect(
            self.atualizar_campos_regime
        )

        self.cmbFormaApuracao = QComboBox()
        self.cmbFormaApuracao.addItems(
            [
                "TRIMESTRAL",
            ]
        )

        self.cmbAtividade = QComboBox()
        self.cmbAtividade.addItems(
            [
                "SERVICOS_GERAIS",
                "COMERCIO_INDUSTRIA",
            ]
        )

        self.txtCompetencia = QLineEdit()
        self.txtCompetencia.setPlaceholderText("MM/AAAA")
        self.txtCompetencia.textChanged.connect(
            self.atualizar_trimestre
        )

        self.lblTrimestre = QLabel(
            "Trimestre: não identificado"
        )

        self.txtReceita = QLineEdit()
        self.txtReceita.setPlaceholderText(
            "Ex.: 100.000,00 - total do trimestre"
        )

        # Campos exclusivos do Lucro Real.
        self.txtCustos = QLineEdit()
        self.txtCustos.setPlaceholderText("Ex.: 700.000,00")

        self.txtDespesasDedutiveis = QLineEdit()
        self.txtDespesasDedutiveis.setPlaceholderText(
            "Ex.: 150.000,00"
        )

        self.txtOutrasReceitas = QLineEdit()
        self.txtOutrasReceitas.setPlaceholderText(
            "Ex.: 50.000,00"
        )

        self.txtAdicoes = QLineEdit()
        self.txtAdicoes.setPlaceholderText( "Ex.: 20.000,00"
)

        self.txtExclusoes = QLineEdit()
        self.txtExclusoes.setPlaceholderText("Ex.: 10.000,00")

        self.txtCompensacoes = QLineEdit()
        self.txtCompensacoes.setPlaceholderText("Ex.: 0,00")

        self.formulario.addRow("Empresa:", self.cmbEmpresa)
        self.formulario.addRow(
            "Regime tributário:",
            self.cmbRegime,
        )
        self.formulario.addRow(
            "Forma de apuração:",
            self.cmbFormaApuracao,
        )
        self.formulario.addRow(
            "Competência:",
            self.txtCompetencia,
        )
        self.formulario.addRow(
            "Período de apuração:",
            self.lblTrimestre,
        )
        self.formulario.addRow(
            "Atividade:",
            self.cmbAtividade,
        )
        self.formulario.addRow(
            "Receita do trimestre:",
            self.txtReceita,
        )
        self.formulario.addRow(
            "Custos:",
            self.txtCustos,
        )
        self.formulario.addRow(
            "Despesas dedutíveis:",
            self.txtDespesasDedutiveis,
        )
        self.formulario.addRow(
            "Outras receitas:",
            self.txtOutrasReceitas,
        )
        self.formulario.addRow(
            "Adições fiscais:",
            self.txtAdicoes,
        )
        self.formulario.addRow(
            "Exclusões fiscais:",
            self.txtExclusoes,
        )
        self.formulario.addRow(
            "Compensações:",
            self.txtCompensacoes,
        )

        layout.addLayout(self.formulario)

        self.btnCalcular = QPushButton(
            "Calcular IRPJ / CSLL"
        )
        self.btnCalcular.clicked.connect(self.calcular)
        layout.addWidget(self.btnCalcular)

        # Recolhimentos.
        formulario_recolhimento = QFormLayout()

        self.txtIrpjRecolhido = QLineEdit()
        self.txtIrpjRecolhido.setPlaceholderText(
            "Ex.: 4.800,00"
        )

        self.txtVencimentoIrpj = QLineEdit()
        self.txtVencimentoIrpj.setPlaceholderText(
            "DD/MM/AAAA"
        )

        self.txtDarfIrpj = QLineEdit()
        self.txtDarfIrpj.setPlaceholderText(
            "Código / referência DARF IRPJ"
        )

        self.txtCsllRecolhida = QLineEdit()
        self.txtCsllRecolhida.setPlaceholderText(
            "Ex.: 2.880,00"
)
        

        self.txtVencimentoCsll = QLineEdit()
        self.txtVencimentoCsll.setPlaceholderText(
            "DD/MM/AAAA"
        )

        self.txtDarfCsll = QLineEdit()
        self.txtDarfCsll.setPlaceholderText(
            "Código / referência DARF CSLL"
        )

        formulario_recolhimento.addRow(
            "IRPJ recolhido:",
            self.txtIrpjRecolhido,
        )
        formulario_recolhimento.addRow(
            "Vencimento IRPJ:",
            self.txtVencimentoIrpj,
        )
        formulario_recolhimento.addRow(
            "DARF IRPJ:",
            self.txtDarfIrpj,
        )
        formulario_recolhimento.addRow(
            "CSLL recolhida:",
            self.txtCsllRecolhida,
        )
        formulario_recolhimento.addRow(
            "Vencimento CSLL:",
            self.txtVencimentoCsll,
        )
        formulario_recolhimento.addRow(
            "DARF CSLL:",
            self.txtDarfCsll,
        )

        layout.addLayout(formulario_recolhimento)

        self.btnRegistrarRecolhimento = QPushButton(
            "Registrar Recolhimento"
        )
        self.btnRegistrarRecolhimento.clicked.connect(
            self.registrar_recolhimento
        )
        layout.addWidget(self.btnRegistrarRecolhimento)

        # Histórico.
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(19)
        self.tabela.setHorizontalHeaderLabels(
            [
                "Empresa",
                "Competência",
                "Regime",
                "Receita",
                "Base IRPJ",
                "IRPJ",
                "Adicional IRPJ",
                "IRPJ Recolhido",
                "Saldo IRPJ",
                "Vencimento IRPJ",
                "DARF IRPJ",
                "Base CSLL",
                "CSLL",
                "CSLL Recolhida",
                "Saldo CSLL",
                "Vencimento CSLL",
                "DARF CSLL",
                "Status IRPJ",
                "Status CSLL",
            ]
        )
        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.tabela.horizontalHeader().setStretchLastSection(
            True
        )
        layout.addWidget(self.tabela)

        botao_atualizar = QPushButton("Atualizar")
        botao_atualizar.clicked.connect(self.carregar)
        layout.addWidget(botao_atualizar)

    # ==========================================================
    # APOIO
    # ==========================================================

    @staticmethod
    def converter_valor_texto(texto):
        texto = (
            str(texto or "")
            .strip()
            .replace(".", "")
            .replace(",", ".")
        )

        if not texto:
            return Decimal("0.00")

        try:
            return Decimal(texto)
        except InvalidOperation as erro:
            raise ValueError(
                "Valor monetário inválido."
            ) from erro

    @staticmethod
    def trimestre_por_mes(mes):
        mes = int(mes)

        if mes in (1, 2, 3):
            return 1
        if mes in (4, 5, 6):
            return 2
        if mes in (7, 8, 9):
            return 3
        if mes in (10, 11, 12):
            return 4

        raise ValueError("Mês inválido.")

    def obter_periodo(self):
        competencia_tela = (
            self.txtCompetencia.text().strip()
        )

        mes, ano = competencia_tela.split("/")

        if (
            len(mes) != 2
            or len(ano) != 4
            or not mes.isdigit()
            or not ano.isdigit()
        ):
            raise ValueError

        trimestre = self.trimestre_por_mes(mes)

        return {
            "mes": mes,
            "ano": ano,
            "trimestre": trimestre,
            "competencia_mensal": f"{ano}-{mes}",
            "periodo_trimestral": f"{ano}-T{trimestre}",
        }

    @staticmethod
    def formatar_periodo(periodo):
        if not periodo:
            return ""

        if "-T" in periodo:
            ano, trimestre = periodo.split("-T")
            return f"{trimestre}º Trimestre/{ano}"

        if len(periodo) == 7 and "-" in periodo:
            ano, mes = periodo.split("-")
            return f"{mes}/{ano}"

        return periodo

    @staticmethod
    def calcular_status(valor_apurado, valor_recolhido):
        apurado = Decimal(str(valor_apurado or 0))
        recolhido = Decimal(str(valor_recolhido or 0))

        if apurado <= 0:
            return "SEM VALOR"

        if recolhido >= apurado:
            return "PAGO"

        if recolhido > 0:
            return "PARCIAL"

        return "PENDENTE"

    # ==========================================================
    # EMPRESAS / REGIME / PERÍODO
    # ==========================================================

    def carregar_empresas(self):
        db = get_session()

        try:
            empresas = (
                db.query(Company)
                .order_by(Company.razao_social)
                .all()
            )

            self.cmbEmpresa.clear()

            for empresa in empresas:
                self.cmbEmpresa.addItem(
                    f"{empresa.razao_social} - {empresa.cnpj}",
                    empresa.id,
                )

        finally:
            db.close()

    def atualizar_trimestre(self):
        try:
            dados = self.obter_periodo()

            self.lblTrimestre.setText(
                (
                    f"{dados['trimestre']}º trimestre "
                    f"de {dados['ano']}"
                )
            )

        except (ValueError, TypeError):
            self.lblTrimestre.setText(
                "Trimestre: não identificado"
            )

    def atualizar_campos_regime(self):
        lucro_real = (
            self.cmbRegime.currentText()
            == "Lucro Real"
        )

        # QFormLayout.setRowVisible existe no Qt 6 e esconde
        # simultaneamente o rótulo e o campo.
        campos_real = [
            self.cmbFormaApuracao,
            self.txtCustos,
            self.txtDespesasDedutiveis,
            self.txtOutrasReceitas,
            self.txtAdicoes,
            self.txtExclusoes,
            self.txtCompensacoes,
        ]

        for campo in campos_real:
            self.formulario.setRowVisible(
                campo,
                lucro_real,
            )

        # Atividade é usada apenas no Lucro Presumido.
        self.formulario.setRowVisible(
            self.cmbAtividade,
            not lucro_real,
        )

    # ==========================================================
    # APURAÇÃO
    # ==========================================================

    def calcular(self):
        company_id = self.cmbEmpresa.currentData()

        if not company_id:
            QMessageBox.warning(
                self,
                "Apuração Federal",
                "Selecione uma empresa.",
            )
            return

        try:
            periodo = self.obter_periodo()
        except (ValueError, TypeError):
            QMessageBox.warning(
                self,
                "Apuração Federal",
                (
                    "Informe a competência no formato "
                    "MM/AAAA. Ex.: 08/2026."
                ),
            )
            return

        try:
            receita = self.converter_valor_texto(
                self.txtReceita.text()
            )
        except ValueError:
            QMessageBox.warning(
                self,
                "Apuração Federal",
                "Informe uma receita válida.",
            )
            return

        regime = self.cmbRegime.currentText()

        try:
            if regime == "Lucro Real":
                self.calcular_lucro_real(
                    company_id,
                    periodo,
                    receita,
                )
            else:
                self.calcular_lucro_presumido(
                    company_id,
                    periodo,
                    receita,
                )

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

    def calcular_lucro_presumido(
        self,
        company_id,
        periodo,
        receita,
    ):
        atividade = self.cmbAtividade.currentText()

        db = get_session()

        try:
            existente = (
                db.query(TributacaoFederal)
                .filter(
                    TributacaoFederal.company_id
                    == company_id,
                    TributacaoFederal.competencia
                    == periodo["periodo_trimestral"],
                )
                .first()
            )
        finally:
            db.close()

        if existente is not None:
            resposta = QMessageBox.question(
                self,
                "Apuração já existente",
                (
                    "Já existe uma apuração de Lucro "
                    "Presumido para "
                    f"{periodo['trimestre']}º trimestre "
                    f"de {periodo['ano']}.\n\n"
                    "Deseja recalcular e substituir "
                    "os valores?"
                ),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if resposta == QMessageBox.No:
                return

        resultado = (
            self.service_presumido.apurar_e_salvar(
                company_id=company_id,
                competencia=periodo[
                    "competencia_mensal"
                ],
                atividade=atividade,
                receita=receita,
            )
        )

        if not resultado.get("salvo"):
            QMessageBox.warning(
                self,
                "Apuração Federal",
                str(resultado),
            )
            return

        QMessageBox.information(
            self,
            "Apuração Federal",
            (
                "IRPJ e CSLL do Lucro Presumido "
                "apurados e salvos com sucesso."
            ),
        )

        self.carregar()

    def calcular_lucro_real(
        self,
        company_id,
        periodo,
        receita,
    ):
        try:
            custos = self.converter_valor_texto(
                self.txtCustos.text()
            )
            despesas = self.converter_valor_texto(
                self.txtDespesasDedutiveis.text()
            )
            outras_receitas = (
                self.converter_valor_texto(
                    self.txtOutrasReceitas.text()
                )
            )
            adicoes = self.converter_valor_texto(
                self.txtAdicoes.text()
            )
            exclusoes = self.converter_valor_texto(
                self.txtExclusoes.text()
            )
            compensacoes = self.converter_valor_texto(
                self.txtCompensacoes.text()
            )
        except ValueError:
            QMessageBox.warning(
                self,
                "Lucro Real",
                (
                    "Verifique os valores informados "
                    "nos campos do Lucro Real."
                ),
            )
            return

        forma_apuracao = (
            self.cmbFormaApuracao.currentText()
        )

        db = get_session()

        try:
            existente = (
                db.query(TributacaoLucroReal)
                .filter(
                    TributacaoLucroReal.company_id
                    == company_id,
                    TributacaoLucroReal.periodo
                    == periodo["periodo_trimestral"],
                    TributacaoLucroReal.forma_apuracao
                    == forma_apuracao,
                )
                .first()
            )
        finally:
            db.close()

        if existente is not None:
            resposta = QMessageBox.question(
                self,
                "Apuração já existente",
                (
                    "Já existe uma apuração de Lucro "
                    "Real para "
                    f"{periodo['trimestre']}º trimestre "
                    f"de {periodo['ano']}.\n\n"
                    "Deseja recalcular e substituir "
                    "os valores?"
                ),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if resposta == QMessageBox.No:
                return

        resultado = (
            self.service_real.apurar_e_salvar(
                company_id=company_id,
                periodo=periodo["periodo_trimestral"],
                forma_apuracao=forma_apuracao,
                receita_bruta=receita,
                custos=custos,
                despesas_dedutiveis=despesas,
                outras_receitas=outras_receitas,
                adicoes=adicoes,
                exclusoes=exclusoes,
                compensacoes=compensacoes,
                meses_periodo=3,
            )
        )

        QMessageBox.information(
            self,
            "Lucro Real",
            (
                "Apuração do Lucro Real salva com sucesso.\n\n"
                f"Lucro contábil: R$ "
                f"{resultado['lucro_contabil']:.2f}\n"
                f"Base IRPJ: R$ "
                f"{resultado['base_irpj']:.2f}\n"
                f"IRPJ: R$ "
                f"{resultado['valor_irpj']:.2f}\n"
                f"Base CSLL: R$ "
                f"{resultado['base_csll']:.2f}\n"
                f"CSLL: R$ "
                f"{resultado['valor_csll']:.2f}"
            ),
        )

        self.carregar()

    # ==========================================================
    # RECOLHIMENTOS
    # ==========================================================

    def registrar_recolhimento(self):
        company_id = self.cmbEmpresa.currentData()

        if not company_id:
            QMessageBox.warning(
                self,
                "Apuração Federal",
                "Selecione uma empresa.",
            )
            return

        try:
            periodo = self.obter_periodo()
        except (ValueError, TypeError):
            QMessageBox.warning(
                self,
                "Apuração Federal",
                (
                    "Informe a competência no formato "
                    "MM/AAAA."
                ),
            )
            return

        try:
            irpj_recolhido = (
                self.converter_valor_texto(
                    self.txtIrpjRecolhido.text()
                )
            )

            csll_recolhida = (
                self.converter_valor_texto(
                    self.txtCsllRecolhida.text()
                )
            )

        except ValueError:
            QMessageBox.warning(
                self,
                "Apuração Federal",
                (
                    "Informe valores de recolhimento "
                    "válidos."
                ),
            )
            return

        regime = self.cmbRegime.currentText()

        if regime == "Lucro Real":
            self.registrar_recolhimento_lucro_real(
                company_id,
                periodo,
                irpj_recolhido,
                csll_recolhida,
            )
        else:
            self.registrar_recolhimento_presumido(
                company_id,
                periodo,
                irpj_recolhido,
                csll_recolhida,
            )

    def registrar_recolhimento_presumido(
        self,
        company_id,
        periodo,
        irpj_recolhido,
        csll_recolhida,
    ):
        db = get_session()

        try:
            registro = (
                db.query(TributacaoFederal)
                .filter(
                    TributacaoFederal.company_id
                    == company_id,
                    TributacaoFederal.competencia
                    == periodo["periodo_trimestral"],
                )
                .first()
            )

            if registro is None:
                QMessageBox.warning(
                    self,
                    "Apuração Federal",
                    (
                        "Apuração de Lucro Presumido "
                        "não encontrada para o período."
                    ),
                )
                return

            vencimento_irpj = (
                self.txtVencimentoIrpj.text().strip()
            )
            vencimento_csll = (
                self.txtVencimentoCsll.text().strip()
            )

            registro.irpj_recolhido = irpj_recolhido
            registro.csll_recolhida = csll_recolhida

            registro.darf_irpj = (
                self.txtDarfIrpj.text().strip()
            )
            registro.darf_csll = (
                self.txtDarfCsll.text().strip()
            )

            registro.vencimento_irpj = (
                datetime.strptime(
                    vencimento_irpj,
                    "%d/%m/%Y",
                ).date()
                if vencimento_irpj
                else None
            )

            registro.vencimento_csll = (
                datetime.strptime(
                    vencimento_csll,
                    "%d/%m/%Y",
                ).date()
                if vencimento_csll
                else None
            )

            registro.status_irpj = (
                self.calcular_status(
                    registro.valor_irpj,
                    irpj_recolhido,
                )
            )

            registro.status_csll = (
                self.calcular_status(
                    registro.valor_csll,
                    csll_recolhida,
                )
            )

            db.commit()

        except ValueError:
            db.rollback()

            QMessageBox.warning(
                self,
                "Apuração Federal",
                "Data inválida. Use DD/MM/AAAA.",
            )
            return

        except Exception as erro:
            db.rollback()

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )
            return

        finally:
            db.close()

        QMessageBox.information(
            self,
            "Apuração Federal",
            "Recolhimento registrado com sucesso.",
        )
        self.carregar()

    def registrar_recolhimento_lucro_real(
        self,
        company_id,
        periodo,
        irpj_recolhido,
        csll_recolhida,
    ):
        forma_apuracao = (
            self.cmbFormaApuracao.currentText()
        )

        db = get_session()

        try:
            registro = (
                db.query(TributacaoLucroReal)
                .filter(
                    TributacaoLucroReal.company_id
                    == company_id,
                    TributacaoLucroReal.periodo
                    == periodo["periodo_trimestral"],
                    TributacaoLucroReal.forma_apuracao
                    == forma_apuracao,
                )
                .first()
            )

            if registro is None:
                QMessageBox.warning(
                    self,
                    "Lucro Real",
                    (
                        "Apuração de Lucro Real não "
                        "encontrada para o período."
                    ),
                )
                return

            registro.irpj_recolhido = irpj_recolhido
            registro.csll_recolhida = csll_recolhida

            registro.status_irpj = (
                self.calcular_status(
                    registro.valor_irpj,
                    irpj_recolhido,
                )
            )

            registro.status_csll = (
                self.calcular_status(
                    registro.valor_csll,
                    csll_recolhida,
                )
            )

            db.commit()

        except Exception as erro:
            db.rollback()

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )
            return

        finally:
            db.close()

        QMessageBox.information(
            self,
            "Lucro Real",
            (
                "Recolhimento do Lucro Real "
                "registrado com sucesso."
            ),
        )

        self.carregar()

    # ==========================================================
    # HISTÓRICO
    # ==========================================================

    def carregar(self):
        db = get_session()

        try:
            presumidos = (
                db.query(TributacaoFederal)
                .order_by(
                    TributacaoFederal.competencia.desc()
                )
                .all()
            )

            reais = (
                db.query(TributacaoLucroReal)
                .order_by(
                    TributacaoLucroReal.periodo.desc()
                )
                .all()
            )

            self.tabela.setRowCount(
                len(presumidos) + len(reais)
            )

            linha = 0

            for registro in presumidos:
                empresa = (
                    registro.empresa.razao_social
                    if getattr(registro, "empresa", None)
                    else self.nome_empresa(
                        db,
                        registro.company_id,
                    )
                )

                saldo_irpj = max(
                    Decimal("0.00"),
                    Decimal(
                        str(registro.valor_irpj or 0)
                    )
                    - Decimal(
                        str(
                            registro.irpj_recolhido
                            or 0
                        )
                    ),
                )

                saldo_csll = max(
                    Decimal("0.00"),
                    Decimal(
                        str(registro.valor_csll or 0)
                    )
                    - Decimal(
                        str(
                            registro.csll_recolhida
                            or 0
                        )
                    ),
                )

                vencimento_irpj = (
                    registro.vencimento_irpj.strftime(
                        "%d/%m/%Y"
                    )
                    if registro.vencimento_irpj
                    else ""
                )

                vencimento_csll = (
                    registro.vencimento_csll.strftime(
                        "%d/%m/%Y"
                    )
                    if registro.vencimento_csll
                    else ""
                )

                valores = [
                    empresa,
                    self.formatar_periodo(
                        registro.competencia
                    ),
                    "Lucro Presumido",
                    self.moeda(registro.receita_bruta),
                    self.moeda(registro.base_irpj),
                    self.moeda(registro.valor_irpj),
                    self.moeda(
                        registro.adicional_irpj
                    ),
                    self.moeda(
                        registro.irpj_recolhido
                    ),
                    self.moeda(saldo_irpj),
                    vencimento_irpj,
                    registro.darf_irpj or "",
                    self.moeda(registro.base_csll),
                    self.moeda(registro.valor_csll),
                    self.moeda(
                        registro.csll_recolhida
                    ),
                    self.moeda(saldo_csll),
                    vencimento_csll,
                    registro.darf_csll or "",
                    registro.status_irpj
                    or "PENDENTE",
                    registro.status_csll
                    or "PENDENTE",
                ]

                self.preencher_linha(
                    linha,
                    valores,
                )
                linha += 1

            for registro in reais:
                empresa = self.nome_empresa(
                    db,
                    registro.company_id,
                )

                saldo_irpj = max(
                    Decimal("0.00"),
                    Decimal(
                        str(registro.valor_irpj or 0)
                    )
                    - Decimal(
                        str(
                            registro.irpj_recolhido
                            or 0
                        )
                    ),
                )

                saldo_csll = max(
                    Decimal("0.00"),
                    Decimal(
                        str(registro.valor_csll or 0)
                    )
                    - Decimal(
                        str(
                            registro.csll_recolhida
                            or 0
                        )
                    ),
                )

                valores = [
                    empresa,
                    self.formatar_periodo(
                        registro.periodo
                    ),
                    (
                        "Lucro Real - "
                        f"{registro.forma_apuracao}"
                    ),
                    self.moeda(registro.receita_bruta),
                    self.moeda(registro.base_irpj),
                    self.moeda(registro.valor_irpj),
                    self.moeda(
                        registro.adicional_irpj
                    ),
                    self.moeda(
                        registro.irpj_recolhido
                    ),
                    self.moeda(saldo_irpj),
                    "",
                    "",
                    self.moeda(registro.base_csll),
                    self.moeda(registro.valor_csll),
                    self.moeda(
                        registro.csll_recolhida
                    ),
                    self.moeda(saldo_csll),
                    "",
                    "",
                    registro.status_irpj
                    or "PENDENTE",
                    registro.status_csll
                    or "PENDENTE",
                ]

                self.preencher_linha(
                    linha,
                    valores,
                )
                linha += 1

        finally:
            db.close()

    @staticmethod
    def nome_empresa(db, company_id):
        empresa = (
            db.query(Company)
            .filter(
                Company.id == company_id
            )
            .first()
        )

        if empresa:
            return empresa.razao_social

        return str(company_id)

    @staticmethod
    def moeda(valor):

        valor = Decimal(
            str(valor or 0)
        )

        valor_formatado = (
            f"{valor:,.2f}"
        )

        valor_formatado = (
            valor_formatado
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        return f"R$ {valor_formatado}"
        valor = Decimal(str(valor or 0))
        return f"R$ {valor:.2f}"

    def preencher_linha(self, linha, valores):
        for coluna, valor in enumerate(valores):
            self.tabela.setItem(
                linha,
                coluna,
                QTableWidgetItem(
                    str(valor)
                ),
            )