# ==================== SERVICIOS DE PROCESAMIENTO ====================
"""
Módulo de servicios para procesamiento de imágenes y generación de reportes.
Contiene la lógica de negocio separada de las vistas.
"""

import os
import hashlib
import tempfile
import logging
from io import BytesIO
from typing import Dict, Tuple, Optional

import cv2
import numpy as np
import pytz
import requests
from PIL import Image
from inference_sdk import InferenceHTTPClient

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import transaction

from .models import Imagen, Historial

logger = logging.getLogger(__name__)

# ==================== CONFIGURACIÓN ====================
def get_inference_client():
    """Obtiene el cliente de inferencia configurado."""
    api_key = settings.ROBOFLOW_API_KEY
    if not api_key:
        raise ValueError("ROBOFLOW_API_KEY no está configurada en settings")
    
    return InferenceHTTPClient(
        api_url="https://outline.roboflow.com",
        api_key=api_key
    )


# ==================== SERVICIOS DE IMAGEN ====================
class ImageProcessingService:
    """Servicio para procesar imágenes y realizar inferencias."""
    
    ECUADOR_TZ = pytz.timezone('America/Guayaquil')
    MODEL_ID = "proy_2/1"
    CONFIDENCE_THRESHOLD = 0.0
    
    @staticmethod
    def generate_encrypted_filename(original_name: str) -> str:
        """Genera un nombre de archivo encriptado."""
        hash_object = hashlib.sha256(original_name.encode())
        encrypted_name = hash_object.hexdigest()
        extension = original_name.split('.')[-1]
        return f"{encrypted_name}.{extension}"
    
    @staticmethod
    def download_image(image_url: str) -> Optional[Image.Image]:
        """Descarga una imagen desde URL."""
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            if not response.content:
                logger.warning(f"Respuesta vacía al descargar imagen: {image_url}")
                return None
            
            image_data = BytesIO(response.content)
            return Image.open(image_data).convert('RGB')
        except requests.RequestException as e:
            logger.error(f"Error descargando imagen {image_url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error procesando imagen descargada: {str(e)}")
            return None
    
    @staticmethod
    def get_inference_result(image_url: str) -> Optional[Dict]:
        """Obtiene el resultado de inferencia del modelo."""
        try:
            client = get_inference_client()
            result = client.infer(image_url, model_id=ImageProcessingService.MODEL_ID)
            return result
        except Exception as e:
            logger.error(f"Error en inferencia: {str(e)}")
            return None
    
    @staticmethod
    def draw_predictions_on_image(img_cv2: np.ndarray, predictions: list) -> np.ndarray:
        """Dibuja las predicciones en la imagen."""
        for pred in predictions:
            try:
                confidence = pred.get('confidence', 0) * 100
                class_name = pred.get('class', 'Unknown')
                
                if 'points' in pred:
                    points = np.array(
                        [[p['x'], p['y']] for p in pred['points']], 
                        dtype=np.int32
                    )
                    
                    # Overlay semi-transparente
                    overlay = img_cv2.copy()
                    cv2.fillPoly(overlay, [points], (0, 0, 255))
                    alpha = 0.4
                    cv2.addWeighted(overlay, alpha, img_cv2, 1 - alpha, 0, img_cv2)
                    
                    # Contorno y etiqueta
                    color = (0, 255, 0) if class_name == 'Sin Hernia' else (255, 0, 0)
                    cv2.polylines(img_cv2, [points], isClosed=True, color=color, thickness=2)
                    
                    x_min = min(points[:, 0])
                    y_min = min(points[:, 1])
                    text = f"{class_name} {confidence:.2f}%"
                    cv2.putText(
                        img_cv2, text, (x_min, y_min - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
                    )
            except Exception as e:
                logger.warning(f"Error dibujando predicción: {str(e)}")
                continue
        
        return img_cv2
    
    @staticmethod
    def save_processed_image(img_cv2: np.ndarray) -> BytesIO:
        """Convierte imagen procesada a BytesIO."""
        img_pil = Image.fromarray(cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB))
        buffer = BytesIO()
        img_pil.save(buffer, format="JPEG", quality=95)
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def extract_prediction_data(result: Dict) -> Tuple[str, float]:
        """Extrae datos de predicción del resultado."""
        predictions = result.get('predictions', [])
        
        if not predictions:
            return "Predicción no encontrada", 0.0
        
        first_pred = predictions[0]
        class_prediction = first_pred.get('class', 'Unknown')
        confidence = first_pred.get('confidence', 0) * 100
        
        grupo = "Sin Hernia" if class_prediction == 'Sin Hernia' else "Hernia"
        porcentaje = round(confidence, 2)
        
        return grupo, porcentaje


