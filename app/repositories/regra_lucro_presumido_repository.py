from app.models.regra_lucro_presumido import RegraLucroPresumido


class RegraLucroPresumidoRepository:

    def __init__(self, db):

        self.db = db

    def listar_ativas(self):

        return (
            self.db.query(
                RegraLucroPresumido
            )
            .filter(
                RegraLucroPresumido.ativa
                == True
            )
            .order_by(
                RegraLucroPresumido.descricao
            )
            .all()
        )

    def buscar_por_atividade(
        self,
        atividade,
    ):

        return (
            self.db.query(
                RegraLucroPresumido
            )
            .filter(
                RegraLucroPresumido.atividade
                == atividade,
                RegraLucroPresumido.ativa
                == True,
            )
            .first()
        )

    def inserir(
        self,
        regra,
    ):

        self.db.add(
            regra
        )

        self.db.commit()

        self.db.refresh(
            regra
        )

        return regra

    def atualizar(self):

        self.db.commit()

    def excluir(
        self,
        regra,
    ):

        regra.ativa = False

        self.db.commit()
