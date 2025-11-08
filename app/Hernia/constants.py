# ==================== CONSTANTES ====================
"""
Módulo de constantes de la aplicación.
"""

# ==================== DIAGNÓSTICOS ====================
DIAGNOSTICO_SIN_HERNIA = "Sin Hernia"
DIAGNOSTICO_HERNIA = "Hernia"

DIAGNOSTICOS = [
    (DIAGNOSTICO_SIN_HERNIA, "Sin Hernia"),
    (DIAGNOSTICO_HERNIA, "Hernia"),
]

# ==================== MENSAJES ====================
MESSAGES = {
    'LOGIN_SUCCESS': 'Sesión iniciada correctamente.',
    'LOGIN_ERROR': 'Correo electrónico o contraseña incorrectos.',
    'REGISTER_SUCCESS': '¡Registro exitoso! Has iniciado sesión automáticamente.',
    'REGISTER_ERROR': 'Error al registrar el usuario.',
    'LOGOUT_SUCCESS': 'Sesión cerrada correctamente.',
    'PROFILE_UPDATE_SUCCESS': 'Perfil actualizado exitosamente.',
    'PROFILE_UPDATE_ERROR': 'Error al actualizar el perfil.',
    'IMAGE_UPLOAD_SUCCESS': 'Imagen procesada exitosamente.',
    'IMAGE_UPLOAD_ERROR': 'Error al procesar la imagen.',
    'IMAGE_VALIDATION_ERROR': 'La imagen no es válida.',
    'HISTORIAL_DELETE_SUCCESS': 'El registro ha sido eliminado correctamente.',
    'HISTORIAL_DELETE_ERROR': 'Error al eliminar el registro.',
    'PDF_GENERATION_SUCCESS': 'PDF generado correctamente.',
    'PDF_GENERATION_ERROR': 'Error al generar el PDF.',
    'PERMISSION_DENIED': 'No tienes permiso para realizar esta acción.',
    'NOT_FOUND': 'El recurso solicitado no fue encontrado.',
    'SERVER_ERROR': 'Error del servidor. Por favor, intenta nuevamente.',
}

# ==================== ERRORES ====================
ERROR_MESSAGES = {
    'INVALID_EMAIL': 'El formato del email no es válido.',
    'INVALID_PHONE': 'El formato del teléfono no es válido.',
    'INVALID_IMAGE_FORMAT': 'Formato de archivo no permitido.',
    'IMAGE_TOO_LARGE': 'Archivo demasiado grande.',
    'IMAGE_TOO_SMALL': 'Imagen demasiado pequeña.',
    'IMAGE_INVALID': 'Archivo no es una imagen válida.',
    'USER_NOT_FOUND': 'Usuario no encontrado.',
    'EMAIL_NOT_REGISTERED': 'El correo electrónico no está registrado.',
    'INVALID_CREDENTIALS': 'Credenciales inválidas.',
    'PERMISSION_DENIED': 'Permiso denegado.',
    'INFERENCE_ERROR': 'Error al procesar la imagen con el modelo.',
    'DATABASE_ERROR': 'Error de base de datos.',
}

# ==================== LÍMITES ====================
LIMITS = {
    'MAX_IMAGE_SIZE': 10 * 1024 * 1024,  # 10 MB
    'MIN_IMAGE_DIMENSION': 100,
    'MAX_IMAGE_DIMENSION': 10000,
    'MAX_FILENAME_LENGTH': 255,
    'MAX_PATIENT_NAME_LENGTH': 255,
    'ITEMS_PER_PAGE': 4,
    'MAX_SEARCH_LENGTH': 100,
}

# ==================== FORMATOS ====================
FORMATS = {
    'DATE': '%d/%m/%Y',
    'DATETIME': '%d/%m/%Y %H:%M:%S',
    'TIME': '%H:%M:%S',
    'DATE_LONG': '%d de %B de %Y',
}

# ==================== EXTENSIONES PERMITIDAS ====================
ALLOWED_IMAGE_EXTENSIONS = {
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'
}

# ==================== CÓDIGOS HTTP ====================
HTTP_CODES = {
    'OK': 200,
    'CREATED': 201,
    'BAD_REQUEST': 400,
    'UNAUTHORIZED': 401,
    'FORBIDDEN': 403,
    'NOT_FOUND': 404,
    'CONFLICT': 409,
    'SERVER_ERROR': 500,
}

# ==================== ROLES ====================
ROLE_ADMIN = 'admin'
ROLE_DOCTOR = 'doctor'
ROLE_PATIENT = 'patient'

ROLES = [
    (ROLE_ADMIN, 'Administrador'),
    (ROLE_DOCTOR, 'Médico'),
    (ROLE_PATIENT, 'Paciente'),
]

# ==================== ESTADOS ====================
STATUS_PENDING = 'pending'
STATUS_PROCESSING = 'processing'
STATUS_COMPLETED = 'completed'
STATUS_ERROR = 'error'

STATUSES = [
    (STATUS_PENDING, 'Pendiente'),
    (STATUS_PROCESSING, 'Procesando'),
    (STATUS_COMPLETED, 'Completado'),
    (STATUS_ERROR, 'Error'),
]

# ==================== COLORES ====================
COLORS = {
    'PRIMARY': '#1a2332',
    'SECONDARY': '#2c3e50',
    'SUCCESS': '#059669',
    'ERROR': '#dc2626',
    'WARNING': '#f59e0b',
    'INFO': '#3b82f6',
    'LIGHT': '#f8fafc',
    'DARK': '#1f2937',
}

# ==================== ZONA HORARIA ====================
TIMEZONE = 'America/Guayaquil'

# ==================== CONFIGURACIÓN DE LOGGING ====================
LOG_LEVELS = {
    'DEBUG': 'DEBUG',
    'INFO': 'INFO',
    'WARNING': 'WARNING',
    'ERROR': 'ERROR',
    'CRITICAL': 'CRITICAL',
}

# ==================== CONFIGURACIÓN DE PAGINACIÓN ====================
PAGINATION_DEFAULTS = {
    'ITEMS_PER_PAGE': 4,
    'MAX_ITEMS_PER_PAGE': 100,
}

# ==================== CONFIGURACIÓN DE CACHÉ ====================
CACHE_TIMEOUTS = {
    'SHORT': 300,  # 5 minutos
    'MEDIUM': 3600,  # 1 hora
    'LONG': 86400,  # 1 día
}

# ==================== CONFIGURACIÓN DE EMAIL ====================
EMAIL_TEMPLATES = {
    'PASSWORD_RESET': 'password_reset_email.html',
    'WELCOME': 'welcome_email.html',
    'RESULT_NOTIFICATION': 'result_notification_email.html',
}

# ==================== CONFIGURACIÓN DE PDF ====================
PDF_CONFIG = {
    'PAGE_SIZE': 'letter',
    'MARGIN_H': 0.6,  # inches
    'MARGIN_V': 0.75,  # inches
    'HEADER_HEIGHT': 0.9,  # inches
    'FOOTER_HEIGHT': 1.0,  # inches
}

# ==================== CONFIGURACIÓN DE ROBOFLOW ====================
ROBOFLOW_CONFIG = {
    'API_URL': 'https://outline.roboflow.com',
    'MODEL_ID': 'proy_2/1',
    'CONFIDENCE_THRESHOLD': 0.0,
    'TIMEOUT': 30,  # segundos
}
