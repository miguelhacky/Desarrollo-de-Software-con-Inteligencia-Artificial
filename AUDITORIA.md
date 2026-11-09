# Auditoría del prototipo

Fecha: 2026-11-09  
Alcance: aplicación local con datos ficticios.

## Resultado funcional

- La aplicación inicia en `http://127.0.0.1:5000` y devuelve HTTP 200.
- Se pudo registrar `ana@example.com`, iniciar sesión y crear la tarea `Revisar auditoría`.

## Hallazgos

| Severidad | Ubicación | Hallazgo | Riesgo |
|---|---|---|---|
| Alta | `app.py:5` | La clave de sesión está escrita en el código. | Permite falsificar sesiones si el código se expone. |
| Alta | `app.py:46-62` | Las contraseñas se guardan y comparan en texto plano. | Una filtración de la base de datos revela las credenciales. |
| Alta | `app.py:83,92` | Actualizar o eliminar una tarea solo usa el ID; no valida `user_id`. | Un usuario podría modificar tareas de otro. |
| Media | `app.py:105` | El modo debug está activado. | Puede revelar información sensible mediante el depurador. |
| Media | Proyecto | No existe `tests/` ni una prueba automatizada. | Los errores pueden reaparecer sin ser detectados. |
| Media | `register` y `create_task` | No hay validación de campos vacíos ni límites de longitud. | Datos inválidos o entradas excesivas. |

## Conclusión

El prototipo funciona para el flujo feliz, pero no está listo para entregarse. Antes de producción se deben corregir los hallazgos, agregar pruebas automatizadas y repetir la auditoría.

