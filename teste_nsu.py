from app.sefaz.distribuicao.nsu_service import NSUService

nsu = NSUService(
    "app/sefaz/cache/ultimo_nsu.json"
)

print("Atual:", nsu.obter())

nsu.atualizar(
    "000000000001234"
)

print("Novo:", nsu.obter())