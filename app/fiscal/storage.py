from datetime import datetime
from pathlib import Path
import shutil

from app.fiscal.document import FiscalDocument


class FiscalStorage:

    def __init__(self):

        self.raiz = Path("xml")

        self.raiz.mkdir(
            exist_ok=True
        )

    ####################################################################

    def pasta_empresa(
        self,
        documento: FiscalDocument,
    ):

        empresa = (
            str(documento.empresa_id)
            if documento.empresa_id
            else "SEM_EMPRESA"
        )

        ano = (
            str(documento.data_emissao.year)
            if documento.data_emissao
            else str(datetime.now().year)
        )

        mes = (
            f"{documento.data_emissao.month:02}"
            if documento.data_emissao
            else f"{datetime.now().month:02}"
        )

        pasta = (
            self.raiz
            / empresa
            / ano
            / mes
        )

        pasta.mkdir(
            parents=True,
            exist_ok=True,
        )

        return pasta

    ####################################################################

    def nome_arquivo(
        self,
        documento: FiscalDocument,
    ):

        chave = documento.chave.strip()

        if chave == "":

            chave = (
                datetime.now()
                .strftime("%Y%m%d%H%M%S")
            )

        return f"{chave}.xml"

    ####################################################################

    def salvar_xml(
        self,
        documento: FiscalDocument,
    ):

        pasta = self.pasta_empresa(
            documento
        )

        arquivo = (
            pasta
            / self.nome_arquivo(documento)
        )

        arquivo.write_text(
            documento.xml,
            encoding="utf-8",
        )

        return arquivo

    ####################################################################

    def copiar_xml(
        self,
        origem,
        documento: FiscalDocument,
    ):

        pasta = self.pasta_empresa(
            documento
        )

        destino = (
            pasta
            / self.nome_arquivo(documento)
        )

        shutil.copy2(
            origem,
            destino,
        )

        return destino

    ####################################################################

    def existe(
        self,
        documento: FiscalDocument,
    ):

        arquivo = (
            self.pasta_empresa(documento)
            / self.nome_arquivo(documento)
        )

        return arquivo.exists()
