# Desambiguar vistas de turnos [#157](https://github.com/cluster311/ggg/issues/157#event-3237659836)

## `/turnos`

-   Se definen los turnos disponibles para los ciudadanos con el botón **Agregar turno**.
-   Blanco = Disponible
-   Azul = Asignado
-   Rojo claro = Cancelado por el establecimiento
-   Rojo oscuro = Cancelado por el paciente

## `/agendar`

-   Permite ver los turnos disponibles por Especialidad en cada Centro de Salud
-   **Solamente se pueden agendar turnos** con el DNI del paciente.
-   Una vez agendado el turno no aparece más porque ya fue agendado.

## `/gestionar_turnos`

-   Parece una versión incompleta de `/agendar`
-   Se pueden agendar turnos sólo del día actual y filtrando por Especialidad
-   Después de agendar el turno **no emite comprobante (modal) para poder ser impreso**

---

## To-do

### 1. Asignar permiso gestionar turno GRUPO_ADMIN

Según el manual un usuario administrativo puede gestionar turnos:

-   [ ] Asignarle permiso para gestionar turno a GRUPO_ADMIN. [Línea en el repo](https://github.com/cluster311/ggg/blob/e9f853f8134df65e6addaae634970347ab8a7857/core/base_permission.py#L26)
-   Arriba está comentada la creación del permiso gestionar turno

### 2. Se puede acceder a **/turnos/gestionar_turnos/asd**

-   Tiene que ver con el funcionamiento de los url de Django?

### 3. Datos de prueba

-   [ ] Crear un paciente de prueba para poder asignar un turno

### 4. Bug CSS

-   Modal al hacer click sobre un turno

### 5. Bug de Javascript en **/turnos/agendar**?

1. Ir a /turnos/agendar
2. Elegir Servicio (Yo elegí Centro de Salud 1)

Parece que cuando se elige el centro de salud, el calendario semanal con turnos se superpone al que está originalmente y lo deja abajo.
