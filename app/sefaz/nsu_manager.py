import json
from pathlib import Path


class NSUManager:

    def __init__(self):

        self.arquivo = (
            Path(__file__).parent /
            "cache" /
            "ultimo_nsu.json"
        )

        self.arquivo.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.arquivo.exists():

            self.salvar("000000000000000")

    ############################################################

    def obter(self):

        with open(
            self.arquivo,
            "r",
            encoding="utf-8",
        ) as f:

            dados = json.load(f)

        return dados["ultimo_nsu"]

    ############################################################

    def salvar(self, nsu):

        with open(
            self.arquivo,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                {
                    "ultimo_nsu": str(nsu)
                },
                f,
                indent=4,
            )