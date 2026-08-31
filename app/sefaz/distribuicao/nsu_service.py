from pathlib import Path
import json


class NSUService:

    def __init__(self, arquivo):

        self.arquivo = Path(arquivo)

        self.arquivo.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.arquivo.exists():

            self.salvar(
                "000000000000000"
            )

    ############################################################

    def obter(self):

        try:

            dados = json.loads(

                self.arquivo.read_text(
                    encoding="utf-8"
                )

            )

            return dados.get(
                "ult_nsu",
                "000000000000000",
            )

        except Exception:

            return "000000000000000"

    ############################################################

    def salvar(
        self,
        nsu,
    ):

        self.arquivo.write_text(

            json.dumps(
                {
                    "ult_nsu": str(nsu).zfill(15)
                },
                indent=4,
            ),

            encoding="utf-8",
        )

    ############################################################

    def atualizar(
        self,
        novo_nsu,
    ):

        atual = self.obter()

        if int(novo_nsu) > int(atual):

            self.salvar(novo_nsu)

            return True

        return False

    ############################################################

    def reiniciar(self):

        self.salvar(
            "000000000000000"
        )