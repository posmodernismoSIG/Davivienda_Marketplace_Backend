# 🏦 Davivienda Marketplace Backend

[![Django](https://img.shields.io/badge/Django-4.2.23-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django_REST-Framework-ff1709?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

## 📋 Descripción

**Davivienda Marketplace Backend** es una API REST desarrollada con Django REST Framework que proporciona la funcionalidad de backend para un marketplace de productos tradicionales y servicios financieros de Davivienda. El sistema permite gestionar usuarios, productos, categorías, pedidos y carritos de compra con un enfoque especial en productos financieros bancarios.

## ✨ Características Principales

### 🔐 Gestión de Usuarios
- **Registro y autenticación** con Djoser
- **Perfil personalizado** con campos adicionales (teléfono, dirección)
- **Autenticación por tokens** y sesiones
- **Permisos granulares** por roles

### 🛍️ Sistema de Productos
- **Categorías dinámicas** de productos
- **Productos financieros** específicos de Davivienda (CDT, Cuentas de Ahorro, Tarjetas)
- **Sistema de reseñas** y calificaciones
- **Gestión de inventario** automática
- **Búsqueda y filtros** avanzados

### 📦 Gestión de Pedidos
- **Estados de pedidos** bien definidos (Pendiente, Procesando, Enviado, Entregado, Cancelado)
- **Cancelación inteligente** con restauración de stock
- **Historial completo** de transacciones
- **Información de envío** detallada

### 🛒 Carrito de Compras
- Estructura base implementada
- Integración con sistema de pedidos

## 🛠️ Tecnologías Utilizadas

### Backend
- **Django 4.2.23** - Framework web principal
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de datos principal
- **Djoser** - Autenticación y gestión de usuarios
- **Django CORS Headers** - Gestión de CORS
- **Django Filter** - Filtros avanzados
- **Pillow** - Manejo de imágenes
- **Python Decouple** - Gestión de variables de entorno

### Frontend (Separado)
- **React** - Interfaz de usuario
- **Create React App** - Configuración base

## 📁 Estructura del Proyecto

```
Davivienda_Marketplace_Backend/
├── ecomerce/                    # Proyecto Django principal
│   ├── ecomerce/               # Configuración del proyecto
│   │   ├── settings.py         # Configuraciones principales
│   │   ├── urls.py            # URLs principales
│   │   └── wsgi.py            # WSGI application
│   ├── accounts/               # App de usuarios
│   │   ├── models.py          # Modelo de usuario personalizado
│   │   ├── serializers.py     # Serializers de usuario
│   │   ├── views.py           # Views de perfil
│   │   └── urls.py            # URLs de cuentas
│   ├── products/               # App de productos
│   │   ├── models.py          # Modelos de Product, Category, Review
│   │   ├── serializers.py     # Serializers de productos
│   │   ├── views.py           # ViewSets de productos
│   │   ├── filters.py         # Filtros personalizados
│   │   └── urls.py            # URLs de productos
│   ├── orders/                 # App de pedidos
│   │   ├── models.py          # Modelos de Order, OrderItem
│   │   ├── serializers.py     # Serializers de pedidos
│   │   ├── views.py           # ViewSets de pedidos
│   │   └── urls.py            # URLs de pedidos
│   ├── cart/                   # App de carrito (básica)
│   ├── create_test_data.py     # Script de datos de prueba
│   └── manage.py              # Comando principal de Django
├── ecomerce_front/             # Frontend React (separado)
├── requirements.txt            # Dependencias Python
└── README.md                  # Este archivo
```

## ⚙️ Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- PostgreSQL 12+
- pip (gestor de paquetes de Python)

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/Davivienda_Marketplace_Backend.git
cd Davivienda_Marketplace_Backend
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crear archivo `.env` en la raíz del proyecto:
```env
SECRET_KEY=tu_clave_secreta_muy_segura_aqui
DEBUG=True
DB_NAME=davivienda_marketplace
DB_USER=tu_usuario_db
DB_PASSWORD=tu_password_db
DB_HOST=localhost
DB_PORT=5432
```

### 5. Configurar Base de Datos
```bash
# Crear base de datos en PostgreSQL
createdb davivienda_marketplace

# Aplicar migraciones
cd ecomerce
python manage.py migrate
```

### 6. Crear Datos de Prueba
```bash
python create_test_data.py
```

### 7. Ejecutar Servidor de Desarrollo
```bash
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

## 📚 Uso de la API

### Base URL
```
http://localhost:8000/api/
```

### Autenticación
La API utiliza autenticación por tokens. Para obtener un token:

```bash
POST /api/auth/token/login/
Content-Type: application/json

{
    "username": "tu_usuario",
    "password": "tu_password"
}
```

Incluir el token en las headers de las peticiones:
```
Authorization: Token tu_token_aqui
```

## 🛣️ Endpoints Principales

### 👤 Usuarios y Autenticación
```http
POST   /api/auth/users/                 # Registro de usuario
POST   /api/auth/token/login/           # Login
POST   /api/auth/token/logout/          # Logout
GET    /api/profile/me/                 # Perfil actual
PATCH  /api/profile/update_profile/     # Actualizar perfil
POST   /api/profile/verify_profile/     # Verificar completitud del perfil
```

### 📦 Productos
```http
GET    /api/products/                   # Listar productos (con filtros)
POST   /api/products/                   # Crear producto (admin)
GET    /api/products/{id}/              # Detalle de producto
PUT    /api/products/{id}/              # Actualizar producto (admin)
DELETE /api/products/{id}/              # Eliminar producto (admin)
POST   /api/products/{id}/add_review/   # Agregar reseña
```

**Parámetros de filtro disponibles:**
- `?search=texto` - Búsqueda en nombre y descripción
- `?category=id` - Filtrar por categoría
- `?price_min=100&price_max=500` - Rango de precios
- `?ordering=price,-created_at` - Ordenamiento

### 📂 Categorías
```http
GET    /api/categories/                 # Listar categorías
POST   /api/categories/                 # Crear categoría (admin)
GET    /api/categories/{id}/            # Detalle de categoría
PUT    /api/categories/{id}/            # Actualizar categoría (admin)
DELETE /api/categories/{id}/            # Eliminar categoría (admin)
```

### 🛒 Pedidos
```http
GET    /api/orders/                     # Listar pedidos del usuario
POST   /api/orders/                     # Crear nuevo pedido
GET    /api/orders/{id}/                # Detalle de pedido
PATCH  /api/orders/{id}/cancel/         # Cancelar pedido
GET    /api/orders/summary/             # Resumen de pedidos del usuario
```

## 🧪 Datos de Prueba

El proyecto incluye un script para generar datos de prueba:

```bash
python create_test_data.py
```

### Usuarios de Prueba Creados:
| Usuario | Password | Rol | Email |
|---------|----------|-----|-------|
| `daviviendaAdmin` | `d4v1v13nd4` | Administrador | admin@davivienda.com |
| `cliente1` | `cliente123` | Cliente | cliente1@example.com |
| `cliente2` | `cliente123` | Cliente | cliente2@example.com |
| `asesor_financiero` | `asesor123` | Staff | asesor@davivienda.com |

### Categorías Incluidas:
- 📱 Electrónicos
- 👕 Ropa  
- 🏠 Hogar
- 📚 Libros
- ⚽ Deportes
- 💰 **Productos Financieros** (Específicos de Davivienda)

### Productos Financieros de Ejemplo:
- **Cuenta de Ahorros DaviPlata** - Gratuita
- **CDT Mi Inversión** - 12% EA
- **Tarjeta de Crédito Mastercard** - $85,000
- **Crédito Hipotecario VIS** - A partir de $120,000,000

## 🔧 Configuración Avanzada

### CORS (Cross-Origin Resource Sharing)
Configurado para desarrollo local:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Paginación
- **Tamaño de página por defecto**: 20 elementos
- **Parámetro**: `?page=2`

### Filtros y Búsqueda
- **Backend de filtros**: DjangoFilterBackend
- **Búsqueda**: SearchFilter en nombre y descripción
- **Ordenamiento**: OrderingFilter por precio, fecha, etc.

## 🚀 Deployment

### Configuraciones para Producción
1. **Cambiar DEBUG a False**
2. **Configurar ALLOWED_HOSTS**
3. **Usar variables de entorno seguras**
4. **Configurar servidor web (Nginx + Gunicorn)**
5. **Configurar archivos estáticos y media**

### Ejemplo con Docker (Recomendado)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "ecomerce.wsgi:application"]
```

## 🧪 Testing

Para ejecutar tests (cuando estén implementados):
```bash
python manage.py test
```

## 📈 Roadmap / TODOs

### 🔥 Prioridad Alta
- [ ] Completar funcionalidad del carrito de compras
- [ ] Implementar sistema de pagos (PSE, Tarjetas)
- [ ] Agregar tests unitarios y de integración
- [ ] Mejorar sistema de seguridad (JWT refresh tokens)

### 📋 Prioridad Media  
- [ ] Sistema de notificaciones (Email/SMS)
- [ ] Implementar Redis para caché
- [ ] Logs y monitoreo avanzado
- [ ] API de reportes y analytics

### 💡 Prioridad Baja
- [ ] Sistema de wishlist
- [ ] Cupones y descuentos
- [ ] Chat en vivo con asesores
- [ ] Integración con servicios de Davivienda

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estándares de Código
- Seguir PEP 8 para Python
- Documentar funciones y clases importantes
- Escribir tests para nuevas funcionalidades
- Actualizar documentación cuando sea necesario

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Contacto y Soporte

- **Equipo de Desarrollo**: [email@davivienda.com]
- **Documentación API**: `http://localhost:8000/api/` (cuando esté implementada)
- **Admin Panel**: `http://localhost:8000/admin/`

---

### 🏦 Desarrollado para Davivienda
*Conectando la tecnología financiera con la experiencia del cliente*

**¿Necesitas ayuda?** Revisa la documentación o contacta al equipo de desarrollo.

## 📊 Status del Proyecto

![Status](https://img.shields.io/badge/Status-En%20Desarrollo-yellow?style=for-the-badge)
![API](https://img.shields.io/badge/API-REST-blue?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Tests-Pendiente-red?style=for-the-badge)
