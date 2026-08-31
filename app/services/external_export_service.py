import shutil

from pathlib import Path


class ExternalExportService:

    def __init__(self):

        pass

    ############################################################
    # IDENTIFICAR TIPO
    ############################################################

    @staticmethod
    def identificar_tipo(documento):

        modelo = str(
            getattr(
                documento,
                "modelo",
                "",
            )
            or ""
        )

        origem = str(
            getattr(
                documento,
                "origem",
                "",
            )
            or ""
        ).upper()

        if modelo == "55":
            return "NFE"

        if modelo == "65":
            return "NFCE"

        if modelo == "57":
            return "CTE"

        if modelo == "67":
            return "CTE_OS"

        if origem == "NFSE":
            return "NFSE"

        if origem == "CTE":
            return "CTE"

        return (
            origem
            or "DFE"
        )

    ############################################################
    # COPIAR DOCUMENTO
    ############################################################

    def exportar_documento(
        self,
        documento,
        pasta_destino,
        cnpj_empresa="SEM_CNPJ",
    ):

        xml_path = getattr(
            documento,
            "xml_path",
            "",
        )

        if not xml_path:

            return {
                "sucesso": False,
                "mensagem": (
                    "Documento sem caminho XML."
                ),
            }

        origem = Path(
            xml_path
        )

        if not origem.exists():

            return {
                "sucesso": False,
                "mensagem": (
                    f"Arquivo não encontrado: "
                    f"{origem}"
                ),
            }

        ########################################################
        # CNPJ
        ########################################################

        cnpj_empresa = "".join(
            caractere
            for caractere in str(
                cnpj_empresa
            )
            if caractere.isdigit()
        )

        if not cnpj_empresa:
            cnpj_empresa = "SEM_CNPJ"

        ########################################################
        # COMPETÊNCIA
        ########################################################

        data = getattr(
            documento,
            "data_emissao",
            None,
        )

        if data is not None:

            ano = str(
                data.year
            )

            mes = (
                f"{data.month:02d}"
            )

        else:

            ano = "SEM_ANO"
            mes = "SEM_MES"

        ########################################################
        # TIPO
        ########################################################

        tipo = (
            self.identificar_tipo(
                documento
            )
        )

        ########################################################
        # PASTA FINAL
        ########################################################

        destino = (
            Path(pasta_destino)
            / cnpj_empresa
            / ano
            / mes
            / tipo
        )

        destino.mkdir(
            parents=True,
            exist_ok=True,
        )

        ########################################################
        # COPIAR
        ########################################################

        arquivo_destino = (
            destino
            / origem.name
        )

        shutil.copy2(
            origem,
            arquivo_destino,
        )

        return {
            "sucesso": True,
            "origem": str(origem),
            "destino": str(
                arquivo_destino
            ),
        }

    ############################################################
    # EXPORTAR VÁRIOS
    ############################################################

    def exportar_documentos(
        self,
        documentos,
        pasta_destino,
        cnpj_empresa="SEM_CNPJ",
    ):

        exportados = 0
        ignorados = 0
        erros = []

        for documento in documentos:

            try:

                resultado = (
                    self.exportar_documento(
                        documento=documento,
                        pasta_destino=pasta_destino,
                        cnpj_empresa=cnpj_empresa,
                    )
                )

                if resultado.get(
                    "sucesso"
                ):

                    exportados += 1

                else:

                    ignorados += 1

            except Exception as erro:

                erros.append(
                    str(erro)
                )

        return {
            "exportados": exportados,
            "ignorados": ignorados,
            "erros": erros,
        }