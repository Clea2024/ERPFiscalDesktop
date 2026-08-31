from pathlib import Path

BASE = Path.cwd()

pastas = [
    "app/core",
]

arquivos = [
    "app/core/__init__.py",
    "app/core/config.py",
    "app/core/logger.py",
    "app/core/paths.py",
    "app/core/constants.py",
    "app/core/environment.py",
    "app/core/exceptions.py",
    "app/core/version.py",
]

print("=" * 60)
print("CRIANDO CORE DO ERP")
print("=" * 60)

for pasta in pastas:

    (BASE / pasta).mkdir(
        parents=True,
        exist_ok=True,
    )

for arquivo in arquivos:

    caminho = BASE / arquivo

    if not caminho.exists():

        caminho.write_text(
            "",
            encoding="utf-8",
        )

        print("[OK]", arquivo)

    else:

        print("[EXISTE]", arquivo)

print()
print("CORE CRIADO COM SUCESSO")