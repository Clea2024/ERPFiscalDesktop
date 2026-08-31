from pathlib import Path

from lxml import etree

from app.database.database import get_session
from app.models.company import Company
from app.services.sefaz_xml_import_service import (
    SefazXmlImportService,
)


NFE_NS = {
    "nfe": "http://www.portalfiscal.inf.br/nfe"
}


class XMLSaidaImportService:

    def __init__(self):

        self.db = get_session()

        self.importador = (
            SefazXmlImportService(
                self.db
            )
        )

    @staticmethod
    def somente_numeros(valor):

        return "".join(
            caractere
            for caractere in str(
                valor or ""
            )
            if caractere.isdigit()
        )

    def obter_empresa(
        self,
        company_id,
    ):

        return (
            self.db.query(
                Company
            )
            .filter(
                Company.id
                == company_id
            )
            .first()
        )

    def identificar_nfe(
        self,
        caminho,
    ):

        try:

            raiz = etree.parse(
                str(caminho)
            ).getroot()

        except Exception:

            return None

        inf_nfe = raiz.find(
            ".//nfe:infNFe",
            namespaces=NFE_NS,
        )

        if inf_nfe is None:

            return None

        emitente = inf_nfe.find(
            ".//nfe:emit/nfe:CNPJ",
            namespaces=NFE_NS,
        )

        modelo = inf_nfe.find(
            ".//nfe:ide/nfe:mod",
            namespaces=NFE_NS,
        )

        return {
            "emitente_cnpj": (
                self.somente_numeros(
                    emitente.text
                    if emitente is not None
                    else ""
                )
            ),
            "modelo": (
                modelo.text
                if modelo is not None
                else ""
            ),
        }

    def importar_arquivo(
        self,
        caminho_xml,
        company_id,
    ):

        caminho = Path(
            caminho_xml
        )

        if not caminho.exists():

            return {
                "importado": False,
                "motivo": (
                    "Arquivo não encontrado."
                ),
            }

        empresa = self.obter_empresa(
            company_id
        )

        if empresa is None:

            return {
                "importado": False,
                "motivo": (
                    "Empresa não encontrada."
                ),
            }

        dados = self.identificar_nfe(
            caminho
        )

        if dados is None:

            return {
                "importado": False,
                "ignorado": True,
                "motivo": (
                    "XML não é NF-e/NFC-e completa."
                ),
            }

        cnpj_empresa = (
            self.somente_numeros(
                empresa.cnpj
            )
        )

        if (
            dados["emitente_cnpj"]
            != cnpj_empresa
        ):

            return {
                "importado": False,
                "ignorado": True,
                "motivo": (
                    "Documento não é saída "
                    "da empresa selecionada."
                ),
            }

        if dados["modelo"] not in (
            "55",
            "65",
        ):

            return {
                "importado": False,
                "ignorado": True,
                "motivo": (
                    "Modelo fiscal não suportado "
                    "neste importador."
                ),
            }

        resultado = (
            self.importador.importar_arquivo(
                caminho,
                cnpj_empresa,
            )
        )

        self.db.commit()

        return {
            "importado": True,
            "tipo": (
                "NFE"
                if dados["modelo"] == "55"
                else "NFCE"
            ),
            "arquivo": str(
                caminho
            ),
            "resultado": resultado,
        }

    def importar_pasta(
        self,
        pasta,
        company_id,
    ):

        pasta = Path(
            pasta
        )

        importados = 0
        ignorados = 0
        erros = 0

        resultados = []

        for caminho in pasta.rglob(
            "*.xml"
        ):

            try:

                resultado = (
                    self.importar_arquivo(
                        caminho,
                        company_id,
                    )
                )

                resultados.append(
                    resultado
                )

                if resultado.get(
                    "importado"
                ):

                    importados += 1

                else:

                    ignorados += 1

            except Exception as erro:

                self.db.rollback()

                erros += 1

                resultados.append(
                    {
                        "importado": False,
                        "arquivo": str(
                            caminho
                        ),
                        "erro": str(
                            erro
                        ),
                    }
                )

        return {
            "importados": importados,
            "ignorados": ignorados,
            "erros": erros,
            "resultados": resultados,
        }

    def fechar(self):

        self.db.close()
