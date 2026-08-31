from app.database.database import get_session
from app.models.user import User
from app.services.password_service import PasswordService

db = get_session()

admin = db.query(User).filter(User.login == "admin").first()

if admin is None:

    admin = User(
        nome="Administrador",
        login="admin",
        senha=PasswordService.gerar_hash("admin"),
        email="admin@erpfiscal.com",
        administrador=True,
        ativo=True,
    )

    db.add(admin)

    print("Administrador criado.")

else:

    admin.senha = PasswordService.gerar_hash("admin")

    print("Senha do administrador atualizada.")

db.commit()

print("Migração concluída.")