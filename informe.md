# Actividad 2: Creación de proyecto Django, superusuario y CRUD de productos

**Asignatura:** Programación IV (Bloque 1 - Frameworks)  
**Estudiante:** Gabriel Alcon  
**Docente:** Jared Lopez Leaños  
**Fecha:** Septiembre 2026  
**Entorno de desarrollo:** Linux Debian 12 (Bookworm), Python 3.11.2, Django 5.2, SQLite 3  

---

## 1. Introducción y Contexto

En el marco del desarrollo de aplicaciones web empresariales, los frameworks robustos de alto nivel como **Django** ofrecen soluciones arquitectónicas completas que agilizan el ciclo de vida del software. El presente proyecto consiste en el diseño, configuración e implementación de un prototipo funcional para la gestión de inventario de productos de una compañía tecnológica.

El sistema implementa una arquitectura orientada a modelos, administración mediante el panel preconstruido de Django (**Django Admin**), autenticación de superusuarios, persistencia relacional con **SQLite** y un flujo completo de operaciones **CRUD** (Create, Read, Update, Delete), adaptado regionalmente a español latinoamericano (`es-419`).

---

## 2. Punto 1: Instalación y Configuración del Entorno Django

### 2.1. Fundamentación Teórica: Entornos Virtuales y Gestor de Dependencias

* **Entornos Virtuales (`venv`):** En Python, un entorno virtual es un directorio autocontenido que aísla las librerías, dependencias e intérprete de un proyecto respecto al entorno global del sistema operativo. Esto evita conflictos de versiones (*dependency hell*) entre distintos proyectos y garantiza la reproducibilidad técnica sin requerir privilegios de superusuario (`root`/`sudo`).
* **Gestor de Paquetes (`pip`) y `requirements.txt`:** `pip` es la herramienta estándar para resolver, descargar e instalar módulos desde el repositorio oficial PyPI (*Python Package Index*). La congelación de dependencias mediante `pip freeze > requirements.txt` genera un manifiesto determinista donde cada paquete queda fijado a su versión exacta (`==`), permitiendo a cualquier otro desarrollador desplegar el proyecto con `pip install -r requirements.txt`.

---

### 2.2. Verificación de Python y Creación del Entorno Virtual

Se verificó la presencia del intérprete Python en su versión 3.11+ y se inicializó el entorno virtual bajo el estándar `.venv`:

```bash
mkdir -p proyecto capturas
python3 --version
```

**Salida en terminal:**
```text
Python 3.11.2
```

![Verificación de la versión de Python instalada en Linux Debian](capturas/Captura%20de%20pantalla_2026-09-11_13-44-54.png)

A continuación, dentro del directorio `proyecto/`, se procedió a crear y activar el entorno virtual aislado:

```bash
cd /home/gabriel/Alcon_Gabriel_Actividad2_ProgramacionIV/proyecto
python3 -m venv .venv
source .venv/bin/activate
```

**Salida en terminal:**
```text
(.venv) [gabriel@upds]-[~/Alcon_Gabriel_Actividad2_ProgramacionIV/proyecto]
$ 
```

![Creación y activación exitosa del entorno virtual .venv](capturas/Captura%20de%20pantalla_2026-09-11_13-46-57.png)

---

### 2.3. Instalación de Django y Generación del Archivo de Dependencias

Con el entorno virtual activado, se actualizó el gestor `pip` y se instaló Django versión 5.x:

```bash
pip install --upgrade pip
pip install "django>=5.0,<6.0"
```

**Salida en terminal:**
```text
Requirement already satisfied: pip in ./.venv/lib/python3.11/site-packages (23.0.1)
Collecting pip
  Using cached pip-26.2.1-py3-none-any.whl (1.8 MB)
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 23.0.1
    Uninstalling pip-23.0.1:
      Successfully uninstalled pip-23.0.1
Successfully installed pip-26.2.1
Collecting django<6.0,>=5.0
  Using cached django-5.2.17-py3-none-any.whl.metadata (4.1 kB)
Collecting asgiref>=3.8.1 (from django<6.0,>=5.0)
Collecting sqlparse>=0.3.1 (from django<6.0,>=5.0)
Successfully installed asgiref-3.12.1 django-5.2.17 sqlparse-0.6.0
```

![Instalación de Django y librerías auxiliares dentro del entorno virtual](capturas/Captura%20de%20pantalla_2026-09-11_13-48-55.png)

Posteriormente, se generó y verificó el archivo `requirements.txt`:

```bash
pip freeze > requirements.txt
cat requirements.txt
```

**Contenido de `requirements.txt`:**
```text
asgiref==3.12.1
Django==5.2.17
sqlparse==0.6.0
```

![Contenido del archivo de dependencias requirements.txt](capturas/Captura%20de%20pantalla_2026-09-11_13-49-48.png)

