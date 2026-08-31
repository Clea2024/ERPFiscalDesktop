from pathlib import Path

ROOT = Path.cwd()

PASTAS = [
    "app",
    "app/core",
    "app/config",
    "app/controllers",
    "app/database",
    "app/models",
    "app/repositories",
    "app/services",
    "app/ui",
    "app/utils",
    "app/resources",
    "database",
    "logs",
    "reports",
    "xml",
    "backups",
    "certificates",
    "tests",
]


ARQUIVOS = [
    "app.py",
    "requirements.txt",
    "README.md",
    "pyproject.toml",
    ".gitignore",
    ".env",
    "app/__init__.py",
    "app/core/__init__.py",
    "app/config/__init__.py",
    "app/controllers/__init__.py",
    "app/database/__init__.py",
    "app/models/__init__.py",
    "app/repositories/__init__.py",
    "app/services/__init__.py",
    "app/ui/__init__.py",
    "app/utils/__init__.py",
]


def criar_pastas():

    print("Criando pastas...")

    for pasta in PASTAS:
        caminho = ROOT / pasta
        caminho.mkdir(parents=True, exist_ok=True)

    print("Pastas criadas.")


def criar_arquivos():

    print("Criando arquivos...")

    for arquivo in ARQUIVOS:

        caminho = ROOT / arquivo

        if not caminho.exists():
            caminho.touch()

    print("Arquivos criados.")


def escrever_requirements():

    texto = """PySide6>=6.8
SQLAlchemy>=2.0
alembic>=1.14
loguru>=0.7
cryptography>=45
python-dotenv>=1.0
pandas>=2.2
openpyxl>=3.1
reportlab>=4.2
"""

    (ROOT / "requirements.txt").write_text(texto, encoding="utf-8")


def escrever_readme():

    texto = """# ERP Fiscal Desktop

Sistema ERP Fiscal Desktop.

"""

    (ROOT / "README.md").write_text(texto, encoding="utf-8")


def escrever_gitignore():

    texto = """__pycache__/
*.pyc
.venv/
database/*.db
logs/*
"""

    (ROOT / ".gitignore").write_text(texto, encoding="utf-8")


def escrever_pyproject():

    texto = """[project]
name="ERPFiscalDesktop"
version="0.1.0"
"""

    (ROOT / "pyproject.toml").write_text(texto, encoding="utf-8")


def main():

    print("=" * 60)
    print("ERP Fiscal Desktop")
    print("=" * 60)

    criar_pastas()
    criar_arquivos()

    escrever_requirements()
    escrever_readme()
    escrever_gitignore()
    escrever_pyproject()

    print()
    print("Projeto criado com sucesso.")


if __name__ == "__main__":
    main()
    def escrever_app():

    codigo = '''import sys

from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow


def main():

    app = QApplication(sys.argv)

    janela = MainWindow()
    janela.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
'''

    (ROOT / "app.py").write_text(codigo, encoding="utf-8")


def escrever_app():

    codigo = '''import sys

from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow


def main():

    app = QApplication(sys.argv)

    janela = MainWindow()
    janela.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
'''

    (ROOT / "app.py").write_text(codigo, encoding="utf-8")


def escrever_main_window():

    codigo = '''from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QHBoxLayout,
    QMainWindow,
    QStatusBar,
    QVBoxLayout,
    QWidget
)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ERP Fiscal Desktop CE")
        self.resize(1400, 800)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout()
        central.setLayout(layout)

        menu = QListWidget()

        menu.addItems([
            "Dashboard",
            "Empresas",
            "Usuários",
            "Certificados",
            "Download XML",
            "Relatórios",
            "Configurações"
        ])

        menu.setMaximumWidth(230)

        layout.addWidget(menu)

        painel = QVBoxLayout()

        titulo = QLabel("ERP Fiscal Desktop")

        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        titulo.setStyleSheet("""
        font-size:26px;
        font-weight:bold;
        """)

        painel.addWidget(titulo)

        painel.addWidget(QLabel("Bem-vindo ao ERP Fiscal Desktop."))

        painel.addStretch()

        layout.addLayout(painel)

        self.setStatusBar(QStatusBar())

        self.statusBar().showMessage("Sistema iniciado.")
'''

    caminho = ROOT / "app" / "ui" / "main_window.py"
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(codigo, encoding="utf-8")
    def main():

    print("=" * 60)
    print("ERP Fiscal Desktop")
    print("=" * 60)

    criar_pastas()
    criar_arquivos()

    escrever_requirements()
    escrever_readme()
    escrever_gitignore()
    escrever_pyproject()

    escrever_app()
    escrever_main_window()

    print()
    print("Projeto criado com sucesso.")