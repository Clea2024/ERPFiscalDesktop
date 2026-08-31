from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from app.database.database import get_session
from app.models.user import User
from app.repositories.user_repository import (
    UserRepository,
)
from app.services.password_service import (
    PasswordService,
)


class UsersDialog(QDialog):

    def __init__(
        self,
        parent=None,
    ):

        super().__init__(parent)

        self.setWindowTitle(
            "Usuários"
        )

        self.resize(
            900,
            650,
        )

        self.db = get_session()

        self.repository = (
            UserRepository(
                self.db
            )
        )

        self.usuario_selecionado = None

        layout = QVBoxLayout(
            self
        )

        ########################################################
        # TÍTULO
        ########################################################

        titulo = QLabel(
            "Gerenciamento de Usuários"
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )

        titulo.setStyleSheet(
            """
            QLabel {
                font-size: 22px;
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

        self.txtNome = QLineEdit()

        self.txtLogin = QLineEdit()

        self.txtEmail = QLineEdit()

        self.txtSenha = QLineEdit()

        self.txtSenha.setEchoMode(
            QLineEdit.Password
        )

        self.chkAdministrador = (
            QCheckBox(
                "Administrador"
            )
        )

        self.chkAtivo = QCheckBox(
            "Usuário ativo"
        )

        self.chkAtivo.setChecked(
            True
        )

        formulario.addRow(
            "Nome:",
            self.txtNome,
        )

        formulario.addRow(
            "Login:",
            self.txtLogin,
        )

        formulario.addRow(
            "E-mail:",
            self.txtEmail,
        )

        formulario.addRow(
            "Senha:",
            self.txtSenha,
        )

        formulario.addRow(
            "",
            self.chkAdministrador,
        )

        formulario.addRow(
            "",
            self.chkAtivo,
        )

        layout.addLayout(
            formulario
        )

        ########################################################
        # BOTÕES DO CADASTRO
        ########################################################

        botoes = QHBoxLayout()

        self.btNovo = QPushButton(
            "Novo"
        )

        self.btSalvar = QPushButton(
            "Salvar"
        )

        self.btDesativar = QPushButton(
            "Ativar / Desativar"
        )

        botoes.addWidget(
            self.btNovo
        )

        botoes.addWidget(
            self.btSalvar
        )

        botoes.addWidget(
            self.btDesativar
        )

        botoes.addStretch()

        layout.addLayout(
            botoes
        )

        ########################################################
        # TABELA
        ########################################################

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(
            6
        )

        self.tabela.setHorizontalHeaderLabels(
            [
                "ID",
                "Nome",
                "Login",
                "E-mail",
                "Administrador",
                "Ativo",
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
        # FECHAR
        ########################################################

        rodape = QHBoxLayout()

        self.btFechar = QPushButton(
            "Fechar"
        )

        rodape.addStretch()

        rodape.addWidget(
            self.btFechar
        )

        layout.addLayout(
            rodape
        )

        ########################################################
        # EVENTOS
        ########################################################

        self.btNovo.clicked.connect(
            self.novo
        )

        self.btSalvar.clicked.connect(
            self.salvar
        )

        self.btDesativar.clicked.connect(
            self.alternar_status
        )

        self.btFechar.clicked.connect(
            self.close
        )

        self.tabela.cellClicked.connect(
            self.selecionar_usuario
        )

        ########################################################

        self.carregar_usuarios()

    ############################################################
    # CARREGAR
    ############################################################

    def carregar_usuarios(self):

        usuarios = (
            self.repository.listar()
        )

        self.tabela.setRowCount(
            len(usuarios)
        )

        for linha, usuario in enumerate(
            usuarios
        ):

            valores = [
                usuario.id,
                usuario.nome,
                usuario.login,
                usuario.email or "",
                (
                    "Sim"
                    if usuario.administrador
                    else "Não"
                ),
                (
                    "Sim"
                    if usuario.ativo
                    else "Não"
                ),
            ]

            for coluna, valor in enumerate(
                valores
            ):

                self.tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(
                        str(valor)
                    ),
                )

        self.tabela.resizeColumnsToContents()

    ############################################################
    # NOVO
    ############################################################

    def novo(self):

        self.usuario_selecionado = None

        self.txtNome.clear()
        self.txtLogin.clear()
        self.txtEmail.clear()
        self.txtSenha.clear()

        self.chkAdministrador.setChecked(
            False
        )

        self.chkAtivo.setChecked(
            True
        )

        self.txtNome.setFocus()

    ############################################################
    # SELECIONAR
    ############################################################

    def selecionar_usuario(
        self,
        linha,
        coluna,
    ):

        item_id = self.tabela.item(
            linha,
            0,
        )

        if item_id is None:
            return

        usuario = (
            self.repository.buscar_por_id(
                int(
                    item_id.text()
                )
            )
        )

        if usuario is None:
            return

        self.usuario_selecionado = (
            usuario
        )

        self.txtNome.setText(
            usuario.nome or ""
        )

        self.txtLogin.setText(
            usuario.login or ""
        )

        self.txtEmail.setText(
            usuario.email or ""
        )

        self.txtSenha.clear()

        self.chkAdministrador.setChecked(
            bool(
                usuario.administrador
            )
        )

        self.chkAtivo.setChecked(
            bool(
                usuario.ativo
            )
        )

    ############################################################
    # SALVAR
    ############################################################

    def salvar(self):

        nome = (
            self.txtNome.text()
            .strip()
        )

        login = (
            self.txtLogin.text()
            .strip()
        )

        email = (
            self.txtEmail.text()
            .strip()
        )

        senha = (
            self.txtSenha.text()
        )

        if not nome:

            QMessageBox.warning(
                self,
                "Usuários",
                "Informe o nome.",
            )

            return

        if not login:

            QMessageBox.warning(
                self,
                "Usuários",
                "Informe o login.",
            )

            return

        existente = (
            self.repository
            .buscar_por_login(
                login
            )
        )

        ########################################################
        # NOVO
        ########################################################

        if self.usuario_selecionado is None:

            if existente is not None:

                QMessageBox.warning(
                    self,
                    "Usuários",
                    "Este login já está cadastrado.",
                )

                return

            if not senha:

                QMessageBox.warning(
                    self,
                    "Usuários",
                    "Informe a senha.",
                )

                return

            usuario = User(
                nome=nome,
                login=login,
                email=email,
                senha=(
                    PasswordService
                    .gerar_hash(
                        senha
                    )
                ),
                administrador=(
                    self.chkAdministrador
                    .isChecked()
                ),
                ativo=(
                    self.chkAtivo
                    .isChecked()
                ),
            )

            self.repository.inserir(
                usuario
            )

        ########################################################
        # EDITAR
        ########################################################

        else:

            usuario = (
                self.usuario_selecionado
            )

            if (
                existente is not None
                and existente.id
                != usuario.id
            ):

                QMessageBox.warning(
                    self,
                    "Usuários",
                    "Este login pertence a outro usuário.",
                )

                return

            usuario.nome = nome
            usuario.login = login
            usuario.email = email

            usuario.administrador = (
                self.chkAdministrador
                .isChecked()
            )

            usuario.ativo = (
                self.chkAtivo
                .isChecked()
            )

            if senha:

                usuario.senha = (
                    PasswordService
                    .gerar_hash(
                        senha
                    )
                )

            self.repository.atualizar()

        QMessageBox.information(
            self,
            "Usuários",
            "Usuário salvo com sucesso.",
        )

        self.novo()

        self.carregar_usuarios()

    ############################################################
    # ATIVAR / DESATIVAR
    ############################################################

    def alternar_status(self):

        if self.usuario_selecionado is None:

            QMessageBox.warning(
                self,
                "Usuários",
                "Selecione um usuário.",
            )

            return

        usuario = (
            self.usuario_selecionado
        )

        usuario.ativo = not bool(
            usuario.ativo
        )

        self.repository.atualizar()

        self.chkAtivo.setChecked(
            usuario.ativo
        )

        self.carregar_usuarios()

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