class HistorialService:
    """Servicio para gestionar el historial médico."""
    
    ECUADOR_TZ = pytz.timezone('America/Guayaquil')
    
    @staticmethod
    @transaction.atomic
    def create_historial_from_image(
        user,
        imagen_obj: Imagen,
        paciente_nombre: str,
        grupo: str,
        porcentaje: float
    ) -> Historial:
        """Crea un registro de historial de forma atómica."""
        try:
            fecha_local = imagen_obj.fecha.astimezone(HistorialService.ECUADOR_TZ)
            
            historial = Historial(
                user=user,
                imagen=imagen_obj.imagen,
                porcentaje=porcentaje,
                grupo=grupo,
                paciente_nombre=paciente_nombre,
                fecha_imagen=fecha_local,
            )
            historial.full_clean()
            historial.save()
            
            logger.info(
                f"Historial creado: ID={historial.id}, "
                f"Paciente={paciente_nombre}, Grupo={grupo}"
            )
            return historial
        except Exception as e:
            logger.error(f"Error creando historial: {str(e)}")
            raise
    
    @staticmethod
    @transaction.atomic
    def delete_historial(historial_id: int, user=None) -> bool:
        """Elimina un historial de forma atómica."""
        try:
            if user:
                historial = Historial.objects.get(id=historial_id, user=user)
            else:
                historial = Historial.objects.get(id=historial_id)
            
            if historial.imagen:
                historial.imagen.delete()
            
            historial.delete()
            logger.info(f"Historial eliminado: ID={historial_id}")
            return True
        except Historial.DoesNotExist:
            logger.warning(f"Historial no encontrado: ID={historial_id}")
            return False
        except Exception as e:
            logger.error(f"Error eliminando historial: {str(e)}")
            raise


# ==================== VALIDADORES ====================
class ImageValidator:
    """Validador para imágenes subidas."""
    
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    MIN_DIMENSION = 100
    MAX_DIMENSION = 10000
    
    @staticmethod
    def validate_file_extension(filename: str) -> bool:
        """Valida la extensión del archivo."""
        extension = filename.rsplit('.', 1)[-1].lower()
        return extension in ImageValidator.ALLOWED_EXTENSIONS
    
    @staticmethod
    def validate_file_size(file_size: int) -> bool:
        """Valida el tamaño del archivo."""
        return 0 < file_size <= ImageValidator.MAX_FILE_SIZE
    
    @staticmethod
    def validate_image_dimensions(image: Image.Image) -> bool:
        """Valida las dimensiones de la imagen."""
        width, height = image.size
        return (
            ImageValidator.MIN_DIMENSION <= width <= ImageValidator.MAX_DIMENSION and
            ImageValidator.MIN_DIMENSION <= height <= ImageValidator.MAX_DIMENSION
        )
    
    @staticmethod
    def validate_image(file_obj) -> Tuple[bool, Optional[str]]:
        """Valida una imagen completa."""
        try:
            # Validar extensión
            if not ImageValidator.validate_file_extension(file_obj.name):
                return False, "Formato de archivo no permitido"
            
            # Validar tamaño
            if not ImageValidator.validate_file_size(file_obj.size):
                return False, f"Archivo demasiado grande (máximo {ImageValidator.MAX_FILE_SIZE / 1024 / 1024}MB)"
            
            # Validar que sea una imagen válida
            try:
                image = Image.open(file_obj)
                image.verify()
                file_obj.seek(0)
                image = Image.open(file_obj)
            except Exception:
                return False, "Archivo no es una imagen válida"
            
            # Validar dimensiones
            if not ImageValidator.validate_image_dimensions(image):
                return False, f"Dimensiones inválidas ({ImageValidator.MIN_DIMENSION}-{ImageValidator.MAX_DIMENSION}px)"
            
            return True, None
        except Exception as e:
            logger.error(f"Error validando imagen: {str(e)}")
            return False, "Error al validar la imagen"
