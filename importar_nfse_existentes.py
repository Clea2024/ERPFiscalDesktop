from pathlib import Path

from app.database.database import get_session
from app.dfe.nfse.import_service import NFSeImportService


CNPJ = "23612215000169"

PASTA = Path(
    r"C:\Users\clea-\ERPFiscalDesktop\xml\nfse"
) / CNPJ / "NFSE"


db = get_session()

try:

    importador = NFSeImportService(
        db
    )

    arquivos = list(
        PASTA.glob("*.xml")
    )

    print(
        "Arquivos encontrados:",
        len(arquivos),
    )

    resultado = (
        importador.importar_arquivos(
            arquivos=arquivos,
            cnpj_empresa=CNPJ,
        )
    )

    db.commit()

    print(
        "Importados:",
        resultado.get(
            "importados",
            0,
        ),
    )

    print(
        "Duplicados:",
        resultado.get(
            "duplicados",
            0,
        ),
    )

    print(
        "Ignorados:",
        resultado.get(
            "ignorados",
            0,
        ),
    )

    print(
        "Erros:",
        resultado.get(
            "erros",
            [],
        ),
    )

finally:

    db.close()