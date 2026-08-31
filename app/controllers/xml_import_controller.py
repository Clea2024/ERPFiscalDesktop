from app.services.xml_import_service import (
    XMLImportService,
)


class XMLImportController:

    def __init__(self):

        self.service = XMLImportService()

    ####################################################################

    def importar(
        self,
        company_id,
        arquivo_xml,
    ):

        return self.service.importar(
            company_id,
            arquivo_xml,
        )

    ####################################################################

    def importar_varios(
        self,
        company_id,
        arquivos,
    ):

        resultado = []

        for arquivo in arquivos:

            ok, retorno = self.importar(
                company_id,
                arquivo,
            )

            resultado.append(
                {
                    "arquivo": arquivo,
                    "sucesso": ok,
                    "resultado": retorno,
                }
            )

        return resultado

    ####################################################################

    def listar(self):

        return self.service.listar()

    ####################################################################

    def listar_empresa(
        self,
        company_id,
    ):

        return self.service.listar_empresa(
            company_id
        )