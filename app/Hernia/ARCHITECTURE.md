# Arquitectura de la Aplicación Hernia

## Descripción General

La aplicación ha sido refactorizada siguiendo principios ACID y una arquitectura modular y escalable. El código está organizado en capas separadas por responsabilidad.

## Estructura de Archivos

```
app/Hernia/
├── views.py              # Vistas HTTP (controladores)
├── services.py           # Lógica de negocio
├── auth_service.py       # Servicios de autenticación
├── pdf_service.py        # Generación de PDFs
├── config.py             # Configuración centralizada
├── models.py             # Modelos de base de datos
├── forms.py              # Formularios Django
├── urls.py               # Rutas URL
├── admin.py              # Configuración admin
├── apps.py               # Configuración de app
├── tests.py              # Tests unitarios
├── migrations/           # Migraciones de BD
├── static/               # Archivos estáticos
├── templates/            # Plantillas HTML
└── templatetags/         # Tags personalizados
```

## Capas de la Aplicación

### 1. **Capa de Vistas (views.py)**
- Maneja solicitudes HTTP
- Coordina con servicios
- Gestiona sesiones y autenticación
- Retorna respuestas HTTP

**Características:**
- Decoradores `@login_required` para proteger vistas
- `@require_http_methods` para validar métodos HTTP
- `@cache_control` para control de caché
- Manejo centralizado de errores
- Logging de operaciones

### 2. **Capa de Servicios (services.py)**
Contiene la lógica de negocio separada de las vistas.

#### ImageProcessingService
- Descarga imágenes desde URLs
- Realiza inferencias con el modelo
- Dibuja predicciones en imágenes
- Procesa y guarda imágenes

#### HistorialService
- Crea registros de historial (transacciones atómicas)
- Elimina historiales (transacciones atómicas)
- Valida datos antes de guardar

#### ImageValidator
- Valida extensiones de archivo
- Valida tamaño de archivo
- Valida dimensiones de imagen
- Valida integridad de imagen

### 3. **Capa de Autenticación (auth_service.py)**
- Autentica usuarios por email
- Registra nuevos usuarios
- Gestiona recuperación de contraseña
- Logging de intentos de autenticación

### 4. **Capa de PDFs (pdf_service.py)**
Generación de reportes en PDF con estilos consistentes.

#### PDFStyles
- Colores estandarizados
- Dimensiones consistentes
- Estilos reutilizables

#### InformeRadiologicoGenerator
- Genera informes individuales
- Incluye imagen radiológica
- Datos del paciente
- Hallazgos y diagnóstico
- Índice de confianza
- Interpretación radiológica

#### HistorialGeneralGenerator
- Genera historial completo
- Múltiples páginas
- Tabla de información
- Imágenes procesadas

### 5. **Capa de Configuración (config.py)**
- API Keys (desde variables de entorno)
- Configuración de zona horaria
- Validación de imágenes
- Paginación
- Logging

## Principios ACID Implementados

### Atomicidad
```python
@transaction.atomic
def create_historial_from_image(...):
    # Todas las operaciones se ejecutan juntas o ninguna
    historial.full_clean()
    historial.save()
```

### Consistencia
- Validación de datos antes de guardar
- Uso de `full_clean()` en modelos
- Restricciones de integridad en BD

### Aislamiento
- Transacciones atómicas
- Decorador `@transaction.atomic`
- Manejo de excepciones

### Durabilidad
- Datos guardados en PostgreSQL
- Imágenes en AWS S3
- Logs persistentes

## Mejoras Implementadas

### 1. **Seguridad**
- ✅ API Key en variables de entorno
- ✅ Validación de permisos (solo superusuarios acceden a historial general)
- ✅ Validación de entrada (ImageValidator)
- ✅ CSRF protection
- ✅ Cache control

### 2. **Validación**
- ✅ Validación de extensiones de archivo
- ✅ Validación de tamaño de archivo
- ✅ Validación de dimensiones de imagen
- ✅ Validación de integridad de imagen

### 3. **Manejo de Errores**
- ✅ Try-catch en operaciones críticas
- ✅ Logging detallado
- ✅ Mensajes de error al usuario
- ✅ Transacciones atómicas

### 4. **Rendimiento**
- ✅ Descarga única de imagen (antes se descargaba 2 veces)
- ✅ Paginación en historial
- ✅ Caché de sesión
- ✅ Optimización de consultas

### 5. **Mantenibilidad**
- ✅ Código modular y reutilizable
- ✅ Separación de responsabilidades
- ✅ Documentación clara
- ✅ Logging centralizado
- ✅ Configuración centralizada

### 6. **Eliminación de Duplicación**
- ✅ `profile_view` y `editar_perfil` unificadas
- ✅ Estilos PDF centralizados
- ✅ Servicios reutilizables

## Flujo de Procesamiento de Imagen

```
1. Usuario sube imagen
   ↓
2. Validación (ImageValidator)
   ↓
3. Guardar imagen con nombre encriptado
   ↓
4. Descargar imagen desde URL
   ↓
5. Realizar inferencia (Roboflow)
   ↓
6. Dibujar predicciones
   ↓
7. Guardar imagen procesada
   ↓
8. Crear historial (transacción atómica)
   ↓
9. Mostrar resultados
```

## Flujo de Generación de PDF

```
1. Usuario solicita PDF
   ↓
2. Obtener historial (con validación de permisos)
   ↓
3. Crear generador (InformeRadiologicoGenerator)
   ↓
4. Dibujar encabezado
   ↓
5. Dibujar imagen radiológica
   ↓
6. Dibujar información clínica
   ↓
7. Dibujar pie de página
   ↓
8. Retornar PDF
```

## Configuración de Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
ROBOFLOW_API_KEY=tu_api_key_aqui
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
```

## Logging

Los logs se guardan en `hernia_app.log` con el siguiente formato:

```
INFO 2024-01-15 10:30:45 services Usuario autenticado: john_doe
ERROR 2024-01-15 10:31:20 views Error procesando imagen: [error details]
```

## Testing

Para ejecutar tests:

```bash
python manage.py test app.Hernia
```

## Mejoras Futuras

1. **Caché de resultados** - Redis para cachear predicciones
2. **Procesamiento asincrónico** - Celery para tareas largas
3. **Versionado de API** - REST API con versiones
4. **Monitoreo** - Sentry para tracking de errores
5. **Análisis** - Analytics de uso
6. **Notificaciones** - Email/SMS de resultados
7. **Reportes** - Dashboard de estadísticas
8. **Auditoría** - Registro de cambios

## Notas Importantes

- Las transacciones atómicas garantizan consistencia de datos
- Los validadores previenen datos inválidos
- El logging facilita debugging en producción
- La separación de capas permite testing independiente
- La configuración centralizada simplifica mantenimiento
