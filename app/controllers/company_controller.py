from app.database.database import get_session
from app.models.company import Company
from app.repositories.company_repository import CompanyRepository


class CompanyController:

    def __init__(self):

        self.db = get_session()
        self.repository = CompanyRepository(self.db)

    def listar(self):

        return self.repository.listar()

    def pesquisar(self, texto):

        return self.repository.pesquisar(texto)

    def salvar(
        self,
        **dados,
    ):

        cnpj = dados.get(
            "cnpj",
            "",
        )

        empresa = (
            self.repository.buscar_por_cnpj(
                cnpj
            )
        )

        ########################################################
        # EMPRESA EXISTENTE - ATUALIZAR
        ########################################################

        if empresa is not None:

            empresa.razao_social = dados.get(
                "razao_social",
                empresa.razao_social,
            )

            empresa.nome_fantasia = dados.get(
                "nome_fantasia",
                empresa.nome_fantasia,
            )

            empresa.inscricao_estadual = dados.get(
                "inscricao_estadual",
                empresa.inscricao_estadual,
            )

            empresa.inscricao_municipal = dados.get(
                "inscricao_municipal",
                empresa.inscricao_municipal,
            )

            empresa.regime = dados.get(
                "regime",
                empresa.regime,
            )

            empresa.certificado = dados.get(
                "certificado",
                empresa.certificado,
            )

            self.repository.atualizar()

            return empresa

        ########################################################
        # EMPRESA NOVA
        ########################################################

        empresa = Company(
            **dados
        )

        return self.repository.inserir(
            empresa
        )

    def excluir(
        self,
        empresa,
    ):

        self.repository.excluir(
            empresa
        )