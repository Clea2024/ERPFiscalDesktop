from pathlib import Path
from xml.etree import ElementTree


class XMLReader:
    """
    Responsável apenas por abrir e devolver
    a árvore XML.

    Não interpreta regras fiscais.
    Não cria objetos.
    Não valida dados.
    """

    ############################################################

    def read(
        self,
        arquivo,
    ):

        arquivo = Path(arquivo)

        if not arquivo.exists():

            raise FileNotFoundError(
                f"XML não encontrado: {arquivo}"
            )

        tree = ElementTree.parse(
            arquivo
        )

        return tree.getroot()

    ############################################################

    def tostring(
        self,
        root,
    ):

        return ElementTree.tostring(
            root,
            encoding="unicode",
        )