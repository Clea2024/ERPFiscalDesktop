from app.sefaz.sefaz_cliente import SefazClient

client = SefazClient(
    certificado_path=r"C:\Users\clea-\ERPFiscalDesktop\certificates\COMERCIAL REIS LTDA_PJ 2026.pfx",
    senha="123456",
)

print("Conectado antes:", client.conectado)

client.conectar()

print("Conectado depois:", client.conectado)

endpoint = client.conectar_wsdl()

print("Endpoint:", endpoint)