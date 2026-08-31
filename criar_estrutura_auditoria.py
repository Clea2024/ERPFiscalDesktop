from pathlib import Path
import json

# ==========================================================
# ESTRUTURA DO MÓDULO DE AUDITORIA
# ==========================================================

BASE = Path("app") / "auditoria"

pastas = [
    BASE,
    BASE / "rules",
    BASE / "validators",
    BASE / "services",
    BASE / "reports",
    BASE / "tables",
]

arquivos_py = [
    BASE / "__init__.py",
    BASE / "audit_engine.py",
    BASE / "audit_result.py",
    BASE / "legislation_engine.py",

    BASE / "rules" / "__init__.py",
    BASE / "rules" / "cfop_rule.py",
    BASE / "rules" / "ncm_rule.py",
    BASE / "rules" / "cest_rule.py",
    BASE / "rules" / "icms_rule.py",
    BASE / "rules" / "icms_st_rule.py",
    BASE / "rules" / "pis_rule.py",
    BASE / "rules" / "cofins_rule.py",
    BASE / "rules" / "ipi_rule.py",
    BASE / "rules" / "difal_rule.py",
    BASE / "rules" / "fecop_rule.py",
    BASE / "rules" / "reforma_tributaria_rule.py",

    BASE / "validators" / "__init__.py",
    BASE / "validators" / "fiscal_validator.py",
    BASE / "validators" / "xml_validator.py",
    BASE / "validators" / "tributario_validator.py",

    BASE / "services" / "__init__.py",
    BASE / "services" / "audit_service.py",

    BASE / "reports" / "__init__.py",
    BASE / "reports" / "audit_pdf.py",
    BASE / "reports" / "audit_excel.py",
    BASE / "reports" / "audit_html.py",
]

arquivos_json = [
    BASE / "tables" / "cfop.json",
    BASE / "tables" / "ncm.json",
    BASE / "tables" / "cest.json",
]

# ==========================================================
# CRIA PASTAS
# ==========================================================

for pasta in pastas:
    pasta.mkdir(parents=True, exist_ok=True)
    print(f"[OK] Pasta criada: {pasta}")

# ==========================================================
# CRIA ARQUIVOS PY
# ==========================================================

for arquivo in arquivos_py:

    if not arquivo.exists():

        arquivo.write_text(
            "# Arquivo criado automaticamente\n",
            encoding="utf-8",
        )

        print(f"[OK] {arquivo}")

    else:

        print(f"[EXISTE] {arquivo}")

# ==========================================================
# CRIA JSON
# ==========================================================

for arquivo in arquivos_json:

    if not arquivo.exists():

        with open(
            arquivo,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                {},
                f,
                indent=4,
                ensure_ascii=False,
            )

        print(f"[OK] {arquivo}")

    else:

        print(f"[EXISTE] {arquivo}")

print()
print("=" * 60)
print("MÓDULO DE AUDITORIA CRIADO COM SUCESSO")
print("=" * 60)