from pathlib import Path

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from app.database.database import get_session
from app.models.company import Company
from app.services.xml_saida_import_service import (
    XMLSaidaImportService,
)


class XMLSaidaImportDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle(
            "Importar XMLs de Saída"
        )

        self.resize(
            700,
            320,
        )

        self.pasta = ""

        self.montar_tela()
        self.carregar_empresas()

    def montar_tela(self):

        layout = QVBoxLayout(
            self
        )

        titulo = QLabel(
            "IMPORTAÇÃO DE NF-e / NFC-e EMITIDAS"
        )

        titulo.setStyleSheet(
            """
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            """
        )

        layout.addWidget(
            titulo
        )

        formulario = QFormLayout()

        self.cmbEmpresa = QComboBox()

        formulario.addRow(
            "Empresa:",
            self.cmbEmpresa,
        )

        self.lblPasta = QLabel(
            "Nenhuma pasta selecionada."
        )

        formulario.addRow(
            "Pasta:",
            self.lblPasta,
        )

        layout.addLayout(
            formulario
        )

        btnPasta = QPushButton(
            "Selecionar pasta"
        )

        btnPasta.clicked.connect(
            self.selecionar_pasta
        )

        layout.addWidget(
            btnPasta
        )

        btnImportar = QPushButton(
            "Importar Saídas"
        )

        btnImportar.clicked.connect(
            self.importar
        )

        layout.addWidget(
            btnImportar
        )

    def carregar_empresas(self):

        db = get_session()

        try:

            empresas = (
                db.query(Company)
                .order_by(
                    Company.razao_social
                )
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

    def selecionar_pasta(self):

        pasta = QFileDialog.getExistingDirectory(
            self,
            "Selecionar pasta de XMLs de saída",
            str(
                Path(
                    r"C:\Users\clea-\ERPFiscalDesktop\xml\saidas"
                )
            ),
        )

        if not pasta:
            return

        self.pasta = pasta

        self.lblPasta.setText(
            pasta
        )

    def importar(self):

        company_id = (
            self.cmbEmpresa.currentData()
        )

        if not company_id:

            QMessageBox.warning(
                self,
                "Importar Saídas",
                "Selecione uma empresa.",
            )

            return

        if not self.pasta:

            QMessageBox.warning(
                self,
                "Importar Saídas",
                "Selecione a pasta dos XMLs.",
            )

            return

        service = XMLSaidaImportService()

        try:

            resultado = (
                service.importar_pasta(
                    self.pasta,
                    company_id,
                )
            )

            mensagem = (
                f"Importados: {resultado['importados']}\n"
                f"Ignorados: {resultado['ignorados']}\n"
                f"Erros: {resultado['erros']}"
            )

            QMessageBox.information(
                self,
                "Importação concluída",
                mensagem,
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

        finally:

            service.fechar()
