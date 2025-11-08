# Documentación de API - Aplicación Hernia

## Descripción General

Esta documentación describe los endpoints y servicios disponibles en la aplicación Hernia.

## Autenticación

### Login
**Endpoint:** `POST /login/`

**Parámetros:**
- `email` (string, requerido): Email del usuario
- `password` (string, requerido): Contraseña

**Respuesta Exitosa:**
- Redirige a `/` (home)
- Establece sesión

**Respuesta Error:**
- Mensaje de error: "Correo electrónico o contraseña incorrectos."

**Ejemplo:**
```bash
curl -X POST http://localhost:8000/login/ \
  -d "email=user@example.com&password=password123"
```

---

### Registro
**Endpoint:** `POST /register/`

**Parámetros:**
- `username` (string, requerido): Nombre de usuario
- `email` (string, requerido): Email
- `password1` (string, requerido): Contraseña
- `password2` (string, requerido): Confirmación de contraseña

**Respuesta Exitosa:**
- Crea usuario
- Inicia sesión automáticamente
- Redirige a `/`

**Respuesta Error:**
- Mensajes de validación

**Ejemplo:**
```bash
curl -X POST http://localhost:8000/register/ \
  -d "username=newuser&email=new@example.com&password1=pass123&password2=pass123"
```

---

### Logout
**Endpoint:** `POST /logout/`

**Respuesta:**
- Cierra sesión
- Redirige a `/login/`

---

## Vistas Principales

### Home
**Endpoint:** `GET /`

**Requerimientos:**
- Usuario autenticado

**Respuesta:**
- Plantilla `home.html`
- Contexto: `user`, `show_welcome_message`

---

### Resultados
**Endpoint:** `GET /resultados/`

**Requerimientos:**
- Usuario autenticado

**Respuesta:**
- Plantilla `resultados.html`

---

### Ver Resultado Específico
**Endpoint:** `GET /resultados/<id>/`

**Parámetros:**
- `id` (integer): ID del historial

**Requerimientos:**
- Usuario autenticado
- Historial pertenece al usuario

**Respuesta:**
- Plantilla `resultados.html`
- Contexto: `grupo`, `porcentaje`, `processed_image_url`, `fecha_imagen`, `paciente_nombre`, `historial_id`

**Ejemplo:**
```bash
curl http://localhost:8000/resultados/1/
```

---

## Perfil de Usuario

### Ver Perfil
**Endpoint:** `GET /perfil/`

**Requerimientos:**
- Usuario autenticado

**Respuesta:**
- Plantilla `perfil.html`
- Contexto: `user_form`, `profile_form`

---

### Editar Perfil
**Endpoint:** `POST /perfil/`

**Parámetros:**
- `first_name` (string): Nombre
- `last_name` (string): Apellido
- `email` (string): Email
- `phone_number` (string): Teléfono
- `address` (string): Dirección
- `profile_image` (file): Imagen de perfil

**Requerimientos:**
- Usuario autenticado

**Respuesta Exitosa:**
- Actualiza perfil
- Mensaje: "Perfil actualizado exitosamente."
- Redirige a `/perfil/`

**Respuesta Error:**
- Mensajes de validación

---

## Historial Médico

### Historial del Usuario
**Endpoint:** `GET /historial/`

**Parámetros Query:**
- `page` (integer, opcional): Número de página

**Requerimientos:**
- Usuario autenticado

**Respuesta:**
- Plantilla `historial_medico.html`
- Contexto: `page_obj` (paginado, 4 items por página)

**Ejemplo:**
```bash
curl http://localhost:8000/historial/?page=1
```

---

### Historial General
**Endpoint:** `GET /historial-general/`

**Parámetros Query:**
- `page` (integer, opcional): Número de página

**Requerimientos:**
- Usuario autenticado
- Usuario es superusuario

**Respuesta:**
- Plantilla `historial_medico_general.html`
- Contexto: `page_obj` (paginado, 4 items por página)

**Respuesta Error:**
- Mensaje: "No tienes permiso para acceder a esta sección."
- Redirige a `/historial/`

---

### Eliminar Historial
**Endpoint:** `POST /historial/<id>/eliminar/`

**Parámetros:**
- `id` (integer): ID del historial

**Requerimientos:**
- Usuario autenticado
- Historial pertenece al usuario

**Respuesta Exitosa:**
- Elimina historial e imagen
- Mensaje: "El registro ha sido eliminado correctamente."
- Redirige a `/historial/`

**Respuesta Error:**
- Mensaje: "No se encontró el registro."

---

### Eliminar Historial General
**Endpoint:** `POST /historial-general/<id>/eliminar/`

**Parámetros:**
- `id` (integer): ID del historial

**Requerimientos:**
- Usuario autenticado
- Usuario es superusuario

**Respuesta Exitosa:**
- Elimina historial e imagen
- Mensaje: "El registro ha sido eliminado correctamente."
- Redirige a `/historial-general/`

**Respuesta Error:**
- Mensaje: "No tienes permiso para realizar esta acción."

---

## Procesamiento de Imágenes

### Subir Imagen
**Endpoint:** `POST /subir-imagen/`

**Parámetros:**
- `imagen` (file, requerido): Archivo de imagen
- `paciente_nombre` (string, requerido): Nombre del paciente

**Validaciones:**
- Extensión permitida: jpg, jpeg, png, gif, bmp, webp
- Tamaño máximo: 10 MB
- Dimensiones: 100-10000 px

**Requerimientos:**
- Usuario autenticado

