import json

from pathlib import Path


class UserSettings:

    BASE_DIR = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    FILE_PATH = (
        BASE_DIR
        / "config"
        / "user_settings.json"
    )

    DEFAULTS = {
        "baixar_nfe": True,
        "baixar_nfce": True,
        "baixar_cte": True,
        "baixar_nfse": True,
        "max_workers": 4,
        "xml_folder": str(
            BASE_DIR / "xml"
        ),
        "external_export_folder": "",
        "report_folder": str(
            BASE_DIR / "reports"
        ),
        "backup_folder": str(
            BASE_DIR / "backups"
        ),
        "certificate_folder": str(
            BASE_DIR / "certificates"
        ),
        "uf": "CE",
        "ambiente": "producao",
        "sefaz_24h": True,
        "intervalo_verificacao": 60,
        "organizar_por_cnpj": True,
        "organizar_por_ano": True,
        "organizar_por_mes": True,
        "organizar_por_tipo": True,
    }

    @classmethod
    def carregar(cls):

        if not cls.FILE_PATH.exists():

            return cls.DEFAULTS.copy()

        try:

            dados = json.loads(
                cls.FILE_PATH.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            return cls.DEFAULTS.copy()

        resultado = (
            cls.DEFAULTS.copy()
        )

        resultado.update(
            dados
        )

        return resultado

    @classmethod
    def salvar(
        cls,
        configuracoes,
    ):

        cls.FILE_PATH.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        cls.FILE_PATH.write_text(
            json.dumps(
                configuracoes,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )