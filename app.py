import sys
import traceback

from PySide6.QtWidgets import QApplication

from app.database.database import create_database
from app.services.background import SefazBackgroundService
from app.ui.login_dialog import LoginDialog
from app.ui.main_window import MainWindow


def main():

    servico_sefaz = None

    try:

        print("1 - Iniciando aplicação")

        app = QApplication(sys.argv)

        print("2 - QApplication criada")

        app.setApplicationName(
            "ERP Fiscal Desktop CE"
        )

        app.setOrganizationName(
            "AJ & CM Tecnologia"
        )

        ########################################################
        # BANCO
        ########################################################

        print("3 - Criando banco")

        create_database()

        print("4 - Banco criado")

        ########################################################
        # LOGIN
        ########################################################

        login = LoginDialog()

        print("5 - Login criado")

        resposta = login.exec()

        print(
            f"6 - Resultado do login: {resposta}"
        )

        if not resposta:

            print(
                "Login cancelado."
            )

            return

        ########################################################
        # SERVIÇO SEFAZ 24H
        ########################################################

        print(
            "7 - Iniciando serviço SEFAZ 24H"
        )

        servico_sefaz = (
            SefazBackgroundService(
                intervalo_verificacao=60
            )
        )

        servico_sefaz.iniciar()

        print(
            "8 - Serviço SEFAZ 24H iniciado"
        )

        ########################################################
        # ENCERRAMENTO SEGURO
        ########################################################

        app.aboutToQuit.connect(
            servico_sefaz.parar
        )

        ########################################################
        # JANELA PRINCIPAL
        ########################################################

        print(
            "9 - Abrindo MainWindow"
        )

        janela = MainWindow()

        ########################################################
        # DISPONIBILIZAR SERVIÇO PARA A INTERFACE
        ########################################################

        janela.sefaz_background_service = (
            servico_sefaz
        )

        print(
            "10 - MainWindow criada"
        )

        janela.show()

        ########################################################
        # QT
        ########################################################

        print(
            "11 - Entrando no loop Qt"
        )

        codigo_saida = app.exec()

        ########################################################
        # FINALIZAÇÃO
        ########################################################

        if (
            servico_sefaz is not None
            and servico_sefaz.ativo
        ):

            servico_sefaz.parar()

        sys.exit(
            codigo_saida
        )

    except Exception:

        traceback.print_exc()

        if (
            servico_sefaz is not None
            and servico_sefaz.ativo
        ):

            try:

                servico_sefaz.parar()

            except Exception:

                pass


if __name__ == "__main__":
    main()