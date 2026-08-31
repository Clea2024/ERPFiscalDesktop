from pathlib import Path
import json


class LegislationEngine:

    def __init__(self):

        self.base_path = (
            Path(__file__).parent / "tables"
        )

        self.cfop = self._carregar("cfop.json")
        self.ncm = self._carregar("ncm.json")
        self.cest = self._carregar("cest.json")

    ############################################################

    def _carregar(self, arquivo):

        caminho = self.base_path / arquivo

        if not caminho.exists():

            return {}

        with open(
            caminho,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    ############################################################

    def obter_cfop(self, codigo):

        return self.cfop.get(str(codigo))

    ############################################################

    def obter_ncm(self, codigo):

        return self.ncm.get(str(codigo))

    ############################################################

    def obter_cest(self, codigo):

        return self.cest.get(str(codigo))