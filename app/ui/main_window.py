from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from app.dashboard.dashboard_widget import DashboardWidget

from app.ui.sidebar import SideBar
from app.ui.company_dialog import CompanyDialog
from app.ui.dialogs.certificate_dialog import CertificateDialog
from app.ui.dialogs.xml_import_dialog import XMLImportDialog
from app.ui.dialogs.xml_consulta_dialog import XMLConsultaDialog
from app.ui.dialogs.sefaz_sync_dialog import SefazSyncDialog
from app.ui.dialogs.audit_dialog import AuditDialog
from app.ui.dialogs.reports_dialog import ReportsDialog
from app.ui.dialogs.users_dialog import UsersDialog
from app.ui.dialogs.settings_dialog import SettingsDialog
from app.ui.dialogs.tributacao_federal_dialog import (
    TributacaoFederalDialog,
)
from app.ui.dialogs.xml_saida_import_dialog import (
    XMLSaidaImportDialog,
)
from app.ui.dialogs.pis_cofins_dialog import (
    PisCofinsDialog,
)

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "ERP Fiscal Desktop CE"
        )

        self.resize(
            1450,
            850,
        )

        ########################################################
        # JANELA CENTRAL
        ########################################################

        central = QWidget()

        self.setCentralWidget(
            central
        )

        layout = QHBoxLayout(
            central
        )

        ########################################################
        # MENU LATERAL
        ########################################################

        self.sidebar = SideBar()

        self.sidebar.itemClicked.connect(
            self.abrir_menu
        )

        layout.addWidget(
            self.sidebar
        )

        ########################################################
        # DASHBOARD
        ########################################################

        painel = QVBoxLayout()

        self.dashboard = DashboardWidget()

        painel.addWidget(
            self.dashboard
        )

        layout.addLayout(
            painel
        )

        ########################################################
        # STATUS
        ########################################################

        self.setStatusBar(
            QStatusBar()
        )

        self.statusBar().showMessage(
            "Sistema iniciado."
        )

    ############################################################
    # ABRIR MENU
    ############################################################

    def abrir_menu(
        self,
        item,
    ):

        texto = item.text()

        print(
            f"[MENU] {texto}"
        )

        ########################################################
        # DASHBOARD
        ########################################################

        if texto == "🏠 Dashboard":

            self.dashboard.atualizar()

            self.statusBar().showMessage(
                "Dashboard atualizado."
            )

        ########################################################
        # CONFIGURAÇÕES
        ########################################################

        elif texto == "⚙ Configurações":

            tela = SettingsDialog(
                self
            )

            tela.exec()

        ########################################################
        # EMPRESAS
        ########################################################

        elif texto == "🏢 Empresas":

            tela = CompanyDialog()

            tela.exec()

            self.dashboard.atualizar()

        ########################################################
        # USUÁRIOS
        ########################################################

        elif texto == "👥 Usuários":

            tela = UsersDialog(
                self
            )

            tela.exec()
        ########################################################
        # CERTIFICADOS
        ########################################################

        elif texto == "🔐 Certificados":

            tela = CertificateDialog()

            tela.exec()

        ########################################################
        # SEFAZ
        ########################################################

        elif texto == "🏛 SEFAZ":

            tela = SefazSyncDialog(
                self
            )

            tela.exec()

            self.dashboard.atualizar()

        ########################################################
        # XML
        ########################################################

        elif texto == "📄 XML":

            tela = XMLConsultaDialog()

            tela.exec()

            self.dashboard.atualizar()

        ########################################################
        # IMPORTAR XML
        ########################################################

        elif texto == "📥 Importar XML":

            tela = XMLImportDialog()

            tela.exec()

            self.dashboard.atualizar()

        ########################################################
        # IMPORTAR SAÍDAS
        ########################################################

        elif texto == "📤 Importar Saídas":

            tela = XMLSaidaImportDialog(
                self
            )

            tela.exec()

            self.dashboard.atualizar()

        ########################################################
        # AUDITORIA
        ########################################################

        elif texto == "📊 Auditoria":

            tela = AuditDialog(
                self
            )

            tela.exec()

        ########################################################
        # RELATÓRIOS
        ########################################################

        elif texto == "📑 Relatórios":

            tela = ReportsDialog(
                self
            )

            tela.exec()
        ########################################################
        # APURAÇÃO FEDERAL
        ########################################################

        elif texto == "💰 Apuração Federal":

            tela = TributacaoFederalDialog(
                self
            )

            tela.exec()

        elif texto == "🧾 PIS / COFINS":

            tela = PisCofinsDialog(
                self
            )

            tela.exec()

        ########################################################
        # OUTROS
        ########################################################

        else:

            print(
                f"Menu não implementado: {texto}"
            )

            self.statusBar().showMessage(
                f"Menu não implementado: {texto}"
            )