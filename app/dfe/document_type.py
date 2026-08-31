from enum import Enum


class DFeType(str, Enum):

    NFE = "NFE"
    NFCE = "NFCE"
    CTE = "CTE"
    CTE_OS = "CTE_OS"
    NFSE = "NFSE"
    MDFE = "MDFE"
    BPE = "BPE"
    NF3E = "NF3E"
    NFCOM = "NFCOM"
    EVENTO = "EVENTO"
    DESCONHECIDO = "DESCONHECIDO"