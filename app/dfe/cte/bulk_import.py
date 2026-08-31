from pathlib import Path

from app.database.database import get_session
from app.dfe.cte.import_service import CTeImportService
from app.models.company import Company


class CTeBulkImport:

    def __init__(
        self,
        pasta_base=None,
    ):

        if pasta_base is None:

            base_dir = (
                Path(__file__)
                .resolve()
                .parents[3]
            )

            pasta_base = (
                base_dir
                / "xml"
                / "cte"
            )

        self.pasta_base = Path(
            pasta_base
        )

    ############################################################
    # IMPORTAR CNPJ
    ############################################################

    def importar_cnpj(
        self,
        cnpj,
    ):

        cnpj = "".join(
            caractere
            for caractere in str(cnpj)
            if caractere.isdigit()
        )

        pasta_cte = (
            self.pasta_base
            / cnpj
            / "cte"
        )

        if not pasta_cte.exists():

            return {
                "importados": 0,
                "duplicados": 0,
                "ignorados": 0,
                "erros": [],
                "mensagem": (
                    "Pasta de CT-e não encontrada."
                ),
            }

        arquivos = sorted(
            pasta_cte.glob(
                "*.xml"
            )
        )

        db = get_session()

        try:

            empresa = (
                db.query(Company)
                .filter(
                    Company.cnpj == cnpj
                )
                .first()
            )

            empresa_id = None

            if empresa is not None:
                empresa_id = empresa.id

            importador = CTeImportService(
                db
            )

            resultado = (
                importador.importar_arquivos(
                    arquivos=[
                        str(arquivo)
                        for arquivo in arquivos
                    ],
                    empresa_id=empresa_id,
                )
            )

            resultado[
                "arquivos_encontrados"
            ] = len(arquivos)

            resultado[
                "cnpj"
            ] = cnpj

            return resultado

        finally:

            db.close()