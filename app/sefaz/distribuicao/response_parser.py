from base64 import b64decode
from gzip import decompress
from xml.etree import ElementTree as ET


class ResponseParser:

    NS = {
        "nfe": "http://www.portalfiscal.inf.br/nfe"
    }

    def __init__(self, xml: str):

        self.root = ET.fromstring(xml)

    ############################################################

    def cstat(self):

        node = self.root.find(".//nfe:cStat", self.NS)

        if node is None:
            return None

        return node.text

    ############################################################

    def motivo(self):

        node = self.root.find(".//nfe:xMotivo", self.NS)

        if node is None:
            return ""

        return node.text

    ############################################################

    def ult_nsu(self):

        node = self.root.find(".//nfe:ultNSU", self.NS)

        if node is None:
            return None

        return node.text

    ############################################################

    def max_nsu(self):

        node = self.root.find(".//nfe:maxNSU", self.NS)

        if node is None:
            return None

        return node.text

    ############################################################

    def documentos(self):

        docs = []

        for doc in self.root.findall(".//nfe:docZip", self.NS):

            nsu = doc.attrib.get("NSU")

            schema = doc.attrib.get("schema")

            conteudo = decompress(
                b64decode(doc.text)
            )

            docs.append(
                {
                    "nsu": nsu,
                    "schema": schema,
                    "xml": conteudo.decode("utf-8"),
                }
            )

        return docs