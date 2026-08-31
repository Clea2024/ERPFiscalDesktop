from pathlib import Path

from app.database.database import get_session
from app.models.fiscal_document import FiscalDocumentModel
from app.models.fiscal_item_model import FiscalItemModel
from app.services.sefaz_xml_import_service import SefazXmlImportService


PASTA_XML = Path(
    r"C:\Users\clea-\ERPFiscalDesktop\xml"
)

db = get_session()

service = SefazXmlImportService(
    db
)

processados = 0
recuperados = 0
erros = []

try:

    documentos = (
        db.query(FiscalDocumentModel)
        .filter(
            FiscalDocumentModel.modelo.in_(
                ["55", "65"]
            )
        )
        .all()
    )

    for documento in documentos:

        quantidade_itens = (
            db.query(FiscalItemModel)
            .filter(
                FiscalItemModel.fiscal_document_id
                == documento.id
            )
            .count()
        )

        if quantidade_itens > 0:
            continue

        caminho = Path(
            documento.xml_path or ""
        )

        if not caminho.exists():

            arquivos = list(
                PASTA_XML.rglob(
                    f"*{documento.chave}*.xml"
                )
            )

            if not arquivos:
                print(
                    "XML não encontrado:",
                    documento.chave
                )
                continue

            caminho = arquivos[0]

        try:

            service.importar_arquivo(
                caminho,
                documento.empresa.cnpj,
            )

            db.commit()

            nova_quantidade = (
                db.query(FiscalItemModel)
                .filter(
                    FiscalItemModel.fiscal_document_id
                    == documento.id
                )
                .count()
            )

            processados += 1

            if nova_quantidade > 0:

                recuperados += 1

                print(
                    "RECUPERADO:",
                    documento.chave,
                    "| itens:",
                    nova_quantidade,
                )

        except Exception as erro:

            db.rollback()

            erros.append(
                (
                    documento.chave,
                    str(erro),
                )
            )

            print(
                "ERRO:",
                documento.chave,
                erro,
            )

finally:

    db.close()

print()
print(
    "PROCESSADOS:",
    processados
)

print(
    "RECUPERADOS:",
    recuperados
)

print(
    "ERROS:",
    len(erros)
)

for chave, erro in erros:
    print(
        chave,
        erro,
    )
