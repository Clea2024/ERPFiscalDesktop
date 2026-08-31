from app.database.database import get_session

from app.models.certificate import Certificate
from app.repositories.certificate_repository import (
    CertificateRepository,
)
from app.services.certificate_service import (
    CertificateService,
)


class CertificateController:

    def __init__(self):

        self.db = get_session()

        self.repository = (
            CertificateRepository(self.db)
        )

        self.service = (
            CertificateService()
        )

    ####################################################################

    def listar(self):

        return self.repository.listar()

    ####################################################################

    def buscar(self, certificado_id):

        return self.repository.buscar_por_id(
            certificado_id
        )

    ####################################################################

    def listar_empresa(self, company_id):

        return self.repository.buscar_por_empresa(
            company_id
        )

    ####################################################################

    def salvar(self, **dados):

        ok, mensagem, dados_certificado = (
            self.service.validar(dados)
        )

        if not ok:

            return False, mensagem

        certificado = Certificate(

            company_id=dados["company_id"],

            descricao=dados["descricao"],

            arquivo=dados["arquivo"],

            senha=dados["senha"],

            validade=dados_certificado[
                "validade_fim"
            ],

            emissor=dados_certificado[
                "emissor"
            ],

            serial=dados_certificado[
                "serial"
            ],

            ativo="S",
        )

        self.repository.inserir(
            certificado
        )

        return (
            True,
            "Certificado cadastrado com sucesso."
        )

    ####################################################################

    def atualizar(self, certificado):

        self.repository.atualizar()

        return (
            True,
            "Certificado atualizado com sucesso."
        )

    ####################################################################

    def excluir(self, certificado):

        self.repository.excluir(
            certificado
        )

        return (
            True,
            "Certificado excluído com sucesso."
        )