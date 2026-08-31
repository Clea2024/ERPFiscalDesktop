import base64
import gzip


class XMLDecoder:

    ############################################################

    @staticmethod
    def decode(doc_zip):

        """
        Recebe um docZip da SEFAZ
        e devolve o XML descompactado.
        """

        dados = base64.b64decode(doc_zip)

        xml = gzip.decompress(dados)

        return xml.decode("utf-8")

    ############################################################

    @staticmethod
    def decode_bytes(doc_zip):

        dados = base64.b64decode(doc_zip)

        return gzip.decompress(dados)

    ############################################################

    @staticmethod
    def encode(xml):

        if isinstance(xml, str):

            xml = xml.encode("utf-8")

        comprimido = gzip.compress(xml)

        return base64.b64encode(
            comprimido
        ).decode("utf-8")