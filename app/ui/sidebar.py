from PySide6.QtWidgets import QListWidget


class SideBar(QListWidget):

    def __init__(self):

        super().__init__()

        self.setFixedWidth(
            240
        )

        self.addItems(
            [
                "🏠 Dashboard",
                "🏢 Empresas",
                "👥 Usuários",
                "🔐 Certificados",
                "📄 XML",
                "📥 Importar XML",
                "📤 Importar Saídas",
                "🏛 SEFAZ",
                "📊 Auditoria",
                "📑 Relatórios",
                "💰 Apuração Federal",
                "🧾 PIS / COFINS",
                "⚙ Configurações",
            ]
        )

        self.setStyleSheet(
            """
            QListWidget {
                background: #223044;
                color: white;
                border: none;
                font-size: 15px;
            }

            QListWidget::item {
                padding: 12px;
            }

            QListWidget::item:selected {
                background: #1565C0;
            }
            """
        )