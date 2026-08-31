import json
from pathlib import Path


class RuleEngine:

    def __init__(self):

        self.base = (
            Path(__file__).parent / "rules_data"
        )

        self.base.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.cache = {}

    ############################################################

    def carregar(self, regra):

        if regra in self.cache:

            return self.cache[regra]

        arquivo = self.base / f"{regra}.json"

        if not arquivo.exists():

            self.cache[regra] = []

            return []

        with open(
            arquivo,
            "r",
            encoding="utf-8",
        ) as f:

            dados = json.load(f)

        self.cache[regra] = dados

        return dados

    ############################################################

    def salvar(
        self,
        regra,
        dados,
    ):

        arquivo = self.base / f"{regra}.json"

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

        self.cache[regra] = dados