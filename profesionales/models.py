from django.db import models


class Profesional(models.Model):
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120, null=True, blank=True)
    
    dni = models.CharField(max_length=20, null=True, blank=True)
    matricula_profesional = models.CharField(max_length=20, null=True, blank=True)

    profesion = models.CharField(max_length=190, null=True, blank=True)
    telefono = models.CharField(max_length=190, null=True, blank=True)
    domicilio = models.CharField(max_length=190, null=True, blank=True)
    
    def importar_matriculado(self, row):
        """ importar desde una base de datos específica matriculados 
        Ejemplo de row de Excel
            AFILIADO: 42000	
            NOMBRE: JUAN PEREZ	
            PROFESION: LIC. EN PSICOLOGIA            
            DOCUMENTO: 5556460	
            TELEFONO: 03555-555555	
            DOMICILIO: CHACO 31	
            BARRIO	
            LOCALIDAD: RIO CEBALLOS	
            DEPARTAMENTO: COLON	
            VOTA: S
        """
        self.nombres = row['NOMBRE'].strip()
        self.matricula_profesional = str(row['AFILIADO'])
        self.profesion = row['PROFESION'].strip()
        self.dni = str(row['DOCUMENTO'])
        self.telefono = row.get('TELEFONO', '').strip()
        domicilio = '{}, {}, {}, {}, Córdoba'.format(row.get('DOMICILIO', '').strip(),
                                                     row.get('BARRIO', ''),
                                                     row.get('LOCALIDAD', ''),
                                                     row.get('DEPARTAMENTO', ''))
        self.domicilio = domicilio

    
    def __str__(self):
        apellidos = '' if self.apellidos is None else self.apellidos
        return f'{self.nombres, apellidos}'

    class Meta:
        permissions = [
            ('can_view_tablero', 'Puede ver los tableros de comandos sobre profesionales'),
            ]