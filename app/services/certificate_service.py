import os

from app.services.certificate_reader import CertificateReader


class CertificateService:

    def __init__(self):

        self.reader = CertificateReader()

    ####################################################################

    def validar(self, dados):

        if dados.get("company_id") is None:

            return (
                False,
                "Selecione uma empresa.",
                None,
            )

        descricao = (
            dados.get("descricao", "")
            .strip()
        )

        if descricao == "":

            return (
                False,
                "Informe uma descrição.",
                None,
            )

        arquivo = (
            dados.get("arquivo", "")
            .strip()
        )

        if arquivo == "":

            return (
                False,
                "Selecione o certificado.",
                None,
            )

        if not os.path.exists(arquivo):

            return (
                False,
                "Arquivo do certificado não encontrado.",
                None,
            )

        if not arquivo.lower().endswith(".pfx"):

            return (
                False,
                "O arquivo deve possuir extensão .pfx.",
                None,
            )

        senha = (
            dados.get("senha", "")
            .strip()
        )

        if senha == "":

            return (
                False,
                "Informe a senha do certificado.",
                None,
            )

        ################################################################

        ok, resultado = (
            self.reader.validar_certificado(
                arquivo,
                senha,
            )
        )

        if not ok:

            return (
                False,
                resultado,
                None,
            )

        if self.reader.esta_vencido(resultado):

            return (
                False,
                (
                    "O certificado está vencido desde "
                    f"{self.reader.validade_formatada(resultado)}."
                ),
                None,
            )

        ################################################################

        return (
            True,
            "Certificado validado com sucesso.",
            resultado,
        )