**Respuesta Exitosa:**
- Procesa imagen
- Realiza inferencia
- Crea historial
- Plantilla `resultados.html`
- Contexto: `grupo`, `porcentaje`, `original_image_url`, `processed_image_url`, `fecha_imagen`, `paciente_nombre`

**Respuesta Error:**
- Mensajes de validación
- Redirige a `/subir-imagen/`

**Ejemplo:**
```bash
curl -X POST http://localhost:8000/subir-imagen/ \
  -F "imagen=@image.jpg" \
  -F "paciente_nombre=Juan Pérez"
```

---

### Ver Formulario de Subida
**Endpoint:** `GET /subir-imagen/`

**Requerimientos:**
- Usuario autenticado

**Respuesta:**
- Plantilla `subir_imagen.html`
- Contexto: `form`

---

## Generación de PDFs

### Generar PDF Individual
**Endpoint:** `GET /pdf/<id>/`

**Parámetros:**
- `id` (integer): ID del historial

**Requerimientos:**
- Usuario autenticado
- Historial pertenece al usuario

**Respuesta:**
- Archivo PDF descargable
- Nombre: `informe_rad_XXXXXX_nombre_paciente.pdf`

**Contenido PDF:**
- Encabezado con información del informe
- Imagen radiológica procesada
- Datos del paciente
- Hallazgos y diagnóstico
- Índice de confianza
- Interpretación radiológica
- Pie de página con notas importantes

**Ejemplo:**
```bash
curl http://localhost:8000/pdf/1/ -o informe.pdf
```

---

### Generar PDF General
**Endpoint:** `GET /pdf-general/`

**Requerimientos:**
- Usuario autenticado

**Respuesta:**
- Archivo PDF descargable
- Nombre: `historial_rad_username.pdf` (usuario normal)
- Nombre: `historial_radiologico_completo.pdf` (superusuario)

**Contenido PDF:**
- Múltiples páginas (una por historial)
- Tabla de información
- Imagen radiológica
- Información de generación

**Ejemplo:**
```bash
curl http://localhost:8000/pdf-general/ -o historial.pdf
```

---

## Servicios Internos

### ImageProcessingService

#### `generate_encrypted_filename(original_name: str) -> str`
Genera un nombre de archivo encriptado usando SHA256.

```python
from app.Hernia.services import ImageProcessingService

encrypted = ImageProcessingService.generate_encrypted_filename("image.jpg")
# Resultado: "a1b2c3d4e5f6...jpg"
```

---

#### `download_image(image_url: str) -> Optional[Image.Image]`
Descarga una imagen desde URL.

```python
image = ImageProcessingService.download_image("https://example.com/image.jpg")
```

---

#### `get_inference_result(image_url: str) -> Optional[Dict]`
Obtiene resultado de inferencia del modelo Roboflow.

```python
result = ImageProcessingService.get_inference_result("https://example.com/image.jpg")
# Resultado: {'predictions': [...], 'visualization': '...'}
```

---

#### `extract_prediction_data(result: Dict) -> Tuple[str, float]`
Extrae datos de predicción del resultado.

```python
grupo, porcentaje = ImageProcessingService.extract_prediction_data(result)
# Resultado: ("Hernia", 95.5)
```

---

### HistorialService

#### `create_historial_from_image(...) -> Historial`
Crea un registro de historial de forma atómica.

```python
from app.Hernia.services import HistorialService

historial = HistorialService.create_historial_from_image(
    user=request.user,
    imagen_obj=imagen,
    paciente_nombre="Juan Pérez",
    grupo="Hernia",
    porcentaje=95.5
)
```

---

#### `delete_historial(historial_id: int, user=None) -> bool`
Elimina un historial de forma atómica.

```python
success = HistorialService.delete_historial(1, user=request.user)
```

---

### ImageValidator

#### `validate_image(file_obj) -> Tuple[bool, Optional[str]]`
Valida una imagen completa.

```python
from app.Hernia.services import ImageValidator

is_valid, error_msg = ImageValidator.validate_image(file_obj)
if not is_valid:
    print(f"Error: {error_msg}")
```

---

## Códigos de Error

| Código | Descripción |
|--------|-------------|
| 200 | OK |
| 201 | Creado |
| 400 | Solicitud inválida |
| 401 | No autenticado |
| 403 | Prohibido |
| 404 | No encontrado |
| 500 | Error del servidor |

---

## Límites y Restricciones

| Límite | Valor |
|--------|-------|
| Tamaño máximo de imagen | 10 MB |
| Dimensión mínima de imagen | 100 px |
| Dimensión máxima de imagen | 10000 px |
| Items por página | 4 |
| Extensiones permitidas | jpg, jpeg, png, gif, bmp, webp |

---

## Ejemplos de Uso

### Flujo Completo de Procesamiento

```bash
# 1. Registrarse
curl -X POST http://localhost:8000/register/ \
  -d "username=doctor1&email=doctor@example.com&password1=pass123&password2=pass123"

# 2. Subir imagen
curl -X POST http://localhost:8000/subir-imagen/ \
  -F "imagen=@radiografia.jpg" \
  -F "paciente_nombre=Juan Pérez"

# 3. Descargar PDF
curl http://localhost:8000/pdf/1/ -o informe.pdf

# 4. Ver historial
curl http://localhost:8000/historial/

# 5. Logout
curl -X POST http://localhost:8000/logout/
```

---

## Notas Importantes

- Todas las vistas requieren autenticación excepto login y register
- Los PDFs se generan bajo demanda
- Las imágenes se encriptan antes de guardarse
- Las transacciones son atómicas para garantizar consistencia
- El logging registra todas las operaciones importantes
