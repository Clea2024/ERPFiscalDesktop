import json
from pathlib import Path


class DataUpdateService:

    def __init__(self):

        self.tables = (
            Path(__file__).parent.parent / "tables"
        )

        self.tables.mkdir(
            exist_ok=True,
            parents=True,
        )

    ############################################################

    def salvar_tabela(
        self,
        nome,
        dados,
    ):

        arquivo = self.tables / f"{nome}.json"

        with open(
            arquivo,
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

    def carregar_tabela(
        self,
        nome,
    ):

        arquivo = self.tables / f"{nome}.json"

        if not arquivo.exists():

            return {}

        with open(
            arquivo,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    ############################################################

    def tabela_existe(
        self,
        nome,
    ):

        return (
            self.tables / f"{nome}.json"
        ).exists()