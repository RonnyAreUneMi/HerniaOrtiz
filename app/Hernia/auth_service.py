# ==================== SERVICIO DE AUTENTICACIÓN ====================
"""
Módulo para gestionar autenticación y recuperación de contraseña.
"""

import logging
from typing import Tuple, Optional

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


class AuthenticationService:
    """Servicio para autenticación de usuarios."""
    
    @staticmethod
    def authenticate_by_email(email: str, password: str) -> Tuple[Optional[User], Optional[str]]:
        """
        Autentica un usuario por email y contraseña.
        
        Returns:
            Tupla (usuario, error_message)
        """
        try:
            user = User.objects.get(email=email)
            authenticated_user = authenticate(username=user.username, password=password)
            
            if authenticated_user is not None:
                logger.info(f"Usuario autenticado: {user.username}")
                return authenticated_user, None
            else:
                logger.warning(f"Intento de autenticación fallido para: {email}")
                return None, "Correo electrónico o contraseña incorrectos."
        
        except User.DoesNotExist:
            logger.warning(f"Usuario no encontrado: {email}")
            return None, "Correo electrónico o contraseña incorrectos."
        except Exception as e:
            logger.error(f"Error en autenticación: {str(e)}")
            return None, "Error al procesar la autenticación."
    
    @staticmethod
    def register_user(form) -> Tuple[Optional[User], Optional[str]]:
        """
        Registra un nuevo usuario.
        
        Returns:
            Tupla (usuario, error_message)
        """
        try:
            if not form.is_valid():
                errors = []
                for field, field_errors in form.errors.items():
                    for error in field_errors:
                        errors.append(str(error))
                return None, " ".join(errors)
            
            user = form.save()
            logger.info(f"Usuario registrado: {user.username}")
            return user, None
        
        except Exception as e:
            logger.error(f"Error al registrar usuario: {str(e)}")
            return None, f"Error al registrar el usuario: {str(e)}"
    
    @staticmethod
    def send_password_reset_email(email: str) -> Tuple[bool, str]:
        """
        Envía un email de recuperación de contraseña.
        
        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            user = User.objects.get(email=email)
            
            # Aquí iría la lógica de envío de email
            # Por ahora solo registramos
            logger.info(f"Email de recuperación solicitado para: {email}")
            
            return True, "Se ha enviado un enlace para restablecer la contraseña a tu correo electrónico."
        
        except User.DoesNotExist:
            logger.warning(f"Intento de recuperación para email no registrado: {email}")
            return False, "El correo electrónico no está registrado en nuestro sistema."
        except Exception as e:
            logger.error(f"Error enviando email de recuperación: {str(e)}")
            return False, "Error al procesar la solicitud."
