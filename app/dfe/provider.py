from abc import ABC
from abc import abstractmethod


class DFeProvider(ABC):

    @property
    @abstractmethod
    def nome(self):
        pass

    @abstractmethod
    def conectar(self):
        pass

    @abstractmethod
    def sincronizar(
        self,
        cnpj: str,
    ):
        pass

    @abstractmethod
    def desconectar(self):
        pass