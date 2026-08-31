from app.database.database import get_session
from app.fiscal.parser import FiscalParser
from app.models.fiscal_document import FiscalDocumentModel
from app.models.fiscal_item_model import FiscalItemModel

caminho = r"C:\Users\clea-\ERPFiscalDesktop\xml\23260702916265022996550010007381001162452251.xml"

parser = FiscalParser()
documento_xml = parser.ler_xml(caminho)

print("CHAVE:", documento_xml.chave)
print("ITENS XML:", len(documento_xml.itens))

db = get_session()

try:
    documento_banco = (
        db.query(FiscalDocumentModel)
        .filter(
            FiscalDocumentModel.chave
            == documento_xml.chave
        )
        .first()
    )

    if documento_banco is None:
        print("Documento ainda não existe no banco.")
    else:
        print(
            "DOCUMENTO ENCONTRADO NO BANCO:",
            documento_banco.id
        )

        atualizados = 0

        for item_xml in documento_xml.itens:

            item_banco = (
                db.query(FiscalItemModel)
                .filter(
                    FiscalItemModel.fiscal_document_id
                    == documento_banco.id,
                    FiscalItemModel.numero_item
                    == item_xml.numero_item,
                )
                .first()
            )

            if item_banco is None:
                print(
                    "Item não encontrado:",
                    item_xml.numero_item
                )
                continue

            item_banco.ibs = item_xml.ibs
            item_banco.cbs = item_xml.cbs
            item_banco.imposto_seletivo = (
                item_xml.imposto_seletivo
            )

            atualizados += 1

            print(
                "ITEM",
                item_xml.numero_item,
                "| IBS:",
                item_xml.ibs,
                "| CBS:",
                item_xml.cbs,
                "| IS:",
                item_xml.imposto_seletivo,
            )

        db.commit()

        print(
            "ITENS ATUALIZADOS:",
            atualizados
        )

except Exception:
    db.rollback()
    raise

finally:
    db.close()
