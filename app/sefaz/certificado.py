from pathlib import Path


class Certificado:

    def __init__(
        self,
        caminho: str,
        senha: str,
    ):

        self.caminho = Path(caminho)
        self.senha = senha

    ############################################################

    def validar(self):

        if not self.caminho.exists():

            raise FileNotFoundError(
                f"Certificado não encontrado: {self.caminho}"
            )

        if self.caminho.suffix.lower() not in (
            ".pfx",
            ".p12",
        ):

            raise ValueError(
                "O certificado deve estar no formato .pfx ou .p12."
            )

        if not self.senha:

            raise ValueError(
                "Senha do certificado não informada."
            )

        return True

    ############################################################

    @property
    def arquivo(self):

        return str(self.caminho)

    ############################################################

    @property
    def senha_certificado(self):

        return self.senha