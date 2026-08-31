import base64
import gzip
import re

from pathlib import Path


CTE_NAMESPACE = {
    "cte": "http://www.portalfiscal.inf.br/cte"
}


class CTeSyncManager:

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
                / "cte"
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
    # LER ELEMENTO
    ############################################################

    @staticmethod
    def texto_elemento(
        resposta,
        nome,
        padrao="",
    ):

        elemento = resposta.find(
            f"cte:{nome}",
            namespaces=CTE_NAMESPACE,
        )

        if elemento is None:
            return padrao

        return (
            elemento.text
            or padrao
        )

    ############################################################
    # SALVAR DOCZIP
    ############################################################

    def salvar_doczip(
        self,
        cnpj,
        doc_zip,
    ):

        if doc_zip.text is None:
            return None

        conteudo = (
            doc_zip.text
            .strip()
        )

        if not conteudo:
            return None

        ########################################################
        # BASE64
        ########################################################

        dados_compactados = (
            base64.b64decode(
                conteudo
            )
        )

        ########################################################
        # GZIP
        ########################################################

        xml_bytes = gzip.decompress(
            dados_compactados
        )

        ########################################################
        # NSU / SCHEMA
        ########################################################

        nsu = doc_zip.get(
            "NSU",
            "SEM_NSU",
        )

        schema = doc_zip.get(
            "schema",
            "documento_cte",
        )

        schema_seguro = re.sub(
            r"[^A-Za-z0-9_.-]",
            "_",
            schema,
        )

        ########################################################
        # IDENTIFICAR TIPO
        ########################################################

        schema_lower = (
            schema.lower()
        )

        if "proceventocte" in schema_lower:

            tipo = "eventos"

        elif "proccte" in schema_lower:

            tipo = "cte"

        elif "rescte" in schema_lower:

            tipo = "resumos"

        else:

            tipo = "outros"

        ########################################################
        # PASTA
        ########################################################

        pasta = (
            self.pasta_xml
            / cnpj
            / tipo
        )

        pasta.mkdir(
            parents=True,
            exist_ok=True,
        )

        ########################################################
        # NOME
        ########################################################

        nome = (
            f"{nsu}_{schema_seguro}"
        )

        if not nome.lower().endswith(
            ".xml"
        ):
            nome += ".xml"

        caminho = (
            pasta
            / nome
        )

        caminho.write_bytes(
            xml_bytes
        )

        return {
            "nsu": nsu,
            "schema": schema,
            "tipo": tipo,
            "caminho": str(caminho),
        }

    ############################################################
    # PROCESSAR DOCUMENTOS
    ############################################################

    def processar_documentos(
        self,
        resposta,
        cnpj,
    ):

        resultado = []

        documentos = resposta.findall(
            ".//cte:docZip",
            namespaces=CTE_NAMESPACE,
        )

        for doc_zip in documentos:

            try:

                arquivo = (
                    self.salvar_doczip(
                        cnpj,
                        doc_zip,
                    )
                )

                if arquivo is not None:

                    resultado.append(
                        arquivo
                    )

            except Exception as erro:

                print(
                    "[CT-e] Erro ao processar docZip:",
                    erro,
                )

        return resultado

    ############################################################
    # SINCRONIZAR UM LOTE
    ############################################################

    def sincronizar(
        self,
        cnpj,
        ultimo_nsu="000000000000000",
    ):

        cnpj = self.limpar_cnpj(
            cnpj
        )

        if len(cnpj) != 14:

            raise ValueError(
                "CNPJ deve possuir 14 dígitos."
            )

        ultimo_nsu = str(
            ultimo_nsu
        ).zfill(15)

        ########################################################
        # CONSULTA
        ########################################################

        resposta = (
            self.client
            .consultar_distribuicao(
                cnpj=cnpj,
                ultimo_nsu=ultimo_nsu,
            )
        )

        ########################################################
        # RETORNO
        ########################################################

        cstat = self.texto_elemento(
            resposta,
            "cStat",
        )

        motivo = self.texto_elemento(
            resposta,
            "xMotivo",
        )

        novo_ultimo_nsu = (
            self.texto_elemento(
                resposta,
                "ultNSU",
                ultimo_nsu,
            )
        )

        max_nsu = (
            self.texto_elemento(
                resposta,
                "maxNSU",
                novo_ultimo_nsu,
            )
        )

        novo_ultimo_nsu = str(
            novo_ultimo_nsu
        ).zfill(15)

        max_nsu = str(
            max_nsu
        ).zfill(15)

        ########################################################
        # DOCUMENTOS
        ########################################################

        arquivos = []

        if cstat == "138":

            arquivos = (
                self.processar_documentos(
                    resposta,
                    cnpj,
                )
            )

        ########################################################
        # CONTADORES
        ########################################################

        total_cte = sum(
            1
            for arquivo in arquivos
            if arquivo["tipo"] == "cte"
        )

        total_eventos = sum(
            1
            for arquivo in arquivos
            if arquivo["tipo"] == "eventos"
        )

        total_resumos = sum(
            1
            for arquivo in arquivos
            if arquivo["tipo"] == "resumos"
        )

        ########################################################
        # MAIS DOCUMENTOS?
        ########################################################

        continuar = False

        try:

            continuar = (
                int(novo_ultimo_nsu)
                < int(max_nsu)
            )

        except Exception:

            continuar = False

        ########################################################
        # EVITAR LOOP SEM AVANÇO
        ########################################################

        if novo_ultimo_nsu == ultimo_nsu:

            continuar = False

        return {
            "sucesso": cstat in (
                "137",
                "138",
            ),
            "cstat": cstat,
            "mensagem": motivo,
            "ultimo_nsu": novo_ultimo_nsu,
            "max_nsu": max_nsu,
            "continuar": continuar,
            "quantidade_xml": len(
                arquivos
            ),
            "quantidade_cte": total_cte,
            "quantidade_eventos": (
                total_eventos
            ),
            "quantidade_resumos": (
                total_resumos
            ),
            "arquivos": arquivos,
        }