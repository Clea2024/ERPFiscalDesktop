from app.auditoria.services.data_update_service import (
    DataUpdateService,
)


class TableLoader:

    def __init__(self):

        self.service = DataUpdateService()

        self.cfop = self.service.carregar_tabela(
            "cfop"
        )

        self.ncm = self.service.carregar_tabela(
            "ncm"
        )

        self.cest = self.service.carregar_tabela(
            "cest"
        )

    ############################################################

    def buscar_cfop(
        self,
        codigo,
    ):

        return self.cfop.get(str(codigo))

    ############################################################

    def buscar_ncm(
        self,
        codigo,
    ):

        return self.ncm.get(str(codigo))

    ############################################################

    def buscar_cest(
        self,
        codigo,
    ):

        return self.cest.get(str(codigo))