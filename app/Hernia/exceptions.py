# ==================== EXCEPCIONES PERSONALIZADAS ====================
"""
Módulo de excepciones personalizadas de la aplicación.
"""


class HerniaAppException(Exception):
    """Excepción base de la aplicación."""
    
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)


# ==================== EXCEPCIONES DE IMAGEN ====================
class ImageException(HerniaAppException):
    """Excepción base para errores de imagen."""
    pass


class InvalidImageFormat(ImageException):
    """Formato de imagen no válido."""
    
    def __init__(self, allowed_formats: list = None):
        message = "Formato de imagen no permitido"
        if allowed_formats:
            message += f". Formatos permitidos: {', '.join(allowed_formats)}"
        super().__init__(message, code='INVALID_IMAGE_FORMAT')


class ImageTooLarge(ImageException):
    """Imagen demasiado grande."""
    
    def __init__(self, max_size_mb: int):
        message = f"Archivo demasiado grande (máximo {max_size_mb}MB)"
        super().__init__(message, code='IMAGE_TOO_LARGE')


class ImageTooSmall(ImageException):
    """Imagen demasiado pequeña."""
    
    def __init__(self, min_dimension: int):
        message = f"Imagen demasiado pequeña (mínimo {min_dimension}px)"
        super().__init__(message, code='IMAGE_TOO_SMALL')


class InvalidImageDimensions(ImageException):
    """Dimensiones de imagen no válidas."""
    
    def __init__(self, min_dim: int, max_dim: int):
        message = f"Dimensiones inválidas ({min_dim}-{max_dim}px)"
        super().__init__(message, code='INVALID_IMAGE_DIMENSIONS')


class ImageProcessingError(ImageException):
    """Error al procesar imagen."""
    
    def __init__(self, details: str = ""):
        message = "Error al procesar la imagen"
        if details:
            message += f": {details}"
        super().__init__(message, code='IMAGE_PROCESSING_ERROR')


class ImageDownloadError(ImageException):
    """Error al descargar imagen."""
    
    def __init__(self, url: str):
        message = f"Error al descargar imagen desde {url}"
        super().__init__(message, code='IMAGE_DOWNLOAD_ERROR')


# ==================== EXCEPCIONES DE AUTENTICACIÓN ====================
class AuthenticationException(HerniaAppException):
    """Excepción base para errores de autenticación."""
    pass


class InvalidCredentials(AuthenticationException):
    """Credenciales inválidas."""
    
    def __init__(self):
        super().__init__(
            "Correo electrónico o contraseña incorrectos.",
            code='INVALID_CREDENTIALS'
        )


class UserNotFound(AuthenticationException):
    """Usuario no encontrado."""
    
    def __init__(self, email: str = ""):
        message = "Usuario no encontrado"
        if email:
            message += f": {email}"
        super().__init__(message, code='USER_NOT_FOUND')


class EmailNotRegistered(AuthenticationException):
    """Email no registrado."""
    
    def __init__(self, email: str):
        message = f"El correo electrónico {email} no está registrado"
        super().__init__(message, code='EMAIL_NOT_REGISTERED')


class RegistrationError(AuthenticationException):
    """Error al registrar usuario."""
    
    def __init__(self, details: str = ""):
        message = "Error al registrar el usuario"
        if details:
            message += f": {details}"
        super().__init__(message, code='REGISTRATION_ERROR')


# ==================== EXCEPCIONES DE HISTORIAL ====================
class HistorialException(HerniaAppException):
    """Excepción base para errores de historial."""
    pass


class HistorialNotFound(HistorialException):
    """Historial no encontrado."""
    
    def __init__(self, historial_id: int):
        message = f"Historial no encontrado: ID {historial_id}"
        super().__init__(message, code='HISTORIAL_NOT_FOUND')


class HistorialCreationError(HistorialException):
    """Error al crear historial."""
    
    def __init__(self, details: str = ""):
        message = "Error al crear el historial"
        if details:
            message += f": {details}"
        super().__init__(message, code='HISTORIAL_CREATION_ERROR')


class HistorialDeletionError(HistorialException):
    """Error al eliminar historial."""
    
    def __init__(self, details: str = ""):
        message = "Error al eliminar el historial"
        if details:
            message += f": {details}"
        super().__init__(message, code='HISTORIAL_DELETION_ERROR')


# ==================== EXCEPCIONES DE INFERENCIA ====================
class InferenceException(HerniaAppException):
    """Excepción base para errores de inferencia."""
    pass


class InferenceError(InferenceException):
    """Error en la inferencia del modelo."""
    
    def __init__(self, details: str = ""):
        message = "Error al procesar la imagen con el modelo"
        if details:
            message += f": {details}"
        super().__init__(message, code='INFERENCE_ERROR')


class ModelNotAvailable(InferenceException):
    """Modelo no disponible."""
    
    def __init__(self):
        super().__init__(
            "El modelo de inferencia no está disponible",
            code='MODEL_NOT_AVAILABLE'
        )


class APIKeyMissing(InferenceException):
    """API Key no configurada."""
    
    def __init__(self):
        super().__init__(
            "API Key de Roboflow no está configurada",
            code='API_KEY_MISSING'
        )


# ==================== EXCEPCIONES DE PDF ====================
class PDFException(HerniaAppException):
    """Excepción base para errores de PDF."""
    pass


class PDFGenerationError(PDFException):
    """Error al generar PDF."""
    
    def __init__(self, details: str = ""):
        message = "Error al generar el PDF"
        if details:
            message += f": {details}"
        super().__init__(message, code='PDF_GENERATION_ERROR')


# ==================== EXCEPCIONES DE PERMISOS ====================
class PermissionException(HerniaAppException):
    """Excepción base para errores de permisos."""
    pass


class PermissionDenied(PermissionException):
    """Permiso denegado."""
    
    def __init__(self, resource: str = ""):
        message = "No tienes permiso para acceder a este recurso"
        if resource:
            message += f": {resource}"
        super().__init__(message, code='PERMISSION_DENIED')


class SuperuserRequired(PermissionException):
    """Se requiere ser superusuario."""
    
    def __init__(self):
        super().__init__(
            "Se requiere ser administrador para acceder a este recurso",
            code='SUPERUSER_REQUIRED'
        )


# ==================== EXCEPCIONES DE BASE DE DATOS ====================
class DatabaseException(HerniaAppException):
    """Excepción base para errores de base de datos."""
    pass


class TransactionError(DatabaseException):
    """Error en transacción."""
    
    def __init__(self, details: str = ""):
        message = "Error en la transacción de base de datos"
        if details:
            message += f": {details}"
        super().__init__(message, code='TRANSACTION_ERROR')


class DataIntegrityError(DatabaseException):
    """Error de integridad de datos."""
    
    def __init__(self, details: str = ""):
        message = "Error de integridad de datos"
        if details:
            message += f": {details}"
        super().__init__(message, code='DATA_INTEGRITY_ERROR')


# ==================== EXCEPCIONES DE VALIDACIÓN ====================
class ValidationException(HerniaAppException):
    """Excepción base para errores de validación."""
    pass


class InvalidInput(ValidationException):
    """Entrada no válida."""
    
    def __init__(self, field: str, details: str = ""):
        message = f"Campo inválido: {field}"
        if details:
            message += f" ({details})"
        super().__init__(message, code='INVALID_INPUT')


class MissingRequiredField(ValidationException):
    """Campo requerido faltante."""
    
    def __init__(self, field: str):
        message = f"Campo requerido faltante: {field}"
        super().__init__(message, code='MISSING_REQUIRED_FIELD')
