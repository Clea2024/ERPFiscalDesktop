import bcrypt


class PasswordService:

    @staticmethod
    def gerar_hash(senha: str) -> str:
        senha_bytes = senha.encode("utf-8")
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(
            senha_bytes,
            salt
        ).decode("utf-8")

    @staticmethod
    def verificar(senha: str, senha_hash: str) -> bool:
        return bcrypt.checkpw(
            senha.encode("utf-8"),
            senha_hash.encode("utf-8")
        )