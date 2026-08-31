from sqlalchemy.orm import Session, joinedload

from app.models.fiscal_document import FiscalDocumentModel
from app.models.fiscal_item_model import FiscalItemModel

from app.fiscal.document import FiscalDocument


class FiscalDocumentRepository:

    def __init__(self, db: Session):

        self.db = db

    ####################################################################
    # INSERIR DOCUMENTO
    ####################################################################

    def inserir(
        self,
        documento: FiscalDocument,
    ):

        try:

            model = FiscalDocumentModel()

            ############################################################
            # DADOS DO DOCUMENTO
            ############################################################

            model.chave = documento.chave
            model.modelo = documento.modelo
            model.numero = documento.numero
            model.serie = documento.serie
            model.data_emissao = documento.data_emissao

            model.emitente_cnpj = documento.emitente_cnpj
            model.emitente_nome = documento.emitente_nome

            model.destinatario_cnpj = documento.destinatario_cnpj
            model.destinatario_nome = documento.destinatario_nome

            model.valor_total = documento.valor_total
            model.protocolo = documento.protocolo
            model.origem = documento.origem

            ############################################################
            # EMPRESA
            ############################################################

            if hasattr(model, "empresa_id"):

                model.empresa_id = documento.empresa_id

            elif hasattr(model, "company_id"):

                model.company_id = documento.empresa_id

            ############################################################
            # XML
            ############################################################

            if hasattr(documento, "xml_path"):

                model.xml_path = documento.xml_path

            ############################################################
            # SALVA DOCUMENTO
            ############################################################

            self.db.add(model)

            self.db.flush()

            ############################################################
            # ITENS
            ############################################################
            for item in documento.itens:

                model_item = FiscalItemModel()

                ########################################################
                # RELACIONAMENTO
                ########################################################

                model_item.fiscal_document_id = model.id

                ########################################################
                # DADOS DO ITEM
                ########################################################

                model_item.numero_item = item.numero_item
                model_item.codigo = item.codigo
                model_item.descricao = item.descricao
                model_item.ean = item.ean
                model_item.unidade = item.unidade

                model_item.quantidade = item.quantidade
                model_item.valor_unitario = item.valor_unitario
                model_item.valor_total = item.valor_total
                model_item.desconto = item.desconto

                ########################################################
                # CLASSIFICAÇÃO FISCAL
                ########################################################

                model_item.ncm = item.ncm
                model_item.cest = item.cest
                model_item.cfop = item.cfop

                ########################################################
                # ICMS
                ########################################################

                model_item.origem = item.origem
                model_item.cst_icms = item.cst_icms
                model_item.csosn = item.csosn

                model_item.base_icms = item.base_icms
                model_item.aliquota_icms = item.aliquota_icms
                model_item.valor_icms = item.valor_icms

                ########################################################
                # PIS
                ########################################################

                model_item.cst_pis = item.cst_pis
                model_item.base_pis = item.base_pis
                model_item.aliquota_pis = item.aliquota_pis
                model_item.valor_pis = item.valor_pis

                ########################################################
                # COFINS
                ########################################################

                model_item.cst_cofins = item.cst_cofins
                model_item.base_cofins = item.base_cofins
                model_item.aliquota_cofins = item.aliquota_cofins
                model_item.valor_cofins = item.valor_cofins

                ########################################################
                # CAMPOS OPCIONAIS
                ########################################################

                if hasattr(model_item, "base_st"):
                    model_item.base_st = item.base_st

                if hasattr(model_item, "valor_st"):
                    model_item.valor_st = item.valor_st

                if hasattr(model_item, "valor_fcp"):
                    model_item.valor_fcp = item.valor_fcp

                if hasattr(model_item, "ibs"):
                    model_item.ibs = item.ibs

                if hasattr(model_item, "cbs"):
                    model_item.cbs = item.cbs

                if hasattr(model_item, "imposto_seletivo"):
                    model_item.imposto_seletivo = item.imposto_seletivo

                self.db.add(model_item)
                            ############################################################
            # FINALIZA TRANSAÇÃO
            ############################################################

            self.db.commit()

            self.db.refresh(model)

            return model

        except Exception:

            self.db.rollback()

            raise

    ####################################################################
    # EXISTE
    ####################################################################

    def existe(
        self,
        chave,
    ):

        return (
            self.db.query(
                FiscalDocumentModel
            )
            .filter(
                FiscalDocumentModel.chave == chave
            )
            .first()
            is not None
        )

    ####################################################################
    # COMPATIBILIDADE
    ####################################################################

    def existe_chave(
        self,
        chave,
    ):

        return self.existe(chave)

    ####################################################################
    # BUSCAR POR CHAVE
    ####################################################################

    def buscar_por_chave(
        self,
        chave,
    ):

        return (
            self.db.query(
                FiscalDocumentModel
            )
            .options(
                joinedload(
                    FiscalDocumentModel.itens
                )
            )
            .filter(
                FiscalDocumentModel.chave == chave
            )
            .first()
        )
            ####################################################################
    # LISTAR
    ####################################################################

    def listar(self):

        return (
            self.db.query(FiscalDocumentModel)
            .options(
                joinedload(FiscalDocumentModel.itens)
            )
            .order_by(
                FiscalDocumentModel.data_emissao.desc()
            )
            .all()
        )

    ####################################################################
    # LISTAR POR EMPRESA
    ####################################################################

    def listar_empresa(
        self,
        empresa_id,
    ):

        if hasattr(
            FiscalDocumentModel,
            "empresa_id",
        ):

            filtro = (
                FiscalDocumentModel.empresa_id
                == empresa_id
            )

        else:

            filtro = (
                FiscalDocumentModel.company_id
                == empresa_id
            )

        return (
            self.db.query(
                FiscalDocumentModel
            )
            .options(
                joinedload(
                    FiscalDocumentModel.itens
                )
            )
            .filter(filtro)
            .order_by(
                FiscalDocumentModel.data_emissao.desc()
            )
            .all()
        )

    ####################################################################
    # BUSCAR POR ID
    ####################################################################

    def buscar_por_id(
        self,
        documento_id,
    ):

        return (
            self.db.query(
                FiscalDocumentModel
            )
            .options(
                joinedload(
                    FiscalDocumentModel.itens
                )
            )
            .filter(
                FiscalDocumentModel.id == documento_id
            )
            .first()
        )
            ####################################################################
    # REMOVER
    ####################################################################

    def remover(
        self,
        chave,
    ):

        documento = self.buscar_por_chave(chave)

        if documento is None:
            return False

        try:

            self.db.delete(documento)

            self.db.commit()

            return True

        except Exception:

            self.db.rollback()

            raise

    ####################################################################
    # CONTAR DOCUMENTOS
    ####################################################################

    def contar(self):

        return (
            self.db.query(
                FiscalDocumentModel
            )
            .count()
        )

    ####################################################################
    # SALVAR ALTERAÇÕES
    ####################################################################

    def salvar(self):

        try:

            self.db.commit()

        except Exception:

            self.db.rollback()

            raise

    ####################################################################
    # FECHAR SESSÃO
    ####################################################################

    def fechar(self):

        self.db.close()