---

### 2.4. Creación del Proyecto `web_project` y Registro de la App `inventory`

Se utilizó la utilidad de línea de comandos `django-admin` y `manage.py` para generar la estructura inicial:

```bash
# Creación del proyecto en el directorio raíz
django-admin startproject web_project .

# Creación de la aplicación modular de inventario
python manage.py startapp inventory
```

Para integrar la nueva aplicación al ciclo de vida del framework, se editó `web_project/settings.py`, incorporando `'inventory'` en la lista `INSTALLED_APPS`:

```python
# web_project/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventory', # App de inventario recién añadida
]
```

![Registro de la aplicación inventory en INSTALLED_APPS de settings.py](capturas/Captura%20de%20pantalla_2026-09-11_13-51-57.png)

---

## 3. Punto 2: Administración de Django Admin y Modelo de Datos

### 3.1. Fundamentación Teórica: ORM y Sistema de Migraciones

* **Object-Relational Mapping (ORM):** El ORM de Django abstrae la base de datos relacional modelando las tablas como clases de Python y las columnas como atributos tipados. Esto permite manipular los registros mediante objetos y métodos en Python sin necesidad de escribir consultas SQL manuales, garantizando protección nativa contra inyecciones SQL y portabilidad entre distintos motores de bases de datos (SQLite, PostgreSQL, MySQL).
* **Sistema de Migraciones:** Las migraciones son la forma que tiene Django de propagar los cambios realizados en los modelos (`models.py`) hacia el esquema físico de la base de datos.
  * `makemigrations`: Inspecciona los modelos e insumos de código y genera archivos de migración (código Python declarativo) que describen las modificaciones.
  * `migrate`: Ejecuta las instrucciones no aplicadas sobre el motor relacional de forma transaccional, actualizando tablas, índices y restricciones.

---

### 3.2. Creación del Superusuario y Acceso Administrativo

Antes de implementar modelos de negocio, se aplicaron las migraciones del sistema base de Django y se creó la cuenta administrativa con permisos globales:

```bash
python manage.py migrate
python manage.py createsuperuser
```

**Salida en terminal:**
```text
Username (leave blank to use 'gabriel'): gabriel
Email address: kevinmaydana448@gmail.com
Password: 
Password (again): 
Superuser created successfully.
```

![Creación del superusuario administrativo gabriel en la terminal](capturas/Captura%20de%20pantalla_2026-09-11_13-53-37.png)

---

### 3.3. Definición del Modelo de Datos `Producto`

En el archivo `inventory/models.py`, se definió la entidad `Producto` con todos los tipos de datos requeridos por la consigna:

```python
# inventory/models.py
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre del producto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    cantidad = models.PositiveIntegerField(default=0, verbose_name="Cantidad en stock")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio unitario")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} (Stock: {self.cantidad} - ${self.precio})"
```

**Decisiones técnicas de diseño:**
1. `PositiveIntegerField`: Garantiza a nivel de validación y base de datos que el inventario físico no acepte valores negativos.
2. `DecimalField(max_digits=10, decimal_places=2)`: Seleccionado en lugar de `FloatField` para evitar errores de redondeo en aritmética de punto flotante en transacciones monetarias.
3. `auto_now_add=True` y `auto_now=True`: Automatizan la trazabilidad temporal del registro en su creación y en cada actualización posterior sin intervención humana.
4. Metaclase `Meta`: Define nombres humanizados legibles y establece el ordenamiento por fecha descendente por defecto.

![Código fuente del modelo Producto en inventory/models.py](capturas/Captura%20de%20pantalla_2026-09-11_13-55-47.png)

---

### 3.4. Generación y Aplicación de Migraciones (Verificación en SQLite)

Se crearon y aplicaron los cambios en la base de datos relacional:

```bash
python manage.py makemigrations inventory
python manage.py migrate
```

**Salida en terminal:**
```text
Migrations for 'inventory':
  inventory/migrations/0001_initial.py
    + Create model Producto
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, inventory, sessions
Running migrations:
  Applying inventory.0001_initial... OK
```

![Ejecución de makemigrations y migrate para la aplicación inventory](capturas/Captura%20de%20pantalla_2026-09-11_13-58-01.png)

**Verificación técnica de la tabla en SQLite:**  
Mediante la inspección de esquema en Django, se constata que la tabla física `inventory_producto` ha sido construida con su estructura DDL correspondiente:

```bash
python manage.py shell -c "from django.db import connection; print([t.name for t in connection.introspection.get_table_list(connection.cursor()) if 'inventory' in t.name])"
```
**Resultado:** `['inventory_producto']`

