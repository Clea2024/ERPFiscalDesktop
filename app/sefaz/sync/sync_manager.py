import base64
import gzip
import re

from datetime import datetime
from datetime import timedelta
from pathlib import Path

from app.database.database import get_session
from app.models.sefaz_sync_state import SefazSyncState
from app.services.sefaz_xml_import_service import SefazXmlImportService

NAMESPACE_NFE = {
    "nfe": "http://www.portalfiscal.inf.br/nfe"
}


class SefazSyncManager:

    def __init__(
        self,
        client,
        pasta_xml: str | None = None,
    ):

        self.client = client

        if pasta_xml is None:
            base_dir = Path(__file__).resolve().parents[3]
            pasta_xml = base_dir / "xml"

        self.pasta_xml = Path(pasta_xml)

        self.pasta_xml.mkdir(
            parents=True,
            exist_ok=True,
        )

    ############################################################

    @staticmethod
    def limpar_cnpj(cnpj: str) -> str:

        return "".join(
            caractere
            for caractere in cnpj
            if caractere.isdigit()
        )

    ############################################################

    def obter_estado(
        self,
        db,
        cnpj: str,
    ):

        cnpj = self.limpar_cnpj(cnpj)

        estado = (
            db.query(SefazSyncState)
            .filter(
                SefazSyncState.cnpj == cnpj
            )
            .first()
        )

        if estado is None:

            estado = SefazSyncState(
                cnpj=cnpj,
                ultimo_nsu="000000000000000",
                max_nsu="000000000000000",
            )

            db.add(estado)
            db.commit()
            db.refresh(estado)

        return estado

    ############################################################

    def pode_consultar(
        self,
        estado,
    ) -> tuple[bool, str]:

        agora = datetime.now()

        if (
            estado.bloqueado_ate is not None
            and agora < estado.bloqueado_ate
        ):

            restante = (
                estado.bloqueado_ate - agora
            )

            minutos = int(
                restante.total_seconds() / 60
            ) + 1

            return (
                False,
                (
                    "SEFAZ temporariamente bloqueada. "
                    f"Nova tentativa em aproximadamente "
                    f"{minutos} minuto(s)."
                ),
            )

        return True, "Consulta permitida."

    ############################################################

    @staticmethod
    def texto_elemento(
        resposta,
        nome: str,
        padrao: str = "",
    ) -> str:

        elemento = resposta.find(
            f"nfe:{nome}",
            namespaces=NAMESPACE_NFE,
        )

        if elemento is None:
            return padrao

        return elemento.text or padrao

    ############################################################

    def salvar_doczip(
        self,
        cnpj: str,
        doc_zip,
    ) -> str | None:

        if doc_zip.text is None:
            return None

        conteudo_base64 = (
            doc_zip.text.strip()
        )

        if not conteudo_base64:
            return None

        dados_compactados = base64.b64decode(
            conteudo_base64
        )

        xml_bytes = gzip.decompress(
            dados_compactados
        )

        nsu = doc_zip.get(
            "NSU",
            "SEM_NSU",
        )

        schema = doc_zip.get(
            "schema",
            "documento.xml",
        )

        schema_seguro = re.sub(
            r"[^A-Za-z0-9_.-]",
            "_",
            schema,
        )

        pasta_cnpj = (
            self.pasta_xml
            / cnpj
        )

        pasta_cnpj.mkdir(
            parents=True,
            exist_ok=True,
        )

        nome_arquivo = (
            f"{nsu}_{schema_seguro}"
        )

        if not nome_arquivo.lower().endswith(
            ".xml"
        ):
            nome_arquivo += ".xml"

        caminho = (
            pasta_cnpj
            / nome_arquivo
        )

        caminho.write_bytes(
            xml_bytes
        )

        return str(caminho)

    ############################################################

    def processar_documentos(
        self,
        resposta,
        cnpj: str,
    ) -> list[str]:

        arquivos = []

        documentos = resposta.findall(
            ".//nfe:docZip",
            namespaces=NAMESPACE_NFE,
        )

        for documento in documentos:

            try:

                caminho = self.salvar_doczip(
                    cnpj,
                    documento,
                )

                if caminho:
                    arquivos.append(caminho)

            except Exception as erro:

                print(
                    "[SEFAZ] Erro ao processar docZip:",
                    erro,
                )

        return arquivos

    ############################################################

    def sincronizar(
        self,
        cnpj: str,
    ) -> dict:

        cnpj = self.limpar_cnpj(
            cnpj
        )

        if len(cnpj) != 14:
            raise ValueError(
                "CNPJ deve possuir 14 dígitos."
            )

        db = get_session()

        try:

            estado = self.obter_estado(
                db,
                cnpj,
            )

            permitido, mensagem = (
                self.pode_consultar(
                    estado
                )
            )

            if not permitido:

                return {
                    "sucesso": False,
                    "bloqueado": True,
                    "mensagem": mensagem,
                    "ultimo_nsu": estado.ultimo_nsu,
                    "max_nsu": estado.max_nsu,
                    "arquivos": [],
                }

            print(
                "[SEFAZ] CNPJ:",
                cnpj,
            )

            print(
                "[SEFAZ] Consultando a partir do NSU:",
                estado.ultimo_nsu,
            )

            resposta = (
                self.client
                .consultar_distribuicao(
                    cnpj=cnpj,
                    ultimo_nsu=estado.ultimo_nsu,
                )
            )

            agora = datetime.now()

            cstat = self.texto_elemento(
                resposta,
                "cStat",
            )

            motivo = self.texto_elemento(
                resposta,
                "xMotivo",
            )

            ultimo_nsu = self.texto_elemento(
                resposta,
                "ultNSU",
                estado.ultimo_nsu,
            )

            max_nsu = self.texto_elemento(
                resposta,
                "maxNSU",
                estado.max_nsu,
            )

            estado.ultima_consulta = agora
            estado.ultimo_cstat = cstat
            estado.ultimo_motivo = motivo

            ####################################################
            # MUITO IMPORTANTE:
            # Sempre preservamos o ultNSU retornado.
            ####################################################

            if ultimo_nsu:
                estado.ultimo_nsu = (
                    ultimo_nsu.zfill(15)
                )

            if max_nsu:
                estado.max_nsu = (
                    max_nsu.zfill(15)
                )

            ####################################################
            # CONSUMO INDEVIDO
            ####################################################

            if cstat == "656":

                estado.bloqueado_ate = (
                    agora
                    + timedelta(hours=1)
                )

                db.commit()

                return {
                    "sucesso": False,
                    "bloqueado": True,
                    "cstat": cstat,
                    "mensagem": motivo,
                    "ultimo_nsu": estado.ultimo_nsu,
                    "max_nsu": estado.max_nsu,
                    "bloqueado_ate": (
                        estado.bloqueado_ate
                    ),
                    "arquivos": [],
                }

            ####################################################
            # SEM DOCUMENTOS / DOCUMENTOS LOCALIZADOS
            ####################################################

            estado.bloqueado_ate = None

            arquivos = self.processar_documentos(
                resposta,
                cnpj,
            )

            ####################################################
            # IMPORTAR XMLs PARA O BANCO
            ####################################################

            importador = SefazXmlImportService(
                db
            )

            resultado_importacao = (
                importador.importar_arquivos(
                    arquivos=arquivos,
                    cnpj_empresa=cnpj,
                )
            )

            db.commit()

            return {
                "sucesso": True,
                "bloqueado": False,
                "cstat": cstat,
                "mensagem": motivo,
                "ultimo_nsu": estado.ultimo_nsu,
                "max_nsu": estado.max_nsu,
                "quantidade_xml": len(arquivos),
                "documentos_importados": (
                    resultado_importacao[
                        "importados"
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