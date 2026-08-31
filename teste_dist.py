from app.sefaz.distribuicao.distribuicao_service import DistribuicaoService

service = DistribuicaoService(
    ambiente="producao",
    cnpj="02387772000153",
    uf_autor=23,
)

soap = service.montar_requisicao()

print(soap)