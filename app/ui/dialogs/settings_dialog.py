from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from app.config.user_settings import (
    UserSettings,
)


class SettingsDialog(QDialog):

    def __init__(
        self,
        parent=None,
    ):

        super().__init__(parent)

        self.setWindowTitle(
            "Configurações"
        )

        self.resize(
            850,
            650,
        )

        self.config = (
            UserSettings.carregar()
        )

        layout = QVBoxLayout(
            self
        )

        ########################################################
        # TÍTULO
        ########################################################

        titulo = QLabel(
            "Configurações do ERP Fiscal"
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
        # FORMULÁRIO
        ########################################################

        formulario = QFormLayout()

        ########################################################
        # XML
        ########################################################

        self.txtXml = QLineEdit()

        self.btXml = QPushButton(
            "Selecionar"
        )

        linha_xml = QHBoxLayout()

        linha_xml.addWidget(
            self.txtXml
        )

        linha_xml.addWidget(
            self.btXml
        )

        formulario.addRow(
            "Pasta interna de XML:",
            linha_xml,
        )

        ########################################################
        # EXPORTAÇÃO
        ########################################################

        self.txtExportacao = QLineEdit()

        self.btExportacao = QPushButton(
            "Selecionar"
        )

        linha_exportacao = QHBoxLayout()

        linha_exportacao.addWidget(
            self.txtExportacao
        )

        linha_exportacao.addWidget(
            self.btExportacao
        )

        formulario.addRow(
            "Pasta externa padrão:",
            linha_exportacao,
        )

        ########################################################
        # RELATÓRIOS
        ########################################################

        self.txtRelatorios = QLineEdit()

        self.btRelatorios = QPushButton(
            "Selecionar"
        )

        linha_relatorios = QHBoxLayout()

        linha_relatorios.addWidget(
            self.txtRelatorios
        )

        linha_relatorios.addWidget(
            self.btRelatorios
        )

        formulario.addRow(
            "Pasta de relatórios:",
            linha_relatorios,
        )

        ########################################################
        # BACKUP
        ########################################################

        self.txtBackup = QLineEdit()

        self.btBackup = QPushButton(
            "Selecionar"
        )

        linha_backup = QHBoxLayout()

        linha_backup.addWidget(
            self.txtBackup
        )

        linha_backup.addWidget(
            self.btBackup
        )

        formulario.addRow(
            "Pasta de backup:",
            linha_backup,
        )

        ########################################################
        # CERTIFICADOS
        ########################################################

        self.txtCertificados = QLineEdit()

        self.btCertificados = QPushButton(
            "Selecionar"
        )

        linha_certificados = QHBoxLayout()

        linha_certificados.addWidget(
            self.txtCertificados
        )

        linha_certificados.addWidget(
            self.btCertificados
        )

        formulario.addRow(
            "Pasta de certificados:",
            linha_certificados,
        )

        ########################################################
        # UF
        ########################################################

        self.comboUF = QComboBox()

        self.comboUF.addItems(
            [
                "CE",
                "AC",
                "AL",
                "AP",
                "AM",
                "BA",
                "DF",
                "ES",
                "GO",
                "MA",
                "MT",
                "MS",
                "MG",
                "PA",
                "PB",
                "PR",
                "PE",
                "PI",
                "RJ",
                "RN",
                "RS",
                "RO",
                "RR",
                "SC",
                "SP",
                "SE",
                "TO",
            ]
        )

        formulario.addRow(
            "UF padrão:",
            self.comboUF,
        )

        ########################################################
        # AMBIENTE
        ########################################################

        self.comboAmbiente = QComboBox()

        self.comboAmbiente.addItem(
            "Produção",
            "producao",
        )

        self.comboAmbiente.addItem(
            "Homologação",
            "homologacao",
        )

        formulario.addRow(
            "Ambiente SEFAZ:",
            self.comboAmbiente,
        )

        ########################################################
        # SERVIÇO 24H
        ########################################################

        self.chk24h = QCheckBox(
            "Ativar serviço automático SEFAZ"
        )

        formulario.addRow(
            "",
            self.chk24h,
        )

        ########################################################
        # INTERVALO
        ########################################################

        self.spinIntervalo = QSpinBox()

        self.spinIntervalo.setRange(
            30,
            3600,
        )

        self.spinIntervalo.setSuffix(
            " segundos"
        )

        formulario.addRow(
            "Intervalo de verificação:",
            self.spinIntervalo,
        )
        
        ########################################################
        # DOCUMENTOS AUTOMÁTICOS
        ########################################################

        self.chkNFe = QCheckBox(
            "Baixar NF-e automaticamente"
        )

        self.chkNFCe = QCheckBox(
            "Baixar NFC-e automaticamente"
        )

        self.chkCTe = QCheckBox(
            "Baixar CT-e automaticamente"
        )

        self.chkNFSe = QCheckBox(
            "Baixar NFS-e automaticamente"
        )

        formulario.addRow(
            "",
            self.chkNFe,
        )

        formulario.addRow(
            "",
            self.chkNFCe,
        )

        formulario.addRow(
            "",
            self.chkCTe,
        )

        formulario.addRow(
            "",
            self.chkNFSe,
        )

        ########################################################
        # EMPRESAS SIMULTÂNEAS
        ########################################################

        self.spinWorkers = QSpinBox()

        self.spinWorkers.setRange(
            1,
            10,
        )

        self.spinWorkers.setValue(
            4
        )

        self.spinWorkers.setSuffix(
            " empresas"
        )

        formulario.addRow(
            "Empresas simultâneas:",
            self.spinWorkers,
        )

        ########################################################
        # ORGANIZAÇÃO
        ########################################################

        self.chkCNPJ = QCheckBox(
            "Organizar por CNPJ"
        )

        self.chkAno = QCheckBox(
            "Organizar por ano"
        )

        self.chkMes = QCheckBox(
            "Organizar por mês"
        )

        self.chkTipo = QCheckBox(
            "Organizar por tipo de documento"
        )

        formulario.addRow(
            "",
            self.chkCNPJ,
        )

        formulario.addRow(
            "",
            self.chkAno,
        )

        formulario.addRow(
            "",
            self.chkMes,
        )

        formulario.addRow(
            "",
            self.chkTipo,
        )

        layout.addLayout(
            formulario
        )

        ########################################################
        # BOTÕES
        ########################################################

        botoes = QHBoxLayout()

        self.btSalvar = QPushButton(
            "Salvar Configurações"
        )

        self.btFechar = QPushButton(
            "Fechar"
        )

        botoes.addWidget(
            self.btSalvar
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

        self.btXml.clicked.connect(
            lambda: self.selecionar_pasta(
                self.txtXml
            )
        )

        self.btExportacao.clicked.connect(
            lambda: self.selecionar_pasta(
                self.txtExportacao
            )
        )

        self.btRelatorios.clicked.connect(
            lambda: self.selecionar_pasta(
                self.txtRelatorios
            )
        )

        self.btBackup.clicked.connect(
            lambda: self.selecionar_pasta(
                self.txtBackup
            )
        )

        self.btCertificados.clicked.connect(
            lambda: self.selecionar_pasta(
                self.txtCertificados
            )
        )

        self.btSalvar.clicked.connect(
            self.salvar
        )

        self.btFechar.clicked.connect(
            self.close
        )

        ########################################################
        # CARREGAR VALORES
        ########################################################

        self.carregar()

    ############################################################
    # SELECIONAR PASTA
    ############################################################

    def selecionar_pasta(
        self,
        campo,
    ):

        pasta = QFileDialog.getExistingDirectory(
            self,
            "Selecionar pasta",
        )

        if pasta:

            campo.setText(
                pasta
            )

    ############################################################
    # CARREGAR
    ############################################################

    def carregar(self):

        self.txtXml.setText(
            self.config.get(
                "xml_folder",
                "",
            )
        )

        self.txtExportacao.setText(
            self.config.get(
                "external_export_folder",
                "",
            )
        )

        self.txtRelatorios.setText(
            self.config.get(
                "report_folder",
                "",
            )
        )

        self.txtBackup.setText(
            self.config.get(
                "backup_folder",
                "",
            )
        )

        self.txtCertificados.setText(
            self.config.get(
                "certificate_folder",
                "",
            )
        )

        uf = self.config.get(
            "uf",
            "CE",
        )

        indice_uf = (
            self.comboUF.findText(
                uf
            )
        )

        if indice_uf >= 0:

            self.comboUF.setCurrentIndex(
                indice_uf
            )

        ambiente = self.config.get(
            "ambiente",
            "producao",
        )

        indice_ambiente = (
            self.comboAmbiente.findData(
                ambiente
            )
        )

        if indice_ambiente >= 0:

            self.comboAmbiente.setCurrentIndex(
                indice_ambiente
            )

        self.chk24h.setChecked(
            bool(
                self.config.get(
                    "sefaz_24h",
                    True,
                )
            )
        )

        self.spinIntervalo.setValue(
            int(
                self.config.get(
                    "intervalo_verificacao",
                    60,
                )
            )
        )

        self.chkCNPJ.setChecked(
            bool(
                self.config.get(
                    "organizar_por_cnpj",
                    True,
                )
            )
        )

        self.chkAno.setChecked(
            bool(
                self.config.get(
                    "organizar_por_ano",
                    True,
                )
            )
        )

        self.chkMes.setChecked(
            bool(
                self.config.get(
                    "organizar_por_mes",
                    True,
                )
            )
        )

        self.chkTipo.setChecked(
            bool(
                self.config.get(
                    "organizar_por_tipo",
                    True,
                )
            )
        )

        ########################################################
        # DOCUMENTOS AUTOMÁTICOS
        ########################################################

        self.chkNFe.setChecked(
            bool(
                self.config.get(
                    "baixar_nfe",
                    True,
                )
            )
        )

        self.chkNFCe.setChecked(
            bool(
                self.config.get(
                    "baixar_nfce",
                    True,
                )
            )
        )

        self.chkCTe.setChecked(
            bool(
                self.config.get(
                    "baixar_cte",
                    True,
                )
            )
        )

        self.chkNFSe.setChecked(
            bool(
                self.config.get(
                    "baixar_nfse",
                    True,
                )
            )
        )

        ########################################################
        # EMPRESAS SIMULTÂNEAS
        ########################################################

        self.spinWorkers.setValue(
            int(
                self.config.get(
                    "max_workers",
                    4,
                )
            )
        )
    ############################################################
    # SALVAR
    ############################################################

    def salvar(self):

        configuracoes = {
            "xml_folder": (
                self.txtXml.text().strip()
            ),
            "external_export_folder": (
                self.txtExportacao.text().strip()
            ),
            "report_folder": (
                self.txtRelatorios.text().strip()
            ),
            "backup_folder": (
                self.txtBackup.text().strip()
            ),
            "certificate_folder": (
                self.txtCertificados.text().strip()
            ),
            "uf": (
                self.comboUF.currentText()
            ),
            "ambiente": (
                self.comboAmbiente.currentData()
            ),
            "sefaz_24h": (
                self.chk24h.isChecked()
            ),
            "intervalo_verificacao": (
                self.spinIntervalo.value()
            ),
            "organizar_por_cnpj": (
                self.chkCNPJ.isChecked()
            ),
            "organizar_por_ano": (
                self.chkAno.isChecked()
            ),
            "organizar_por_mes": (
                self.chkMes.isChecked()
            ),
            "organizar_por_tipo": (
                self.chkTipo.isChecked()
            ),
            "baixar_nfe": (
                self.chkNFe.isChecked()
            ),

            "baixar_nfce": (
                self.chkNFCe.isChecked()
            ),

            "baixar_cte": (
                self.chkCTe.isChecked()
            ),

            "baixar_nfse": (
                self.chkNFSe.isChecked()
            ),

            "max_workers": (
                self.spinWorkers.value()
            ),
        }

        UserSettings.salvar(
            configuracoes
        )

        self.config = configuracoes

        QMessageBox.information(
            self,
            "Configurações",
            "Configurações salvas com sucesso.",
        )