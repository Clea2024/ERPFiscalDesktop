"""
Configurações dos WebServices da NF-e
"""


class SefazConfig:

    ENDPOINTS = {

        "producao": {

            "NFeDistribuicaoDFe": {
                "AN": "https://www1.nfe.fazenda.gov.br/NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx",
            },

        },

        "homologacao": {

            "NFeDistribuicaoDFe": {
                "AN": "https://hom.nfe.fazenda.gov.br/NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx",
            },

        },

    }

    @classmethod
    def get_endpoint(
        cls,
        servico: str,
        ambiente: str,
        uf: str = "AN",
    ):

        ambiente = ambiente.lower()

        return cls.ENDPOINTS[ambiente][servico][uf]