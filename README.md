# Restaurante App — Semana 16 

**Estudiante:** Anderson Joel Pilachanga Caguana 

## Propósito de la semana

Aplicar de forma práctica el manejo de eventos de Tkinter sobre la
sección de **Usuarios** de `restaurante_app`, evidenciando el flujo:

```
interacción del usuario → evento → bind() → callback → RestauranteServicio
   → persistencia en usuarios.json → respuesta visual
```

La gestión de usuarios pasa de ser una simple consulta a un **CRUD
completo** (registrar, consultar, actualizar, eliminar), incorporando
además un **rol** (`Administrador`, `Empleado`, `Cliente`) que determina
quién puede acceder a esta gestión.

## Evolución realizada sobre el proyecto anterior

- Se conservaron sin cambios el inicio de sesión, la navegación, la
  gestión de productos y el registro de ventas desarrollados en las
  semanas 13 a 15.
- Se agregó el atributo **`rol`** al modelo `Usuario` y se persiste en
  `usuarios.json`.
- Se agregó **`guardar_usuarios()`** a `ArchivoServicio` (antes solo se
  leían los usuarios).
- Se agregaron a `RestauranteServicio` los métodos **`es_administrador()`**,
  **`registrar_usuario()`**, **`actualizar_usuario()`** y
  **`eliminar_usuario()`**, con sus validaciones.
- La pantalla de acceso ahora entrega el objeto `Usuario` autenticado a
  `MainView` (antes solo avisaba que el acceso fue exitoso).
- La pestaña **Usuarios** se reconstruye según el rol de quien inició
  sesión: un Administrador ve el formulario y la tabla completos; un
  Empleado o Cliente ve únicamente un mensaje de acceso restringido.
- Se incorporaron los eventos `<<TreeviewSelect>>`, `<Return>`,
  `<Escape>` y `<<ComboboxSelected>>` mediante `bind()`, además de los
  botones ya existentes con `command=`.

## Estructura del proyecto

```
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── logo.png
│   ├── icono_productos.png
│   ├── icono_usuarios.png
│   └── icono_ventas.png
├── main.py
└── README.md
```

## Rol de usuario y control de acceso

`Usuario` ahora incluye `rol`, limitado a tres valores:
`Administrador`, `Empleado`, `Cliente` (validado en
`RestauranteServicio.ROLES_VALIDOS`).

```python
def es_administrador(self, usuario: Usuario) -> bool:
    return usuario.rol == "Administrador"
```

Al iniciar sesión, `LoginView` entrega el objeto `Usuario` autenticado a
`main.py`, que lo pasa a `MainView.establecer_usuario_actual()`. Este
método reconstruye el contenido de la pestaña **Usuarios**:

- Si `es_administrador(usuario_actual)` es verdadero → se construye el
  formulario completo, la tabla y las acciones de gestión.
- En caso contrario → se muestra únicamente un mensaje: *"Esta sección
  está disponible únicamente para usuarios con rol Administrador."*

Usuarios de prueba y su rol:

| Usuario | Contraseña | Rol |
|---|---|---|
| `daniel` | `1234` | Administrador |
| `dareck` | `1234` | Empleado |
| `ariel` | `1234` | Cliente |

## Gestión de usuarios (solo Administrador)

El formulario permite **registrar**, **consultar** (mediante selección en
la tabla), **actualizar** y **eliminar** usuarios, con los mismos botones
`command=` usados en Productos:

| Botón | Método del servicio |
|---|---|
| Registrar | `registrar_usuario()` |
| Actualizar | `actualizar_usuario()` |
| Eliminar | `eliminar_usuario()` |
| Limpiar | — (solo vacía el formulario y la selección) |

Validaciones en `RestauranteServicio`:

- Identificación, nombre, usuario y contraseña son obligatorios.
- El rol debe ser uno de los tres valores válidos.
- No se permite una identificación duplicada al registrar.
- No se permite un nombre de usuario duplicado (al registrar o actualizar).
- No se puede actualizar ni eliminar un usuario que no existe.
- **No se puede eliminar la cuenta con la que se inició sesión
  actualmente** (`eliminar_usuario()` recibe la identificación del
  usuario autenticado y la compara antes de borrar).

La eliminación pide confirmación con `messagebox.askyesno()` antes de
llamar al servicio.

## Eventos implementados

### `<<TreeviewSelect>>` — cargar usuario desde la tabla

```python
self.tabla_usuarios.bind("<<TreeviewSelect>>", self.al_seleccionar_usuario)
```

`al_seleccionar_usuario(evento)` toma el **identificador** de la fila
seleccionada (primera columna) y pide el usuario completo a
`RestauranteServicio.buscar_usuario()`; la tabla nunca guarda la
contraseña ni otros datos directamente, solo lo necesario para mostrarse.

