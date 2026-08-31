from app.dfe.document_type import DFeType


class DFeManager:

    def __init__(self):

        self.providers = {}

    ############################################################
    # REGISTRAR PROVIDER
    ############################################################

    def registrar(
        self,
        tipo: DFeType,
        provider,
    ):

        self.providers[tipo] = provider

    ############################################################
    # OBTER PROVIDER
    ############################################################

    def obter(
        self,
        tipo: DFeType,
    ):

        provider = self.providers.get(
            tipo
        )

        if provider is None:

            raise RuntimeError(
                f"Provider não configurado para {tipo.value}."
            )

        return provider

    ############################################################
    # SINCRONIZAR
    ############################################################

    def sincronizar(
        self,
        tipo: DFeType,
        cnpj: str,
    ):

        provider = self.obter(
            tipo
        )

        try:

            provider.conectar()

            return provider.sincronizar(
                cnpj
            )

        finally:

            provider.desconectar()

    ############################################################
    # TIPOS DISPONÍVEIS
    ############################################################

    def tipos_disponiveis(self):

        return list(
            self.providers.keys()
        )