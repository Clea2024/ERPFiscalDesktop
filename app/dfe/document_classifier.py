class DFeDocumentClassifier:

    @staticmethod
    def identificar_por_modelo(
        modelo,
    ):

        modelo = str(
            modelo or ""
        ).strip()

        if modelo == "55":
            return "NFE"

        if modelo == "65":
            return "NFCE"

        if modelo == "57":
            return "CTE"

        if modelo == "67":
            return "CTE_OS"

        return "DFE"

    @staticmethod
    def nome_exibicao(
        modelo,
    ):

        tipo = (
            DFeDocumentClassifier
            .identificar_por_modelo(
                modelo
            )
        )

        nomes = {
            "NFE": "NF-e",
            "NFCE": "NFC-e",
            "CTE": "CT-e",
            "CTE_OS": "CT-e OS",
            "DFE": "DF-e",
        }

        return nomes.get(
            tipo,
            "DF-e",
        )