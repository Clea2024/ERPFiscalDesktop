from datetime import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import pkcs12


class CertificateReader:

    def __init__(self):
        pass

    ####################################################################

    def ler(self, arquivo, senha):

        with open(arquivo, "rb") as f:
            dados = f.read()

        _, certificado, _ = (
            pkcs12.load_key_and_certificates(
                dados,
                senha.encode("utf-8"),
                backend=default_backend(),
            )
        )

        if certificado is None:
            raise Exception(
                "Não foi possível abrir o certificado."
            )

        return self.extrair_dados(certificado)

    ####################################################################

    def extrair_dados(self, certificado):

        assunto = certificado.subject

        emissor = certificado.issuer

        dados = {

            "cnpj": "",

            "razao_social": "",

            "emissor": "",

            "serial": str(
                certificado.serial_number
            ),

            "validade_inicio":
                certificado.not_valid_before,

            "validade_fim":
                certificado.not_valid_after,

        }

        ###############################################################

        for atributo in assunto:

            nome = atributo.oid._name

            valor = atributo.value

            if nome == "commonName":

                dados["razao_social"] = valor

            elif nome == "organizationIdentifier":

                texto = (
                    valor.upper()
                    .replace("BR", "")
                    .replace("CNPJ", "")
                    .replace(":", "")
                    .strip()
                )

                dados["cnpj"] = texto
        ###############################################################

        nomes_emissor = []

        for atributo in emissor:

            nomes_emissor.append(
                atributo.value
            )

        dados["emissor"] = " | ".join(
            nomes_emissor
        )

        ###############################################################

        dados["vencido"] = (
            datetime.now()
            > certificado.not_valid_after
        )

        return dados

    ####################################################################

    def validar_certificado(
        self,
        arquivo,
        senha,
    ):

        try:

            dados = self.ler(
                arquivo,
                senha,
            )

            return True, dados

        except FileNotFoundError:

            return (
                False,
                "Arquivo do certificado não encontrado.",
            )

        except ValueError:

            return (
                False,
                "Senha do certificado inválida.",
            )

        except Exception as erro:

            return (
                False,
                str(erro),
            )

    ####################################################################

    def esta_vencido(self, dados):

        return dados.get(
            "vencido",
            False,
        )

    ####################################################################

    def validade_formatada(self, dados):

        validade = dados.get(
            "validade_fim"
        )

        if validade is None:

            return ""

        return validade.strftime(
            "%d/%m/%Y"
        )

    ####################################################################

    def razao_social(self, dados):

        return dados.get(
            "razao_social",
            ""
        )

    ####################################################################

    def cnpj(self, dados):

        return dados.get(
            "cnpj",
            ""
        )

    ####################################################################

    def emissor(self, dados):

        return dados.get(
            "emissor",
            ""
        )