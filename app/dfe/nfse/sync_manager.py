import base64
import gzip

from pathlib import Path

from app.dfe.nfse.import_service import (
    NFSeImportService,
)
from app.database.database import get_session
from app.repositories.dfe_sync_repository import (
    DFeSyncRepository,
)


class NFSeSyncManager:

    def __init__(
        self,
        client,
        pasta_xml=None,
    ):

        self.client = client

        if pasta_xml is None:

            base_dir = (
                Path(__file__)
                .resolve()
                .parents[3]
            )

            pasta_xml = (
                base_dir
                / "xml"
                / "nfse"
            )

        self.pasta_xml = Path(
            pasta_xml
        )

        self.pasta_xml.mkdir(
            parents=True,
            exist_ok=True,
        )

    ############################################################
    # LIMPAR CNPJ
    ############################################################

    @staticmethod
    def limpar_cnpj(
        cnpj,
    ):

        return "".join(
            caractere
            for caractere in str(cnpj)
            if caractere.isdigit()
        )

    ############################################################
    # DECODIFICAR XML
    ############################################################

    @staticmethod
    def decodificar_xml(
        arquivo_base64,
    ):

        dados_compactados = (
            base64.b64decode(
                arquivo_base64
            )
        )

        return gzip.decompress(
            dados_compactados
        )

    ############################################################
    # SALVAR DOCUMENTO
    ############################################################

    def salvar_documento(
        self,
        cnpj,
        documento,
    ):

        nsu = str(
            documento.get(
                "NSU",
                "",
            )
        )

        chave = str(
            documento.get(
                "ChaveAcesso",
                "",
            )
        )

        tipo = str(
            documento.get(
                "TipoDocumento",
                "NFSE",
            )
        ).upper()

        arquivo_base64 = (
            documento.get(
                "ArquivoXml"
            )
        )

        if not arquivo_base64:

            return None

        xml_bytes = (
            self.decodificar_xml(
                arquivo_base64
            )
        )

        pasta = (
            self.pasta_xml
            / cnpj
            / tipo
        )

        pasta.mkdir(
            parents=True,
            exist_ok=True,
        )

        nome = (
            f"{nsu}_{chave}.xml"
        )

        caminho = (
            pasta
            / nome
        )

        caminho.write_bytes(
            xml_bytes
        )

        return {
            "nsu": nsu,
            "chave": chave,
            "tipo": tipo,
            "caminho": str(caminho),
        }

    ############################################################
    # SINCRONIZAR UM LOTE
    ############################################################

    def sincronizar(
        self,
        cnpj,
    ):

        cnpj = self.limpar_cnpj(
            cnpj
        )

        if len(cnpj) != 14:

            raise ValueError(
                "CNPJ deve possuir 14 dígitos."
            )

        db = get_session()

        try:

            repository = (
                DFeSyncRepository(
                    db
                )
            )

            estado = (
                repository.obter_ou_criar(
                    cnpj=cnpj,
                    tipo="NFSE",
                )
            )

            ultimo_nsu = (
                estado.ultimo_nsu
                or "000000000000000"
            )

            ####################################################
            # API NFS-e
            ####################################################

            resposta = (
                self.client.consultar_nsu(
                    ultimo_nsu
                )
            )

            if not resposta.ok:

                return {
                    "sucesso": False,
                    "status_http": (
                        resposta.status_code
                    ),
                    "mensagem": (
                        resposta.text[:500]
                    ),
                    "arquivos": [],
                }

            dados = resposta.json()

            status = dados.get(
                "StatusProcessamento",
                "",
            )

            lote = dados.get(
                "LoteDFe",
                [],
            )

            ####################################################
            # SALVAR XMLs
            ####################################################

            arquivos = []

            maior_nsu = int(
                ultimo_nsu
                or "0"
            )

            for documento in lote:

                arquivo = (
                    self.salvar_documento(
                        cnpj,
                        documento,
                    )
                )

                if arquivo:

                    arquivos.append(
                        arquivo
                    )

                try:

                    nsu_documento = int(
                        documento.get(
                            "NSU",
                            0,
                        )
                    )

                    maior_nsu = max(
                        maior_nsu,
                        nsu_documento,
                    )

                except Exception:

                    pass
            ####################################################
            # IMPORTAR NFS-e PARA O BANCO
            ####################################################

            importador = NFSeImportService(
                db
            )

            resultado_importacao = (
                importador.importar_arquivos(
                    arquivos=arquivos,
                    cnpj_empresa=cnpj,
                )
            )
            ####################################################
            # ATUALIZAR NSU
            ####################################################

            novo_nsu = str(
                maior_nsu
            ).zfill(15)

            repository.atualizar(
                estado=estado,
                ultimo_nsu=novo_nsu,
                max_nsu=novo_nsu,
                cstat="200",
                motivo=status,
            )

            return {
                "sucesso": True,
                "status_http": (
                    resposta.status_code
                ),
                "status_processamento": (
                    status
                ),
                "ultimo_nsu": novo_nsu,
                "quantidade_xml": len(
                    arquivos
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
                "arquivos": arquivos,
            }

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()