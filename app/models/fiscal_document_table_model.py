from decimal import Decimal

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
)


class FiscalDocumentTableModel(QAbstractTableModel):

    HEADERS = [
        "Chave",
        "Modelo",
        "Número",
        "Série",
        "Emitente",
        "Destinatário",
        "Valor",
        "Emissão",
    ]

    def __init__(self, documentos=None):

        super().__init__()

        self._documentos = documentos or []

    ####################################################################
    # Dados
    ####################################################################

    def atualizar(self, documentos):

        self.beginResetModel()

        self._documentos = documentos

        self.endResetModel()

    ####################################################################
    # Linhas
    ####################################################################

    def rowCount(
        self,
        parent=QModelIndex(),
    ):

        return len(self._documentos)

    ####################################################################
    # Colunas
    ####################################################################

    def columnCount(
        self,
        parent=QModelIndex(),
    ):

        return len(self.HEADERS)

    ####################################################################
    # Cabeçalhos
    ####################################################################

    def headerData(
        self,
        section,
        orientation,
        role,
    ):

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:

            return self.HEADERS[section]

        return str(section + 1)

    ####################################################################
    # Conteúdo das células
    ####################################################################

    def data(
        self,
        index,
        role,
    ):

        if not index.isValid():
            return None

        documento = self._documentos[index.row()]

        if role == Qt.DisplayRole:

            coluna = index.column()

            if coluna == 0:
                return documento.chave

            elif coluna == 1:
                return documento.modelo

            elif coluna == 2:
                return documento.numero

            elif coluna == 3:
                return documento.serie

            elif coluna == 4:
                return documento.emitente_nome

            elif coluna == 5:
                return documento.destinatario_nome

            elif coluna == 6:

                valor = documento.valor_total

                if isinstance(valor, Decimal):

                    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                return str(valor)

            elif coluna == 7:

                if documento.data_emissao:

                    return documento.data_emissao.strftime(
                        "%d/%m/%Y"
                    )

                return ""

        if role == Qt.TextAlignmentRole:

            if index.column() in (2, 3, 6):

                return Qt.AlignCenter

        return None

    ####################################################################
    # Documento selecionado
    ####################################################################

    def documento(self, linha):

        if linha < 0:

            return None

        if linha >= len(self._documentos):

            return None

        return self._documentos[linha]