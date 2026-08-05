class AIException(Exception):
    pass



class ProviderError(AIException):
    pass



class ExtractionError(AIException):
    pass



class CacheError(AIException):
    pass