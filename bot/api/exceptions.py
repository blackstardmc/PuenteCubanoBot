class ApiError(Exception):
    """Error general comunicándose con la API."""


class ApiConnectionError(ApiError):
    """No se pudo conectar con la API."""


class ApiTimeoutError(ApiError):
    """La API tardó demasiado en responder."""


class ApiResponseError(ApiError):
    """La API respondió con un código HTTP incorrecto."""