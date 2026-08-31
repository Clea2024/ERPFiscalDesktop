from datetime import datetime
from pathlib import Path
import json

from app.auditoria.services.data_update_service import (
    DataUpdateService,
)


class UpdateManager:

    def __init__(self):

        self.service = DataUpdateService()

        self.base = (
            Path(__file__).parent / "tables"
        )

        self.version_file = (
            self.base / "version.json"
        )

    ############################################################

    def obter_versao(self):

        if not self.version_file.exists():

            return {
                "versao": "0.0.0",
                "ultima_atualizacao": None,
            }

        with open(
            self.version_file,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    ############################################################

    def salvar_versao(self, versao):

        dados = {

            "versao": versao,

            "ultima_atualizacao":
                datetime.now().isoformat()

        }

        with open(
            self.version_file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                dados,
                f,
                indent=4,
                ensure_ascii=False,
            )

    ############################################################

    def atualizar_tabela(
        self,
        nome,
        dados,
        versao,
    ):

        self.service.salvar_tabela(
            nome,
            dados,
        )

        self.salvar_versao(
            versao,
        )

    ############################################################

    def listar_tabelas(self):

        return [

            "cfop",

            "ncm",

            "cest",

            "beneficios",

            "cst",

            "csosn",

            "pis",

            "cofins",

            "ipi",

            "ibs",

            "cbs",

            "is",

        ]