import re


def limpar_cnpj(cnpj: str) -> str:
    return re.sub(r"\D", "", cnpj)


def validar_cnpj(cnpj: str) -> bool:

    cnpj = limpar_cnpj(cnpj)

    if len(cnpj) != 14:
        return False

    if cnpj == cnpj[0] * 14:
        return False

    return True