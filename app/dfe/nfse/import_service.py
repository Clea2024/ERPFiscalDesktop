from datetime import datetime
from decimal import Decimal
from pathlib import Path

from lxml import etree

from app.models.company import Company
from app.models.fiscal_document import FiscalDocumentModel


class NFSeImportService:

    def __init__(
        self,
        db,
    ):

        self.db = db

    ############################################################
    # UTILITÁRIOS
    ############################################################

    @staticmethod
    def somente_numeros(
        valor,
    ):

        return "".join(
            caractere
            for caractere in str(
                valor or ""
            )
            if caractere.isdigit()
        )

    @staticmethod
    def localizar_texto(
        raiz,
        nomes,
    ):

        for elemento in raiz.iter():

            nome_local = (
                etree.QName(
                    elemento
                ).localname
            )

            if nome_local in nomes:

                texto = (
                    elemento.text or ""
                ).strip()

                if texto:
                    return texto

        return ""

    @staticmethod
    def localizar_bloco(
        raiz,
        nomes,
    ):

        for elemento in raiz.iter():

            nome_local = (
                etree.QName(
                    elemento
                ).localname
            )

            if nome_local in nomes:
                return elemento

        return None

    @classmethod
    def localizar_texto_bloco(
        cls,
        bloco,
        nomes,
    ):

        if bloco is None:
            return ""

        return cls.localizar_texto(
            bloco,
            nomes,
        )

    @staticmethod
    def converter_data(
        valor,
    ):

        if not valor:
            return None

        try:

            return datetime.fromisoformat(
                valor.replace(
                    "Z",
                    "+00:00",
                )
            ).replace(
                tzinfo=None
            )

        except Exception:

            try:

                return datetime.strptime(
                    valor[:10],
                    "%Y-%m-%d",
                )

            except Exception:

                return None  
    @staticmethod
    def converter_data(
        valor,
    ):

        if not valor:
            return None

        try:

            return datetime.fromisoformat(
                valor.replace(
                    "Z",
                    "+00:00",
                )
            ).replace(
                tzinfo=None
            )

        except Exception:

            try:

                return datetime.strptime(
                    valor[:10],
                    "%Y-%m-%d",
                )

            except Exception:

                return None

    @staticmethod
    def converter_decimal(
        valor,
    ):

        try:

            return Decimal(
                str(
                    valor or "0"
                ).replace(
                    ",",
                    ".",
                )
            )

        except Exception:

            return Decimal("0")

    ############################################################
    # EMPRESA
    ############################################################

    def obter_empresa(
        self,
        cnpj,
    ):

        cnpj = (
            self.somente_numeros(
                cnpj
            )
        )

        empresa = (
            self.db.query(Company)
            .filter(
                Company.cnpj == cnpj
            )
            .first()
        )

        if empresa is not None:
            return empresa

        empresa = Company(
            cnpj=cnpj,
            razao_social=(
                f"Empresa {cnpj}"
            ),
        )

        self.db.add(
            empresa
        )

        self.db.flush()

        return empresa

    ############################################################
    # IMPORTAR UM XML
    ############################################################

    def importar_arquivo(
        self,
        caminho_xml,
        cnpj_empresa,
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

        try:

            raiz = etree.parse(
                str(caminho)
            ).getroot()

        except Exception as erro:

            return {
                "importado": False,
                "motivo": str(erro),
            }

        ########################################################
        # CHAVE
        ########################################################

        chave = self.localizar_texto(
            raiz,
            [
                "chNFSe",
                "ChaveAcesso",
                "chaveAcesso",
            ],
        )

        if not chave:

            nome = caminho.stem

            partes = nome.split(
                "_",
                1,
            )

            if len(partes) == 2:
                chave = partes[1]

        chave = (
            self.somente_numeros(
                chave
            )
        )

        if not chave:

            return {
                "importado": False,
                "motivo": (
                    "Chave da NFS-e não encontrada."
                ),
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
        # CAMPOS PRINCIPAIS
        ########################################################

        numero = self.localizar_texto(
            raiz,
            [
                "nNFSe",
                "numero",
                "Numero",
            ],
        )

        serie = self.localizar_texto(
            raiz,
            [
                "serie",
                "Serie",
            ],
        )

        data_texto = self.localizar_texto(
            raiz,
            [
                "dhEmi",
                "dEmi",
                "DataEmissao",
            ],
        )

        data_emissao = (
            self.converter_data(
                data_texto
            )
        )

        ########################################################
        # PRESTADOR
        ########################################################

        bloco_prestador = (
            self.localizar_bloco(
                raiz,
                [
                    "prest",
                    "Prestador",
                    "prestador",
                    "emit",
                    "Emitente",
                ],
            )
        )

        prestador_cnpj = (
            self.localizar_texto_bloco(
                bloco_prestador,
                [
                    "CNPJ",
                    "Cnpj",
                    "CPF",
                ],
            )
        )

        prestador_nome = (
            self.localizar_texto_bloco(
                bloco_prestador,
                [
                    "xNome",
                    "RazaoSocial",
                    "Nome",
                ],
            )
        )

        ########################################################
        # TOMADOR
        ########################################################

        bloco_tomador = (
            self.localizar_bloco(
                raiz,
                [
                    "toma",
                    "Tomador",
                    "tomador",
                    "toma3",
                    "toma4",
                ],
            )
        )

        tomador_cnpj = (
            self.localizar_texto_bloco(
                bloco_tomador,
                [
                    "CNPJ",
                    "Cnpj",
                    "CPF",
                ],
            )
        )

        tomador_nome = (
            self.localizar_texto_bloco(
                bloco_tomador,
                [
                    "xNome",
                    "RazaoSocial",
                    "Nome",
                ],
            )
        )

                ########################################################
        # VALOR TOTAL
        ########################################################

        valor_texto = (
            self.localizar_texto(
                raiz,
                [
                    "ValorServicos",
                    "valorServicos",
                    "ValorLiquidoNfse",
                    "ValorLiquido",
                    "ValorNfse",
                    "ValorNota",
                    "vServ",
                ],
            )
        )

        valor_total = (
            self.converter_decimal(
                valor_texto
            )
        )    
	########################################################
        # EMPRESA
        ########################################################

        empresa = self.obter_empresa(
            cnpj_empresa
        )

        ########################################################
        # GRAVAR
        ########################################################

        if documento_existente is not None:

            documento = (
                documento_existente
            )

        else:

            documento = (
                FiscalDocumentModel()
            )

        documento.company_id = empresa.id
        documento.chave = chave
        documento.modelo = "NFSE"
        documento.numero = numero or ""
        documento.serie = serie or ""
        documento.data_emissao = data_emissao

        documento.emitente_cnpj = (
            self.somente_numeros(
                prestador_cnpj
            )
        )

        documento.emitente_nome = (
            prestador_nome
            or "Não informado"
        )

        documento.destinatario_cnpj = (
            self.somente_numeros(
                tomador_cnpj
            )
        )

        documento.destinatario_nome = (
            tomador_nome
            or "Não informado"
        )

        documento.valor_total = (
            valor_total
        )

        documento.protocolo = ""
        documento.origem = "NFSE"
        documento.xml_path = str(
            caminho
        )

        documento.status = "IMPORTADO"

        self.db.add(
            documento
        )

        self.db.flush()


        return {
            "importado": True,
            "duplicado": False,
            "chave": chave,
            "documento_id": (
                documento.id
            ),
        }

    ############################################################
    # IMPORTAR VÁRIOS
    ############################################################

    def importar_arquivos(
        self,
        arquivos,
        cnpj_empresa,
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

                    caminho = arquivo.get(
                        "caminho"
                    )

                else:

                    caminho = arquivo

                resultado = (
                    self.importar_arquivo(
                        caminho_xml=caminho,
                        cnpj_empresa=cnpj_empresa,
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

                erros.append(
                    str(erro)
                )

        return {
            "importados": importados,
            "duplicados": duplicados,
            "ignorados": ignorados,
            "erros": erros,
        }
