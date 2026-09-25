"""ALPHAWEB - Configuración de archivos estáticos y medios."""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = Path(BASE_DIR, "staticfiles")

# Additional locations of static files
STATICFILES_DIRS = [
    Path(BASE_DIR, "Aplicacion", "static"),
]

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = Path(BASE_DIR, "media")