Equivalente en SQL generado internamente por Django (`sqlmigrate`):
```sql
CREATE TABLE "inventory_producto" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "nombre" varchar(150) NOT NULL,
    "descripcion" text NULL,
    "cantidad" integer unsigned NOT NULL CHECK ("cantidad" >= 0),
    "precio" decimal NOT NULL,
    "fecha_creacion" datetime NOT NULL,
    "fecha_actualizacion" datetime NOT NULL
);
```

---

### 3.5. Personalización y Registro en `inventory/admin.py`

Se registró el modelo `Producto` en el módulo administrativo aplicando directivas avanzadas de visualización y filtrado:

```python
# inventory/admin.py
from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'cantidad', 'fecha_creacion', 'fecha_actualizacion')
    list_display_links = ('id', 'nombre')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('fecha_creacion', 'fecha_actualizacion')
    ordering = ('-fecha_creacion',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
```

**Beneficios de la configuración implementada:**
* `list_display`: Presenta una grilla con los datos clave del producto en lugar de una simple cadena de texto.
* `list_display_links`: Facilita la navegación al permitir abrir la edición haciendo clic tanto en el identificador numérico como en el nombre del producto.
* `search_fields`: Provee una barra de búsqueda indexada por nombre y descripción.
* `list_filter`: Añade paneles laterales interactivos para segmentar artículos por fecha de alta y última modificación.
* `readonly_fields`: Protege los campos de auditoría temporal contra alteraciones manuales indebidas.

![Código de personalización del modelo Producto en inventory/admin.py](capturas/Captura%20de%20pantalla_2026-09-11_13-59-49.png)

---

## 4. Punto 3: CRUD, Pruebas y Diagnóstico en Django Admin

### 4.1. Localización e Internacionalización (`es-419`)

Para cumplir con el estándar regional latinoamericano y optimizar la experiencia de usuario, se modificó `web_project/settings.py`:

```python
# web_project/settings.py
LANGUAGE_CODE = 'es-419'
TIME_ZONE = 'America/La_Paz'
USE_I18N = True
USE_TZ = True
```

Esto adaptó automáticamente todas las etiquetas, botones, mensajes del sistema y formatos de fecha/hora al español de Latinoamérica.

---

### 4.2. Inicio del Servidor de Desarrollo y Autenticación

Se ejecutó el servidor de desarrollo local:

```bash
python manage.py runserver
```

**Comprobación del servicio web (`http://127.0.0.1:8000/`):**

![Pantalla de bienvenida exitosa de Django 5.2](capturas/Captura%20de%20pantalla_2026-09-11_14-02-31.png)

A continuación, se ingresó al endpoint de administración (`http://127.0.0.1:8000/admin/`) validando las credenciales del superusuario `gabriel`:

![Formulario de inicio de sesión de Django Admin en español](capturas/Captura%20de%20pantalla_2026-09-11_14-06-05.png)

Una vez autenticado, se visualiza el panel de control principal con la sección modular **INVENTORY -> Productos**:

![Panel de control principal de Django Admin](capturas/Captura%20de%20pantalla_2026-09-11_14-06-18.png)

---

### 4.3. Evidencias de las Operaciones CRUD

#### A) Operaciones CREATE y READ (Listado General)
Se registraron en el sistema los productos del catálogo mediante el formulario de alta, validando que el listado mostrara las columnas configuradas (`ID`, `NOMBRE DEL PRODUCTO`, `PRECIO UNITARIO`, `CANTIDAD EN STOCK` y `FECHA DE CREACIÓN`):

1. **Laptop Lenovo ThinkPad T14** (Stock: 15, Precio: $850.00)
2. **Monitor Dell UltraSharp 27** (Stock: 8, Precio: $420.80)
3. **Teclado Mecánico Keychron K2** (Stock: 25, Precio: $100.00)
4. **Mouse Óptico Genérico USB** (Stock: 7, Precio: $8.50)

![Tabla general con los productos registrados y filtros laterales disponibles](capturas/Captura%20de%20pantalla_2026-09-11_14-09-25.png)

---

#### B) Operación READ: Búsqueda Indexada
Se ejecutó una prueba de búsqueda ingresando el término `"teclado"` en la barra superior. El sistema filtró instantáneamente la grilla devolviendo exclusivamente el registro correspondiente (`1 resultado (4 total)`):

![Prueba de búsqueda por texto en Django Admin](capturas/Captura%20de%20pantalla_2026-09-11_14-11-09.png)

---

#### C) Operación READ: Filtrado por Fecha
Se verificó el panel de filtros lateral seleccionando `"Hoy"` bajo el criterio *Por Fecha de creación*. El ORM procesó la consulta temporal mostrando los productos registrados durante la jornada actual:

![Prueba de filtrado dinámico por fecha en Django Admin](capturas/Captura%20de%20pantalla_2026-09-11_14-12-39.png)

