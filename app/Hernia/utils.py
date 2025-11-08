# ==================== UTILIDADES ====================
"""
Módulo de utilidades y funciones auxiliares.
"""

import logging
from typing import Optional, Dict, Any
from functools import wraps

import pytz
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse

logger = logging.getLogger(__name__)


# ==================== DECORADORES ====================
def handle_exceptions(view_func):
    """
    Decorador para manejar excepciones en vistas.
    Registra errores y muestra mensajes al usuario.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error en {view_func.__name__}: {str(e)}")
            messages.error(request, "Ocurrió un error. Por favor, intenta nuevamente.")
            return redirect('index')
    return wrapper


def superuser_required(view_func):
    """
    Decorador para requerir que el usuario sea superusuario.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            logger.warning(f"Acceso denegado para usuario no superusuario: {request.user.username}")
            messages.error(request, "No tienes permiso para acceder a esta sección.")
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapper


# ==================== FUNCIONES DE FECHA ====================
def get_local_datetime(dt, timezone_str: str = 'America/Guayaquil'):
    """
    Convierte un datetime a zona horaria local.
    
    Args:
        dt: datetime object
        timezone_str: string de zona horaria
    
    Returns:
        datetime en zona horaria local
    """
    try:
        tz = pytz.timezone(timezone_str)
        return dt.astimezone(tz)
    except Exception as e:
        logger.error(f"Error convirtiendo zona horaria: {str(e)}")
        return dt


def format_datetime(dt, format_str: str = '%d/%m/%Y %H:%M:%S') -> str:
    """
    Formatea un datetime a string.
    
    Args:
        dt: datetime object
        format_str: formato deseado
    
    Returns:
        string formateado
    """
    try:
        return dt.strftime(format_str)
    except Exception as e:
        logger.error(f"Error formateando fecha: {str(e)}")
        return str(dt)


# ==================== FUNCIONES DE VALIDACIÓN ====================
def is_valid_email(email: str) -> bool:
    """Valida formato de email."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_phone(phone: str) -> bool:
    """Valida formato de teléfono."""
    import re
    pattern = r'^[\d\s\-\+\(\)]{7,}$'
    return re.match(pattern, phone) is not None


# ==================== FUNCIONES DE RESPUESTA ====================
def json_response(data: Dict[str, Any], status: int = 200) -> HttpResponse:
    """
    Retorna una respuesta JSON.
    
    Args:
        data: diccionario a convertir a JSON
        status: código HTTP
    
    Returns:
        HttpResponse con JSON
    """
    import json
    return HttpResponse(
        json.dumps(data),
        content_type='application/json',
        status=status
    )


def error_response(message: str, status: int = 400) -> HttpResponse:
    """
    Retorna una respuesta de error en JSON.
    
    Args:
        message: mensaje de error
        status: código HTTP
    
    Returns:
        HttpResponse con error
    """
    return json_response({'error': message}, status=status)


def success_response(message: str, data: Optional[Dict] = None, status: int = 200) -> HttpResponse:
    """
    Retorna una respuesta de éxito en JSON.
    
    Args:
        message: mensaje de éxito
        data: datos adicionales
        status: código HTTP
    
    Returns:
        HttpResponse con éxito
    """
    response = {'success': True, 'message': message}
    if data:
        response.update(data)
    return json_response(response, status=status)


# ==================== FUNCIONES DE PAGINACIÓN ====================
def get_page_range(paginator, page_obj, range_size: int = 5) -> list:
    """
    Obtiene un rango de números de página para mostrar.
    
    Args:
        paginator: objeto Paginator
        page_obj: página actual
        range_size: cantidad de páginas a mostrar
    
    Returns:
        lista de números de página
    """
    current_page = page_obj.number
    total_pages = paginator.num_pages
    
    start = max(1, current_page - range_size // 2)
    end = min(total_pages + 1, start + range_size)
    
    if end - start < range_size:
        start = max(1, end - range_size)
    
    return list(range(start, end))


# ==================== FUNCIONES DE ARCHIVO ====================
def get_file_extension(filename: str) -> str:
    """Obtiene la extensión de un archivo."""
    return filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''


def get_file_size_mb(file_size: int) -> float:
    """Convierte tamaño de bytes a MB."""
    return round(file_size / (1024 * 1024), 2)


def format_file_size(file_size: int) -> str:
    """Formatea tamaño de archivo a string legible."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if file_size < 1024:
            return f"{file_size:.2f} {unit}"
        file_size /= 1024
    return f"{file_size:.2f} TB"


# ==================== FUNCIONES DE LOGGING ====================
def log_user_action(user, action: str, details: str = ""):
    """
    Registra una acción del usuario.
    
    Args:
        user: usuario que realiza la acción
        action: tipo de acción
        details: detalles adicionales
    """
    message = f"Usuario: {user.username} | Acción: {action}"
    if details:
        message += f" | Detalles: {details}"
    logger.info(message)


def log_error(error_type: str, error_message: str, context: str = ""):
    """
    Registra un error.
    
    Args:
        error_type: tipo de error
        error_message: mensaje de error
        context: contexto del error
    """
    message = f"Error [{error_type}]: {error_message}"
    if context:
        message += f" | Contexto: {context}"
    logger.error(message)


# ==================== FUNCIONES DE CONTEXTO ====================
def get_base_context(request) -> Dict[str, Any]:
    """
    Obtiene contexto base para todas las vistas.
    
    Args:
        request: objeto request
    
    Returns:
        diccionario con contexto base
    """
    return {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'is_superuser': request.user.is_superuser,
        'username': request.user.username if request.user.is_authenticated else None,
    }


# ==================== FUNCIONES DE BÚSQUEDA ====================
def search_historiales(queryset, search_term: str):
    """
    Busca en historiales por nombre de paciente o usuario.
    
    Args:
        queryset: QuerySet de Historial
        search_term: término de búsqueda
    
    Returns:
        QuerySet filtrado
    """
    from django.db.models import Q
    
    if not search_term:
        return queryset
    
    return queryset.filter(
        Q(paciente_nombre__icontains=search_term) |
        Q(user__username__icontains=search_term) |
        Q(grupo__icontains=search_term)
    )


# ==================== FUNCIONES DE ESTADÍSTICAS ====================
def get_historial_stats(queryset) -> Dict[str, Any]:
    """
    Obtiene estadísticas del historial.
    
    Args:
        queryset: QuerySet de Historial
    
    Returns:
        diccionario con estadísticas
    """
    from django.db.models import Avg, Count
    
    stats = queryset.aggregate(
        total=Count('id'),
        promedio_confianza=Avg('porcentaje'),
    )
    
    hernias = queryset.filter(grupo='Hernia').count()
    sin_hernias = queryset.filter(grupo='Sin Hernia').count()
    
    return {
        'total': stats['total'],
        'promedio_confianza': round(stats['promedio_confianza'] or 0, 2),
        'hernias': hernias,
        'sin_hernias': sin_hernias,
        'porcentaje_hernias': round((hernias / stats['total'] * 100) if stats['total'] > 0 else 0, 2),
    }
