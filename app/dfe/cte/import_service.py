from datetime import datetime
from decimal import Decimal
from pathlib import Path

from lxml import etree

from app.models.fiscal_document import FiscalDocumentModel


class CTeImportService:

    NS = {
        "cte": "http://www.portalfiscal.inf.br/cte"
    }

    def __init__(self, db):

        self.db = db

    ############################################################

    @staticmethod
    def texto(elemento, xpath, namespaces):

        resultado = elemento.find(
            xpath,
            namespaces=namespaces,
        )

        if resultado is None:
            return ""

        return (
            resultado.text or ""
        ).strip()

    ############################################################
    @staticmethod
    def somente_numeros(valor):

        return "".join(
        caractere
            for caractere in str(valor)
            if caractere.isdigit()
        )

    ############################################################

    @staticmethod
    def converter_data(valor):

        if not valor:
            return None

        try:
            return datetime.fromisoformat(
                valor.replace(
                    "Z",
                    "+00:00",
                )
            )
        except Exception:
            return None

    ############################################################

    @staticmethod
    def converter_decimal(valor):

        try:
            return Decimal(
                str(valor or "0")
                .replace(",", ".")
            )
        except Exception:
            return Decimal("0")

    ############################################################

    def importar_arquivo(
        self,
        caminho,
        empresa_id=None,
    ):

        caminho = Path(caminho)

        if not caminho.exists():

            return {
                "importado": False,
                "motivo": "Arquivo não encontrado.",
            }

        parser = etree.XMLParser(
            remove_blank_text=True
        )

        raiz = etree.parse(
            str(caminho),
            parser,
        ).getroot()

        ########################################################
        # LOCALIZAR INFCTE
        ########################################################

        inf_cte = raiz.find(
            ".//cte:infCte",
            namespaces=self.NS,
        )

        if inf_cte is None:

            return {
                "importado": False,
                "motivo": (
                    "XML não contém infCte. "
                    "Pode ser evento ou resumo."
                ),
            }

        ########################################################
        # CHAVE
        ########################################################

        id_cte = inf_cte.get(
            "Id",
            "",
        )

        chave = id_cte

        if chave.startswith("CTe"):
            chave = chave[3:]

        chave = self.somente_numeros(
            chave
        )

        if not chave:

            return {
                "importado": False,
                "motivo": "CT-e sem chave.",
            }

        ########################################################
        # DUPLICIDADE
        ########################################################

        existente = (
            self.db.query(
                FiscalDocumentModel
            )
            .filter(
                FiscalDocumentModel.chave
                == chave
            )
            .first()
        )

        documento_existente = (
            existente
        )

        ########################################################
        # IDENTIFICAÇÃO
        ########################################################

        modelo = self.texto(
            inf_cte,
            ".//cte:ide/cte:mod",
            self.NS,
        )

        numero = self.texto(
            inf_cte,
            ".//cte:ide/cte:nCT",
            self.NS,
        )

        serie = self.texto(
            inf_cte,
            ".//cte:ide/cte:serie",
            self.NS,
        )

        data_texto = self.texto(
            inf_cte,
            ".//cte:ide/cte:dhEmi",
            self.NS,
        )

        data_emissao = (
            self.converter_data(
                data_texto
            )
        )

        ########################################################
        # EMITENTE
        ########################################################

        emitente_cnpj = self.texto(
            inf_cte,
            ".//cte:emit/cte:CNPJ",
            self.NS,
        )

        emitente_nome = self.texto(
            inf_cte,
            ".//cte:emit/cte:xNome",
            self.NS,
        )

        ########################################################
        # DESTINATÁRIO
        ########################################################

        destinatario_cnpj = self.texto(
            inf_cte,
            ".//cte:dest/cte:CNPJ",
            self.NS,
        )

        destinatario_cpf = self.texto(
            inf_cte,
            ".//cte:dest/cte:CPF",
            self.NS,
        )

        if not destinatario_cnpj:
            destinatario_cnpj = (
                destinatario_cpf
            )

        destinatario_nome = self.texto(
            inf_cte,
            ".//cte:dest/cte:xNome",
            self.NS,
        )

        ########################################################
        # VALOR
        ########################################################

        valor_total = self.texto(
            inf_cte,
            ".//cte:vPrest/cte:vTPrest",
            self.NS,
        )

        ########################################################
        # PROTOCOLO
        ########################################################

        protocolo = self.texto(
            raiz,
            ".//cte:protCTe/cte:infProt/cte:nProt",
            self.NS,
        )

        ########################################################
        # CRIAR DOCUMENTO
        ########################################################

        if documento_existente is not None:

            model = (
                documento_existente
            )

        else:

            model = (
                FiscalDocumentModel()
            )

        model.chave = chave
        model.modelo = modelo or "57"
        model.numero = numero
        model.serie = serie
        model.data_emissao = data_emissao

        model.emitente_cnpj = (
            emitente_cnpj
        )

        model.emitente_nome = (
            emitente_nome
        )

        model.destinatario_cnpj = (
            destinatario_cnpj
        )

        model.destinatario_nome = (
            destinatario_nome
        )

        model.valor_total = (
            self.converter_decimal(
                valor_total
            )
        )

        model.protocolo = protocolo

        ########################################################
        # ORIGEM
        ########################################################

        model.origem = "CTE"

        ########################################################
        # EMPRESA
        ########################################################

        if empresa_id is not None:

            if hasattr(
                model,
                "empresa_id",
            ):

                model.empresa_id = (
                    empresa_id
                )

            elif hasattr(
                model,
                "company_id",
            ):

                model.company_id = (
                    empresa_id
                )

        ########################################################
        # CAMINHO XML
        ########################################################

        if hasattr(
            model,
            "xml_path",
        ):

            model.xml_path = str(
                caminho
            )

        ########################################################
        # SALVAR
        ########################################################

        self.db.add(
            model
        )

        self.db.flush()

        return{
            "importado": True,
            "duplicado": False,
            "chave": chave,
            "numero": numero,
            "serie": serie,
            "modelo": modelo,
            "data_emissao": data_emissao,
            "valor_total": valor_total,
        }
    def importar_arquivos(
        self,
        arquivos,
        empresa_id=None,
    ):

        importados = 0
        duplicados = 0
        ignorados = 0
        erros = []

        for arquivo in arquivos:

            try:

                if isinstance(
                    arquivo,
                    dict,
                ):

                    if (
                        arquivo.get("tipo")
                        != "cte"
                    ):
                        ignorados += 1
                        continue

                    caminho = arquivo.get(
                        "caminho"
                    )

                else:

                    caminho = arquivo

                resultado = (
                    self.importar_arquivo(
                        caminho=caminho,
                        empresa_id=empresa_id,
                    )
                )

                if resultado.get(
                    "importado"
                ):

                    importados += 1

                elif resultado.get(
                    "duplicado"
                ):

                    duplicados += 1

                else:

                    ignorados += 1

            except Exception as erro:

                self.db.rollback()

                erros.append(
                    {
                        "arquivo": str(
                            arquivo
                        ),
                        "erro": str(
                            erro
                        ),
                    }
                )

        return {
            "importados": importados,
            "duplicados": duplicados,
            "ignorados": ignorados,
            "erros": erros,
        }