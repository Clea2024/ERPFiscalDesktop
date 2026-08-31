from app.auditoria.audit_engine import AuditEngine
from app.ui.dialogs.audit_dialog import AuditDialog

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QWidget,
    QScrollArea,
)
class XMLDetailDialog(QDialog):
    def __init__(self, documento, parent=None):
        super().__init__(parent)
        self.documento=documento
        self.setWindowTitle(f"NF-e {documento.numero}")
        self.resize(1200,980)
        self.montar_tela()

    def montar_tela(self):
        layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        conteudo = QVBoxLayout(container)

        conteudo.setContentsMargins(
            10,
            10,
            10,
            10,
        )

        conteudo.setSpacing(
            8
        )

        scroll.setWidget(
            container
        )

        layout.addWidget(
            scroll
        )

        titulo=QLabel("DETALHES DA NOTA FISCAL ELETRÔNICA")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size:22px;font-weight:bold;padding:8px;")
        conteudo.addWidget(titulo)

        def add_group(title, rows):
            box=QGroupBox(title)
            grid=QGridLayout(box)
            for i,(k,v) in enumerate(rows):
                grid.addWidget(QLabel(k),i,0)
                grid.addWidget(QLabel(str(v)),i,1)
            conteudo.addWidget(box)

        add_group("Dados Gerais",[
            ("Chave",self.documento.chave),
            ("Número",self.documento.numero),
            ("Série",self.documento.serie),
            ("Modelo",self.documento.modelo),
            ("Emissão",self.documento.data_emissao.strftime("%d/%m/%Y %H:%M") if self.documento.data_emissao else "")
        ])
        add_group("Emitente",[("Nome",self.documento.emitente_nome),("CNPJ",self.documento.emitente_cnpj)])
        add_group("Destinatário",[("Nome",self.documento.destinatario_nome),("CNPJ",self.documento.destinatario_cnpj)])
        box=QGroupBox("Produtos")
        box.setMaximumHeight(380)
        v=QVBoxLayout(box)
        tabela=QTableWidget()
        tabela.setColumnCount(10)

        tabela.setHorizontalHeaderLabels(
            [
                "Item",
                "Código",
                "Descrição",
                "CFOP",
                "NCM",
                "Quantidade",
                "Valor",
                "IBS",
                "CBS",
                "IS",
            ]
        )
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        tabela.horizontalHeader().setStretchLastSection(True)

        itens = getattr(
            self.documento,
            "itens",
            [],
        )
        total_ibs = sum(
            getattr(
                item,
                "ibs",
                0,
            )
            or 0
            for item in itens
        )

        total_cbs = sum(
            getattr(
                item,
                "cbs",
                0,
            )
            or 0
            for item in itens
        )

        total_is = sum(
            getattr(
                item,
                "imposto_seletivo",
                0,
            )
            or 0
            for item in itens
        )

        add_group(
            "Totais",
            [
                (
                    "Valor Total",
                    f"R$ {self.documento.valor_total}",
                ),
                (
                    "Total IBS",
                    f"R$ {total_ibs:.2f}",
                ),
                (
                    "Total CBS",
                    f"R$ {total_cbs:.2f}",
                ),
                (
                    "Total IS",
                    f"R$ {total_is:.2f}",
                ),
            ],
        )

        tabela.setRowCount(len(itens))
        for r, item in enumerate(itens):

            ibs = getattr(
                item,
                "ibs",
                0,
            ) or 0

            cbs = getattr(
                item,
                "cbs",
                0,
            ) or 0

            imposto_seletivo = getattr(
                item,
                "imposto_seletivo",
                0,
            ) or 0

            vals = [
                item.numero_item,
                item.codigo,
                item.descricao,
                item.cfop,
                item.ncm,
                item.quantidade,
                f"R$ {item.valor_total}",
                f"R$ {ibs}",
                f"R$ {cbs}",
                f"R$ {imposto_seletivo}",
            ]

            for c, val in enumerate(vals):

                tabela.setItem(
                    r,
                    c,
                    QTableWidgetItem(
                        str(val)
                    )
                )
        tabela.setMinimumHeight(250)
        tabela.setMaximumHeight(320)
        v.addWidget(tabela)
        conteudo.addWidget(box)

        hb=QHBoxLayout()
        hb.addStretch()
        ba=QPushButton("🔍 Auditoria Fiscal")
        bf=QPushButton("❌ Fechar")
        ba.clicked.connect(self.executar_auditoria)
        bf.clicked.connect(self.close)
        hb.addWidget(ba)
        hb.addWidget(bf)
        conteudo.addLayout(hb)

    def executar_auditoria(self):
        try:
            resultados=AuditEngine().auditar(self.documento)
            AuditDialog(resultados,self).exec()
        except Exception as e:
            QMessageBox.critical(self,"Erro",str(e))