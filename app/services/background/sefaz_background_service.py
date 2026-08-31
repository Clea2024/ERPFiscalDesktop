import logging
import threading
import time

from app.dfe.providers import (
    CTeProvider,
    NFSeProvider,
)

from app.dfe.nfce_import_service import NFCeImportService
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from app.dfe.providers import CTeProvider
from app.config.user_settings import UserSettings
from datetime import datetime
from datetime import timedelta

from app.database.database import get_session
from app.models.sefaz_sync_state import SefazSyncState
from app.sefaz.client import SefazClient
from app.sefaz.sync import SefazSyncManager
from app.models.company import Company
from app.models.certificate import Certificate


class SefazBackgroundService:


    def __init__(
        self,
        intervalo_verificacao: int = 60,
        max_workers: int = 4,
    ):

        self.intervalo_verificacao = max(
            30,
            int(intervalo_verificacao),
        )

        self.max_workers = max(
            1,
            int(max_workers),
        )

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        self._thread = None
        self._parar = threading.Event()

        self.empresas = {}
        self.config = UserSettings.carregar()

        self.intervalo_verificacao = max(
            30,
            int(
                self.config.get(
                    "intervalo_verificacao",
                    intervalo_verificacao,
                )
            )
        )

        self.max_workers = max(
            1,
            int(
                self.config.get(
                    "max_workers",
                    max_workers,
                )
            )
        )

        self.ativo_24h = bool(
            self.config.get(
                "sefaz_24h",
                True,
            )
        )

        self.baixar_nfe = bool(
            self.config.get(
                "baixar_nfe",
                True,
            )
        )

        self.baixar_nfce = bool(
            self.config.get(
                "baixar_nfce",
                True,
            )
        )

        self.baixar_cte = bool(
            self.config.get(
                "baixar_cte",
                True,
            )
        )

        self.baixar_nfse = bool(
            self.config.get(
                "baixar_nfse",
                True,
            )
        )


    ############################################################
    # CADASTRO TEMPORÁRIO DE EMPRESAS
    ############################################################

    def adicionar_empresa(
        self,
        cnpj: str,
        certificado_path: str,
        senha: str,
        ambiente: str = "producao",
        uf: str = "CE",
    ):

        cnpj = "".join(
            caractere
            for caractere in str(cnpj)
            if caractere.isdigit()
        )

        if len(cnpj) != 14:
            raise ValueError(
                "CNPJ deve possuir 14 dígitos."
            )

        self.empresas[cnpj] = {
            "cnpj": cnpj,
            "certificado_path": certificado_path,
            "senha": senha,
            "ambiente": ambiente,
            "uf": uf,
        }

    ############################################################
    # VERIFICAR SE PODE CONSULTAR
    ############################################################

    def deve_consultar(
        self,
        cnpj: str,
    ) -> tuple[bool, str]:

        db = get_session()

        try:

            estado = (
                db.query(SefazSyncState)
                .filter(
                    SefazSyncState.cnpj == cnpj
                )
                .first()
            )

            if estado is None:

                return (
                    True,
                    "Primeira sincronização.",
                )

            agora = datetime.now()

            ####################################################
            # BLOQUEIO 656
            ####################################################

            if (
                estado.bloqueado_ate is not None
                and agora < estado.bloqueado_ate
            ):

                return (
                    False,
                    "Aguardando liberação da SEFAZ.",
                )

            ####################################################
            # EXISTEM NSUs PENDENTES
            ####################################################

            try:

                ultimo = int(
                    estado.ultimo_nsu
                    or "0"
                )

                maximo = int(
                    estado.max_nsu
                    or "0"
                )

            except ValueError:

                ultimo = 0
                maximo = 0

            if ultimo < maximo:

                return (
                    True,
                    "Existem documentos pendentes.",
                )

            ####################################################
            # FILA JÁ SINCRONIZADA
            ####################################################

            if estado.ultima_consulta is None:

                return (
                    True,
                    "Nenhuma consulta anterior.",
                )

            proxima_consulta = (
                estado.ultima_consulta
                + timedelta(hours=1)
            )

            if agora >= proxima_consulta:

                return (
                    True,
                    "Janela de nova verificação atingida.",
                )

            return (
                False,
                "Empresa já sincronizada recentemente.",
            )

        finally:

            db.close()

    ############################################################
    # SINCRONIZAR UMA EMPRESA
    ############################################################

    def sincronizar_empresa(
        self,
        configuracao: dict,
    ):

        cnpj = configuracao[
            "cnpj"
        ]

        cnpj = configuracao[
                "cnpj"
        ]

        ########################################################
        # RECARREGAR CONFIGURAÇÕES
        ########################################################

        config = UserSettings.carregar()

        baixar_nfe = bool(
            config.get(
                "baixar_nfe",
                True,
            )
        )

        baixar_nfce = bool(
            config.get(
                "baixar_nfce",
                True,
            )
        )

        baixar_cte = bool(
            config.get(
                "baixar_cte",
                True,
            )
        )

        baixar_nfse = bool(
            config.get(
                "baixar_nfse",
                True,
            )
        )

        ########################################################
        # NF-e / NFC-e
        ########################################################

        if (
            baixar_nfe
            or baixar_nfce
        ):

            permitido, motivo = (
                self.deve_consultar(
                    cnpj
                )
            )

            if permitido:

                print(
                    f"[24H] NF-e/NFC-e: "
                    f"sincronizando {cnpj}..."
                )

                client = None

                try:

                    client = SefazClient(
                        certificado_path=(
                            configuracao[
                                "certificado_path"
                            ]
                        ),
                        senha=(
                            configuracao[
                                "senha"
                            ]
                        ),
                        ambiente=(
                            configuracao[
                                "ambiente"
                            ]
                        ),
                        uf=(
                            configuracao[
                                "uf"
                            ]
                        ),
                    )

                    client.conectar()

                    wsdl = (
                        client.conectar_wsdl()
                        + "?WSDL"
                    )

                    client.carregar_wsdl(
                        wsdl
                    )

                    manager = (
                        SefazSyncManager(
                            client
                        )
                    )

                    resultado = (
                        manager.sincronizar(
                            cnpj
                        )
                    )

                    print(
                        "[24H] NF-e/NFC-e:",
                        cnpj,
                        resultado.get(
                            "cstat",
                            "-"
                        ),
                        resultado.get(
                            "mensagem",
                            "-"
                        ),
                    )

                    print(
                        "[24H] XMLs NF-e/NFC-e:",
                        resultado.get(
                            "quantidade_xml",
                            0,
                        ),
                    )

                except Exception as erro:

                    self.logger.exception(
                        "Erro NF-e/NFC-e do CNPJ %s",
                        cnpj,
                    )

                    print(
                        f"[24H] ERRO NF-e/NFC-e "
                        f"{cnpj}: {erro}"
                    )

                finally:

                    if client is not None:

                        try:

                            client.desconectar()

                        except Exception:

                            pass

            else:

                print(
                    f"[24H] NF-e/NFC-e "
                    f"{cnpj}: {motivo}"
                )

        ########################################################
        # NFC-e - IMPORTAÇÃO LOCAL
        ########################################################

        if baixar_nfce:

            try:

                importador_nfce = NFCeImportService()

                resultado_nfce = (
                    importador_nfce.importar(
                        cnpj
                    )
                )

                print(
                    "[24H] NFC-e encontradas:",
                    resultado_nfce.get(
                        "encontrados",
                        0,
                    ),
                )

                print(
                    "[24H] NFC-e importadas:",
                    resultado_nfce.get(
                        "importados",
                        0,
                    ),
                )

            except Exception as erro:

                self.logger.exception(
                    "Erro na importação NFC-e do CNPJ %s",
                    cnpj,
                )

                print(
                    f"[24H] ERRO NFC-e "
                    f"{cnpj}: {erro}"
                )

        ########################################################
        # CT-e
        ########################################################

        if baixar_cte:

            print(
                f"[24H] CT-e: "
                f"sincronizando {cnpj}..."
            )

            provider_cte = None

            try:

                provider_cte = CTeProvider(
                    certificado_path=(
                        configuracao[
                            "certificado_path"
                        ]
                    ),
                    senha=(
                        configuracao[
                            "senha"
                        ]
                    ),
                    ambiente=(
                        configuracao[
                            "ambiente"
                        ]
                    ),
                    uf=(
                        configuracao[
                            "uf"
                        ]
                    ),
                )

                resultado_cte = (
                    provider_cte.sincronizar(
                        cnpj
                    )
                )

                print(
                    "[24H] CT-e:",
                    cnpj,
                    resultado_cte.get(
                        "cstat",
                        "-"
                    ),
                    resultado_cte.get(
                        "mensagem",
                        "-"
                    ),
                )

                print(
                    "[24H] CT-e XMLs:",
                    resultado_cte.get(
                        "quantidade_xml",
                        0,
                    ),
                )

            except Exception as erro:

                self.logger.exception(
                    "Erro CT-e do CNPJ %s",
                    cnpj,
                )

                print(
                    f"[24H] ERRO CT-e "
                    f"{cnpj}: {erro}"
                )

            finally:

                if provider_cte is not None:

                    try:

                        provider_cte.desconectar()

                    except Exception:

                        pass

        ########################################################
        # NFS-e
        ########################################################

        if baixar_nfse:

            print(
                f"[24H] NFS-e: "
                f"sincronizando {cnpj}..."
            )

            provider_nfse = None

            try:

                provider_nfse = NFSeProvider(
                    certificado_path=(
                        configuracao[
                            "certificado_path"
                        ]
                    ),
                    senha=(
                        configuracao[
                            "senha"
                        ]
                    ),
                    ambiente=(
                        configuracao[
                            "ambiente"
                        ]
                    ),
                    uf=(
                        configuracao[
                            "uf"
                        ]
                    ),
                )

                resultado_nfse = (
                    provider_nfse.sincronizar(
                        cnpj
                    )
                )

                print(
                    "[24H] NFS-e:",
                    cnpj,
                    resultado_nfse.get(
                        "status_processamento",
                        "-"
                    ),
                )

                print(
                    "[24H] NFS-e XMLs:",
                    resultado_nfse.get(
                        "quantidade_xml",
                        0,
                    ),
                )

            except Exception as erro:

                self.logger.exception(
                    "Erro NFS-e do CNPJ %s",
                    cnpj,
                )

                print(
                    f"[24H] ERRO NFS-e "
                    f"{cnpj}: {erro}"
                )

            finally:

                if provider_nfse is not None:

                    try:

                        provider_nfse.desconectar()

                    except Exception:

                        pass
        
    ############################################################
    # CARREGAR EMPRESAS DO BANCO
    ############################################################

    def carregar_empresas_banco(self):

        db = get_session()

        try:

            empresas = (
                db.query(Company)
                .all()
            )

            configuracoes = {}

            for empresa in empresas:

                cnpj = "".join(
                    caractere
                    for caractere in str(
                        empresa.cnpj
                    )
                    if caractere.isdigit()
                )

                if len(cnpj) != 14:
                    continue

                certificado = (
                    db.query(Certificate)
                    .filter(
                        Certificate.company_id
                        == empresa.id,
                        Certificate.ativo
                        == "S",
                    )
                    .first()
                )

                if certificado is None:

                    print(
                        f"[24H] {cnpj}: "
                        "nenhum certificado ativo."
                    )

                    continue

                if not certificado.arquivo:

                    print(
                        f"[24H] {cnpj}: "
                        "certificado sem caminho."
                    )

                    continue

                if not certificado.senha:

                    print(
                        f"[24H] {cnpj}: "
                        "certificado sem senha."
                    )

                    continue

                ambiente = getattr(
                    empresa,
                    "ambiente",
                    "producao",
                )

                if not ambiente:
                    ambiente = "producao"

                configuracoes[cnpj] = {
                    "cnpj": cnpj,
                    "certificado_path": (
                        certificado.arquivo
                    ),
                    "senha": (
                        certificado.senha
                    ),
                    "ambiente": ambiente,
                    "uf": "CE",
                }

            self.empresas = (
                configuracoes
            )

            return len(
                configuracoes
            )

        finally:

            db.close()

    ############################################################
    # UM CICLO
    ############################################################

    def executar_ciclo(self):

        ########################################################
        # RECARREGA EMPRESAS DO BANCO
        ########################################################

        quantidade = (
            self.carregar_empresas_banco()
        )

        if quantidade == 0:

            print(
                "[24H] Nenhuma empresa com "
                "certificado ativo encontrada."
            )

            return

        print(
            "[24H] Empresas carregadas:",
            quantidade,
        )

        print(
            "[24H] Verificação:",
            datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            ),
        )

        ########################################################
        # CONFIGURAÇÕES A PROCESSAR
        ########################################################

        configuracoes = list(
            self.empresas.values()
        )

        ########################################################
        # PROCESSAMENTO SIMULTÂNEO
        ########################################################

        with ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:

            futuros = {}

            for configuracao in configuracoes:

                if self._parar.is_set():
                    break

                futuro = executor.submit(
                    self.sincronizar_empresa,
                    configuracao,
                )

                futuros[futuro] = (
                    configuracao["cnpj"]
                )

            ####################################################
            # RESULTADO DAS THREADS
            ####################################################

            for futuro in as_completed(
                futuros
            ):

                cnpj = futuros[
                    futuro
                ]

                try:

                    futuro.result()

                    print(
                        f"[24H] {cnpj}: "
                        "processamento concluído."
                    )

                except Exception as erro:

                    self.logger.exception(
                        "Erro no processamento do CNPJ %s",
                        cnpj,
                    )

                    print(
                        f"[24H] ERRO {cnpj}: "
                        f"{erro}"
                    )

    ############################################################
    # LOOP
    ############################################################

    def _loop(self):

        print(
            "[24H] Serviço SEFAZ iniciado."
        )

        while not self._parar.is_set():

            try:

                self.executar_ciclo()

            except Exception:

                self.logger.exception(
                    "Erro no ciclo do serviço SEFAZ."
                )

            self._parar.wait(
                self.intervalo_verificacao
            )

        print(
            "[24H] Serviço SEFAZ encerrado."
        )

    ############################################################
    # INICIAR
    ############################################################

        self.config = UserSettings.carregar()

        if not self.config.get(
            "sefaz_24h",
            True,
        ):

            print(
                "[24H] Serviço automático desativado "
                "nas Configurações."
            )

            return

        self.intervalo_verificacao = max(
            30,
            int(
                self.config.get(
                    "intervalo_verificacao",
                    60,
                )
            ),
        )

        self.max_workers = max(
            1,
            int(
                self.config.get(
                    "max_workers",
                    4,
                )
            ),
        )

    def iniciar(self):

        if (
            self._thread is not None
            and self._thread.is_alive()
        ):

            return

        self._parar.clear()

        self._thread = threading.Thread(
            target=self._loop,
            name="SefazBackgroundService",
            daemon=True,
        )

        self._thread.start()

    ############################################################
    # PARAR
    ############################################################

    def parar(self):

        self._parar.set()

        if self._thread is not None:

            self._thread.join(
                timeout=5
            )

        self._thread = None

    ############################################################
    # STATUS
    ############################################################

    @property
    def ativo(self):

        return (
            self._thread is not None
            and self._thread.is_alive()
        )
