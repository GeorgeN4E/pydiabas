from .ediabas import EDIABAS
from .exceptions import JobFailedError
from .statics import API_RESULT_FORMAT

def getResult(ediabas : EDIABAS, name : str, set : int = 1) -> str | bytes | int | float:
    try:
        match ediabas.resultFormat(name, set):
            case API_RESULT_FORMAT.BINARY:
                return ediabas.resultBinary(name, set)

            case API_RESULT_FORMAT.BYTE:
                return ediabas.resultByte(name, set)
            
            case API_RESULT_FORMAT.CHAR:
                return ediabas.resultChar(name, set)
            
            case API_RESULT_FORMAT.DWORD:
                return ediabas.resultDWord(name, set)
            
            case API_RESULT_FORMAT.INTEGER:
                return ediabas.resultInt(name, set)

            case API_RESULT_FORMAT.LONG:
                return ediabas.resultLong(name, set)
            
            case API_RESULT_FORMAT.REAL:
                return ediabas.resultReal(name, set)

            case API_RESULT_FORMAT.TEXT:
                return ediabas.resultText(name, set)
            
            case API_RESULT_FORMAT.WORD:
                return ediabas.resultWord(name, set)
            
    except JobFailedError:
        return None
