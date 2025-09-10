# Sistema de Gestión de Licencias Escolares 📚

Este sistema está diseñado para gestionar de manera eficiente las licencias y permisos del personal docente en instituciones educativas. Proporciona una interfaz moderna y fácil de usar tanto para profesores como para administradores.

## 🌟 Características Principales

### Para Profesores
- Solicitud digital de licencias
- Carga de comprobantes y documentación
- Seguimiento del estado de solicitudes
- Gestión de perfil personal con foto
- Historial completo de licencias

### Para Administradores
- Panel de control intuitivo
- Gestión completa del personal docente
- Aprobación/rechazo de solicitudes
- Visualización de comprobantes
- Registro de nuevos profesores

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python con Flask
- **Base de Datos**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Iconos**: Font Awesome
- **Diseño**: Responsive Design (Mobile-first)

## 📋 Requisitos del Sistema

```
Flask
Werkzeug
SQLite3
```

## 🚀 Instalación y Configuración

1. Clonar el repositorio:
```bash
git clone [url-del-repositorio]
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Iniciar la aplicación:
```bash
python app.py
```

## 📱 Diseño Responsivo

El sistema está completamente optimizado para diferentes dispositivos:
- Escritorio (>768px)
- Tablets (768px - 1024px)
- Móviles (<768px)

## 🔐 Seguridad

- Contraseñas hasheadas
- Manejo seguro de sesiones
- Validación de formularios
- Protección contra CSRF

## 📁 Estructura del Proyecto

```
colegio-licencias/
│
├── app.py                 # Aplicación principal
├── database.db           # Base de datos SQLite
├── requirements.txt      # Dependencias
├── Procfile             # Configuración para despliegue
│
├── static/
│   ├── css/
│   │   ├── styles.css    # Estilos principales
│   │   └── responsive.css # Estilos responsivos
│   │
│   ├── uploads/          # Fotos de perfil
│   └── comprobantes/     # Documentos adjuntos
│
└── templates/
    ├── base.html         # Plantilla base
    ├── login.html        # Página de inicio de sesión
    ├── dashboard_admin.html   # Panel de administrador
    ├── dashboard_profesor.html # Panel de profesor
    └── solicitudes.html   # Formulario de solicitudes
```

## 👥 Roles de Usuario

### Administrador
- Usuario: ...
- Acceso completo al sistema
- Gestión de usuarios
- Aprobación de licencias

### Profesor
- Solicitud de licencias
- Gestión de perfil
- Seguimiento de solicitudes

## 🔄 Flujo de Trabajo

1. El profesor inicia sesión
2. Completa formulario de solicitud
3. Adjunta documentación (opcional)
4. El administrador revisa la solicitud
5. Aprueba o rechaza con comentarios
6. El profesor recibe la actualización

## 📌 Características Adicionales

- Interfaz moderna e intuitiva
- Diseño responsivo y adaptable
- Sistema de notificaciones
- Gestión de documentos
- Estadísticas y reportes

## 🌐 Despliegue

El sistema está preparado para ser desplegado en:
- Render
- Heroku
- Cualquier servidor que soporte Python/Flask

## 🤝 Contribución

Para contribuir al proyecto:
1. Fork del repositorio
2. Crear rama para nueva característica
3. Commit de cambios
4. Push a la rama
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT , desarrollado por Juan david Uscamayta ramos

## 📧 Contacto

Para soporte o consultas, contactar a:
[Información de contacto del desarrollador]

## 🔍 Estado del Proyecto

En desarrollo activo - Versión 1.0.0
