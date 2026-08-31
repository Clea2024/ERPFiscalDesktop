from app.core.exceptions import ERPException, SefazException

try:
    raise ERPException("ERP funcionando")
except ERPException as e:
    print(e)

try:
    raise SefazException("SEFAZ funcionando")
except SefazException as e:
    print(e)