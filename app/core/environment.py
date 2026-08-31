"""
Informações do ambiente de execução do ERP
"""

import platform
import sys
from pathlib import Path


class Environment:

    @staticmethod
    def info():

        return {
            "python": platform.python_version(),
            "sistema": platform.system(),
            "release": platform.release(),
            "arquitetura": platform.machine(),
            "executavel": sys.executable,
            "diretorio": str(Path.cwd()),
        }

    @staticmethod
    def mostrar():

        info = Environment.info()

        print("=" * 60)
        print("AMBIENTE DO ERP")
        print("=" * 60)

        for chave, valor in info.items():
            print(f"{chave:15}: {valor}")