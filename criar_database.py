from pathlib import Path

BASE = Path.cwd()

pastas = [
    "app/database",
    "app/database/models",
]

arquivos = [
    "app/database/__init__.py",
    "app/database/database.py",
    "app/database/base.py",
    "app/database/session.py",
    "app/database/engine.py",
    "app/database/models/__init__.py",
]

print("=" * 60)
print("CRIANDO MÓDULO DATABASE")
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
print("=" * 60)
print("DATABASE CRIADO COM SUCESSO")
print("=" * 60)