from pathlib import Path

# ==========================================================
# ERP Fiscal Desktop
# Entrega 1A - Estrutura Cliente SOAP
# ==========================================================

BASE = Path.cwd()

estrutura = [
    "app/sefaz/client",
    "app/sefaz/certificate",
    "app/sefaz/distribuicao",
    "app/sefaz/models",
    "app/sefaz/cache",
]

arquivos = [
    # CLIENT
    "app/sefaz/client/__init__.py",
    "app/sefaz/client/endpoints.py",
    "app/sefaz/client/exceptions.py",
    "app/sefaz/client/transport.py",
    "app/sefaz/client/soap_client.py",
    "app/sefaz/client/envelope.py",

    # CERTIFICATE
    "app/sefaz/certificate/__init__.py",
    "app/sefaz/certificate/loader.py",
    "app/sefaz/certificate/validator.py",
    "app/sefaz/certificate/manager.py",

    # DISTRIBUIÇÃO
    "app/sefaz/distribuicao/__init__.py",
    "app/sefaz/distribuicao/distribuicao_service.py",
    "app/sefaz/distribuicao/nsu_service.py",
    "app/sefaz/distribuicao/xml_decoder.py",
    "app/sefaz/distribuicao/xml_repository.py",
    "app/sefaz/distribuicao/response_parser.py",

    # MODELS
    "app/sefaz/models/__init__.py",
    "app/sefaz/models/dist_dfe.py",
    "app/sefaz/models/documento.py",

    # CACHE
    "app/sefaz/cache/ultimo_nsu.json",
]

print("=" * 60)
print("CRIANDO ESTRUTURA DO MÓDULO SEFAZ")
print("=" * 60)

# ----------------------------------------------------------

for pasta in estrutura:

    caminho = BASE / pasta

    caminho.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(f"[OK] Pasta criada: {pasta}")

# ----------------------------------------------------------

for arquivo in arquivos:

    caminho = BASE / arquivo

    if not caminho.exists():

        if caminho.suffix == ".json":

            caminho.write_text(
                '{\n    "ultimo_nsu": "000000000000000"\n}',
                encoding="utf-8",
            )

        else:

            caminho.write_text(
                "",
                encoding="utf-8",
            )

        print(f"[OK] Arquivo criado: {arquivo}")

    else:

        print(f"[EXISTE] {arquivo}")

print()
print("=" * 60)
print("ESTRUTURA CRIADA COM SUCESSO")
print("=" * 60)