---

#### D) Operación UPDATE: Modificación de Registro
Se ingresó a la ficha del producto `Laptop Lenovo ThinkPad T14` y se actualizó su inventario físico de 15 a **20 unidades**, confirmando los cambios con el botón Guardar. El sistema arrojó el mensaje de éxito de Django:  
> *"El Producto 'Laptop Lenovo ThinkPad T14 (Stock: 20 - $850.00)' se cambió correctamente."*

![Mensaje de confirmación tras modificar con éxito un producto](capturas/Captura%20de%20pantalla_2026-09-11_14-19-26.png)

---

#### E) Operación DELETE: Eliminación de Registro
Para verificar la eliminación segura, se seleccionó el artículo `Mouse Óptico Genérico USB` y se procedió con su baja definitiva del inventario. El sistema desplegó el banner de confirmación:  
> *"Eliminado/s 1 Producto satisfactoriamente."*

La base de datos `db.sqlite3` conserva los **3 productos principales**, dando pleno cumplimiento a la consigna de evaluación:

![Confirmación de eliminación de registro y catálogo final con 3 productos](capturas/Captura%20de%20pantalla_2026-09-11_14-20-06.png)

---

## 5. Reflexión Técnica

### 5.1. Dificultades Encontradas y Soluciones Técnicas Aplicadas

1. **Comprensión del flujo de edición en Django Admin:**  
   * *Incidencia:* Inicialmente se buscaba un botón gráfico explícito denominado «Editar» en cada fila de la grilla de productos.
   * *Diagnóstico:* Por diseño, Django Admin no añade botones redundantes; utiliza enlaces directos en los campos de la tabla. Por omisión, sólo el primer campo de `list_display` actúa como hipervínculo hacia la vista de modificación (`change_view`).
   * *Solución:* Se implementó la directiva `list_display_links = ('id', 'nombre')` en `inventory/admin.py`, logrando que tanto el identificador como el nombre del producto permitan el acceso inmediato al formulario de edición con un clic intuitivo.

2. **Gestión de zonas horarias y localización:**  
   * *Incidencia:* Al registrar productos con `auto_now_add=True`, las horas por defecto se registraban con desfase si la zona horaria permanecía en `UTC`.
   * *Solución:* Se ajustaron los parámetros `LANGUAGE_CODE = 'es-419'` y `TIME_ZONE = 'America/La_Paz'`, sincronizando las marcas temporales de creación y actualización con el huso horario local.

### 5.2. Aprendizajes y Competencias Adquiridas

* Dominio del ciclo de vida de proyectos en **Django 5.x**, desde el aislamiento de librerías mediante entornos virtuales (`.venv`) hasta la arquitectura modular basada en aplicaciones independientes (`apps`).
* Comprensión práctica del patrón de diseño **MVT** (*Model-View-Template*) y de la potencia del **ORM**, que desacopla la lógica de negocio del lenguaje SQL subyacente.
* Capacidad para extender, securizar y adaptar el panel administrativo de Django para convertirlo en un software de gestión corporativo listo para producción.

---

## 6. Vinculación con los Objetivos de Desarrollo Sostenible (ODS)

* **ODS 4: Educación de calidad:**  
  La práctica fomenta el aprendizaje aplicado de estándares profesionales de ingeniería de software, fortaleciendo habilidades críticas en arquitecturas web modernas requeridas por el sector productivo y laboral.
* **ODS 8: Trabajo decente y crecimiento económico:**  
  El desarrollo de soluciones computacionales eficientes mediante herramientas libres capacita al futuro profesional para impulsar la digitalización de pequeñas y medianas empresas (PyMEs), reduciendo costos operativos e incrementando la productividad comercial.
* **ODS 9: Industria, innovación e infraestructura:**  
  El uso de tecnologías de código abierto (*open source*) como Python, Django y SQLite democratiza el acceso al desarrollo tecnológico, permitiendo crear infraestructura digital escalable, resiliente y accesible para la comunidad.

---

## 7. Referencias Bibliográficas

* Django Software Foundation. (2024). *Django documentation (Version 5.2)*. Recuperado de https://docs.djangoproject.com/en/5.2/
* Django Software Foundation. (2024). *The Django admin site*. Recuperado de https://docs.djangoproject.com/en/5.2/ref/contrib/admin/
* Django Software Foundation. (2024). *Model field reference*. Recuperado de https://docs.djangoproject.com/en/5.2/ref/models/fields/
* Python Software Foundation. (2024). *venv — Creation of virtual environments*. Python 3.11 Documentation. Recuperado de https://docs.python.org/3.11/library/venv.html
* SQLite Consortium. (2024). *SQLite Documentation*. Recuperado de https://www.sqlite.org/docs.html
