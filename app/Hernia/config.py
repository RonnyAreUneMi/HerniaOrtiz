# ==================== CONFIGURACIÓN ====================
"""
Módulo de configuración centralizada para la aplicación.
"""

import os
from django.conf import settings

# API Keys y URLs
ROBOFLOW_API_KEY = os.getenv('ROBOFLOW_API_KEY', settings.ROBOFLOW_API_KEY if hasattr(settings, 'ROBOFLOW_API_KEY') else None)
ROBOFLOW_API_URL = "https://outline.roboflow.com"
ROBOFLOW_MODEL_ID = "proy_2/1"

# Configuración de zona horaria
ECUADOR_TIMEZONE = 'America/Guayaquil'

# Configuración de validación de imágenes
IMAGE_VALIDATION = {
    'ALLOWED_EXTENSIONS': {'jpg', 'jpeg', 'png', 'gif', 'bmp'},
    'MAX_FILE_SIZE': 10 * 1024 * 1024,  # 10 MB
    'MIN_DIMENSION': 100,
    'MAX_DIMENSION': 10000,
}

# Configuración de paginación
PAGINATION = {
    'ITEMS_PER_PAGE': 4,
}

# Configuración de logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'hernia_app.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'app.Hernia': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
