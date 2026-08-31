import re


def somente_numeros(valor):

    return re.sub(r"\D", "", valor)


def formatar_cnpj(cnpj):

    cnpj = somente_numeros(cnpj)

    if len(cnpj) != 14:
        return cnpj

    return (
        f"{cnpj[:2]}."
        f"{cnpj[2:5]}."
        f"{cnpj[5:8]}/"
        f"{cnpj[8:12]}-"
        f"{cnpj[12:]}"
    )