import logging

from app.database.database import get_session
from app.dfe.provider import DFeProvider
from app.dfe.cte import CTeClient, CTeSyncManager
from app.dfe.cte.import_service import CTeImportService
from app.models.company import Company
from app.repositories.dfe_sync_repository import DFeSyncRepository


class CTeProvider(DFeProvider):

    def __init__(
        self,
        certificado_path: str,
        senha: str,
        ambiente: str = "producao",
        uf: str = "CE",
    ):

        self.certificado_path = certificado_path
        self.senha = senha
        self.ambiente = ambiente
        self.uf = uf.upper()

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        self.client = None
        self.manager = None

    ############################################################
    # NOME
    ############################################################

    @property
    def nome(self):

        return "CT-e / CT-e OS"

    ############################################################
    # CONECTAR
    ############################################################

    def conectar(self):

        self.client = CTeClient(
            certificado_path=self.certificado_path,
            senha=self.senha,
            ambiente=self.ambiente,
            uf=self.uf,
        )

        self.client.conectar()

        self.client.carregar_wsdl()

        self.manager = CTeSyncManager(
            self.client
        )

        return True

    ############################################################
    # SINCRONIZAR
    ############################################################

    def sincronizar(
        self,
        cnpj: str,
    ):

        if self.client is None:
            self.conectar()

        if self.manager is None:
            raise RuntimeError(
                "CTeSyncManager não inicializado."
            )

        db = get_session()

        try:

            ####################################################
            # REPOSITÓRIO DE CONTROLE DO NSU
            ####################################################

            repository = DFeSyncRepository(
                db
            )

            ####################################################
            # EMPRESA
            ####################################################

            empresa = (
                db.query(Company)
                .filter(
                    Company.cnpj == cnpj
                )
                .first()
            )

            empresa_id = None

            if empresa is not None:
                empresa_id = empresa.id

            ####################################################
            # ESTADO CT-e
            ####################################################

            estado = repository.obter_ou_criar(
                cnpj=cnpj,
                tipo="CTE",
            )

            print(
                "[CT-e] Último NSU salvo:",
                estado.ultimo_nsu,
            )

            ####################################################
            # CONTADORES
            ####################################################

            total_arquivos = []

            total_cte = 0
            total_eventos = 0
            total_resumos = 0

            ultimo_resultado = None
            lotes_processados = 0

            ####################################################
            # PROCESSAR LOTES
            ####################################################

            for numero_lote in range(
                1,
                21,
            ):

                lotes_processados = (
                    numero_lote
                )

                nsu_anterior = (
                    estado.ultimo_nsu
                )

                print(
                    "[CT-e] Processando lote:",
                    numero_lote,
                )

                print(
                    "[CT-e] Consultando a partir do NSU:",
                    nsu_anterior,
                )

                resultado = (
                    self.manager.sincronizar(
                        cnpj=cnpj,
                        ultimo_nsu=nsu_anterior,
                    )
                )

                ultimo_resultado = resultado

                ################################################
                # ATUALIZAR NSU
                ################################################

                repository.atualizar(
                    estado=estado,
                    ultimo_nsu=resultado.get(
                        "ultimo_nsu"
                    ),
                    max_nsu=resultado.get(
                        "max_nsu"
                    ),
                    cstat=resultado.get(
                        "cstat"
                    ),
                    motivo=resultado.get(
                        "mensagem"
                    ),
                )

                ################################################
                # DOCUMENTOS DO LOTE
                ################################################

                arquivos_lote = (
                    resultado.get(
                        "arquivos",
                        [],
                    )
                )

                total_arquivos.extend(
                    arquivos_lote
                )

                total_cte += resultado.get(
                    "quantidade_cte",
                    0,
                )

                total_eventos += resultado.get(
                    "quantidade_eventos",
                    0,
                )

                total_resumos += resultado.get(
                    "quantidade_resumos",
                    0,
                )

                print(
                    "[CT-e] NSU:",
                    estado.ultimo_nsu,
                    "/",
                    estado.max_nsu,
                )

                print(
                    "[CT-e] Documentos no lote:",
                    len(arquivos_lote),
                )

                ################################################
                # PROTEÇÃO CONTRA LOOP
                ################################################

                if (
                    estado.ultimo_nsu
                    == nsu_anterior
                ):

                    print(
                        "[CT-e] NSU não avançou."
                    )

                    break

                ################################################
                # CHEGOU AO MAX NSU
                ################################################

                try:

                    if (
                        int(estado.ultimo_nsu)
                        >= int(estado.max_nsu)
                    ):

                        print(
                            "[CT-e] Sincronização atualizada."
                        )

                        break

                except (
                    TypeError,
                    ValueError,
                ):

                    pass

                ################################################
                # SERVIÇO INDICOU PARADA
                ################################################

                if not resultado.get(
                    "continuar",
                    False,
                ):

                    break

            ####################################################
            # NENHUM RESULTADO
            ####################################################

            if ultimo_resultado is None:

                return {
                    "sucesso": False,
                    "mensagem": (
                        "Nenhum lote CT-e processado."
                    ),
                    "quantidade_xml": 0,
                    "documentos_importados": 0,
                    "documentos_duplicados": 0,
                    "documentos_ignorados": 0,
                    "arquivos": [],
                }

            ####################################################
            # IMPORTAR CT-e PARA O BANCO
            ####################################################

            importador = CTeImportService(
                db
            )

            resultado_importacao = (
                importador.importar_arquivos(
                    arquivos=total_arquivos,
                    empresa_id=empresa_id,
                )
            )

            print(
                "[CT-e] Importados:",
                resultado_importacao[
                    "importados"
                ],
            )

            print(
                "[CT-e] Duplicados:",
                resultado_importacao[
                    "duplicados"
                ],
            )

            print(
                "[CT-e] Ignorados:",
                resultado_importacao[
                    "ignorados"
                ],
            )

            ####################################################
            # RESULTADO FINAL
            ####################################################

            return {
                "sucesso": ultimo_resultado.get(
                    "sucesso",
                    False,
                ),
                "cstat": ultimo_resultado.get(
                    "cstat",
                    "",
                ),
                "mensagem": ultimo_resultado.get(
                    "mensagem",
                    "",
                ),
                "ultimo_nsu": estado.ultimo_nsu,
                "max_nsu": estado.max_nsu,
                "quantidade_xml": len(
                    total_arquivos
                ),
                "quantidade_cte": total_cte,
                "quantidade_eventos": (
                    total_eventos
                ),
                "quantidade_resumos": (
                    total_resumos
                ),
                "documentos_importados": (
                    resultado_importacao[
                        "importados"
                    ]
                ),
                "documentos_duplicados": (
                    resultado_importacao[
                        "duplicados"
                    ]
                ),
                "documentos_ignorados": (
                    resultado_importacao[
                        "ignorados"
                    ]
                ),
                "lotes_processados": (
                    lotes_processados
                ),
                "arquivos": total_arquivos,
            }

        except Exception:

            db.rollback()

            raise

        finally:

            db.close()

    ############################################################
    # DESCONECTAR
    ############################################################

    def desconectar(self):

        if self.client is not None:

            try:

                self.client.desconectar()

            finally:

                self.client = None
                self.manager = None