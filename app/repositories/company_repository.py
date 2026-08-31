from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.company import Company


class CompanyRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def listar(self):

        return (
            self.db.query(Company)
            .order_by(
                Company.razao_social
            )
            .all()
        )

    def buscar_por_id(
        self,
        empresa_id,
    ):

        return (
            self.db.query(Company)
            .filter(
                Company.id == empresa_id
            )
            .first()
        )

    def buscar_por_cnpj(
        self,
        cnpj,
    ):

        return (
            self.db.query(Company)
            .filter(
                Company.cnpj == cnpj
            )
            .first()
        )

    def pesquisar(
        self,
        texto,
    ):

        return (
            self.db.query(Company)
            .filter(
                or_(
                    Company.razao_social.contains(
                        texto
                    ),
                    Company.nome_fantasia.contains(
                        texto
                    ),
                    Company.cnpj.contains(
                        texto
                    ),
                )
            )
            .all()
        )

    def inserir(
        self,
        empresa,
    ):

        self.db.add(
            empresa
        )

        self.db.commit()

        self.db.refresh(
            empresa
        )

        return empresa

    def atualizar(self):

        self.db.commit()

    def excluir(
        self,
        empresa,
    ):

        self.db.delete(
            empresa
        )

        self.db.commit()