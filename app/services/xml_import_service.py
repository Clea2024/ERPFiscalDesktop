from pathlib import Path

from app.database.database import get_session
from app.fiscal.service import FiscalService
from app.models.fiscal_document import FiscalDocumentModel
from app.repositories.fiscal_document_repository import (
    FiscalDocumentRepository,
)


class XMLImportService:

    def __init__(self):

        self.db = get_session()

        self.fiscal = FiscalService()

        self.repository = FiscalDocumentRepository(
            self.db
        )

    ####################################################################

    def importar(
        self,
        company_id,
        arquivo_xml,
    ):

        ok, resultado = self.fiscal.importar_xml(
            arquivo_xml,
            company_id,
        )

        if not ok:

            return False, resultado

        documento = resultado

        registro = FiscalDocumentModel(

            company_id=company_id,

            chave=documento.chave,

            modelo=documento.modelo,

            numero=documento.numero,

            serie=documento.serie,

            data_emissao=documento.data_emissao,

            emitente_cnpj=documento.emitente_cnpj,

            emitente_nome=documento.emitente_nome,

            destinatario_cnpj=documento.destinatario_cnpj,

            destinatario_nome=documento.destinatario_nome,

            valor_total=documento.valor_total,

            protocolo=documento.protocolo,

            origem=documento.origem,

            xml_path=str(
                Path("xml")
            ),

            status="IMPORTADO",
        )

        if self.repository.existe_chave(
            registro.chave
        ):

            return (
                False,
                [
                    "Documento já cadastrado."
                ],
            )

        self.repository.inserir(
            registro
        )

        return (
            True,
            registro,
        )

    ####################################################################

    def listar(self):

        return self.repository.listar()

    ####################################################################

    def listar_empresa(
        self,
        company_id,
    ):

        return self.repository.listar_empresa(
            company_id
        )