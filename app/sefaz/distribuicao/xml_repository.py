from pathlib import Path
from datetime import datetime


class XmlRepository:

    def __init__(self, pasta_base="xml"):

        self.base = Path(pasta_base)

        self.base.mkdir(
            parents=True,
            exist_ok=True,
        )

    ############################################################

    def salvar(
        self,
        chave: str,
        xml: str,
        data=None,
    ):

        if data is None:

            data = datetime.now()

        ano = str(data.year)

        mes = f"{data.month:02d}"

        pasta = self.base / ano / mes

        pasta.mkdir(
            parents=True,
            exist_ok=True,
        )

        arquivo = pasta / f"{chave}.xml"

        arquivo.write_text(
            xml,
            encoding="utf-8",
        )

        return arquivo

    ############################################################

    def existe(
        self,
        chave: str,
        data=None,
    ):

        if data is None:

            data = datetime.now()

        ano = str(data.year)

        mes = f"{data.month:02d}"

        arquivo = (
            self.base
            / ano
            / mes
            / f"{chave}.xml"
        )

        return arquivo.exists()

    ############################################################

    def listar(
        self,
        ano=None,
        mes=None,
    ):

        pasta = self.base

        if ano:

            pasta = pasta / str(ano)

        if mes:

            pasta = pasta / f"{int(mes):02d}"

        if not pasta.exists():

            return []

        return sorted(
            pasta.glob("*.xml")
        )