from sqlalchemy.orm import Session

from app.models.certificate import Certificate


class CertificateRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return (
            self.db.query(Certificate)
            .order_by(Certificate.descricao)
            .all()
        )

    def buscar_por_id(self, certificado_id: int):

        return (
            self.db.query(Certificate)
            .filter(Certificate.id == certificado_id)
            .first()
        )

    def buscar_por_empresa(self, company_id: int):

        return (
            self.db.query(Certificate)
            .filter(Certificate.company_id == company_id)
            .order_by(Certificate.descricao)
            .all()
        )

    def inserir(self, certificado: Certificate):

        self.db.add(certificado)

        self.db.commit()

        self.db.refresh(certificado)

        return certificado

    def atualizar(self):

        self.db.commit()

    def excluir(self, certificado: Certificate):

        self.db.delete(certificado)

        self.db.commit()