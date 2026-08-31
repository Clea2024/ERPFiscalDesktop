from app.utils.cnpj_validator import validar_cnpj


class CompanyService:

    def validar(self, dados):

        if dados["razao_social"].strip() == "":
            return False, "Informe a Razão Social."

        if dados["cnpj"].strip() == "":
            return False, "Informe o CNPJ."

        if not validar_cnpj(dados["cnpj"]):
            return False, "CNPJ inválido."

        return True, ""