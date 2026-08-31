from pathlib import Path

from lxml import etree
from app.database.database import get_session
from app.services.sefaz_xml_import_service import (
    SefazXmlImportService,
)


class NFCeImportService:

    def __init__(
        self,
        pasta=None,
    ):

        if pasta is None:

            base_dir = (
                Path(__file__)
                .resolve()
                .parents[2]
            )

            pasta = (
                base_dir
                / "xml"
                / "nfce"
            )

        self.pasta = Path(
            pasta
        )

        self.pasta.mkdir(
            parents=True,
            exist_ok=True,
        )

    ############################################################
    # LOCALIZAR XMLs POR EMPRESA
    ############################################################

    def localizar_xmls(
        self,
        cnpj_empresa,
    ):

        cnpj = "".join(
            caractere
            for caractere in str(cnpj_empresa)
            if caractere.isdigit()
        )

        if len(cnpj) != 14:

            raise ValueError(
                "CNPJ deve possuir 14 dígitos."
            )

        pasta_empresa = (
            self.pasta
            / cnpj
        )

        pasta_empresa.mkdir(
            parents=True,
            exist_ok=True,
        )

        return list(
            pasta_empresa.rglob(
                "*.xml"
            )
        )

    ############################################################
    # IMPORTAR
    ############################################################

    ############################################################
    # VALIDAR MODELO 65
    ############################################################

    @staticmethod
    def eh_nfce(
        caminho_xml,
    ):

        try:

            raiz = etree.parse(
                str(caminho_xml)
            ).getroot()

            elementos = raiz.xpath(
                "//*[local-name()='mod']"
            )

            if not elementos:
                return False

            modelo = (
                elementos[0].text
                or ""
            ).strip()

            return modelo == "65"

        except Exception:

            return False

    def importar(
        self,
        cnpj_empresa,
    ):

        arquivos = (
            self.localizar_xmls(
                cnpj_empresa
            )
        )

        arquivos = [
            arquivo
            for arquivo in arquivos
            if self.eh_nfce(
                arquivo
            )
        ]
        if not arquivos:

            return {
                "encontrados": 0,
                "importados": 0,
                "duplicados": 0,
                "ignorados": 0,
            }

        db = get_session()

        try:

            importador = (
                SefazXmlImportService(
                    db
                )
            )

            resultado = (
                importador.importar_arquivos(
                    arquivos=arquivos,
                    cnpj_empresa=cnpj_empresa,
                )
            )

            db.commit()

            return {
                "encontrados": len(
                    arquivos
                ),
                "importados": resultado.get(
                    "importados",
                    0,
                ),
                "duplicados": resultado.get(
                    "duplicados",
                    0,
                ),
                "ignorados": resultado.get(
                    "ignorados",
                    0,
                ),
            }

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()