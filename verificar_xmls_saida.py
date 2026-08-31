from pathlib import Path
from lxml import etree

PASTA_XML = Path(
    r"C:\Users\clea-\ERPFiscalDesktop\xml"
)

CNPJ_EMPRESA = "23612215000169"

NS = {
    "nfe": "http://www.portalfiscal.inf.br/nfe"
}

encontrados = []

for caminho in PASTA_XML.rglob("*.xml"):

    try:

        raiz = etree.parse(
            str(caminho)
        ).getroot()

        emitente = raiz.find(
            ".//nfe:emit/nfe:CNPJ",
            namespaces=NS,
        )

        if emitente is None:
            continue

        cnpj_emitente = "".join(
            caractere
            for caractere in (
                emitente.text or ""
            )
            if caractere.isdigit()
        )

        if cnpj_emitente == CNPJ_EMPRESA:

            encontrados.append(
                caminho
            )

    except Exception:
        pass

print(
    "XMLs COM A EMPRESA COMO EMITENTE:",
    len(encontrados),
)

for caminho in encontrados[:30]:

    print(
        caminho
    )
