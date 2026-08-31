from datetime import datetime
from decimal import Decimal
from pathlib import Path

from app.fiscal.parser import FiscalParser
from app.models.fiscal_item_model import FiscalItemModel
from lxml import etree

from app.models.company import Company
from app.models.fiscal_document import FiscalDocumentModel


NFE_NS = {
    "nfe": "http://www.portalfiscal.inf.br/nfe"
}


class SefazXmlImportService:

    def __init__(self, db):
        self.db = db

    @staticmethod
    def somente_numeros(valor):
        if not valor:
            return ""

        return "".join(
            caractere
            for caractere in str(valor)
            if caractere.isdigit()
        )

    @staticmethod
    def texto(elemento, xpath, padrao=""):

        resultado = elemento.find(
            xpath,
            namespaces=NFE_NS,
        )

        if resultado is None:
            return padrao

        return resultado.text or padrao

    def obter_empresa(self, cnpj):

        cnpj_limpo = self.somente_numeros(cnpj)

        empresas = (
            self.db.query(Company)
            .all()
        )

        for empresa in empresas:

            if (
                self.somente_numeros(
                    empresa.cnpj
                )
                == cnpj_limpo
            ):
                return empresa

        empresa = Company(
            razao_social=f"Empresa {cnpj_limpo}",
            cnpj=cnpj_limpo,
        )

        self.db.add(empresa)
        self.db.flush()

        return empresa

    @staticmethod
    def converter_data(valor):

        if not valor:
            return datetime.now()

        try:
            return datetime.fromisoformat(
                valor.replace("Z", "+00:00")
            ).replace(tzinfo=None)

        except Exception:
            return datetime.now()

    def importar_arquivo(
        self,
        caminho_xml,
        cnpj_empresa,
    ):

        caminho = Path(caminho_xml)
        parser_fiscal = FiscalParser()

        if not caminho.exists():
            return None

        try:

            arvore = etree.parse(
                str(caminho)
            )

            raiz = arvore.getroot()

        except Exception as erro:

            print(
                "[XML] Erro ao ler:",
                caminho,
                erro,
            )

            return None

        ########################################################
        # LOCALIZAR infNFe
        ########################################################

        inf_nfe = raiz.find(
            ".//nfe:infNFe",
            namespaces=NFE_NS,
        )

        if inf_nfe is None:

            print(
                "[XML] Ignorado por não ser NF-e completa:",
                caminho.name,
            )

            return None

        ########################################################
        # CHAVE
        ########################################################

        chave = (
            inf_nfe.get("Id", "")
            .replace("NFe", "")
        )

        if len(chave) != 44:

            print(
                "[XML] Chave inválida:",
                caminho.name,
            )

            return None

        existente = (
            self.db.query(FiscalDocumentModel)
            .filter(
                FiscalDocumentModel.chave == chave
            )
            .first()
        )

        if existente:

            print(
                "[XML] Documento já existente:",
                chave,
            )

            total_itens = (
                self.db.query(FiscalItemModel)
                .filter(
                    FiscalItemModel.fiscal_document_id
                    == existente.id
                )
                .count()
            )

            if total_itens > 0:

                return existente

            ####################################################
            # DOCUMENTO EXISTE, MAS ESTÁ SEM ITENS
            ####################################################

            try:

                documento_fiscal = (
                    parser_fiscal.ler_xml(
                        str(caminho)
                    )
                )

                for item in documento_fiscal.itens:

                    model_item = FiscalItemModel()

                    model_item.fiscal_document_id = (
                        existente.id
                    )

                    model_item.numero_item = (
                        item.numero_item
                    )

                    model_item.codigo = item.codigo
                    model_item.descricao = item.descricao
                    model_item.ean = item.ean
                    model_item.unidade = item.unidade

                    model_item.quantidade = (
                        item.quantidade
                    )

                    model_item.valor_unitario = (
                        item.valor_unitario
                    )

                    model_item.valor_total = (
                        item.valor_total
                    )

                    model_item.desconto = (
                        item.desconto
                    )

                    model_item.ncm = item.ncm
                    model_item.cest = item.cest
                    model_item.cfop = item.cfop

                    model_item.origem = item.origem
                    model_item.cst_icms = item.cst_icms
                    model_item.csosn = item.csosn

                    model_item.base_icms = (
                        item.base_icms
                    )

                    model_item.aliquota_icms = (
                        item.aliquota_icms
                    )

                    model_item.valor_icms = (
                        item.valor_icms
                    )

                    model_item.cst_pis = item.cst_pis
                    model_item.base_pis = item.base_pis

                    model_item.aliquota_pis = (
                        item.aliquota_pis
                    )

                    model_item.valor_pis = (
                        item.valor_pis
                    )

                    model_item.cst_cofins = (
                        item.cst_cofins
                    )

                    model_item.base_cofins = (
                        item.base_cofins
                    )

                    model_item.aliquota_cofins = (
                        item.aliquota_cofins
                    )

                    model_item.valor_cofins = (
                        item.valor_cofins
                    )

                    model_item.ibs = item.ibs
                    model_item.cbs = item.cbs

                    model_item.imposto_seletivo = (
                        item.imposto_seletivo
                    )

                    self.db.add(
                        model_item
                    )

                self.db.flush()

                print(
                    "[XML] Itens recuperados:",
                    len(documento_fiscal.itens),
                )

            except Exception as erro:

                print(
                    "[XML] Erro ao recuperar itens:",
                    erro,
                )

                raise

            return existente
        ########################################################
        # IDE
        ########################################################

        modelo = self.texto(
            inf_nfe,
            ".//nfe:ide/nfe:mod",
        )
        ########################################################
        # TIPO DO DOCUMENTO
        ########################################################

        if modelo == "55":

            tipo_documento = "NFE"
            nome_documento = "NF-e"

        elif modelo == "65":

            tipo_documento = "NFCE"
            nome_documento = "NFC-e"

        else:

            tipo_documento = "DFE"
            nome_documento = (
                f"DF-e modelo {modelo}"
            )

        numero = self.texto(
            inf_nfe,
            ".//nfe:ide/nfe:nNF",
        )

        serie = self.texto(
            inf_nfe,
            ".//nfe:ide/nfe:serie",
        )

        data_emissao_texto = self.texto(
            inf_nfe,
            ".//nfe:ide/nfe:dhEmi",
        )

        if not data_emissao_texto:

            data_emissao_texto = self.texto(
                inf_nfe,
                ".//nfe:ide/nfe:dEmi",
            )

        data_emissao = self.converter_data(
            data_emissao_texto
        )

        ########################################################
        # EMITENTE
        ########################################################

        emitente_cnpj = self.texto(
            inf_nfe,
            ".//nfe:emit/nfe:CNPJ",
        )

        emitente_nome = self.texto(
            inf_nfe,
            ".//nfe:emit/nfe:xNome",
        )

        ########################################################
        # DESTINATÁRIO
        ########################################################

        destinatario_cnpj = self.texto(
            inf_nfe,
            ".//nfe:dest/nfe:CNPJ",
        )

        if not destinatario_cnpj:

            destinatario_cnpj = self.texto(
                inf_nfe,
                ".//nfe:dest/nfe:CPF",
            )

        destinatario_nome = self.texto(
            inf_nfe,
            ".//nfe:dest/nfe:xNome",
        )

        ########################################################
        # VALOR
        ########################################################

        valor_texto = self.texto(
            inf_nfe,
            ".//nfe:total/nfe:ICMSTot/nfe:vNF",
            "0",
        )

        try:
            valor_total = Decimal(
                valor_texto
            )

        except Exception:
            valor_total = Decimal("0")

        ########################################################
        # PROTOCOLO
        ########################################################

        protocolo = self.texto(
            raiz,
            ".//nfe:protNFe/nfe:infProt/nfe:nProt",
        )

        ########################################################
        # EMPRESA DO ERP
        ########################################################

        empresa = self.obter_empresa(
            cnpj_empresa
        )

        ########################################################
        # GRAVAR DOCUMENTO
        ########################################################

        documento = FiscalDocumentModel(
            company_id=empresa.id,
            chave=chave,
            modelo=modelo or "55",
            numero=numero or "",
            serie=serie or "",
            data_emissao=data_emissao,
            emitente_cnpj=(
                emitente_cnpj or ""
            ),
            emitente_nome=(
                emitente_nome
                or "Não informado"
            ),
            destinatario_cnpj=(
                destinatario_cnpj or ""
            ),
            destinatario_nome=(
                destinatario_nome
                or "Não informado"
            ),
            valor_total=valor_total,
            protocolo=protocolo or "",
            origem=tipo_documento,
            xml_path=str(caminho),
            status="IMPORTADO",
        )

        self.db.add(
            documento
        )

        self.db.flush()

        print(
            f"[XML] {nome_documento} importada:",
            chave,
        )
        return documento

    def importar_arquivos(
        self,
        arquivos,
        cnpj_empresa,
    ):

        importados = 0
        ignorados = 0

        for caminho in arquivos:

            resultado = self.importar_arquivo(
                caminho,
                cnpj_empresa,
            )

            if resultado is None:
                ignorados += 1
            else:
                importados += 1

        return {
            "importados": importados,
            "ignorados": ignorados,
        }