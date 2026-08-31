from getpass import getpass

from app.dfe.providers import NFSeProvider


CNPJ = input(
    "CNPJ da empresa: "
).strip()

CERTIFICADO = input(
    "Caminho completo do certificado PFX: "
).strip()

SENHA = getpass(
    "Senha do certificado: "
)

provider = NFSeProvider(
    certificado_path=CERTIFICADO,
    senha=SENHA,
    ambiente="producao",
    uf="CE",
)

try:

    print(
        "[NFS-e] Iniciando..."
    )

    resultado = provider.sincronizar(
        CNPJ
    )

    print("=" * 60)
    print(
        "SUCESSO:",
        resultado.get("sucesso")
    )
    print(
        "STATUS HTTP:",
        resultado.get("status_http")
    )
    print(
        "STATUS:",
        resultado.get(
            "status_processamento"
        )
    )
    print(
        "ÚLTIMO NSU:",
        resultado.get("ultimo_nsu")
    )
    print(
        "XMLs:",
        resultado.get(
            "quantidade_xml",
            0,
        )
    )

    print("=" * 60)

    for arquivo in resultado.get(
        "arquivos",
        []
    ):

        print(
            "SALVO:",
            arquivo.get("caminho")
        )

finally:

    provider.desconectar()