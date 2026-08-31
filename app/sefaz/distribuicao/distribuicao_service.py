from xml.sax.saxutils import escape


def montar_envelope(self, xml_dist: bytes) -> str:

    xml = xml_dist.decode("utf-8")

    return f"""<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">

    <soap12:Body>

        <nfeDistDFeInteresse
            xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/NFeDistribuicaoDFe">

            <nfeDadosMsg>

                {xml}

            </nfeDadosMsg>

        </nfeDistDFeInteresse>

    </soap12:Body>

</soap12:Envelope>
"""


############################################################

def montar_requisicao(self, ult_nsu="000000000000000"):

    xml = self.montar_xml_dist_nsu(ult_nsu)

    return self.montar_envelope(xml)