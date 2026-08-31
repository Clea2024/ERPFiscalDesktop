from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from app.sefaz.client import SefazClient
from app.sefaz.sync import SefazSyncManager


class SefazSyncDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle(
            "SEFAZ - Sincronização de Documentos Fiscais"
        )

        self.resize(
            900,
            650,
        )

        self.client = None

        self.montar_interface()

    ############################################################
    # INTERFACE
    ############################################################

    def montar_interface(self):

        layout = QVBoxLayout(self)

        ########################################################
        # TÍTULO
        ########################################################

        titulo = QLabel(
            "Central de Sincronização SEFAZ"
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

        self.cnpj = QLineEdit()

        self.cnpj.setPlaceholderText(
            "CNPJ da empresa"
        )

        formulario.addRow(
            "CNPJ:",
            self.cnpj,
        )

        ########################################################
        # CERTIFICADO
        ########################################################

        certificado_layout = QHBoxLayout()

        self.certificado = QLineEdit()

        self.certificado.setPlaceholderText(
            "Selecione o certificado A1 (.pfx)"
        )

        botao_certificado = QPushButton(
            "Selecionar"
        )

        botao_certificado.clicked.connect(
            self.selecionar_certificado
        )

        certificado_layout.addWidget(
            self.certificado
        )

        certificado_layout.addWidget(
            botao_certificado
        )

        formulario.addRow(
            "Certificado:",
            certificado_layout,
        )

        ########################################################
        # SENHA
        ########################################################

        self.senha = QLineEdit()

        self.senha.setEchoMode(
            QLineEdit.Password
        )

        formulario.addRow(
            "Senha:",
            self.senha,
        )

        ########################################################
        # AMBIENTE
        ########################################################

        self.ambiente = QComboBox()

        self.ambiente.addItem(
            "Produção",
            "producao",
        )

        self.ambiente.addItem(
            "Homologação",
            "homologacao",
        )

        formulario.addRow(
            "Ambiente:",
            self.ambiente,
        )

        layout.addLayout(
            formulario
        )

        ########################################################
        # STATUS
        ########################################################

        status_grid = QGridLayout()

        self.lbl_status = QLabel(
            "Não conectado"
        )

        self.lbl_ultimo_nsu = QLabel(
            "-"
        )

        self.lbl_max_nsu = QLabel(
            "-"
        )

        self.lbl_xml = QLabel(
            "0"
        )

        self.lbl_importados = QLabel(
            "0"
        )

        self.lbl_lotes = QLabel(
            "0"
        )

        status_grid.addWidget(
            QLabel("Status:"),
            0,
            0,
        )

        status_grid.addWidget(
            self.lbl_status,
            0,
            1,
        )

        status_grid.addWidget(
            QLabel("Último NSU:"),
            1,
            0,
        )

        status_grid.addWidget(
            self.lbl_ultimo_nsu,
            1,
            1,
        )

        status_grid.addWidget(
            QLabel("Máximo NSU:"),
            1,
            2,
        )

        status_grid.addWidget(
            self.lbl_max_nsu,
            1,
            3,
        )

        status_grid.addWidget(
            QLabel("XMLs baixados:"),
            2,
            0,
        )

        status_grid.addWidget(
            self.lbl_xml,
            2,
            1,
        )

        status_grid.addWidget(
            QLabel("NF-e importadas:"),
            2,
            2,
        )

        status_grid.addWidget(
            self.lbl_importados,
            2,
            3,
        )

        status_grid.addWidget(
            QLabel("Lotes processados:"),
            3,
            0,
        )

        status_grid.addWidget(
            self.lbl_lotes,
            3,
            1,
        )

        layout.addLayout(
            status_grid
        )

        ########################################################
        # PROGRESSO
        ########################################################

        self.progresso = QProgressBar()

        self.progresso.setMinimum(
            0
        )

        self.progresso.setMaximum(
            100
        )

        self.progresso.setValue(
            0
        )

        layout.addWidget(
            self.progresso
        )

        ########################################################
        # BOTÕES
        ########################################################

        botoes = QHBoxLayout()

        self.botao_testar = QPushButton(
            "Testar conexão"
        )

        self.botao_sync = QPushButton(
            "🔄 Sincronizar agora"
        )

        self.botao_limpar = QPushButton(
            "Limpar log"
        )

        self.botao_fechar = QPushButton(
            "Fechar"
        )

        self.botao_testar.clicked.connect(
            self.testar_conexao
        )

        self.botao_sync.clicked.connect(
            self.sincronizar
        )

        self.botao_limpar.clicked.connect(
            self.limpar_log
        )

        self.botao_fechar.clicked.connect(
            self.close
        )

        botoes.addWidget(
            self.botao_testar
        )

        botoes.addWidget(
            self.botao_sync
        )

        botoes.addWidget(
            self.botao_limpar
        )

        botoes.addWidget(
            self.botao_fechar
        )

        layout.addLayout(
            botoes
        )

        ########################################################
        # LOG
        ########################################################

        self.log = QTextEdit()

        self.log.setReadOnly(
            True
        )

        self.log.setPlaceholderText(
            "O histórico da sincronização aparecerá aqui."
        )

        layout.addWidget(
            self.log
        )

    ############################################################
    # CERTIFICADO
    ############################################################

    def selecionar_certificado(self):

        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar certificado A1",
            "",
            "Certificado digital (*.pfx *.p12)",
        )

        if arquivo:

            self.certificado.setText(
                arquivo
            )

            self.adicionar_log(
                f"Certificado selecionado: {arquivo}"
            )

    ############################################################
    # LOG
    ############################################################

    def adicionar_log(
        self,
        mensagem,
    ):

        self.log.append(
            str(mensagem)
        )

    def limpar_log(self):

        self.log.clear()

    ############################################################
    # CRIAR CLIENT
    ############################################################

    def criar_client(self):

        cnpj = "".join(
            caractere
            for caractere in self.cnpj.text()
            if caractere.isdigit()
        )

        if len(cnpj) != 14:

            raise ValueError(
                "Informe um CNPJ válido com 14 dígitos."
            )

        certificado = (
            self.certificado
            .text()
            .strip()
        )

        if not certificado:

            raise ValueError(
                "Selecione o certificado digital."
            )

        senha = self.senha.text()

        if not senha:

            raise ValueError(
                "Informe a senha do certificado."
            )

        ambiente = (
            self.ambiente.currentData()
        )

        self.client = SefazClient(
            certificado_path=certificado,
            senha=senha,
            ambiente=ambiente,
            uf="CE",
        )

        return cnpj

    ############################################################
    # TESTAR CONEXÃO
    ############################################################

    def testar_conexao(self):

        try:

            self.lbl_status.setText(
                "Conectando..."
            )

            self.adicionar_log(
                "Validando certificado digital..."
            )

            self.criar_client()

            self.client.conectar()

            wsdl = (
                self.client.conectar_wsdl()
                + "?WSDL"
            )

            self.client.carregar_wsdl(
                wsdl
            )

            self.lbl_status.setText(
                "Conectado"
            )

            self.progresso.setValue(
                20
            )

            self.adicionar_log(
                "Conexão com a SEFAZ estabelecida."
            )

            QMessageBox.information(
                self,
                "SEFAZ",
                "Conexão realizada com sucesso.",
            )

        except Exception as erro:

            self.lbl_status.setText(
                "Erro"
            )

            self.adicionar_log(
                f"ERRO: {erro}"
            )

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

    ############################################################
    # SINCRONIZAR
    ############################################################

    def sincronizar(self):

        try:

            self.botao_sync.setEnabled(
                False
            )

            self.progresso.setValue(
                5
            )

            self.lbl_status.setText(
                "Preparando..."
            )

            self.adicionar_log(
                "===================================="
            )

            self.adicionar_log(
                "Iniciando sincronização SEFAZ."
            )

            cnpj = self.criar_client()

            ####################################################
            # CONECTAR
            ####################################################

            self.lbl_status.setText(
                "Conectando..."
            )

            self.client.conectar()

            self.progresso.setValue(
                15
            )

            self.adicionar_log(
                "Certificado validado."
            )

            wsdl = (
                self.client.conectar_wsdl()
                + "?WSDL"
            )

            self.client.carregar_wsdl(
                wsdl
            )

            self.progresso.setValue(
                25
            )

            self.adicionar_log(
                "Web Service carregado."
            )

            ####################################################
            # SINCRONIZAÇÃO
            ####################################################

            self.lbl_status.setText(
                "Sincronizando..."
            )

            manager = SefazSyncManager(
                self.client
            )

            resultado = manager.sincronizar(
                cnpj
            )

            ####################################################
            # ATUALIZAR TELA
            ####################################################

            ultimo_nsu = resultado.get(
                "ultimo_nsu",
                "-",
            )

            max_nsu = resultado.get(
                "max_nsu",
                "-",
            )

            quantidade_xml = resultado.get(
                "quantidade_xml",
                0,
            )

            importados = resultado.get(
                "documentos_importados",
                0,
            )

            lotes = resultado.get(
                "lotes_processados",
                0,
            )

            self.lbl_ultimo_nsu.setText(
                str(ultimo_nsu)
            )

            self.lbl_max_nsu.setText(
                str(max_nsu)
            )

            self.lbl_xml.setText(
                str(quantidade_xml)
            )

            self.lbl_importados.setText(
                str(importados)
            )

            self.lbl_lotes.setText(
                str(lotes)
            )

            ####################################################
            # LOG
            ####################################################

            self.adicionar_log(
                f"cStat: {resultado.get('cstat', '-')}"
            )

            self.adicionar_log(
                f"Motivo: {resultado.get('mensagem', '-')}"
            )

            self.adicionar_log(
                f"Último NSU: {ultimo_nsu}"
            )

            self.adicionar_log(
                f"Máximo NSU: {max_nsu}"
            )

            self.adicionar_log(
                f"XMLs baixados: {quantidade_xml}"
            )

            self.adicionar_log(
                f"NF-e importadas: {importados}"
            )

            self.adicionar_log(
                f"Lotes processados: {lotes}"
            )

            ####################################################
            # BLOQUEIO
            ####################################################

            if resultado.get(
                "bloqueado"
            ):

                self.lbl_status.setText(
                    "Aguardando SEFAZ"
                )

                self.progresso.setValue(
                    50
                )

                QMessageBox.warning(
                    self,
                    "SEFAZ",
                    resultado.get(
                        "mensagem",
                        "Consulta temporariamente bloqueada.",
                    ),
                )

                return

            ####################################################
            # SUCESSO
            ####################################################

            self.lbl_status.setText(
                "Sincronização concluída"
            )

            self.progresso.setValue(
                100
            )

            self.adicionar_log(
                "Sincronização concluída."
            )

            QMessageBox.information(
                self,
                "SEFAZ",
                (
                    "Sincronização concluída.\n\n"
                    f"XMLs baixados: {quantidade_xml}\n"
                    f"NF-e importadas: {importados}\n"
                    f"Último NSU: {ultimo_nsu}"
                ),
            )

        except Exception as erro:

            self.lbl_status.setText(
                "Erro"
            )

            self.progresso.setValue(
                0
            )

            self.adicionar_log(
                f"ERRO: {erro}"
            )

            QMessageBox.critical(
                self,
                "Erro na sincronização",
                str(erro),
            )

        finally:

            self.botao_sync.setEnabled(
                True
            )

            if self.client is not None:

                try:

                    self.client.desconectar()

                except Exception:

                    pass