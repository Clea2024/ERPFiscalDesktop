from app.database.database import get_session

from app.fiscal.parser import FiscalParser
from app.fiscal.validator import FiscalValidator
from app.fiscal.storage import FiscalStorage

from app.repositories.fiscal_document_repository import (
    FiscalDocumentRepository,
)


class FiscalService:

    def __init__(self):

        self.db = get_session()

        self.parser = FiscalParser()

        self.validator = FiscalValidator()

        self.storage = FiscalStorage()

        self.repository = FiscalDocumentRepository(
            self.db
        )

    ####################################################################
    # IMPORTAÇÃO
    ####################################################################

    def importar_xml(
        self,
        arquivo,
        empresa_id=None,
    ):

        documento = self.parser.ler_xml(
            arquivo
        )

        documento.empresa_id = empresa_id

        valido, erros = self.validator.validar(
            documento
        )

        if not valido:

            return (
                False,
                erros,
            )

        if self.repository.existe(
            documento.chave
        ):

            return (
                False,
                [
                    "Documento já importado."
                ],
            )

        ############################################################
        # Copia o XML para a pasta definitiva
        ############################################################

        caminho = self.storage.copiar_xml(
            arquivo,
            documento,
        )

        ############################################################
        # Guarda o caminho no documento
        ############################################################

        documento.xml_path = str(caminho)

        ############################################################
        # Grava no banco
        ############################################################

        self.repository.inserir(
            documento
        )

        return (
            True,
            documento,
        )

    ####################################################################
    # LISTAR
    ####################################################################

    def listar(self):

        return self.repository.listar()

    ####################################################################
    # BUSCAR
    ####################################################################

    def buscar_por_chave(
        self,
        chave,
    ):

        return self.repository.buscar_por_chave(
            chave
        )

    ####################################################################
    # REMOVER
    ####################################################################

    def remover(
        self,
        chave,
    ):

        return self.repository.remover(
            chave
        )