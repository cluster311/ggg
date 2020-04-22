# Desambiguar vistas de turnos [#157](https://github.com/cluster311/ggg/issues/157#event-3237659836)

## `/turnos`

-   Se definen los turnos disponibles para los ciudadanos con el botón **Agregar turno**.
-   Blanco = Disponible
-   Azul = Asignado
-   Rojo claro = Cancelado por el establecimiento
-   Rojo oscuro = Cancelado por el paciente

![Turnos](https://i.imgur.com/cBwXlRc.png)

## `/agendar`

-   Permite ver los turnos disponibles por Especialidad en cada Centro de Salud
-   **Solamente se pueden agendar turnos** con el DNI del paciente.
-   Una vez agendado el turno no aparece más porque ya fue agendado.

![Agendar](https://i.imgur.com/vliGVIA.png)

## `/gestionar_turnos`

-   Parece una versión incompleta de `/agendar`
-   Se pueden agendar turnos sólo del día actual y filtrando por Especialidad
-   Después de agendar el turno **no emite comprobante (modal) para poder ser impreso**

![Gestionar](https://i.imgur.com/ZrDoSTi.png)