### `<Return>` — atajo para registrar

```python
widget.bind("<Return>", self.manejar_enter_usuario)
```

`manejar_enter_usuario(evento)` **reutiliza** `self.registrar_usuario()`,
el mismo método que usa el botón "Registrar" con `command=`. No se
duplica la lógica de registro.

### `<Escape>` — limpiar formulario y selección

```python
widget.bind("<Escape>", self.manejar_escape_usuario)
```

`manejar_escape_usuario(evento)` **reutiliza**
`self.limpiar_formulario_usuario()`, el mismo método del botón "Limpiar".

### `<<ComboboxSelected>>` — responder al cambio de rol

```python
combo_rol.bind("<<ComboboxSelected>>", self.al_cambiar_rol)
```

`al_cambiar_rol(evento)` actualiza el mensaje de estado del formulario
indicando el rol elegido, sin alterar ningún dato todavía.

### Resumen: `command=` vs `bind()`

| Mecanismo | Dónde se usa | Qué dispara |
|---|---|---|
| `command=` | Botones Registrar, Actualizar, Eliminar, Limpiar (Usuarios y Productos), Registrar venta, Cerrar sesión | Un clic del usuario |
| `bind()` | Tabla de usuarios, campos del formulario, Combobox de rol | Selección de fila, teclas Enter/Escape, cambio de opción |

## Separación de responsabilidades

```
MainView  →  RestauranteServicio (validaciones y reglas)  →  ArchivoServicio (lectura/escritura)  →  JSON
```

Los callbacks de los eventos solo recogen información de la interfaz
(identificación seleccionada, valores del formulario) y llaman a
`RestauranteServicio`; ninguno valida reglas de negocio ni escribe
archivos directamente. `main_view.py` y `login_view.py` siguen sin
importar `json`.

## Persistencia en `usuarios.json`

`ArchivoServicio.guardar_usuarios()` serializa la colección completa de
usuarios (incluido el nuevo campo `rol`) cada vez que se registra,
actualiza o elimina un usuario, siguiendo el mismo patrón usado para
`productos.json` y `ventas.json`.

## Cómo ejecutar el programa

1. Tener **Python 3** con Tkinter disponible (incluido en la instalación
   estándar en Windows y macOS; en Linux puede requerir `python3-tk`).
2. Ubicarse dentro de la carpeta `restaurante_app/`:
   ```bash
   cd restaurante_app
   ```
3. Ejecutar:
   ```bash
   python3 main.py
   ```
4. Ingresar como `daniel` / `1234` para acceder a la gestión completa de
   usuarios, o como `dareck` / `1234` o `ariel` / `1234` para comprobar
   el mensaje de acceso restringido.

## Comprobación de funcionamiento realizada

1. La aplicación inicia sin errores; el login, la navegación, Productos
   y Ventas continúan funcionando como en la Semana 15.
2. Con `daniel` (Administrador), la pestaña **Usuarios** muestra el
   formulario y la tabla completos.
3. Con `ariel` (Cliente) o `dareck` (Empleado), la pestaña **Usuarios**
   muestra únicamente el mensaje de acceso restringido, sin formulario
   ni tabla editable.
4. Se registró un usuario de prueba (`U010`, rol Empleado) y apareció de
   inmediato en el `Treeview`.
5. Al seleccionar su fila, `<<TreeviewSelect>>` cargó correctamente sus
   datos en el formulario.
6. Se modificó el nombre y se presionó "Actualizar": el cambio se
   reflejó en la tabla y en `usuarios.json`.
7. Se probó eliminar la cuenta con la que se inició sesión
   (`daniel`/`U001`): la operación fue **rechazada** con el mensaje
   correspondiente, confirmando que no puede eliminarse accidentalmente.
8. Se eliminó el usuario de prueba con confirmación previa
   (`messagebox.askyesno`) y dejó de aparecer en la tabla.
9. Se verificó que `<Return>`, estando el foco en cualquier campo del
   formulario, ejecuta el registro reutilizando `registrar_usuario()`.
10. Se verificó que `<Escape>` limpia el formulario y quita la selección
    de la tabla, reutilizando `limpiar_formulario_usuario()`.
11. Se verificó que seleccionar una opción en el Combobox de rol dispara
    `<<ComboboxSelected>>` y actualiza el mensaje de estado.
12. Se reinició la aplicación (nueva instancia de `RestauranteServicio`)
    y los usuarios registrados se recuperaron correctamente desde
    `usuarios.json`.
13. Se revisó el código fuente completo confirmando que no existen
    referencias a "libro" ni "biblioteca", y que ninguna vista importa
    el módulo `json`.
