from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import datetime

class Personal(models.Model):
    TIPO_PERSONAL_CHOICES = [
        ('Medicos veterinarios', 'Medicos veterinarios'),
        ('Recepcionista', 'Recepcionista'),
        ('Encargado de acuario', 'Encargado de acuario'),
        ('Encargado de accesorios', 'Encargado de accesorios'),
        ('Encargado de articulos generales', 'Encargado de articulos generales'),
        ('Encargado de estetica', 'Encargado de estetica'),
    ]
    TURNO_CHOICES = [
        ('M', 'M'),
        ('V', 'V'),
    ]
    HORARIO_CHOICES = [
        ('8-4', '8-4'),
        ('1-9', '1-9'),
    ]

    id_personal = models.AutoField(primary_key=True)
    tipo_personal = models.CharField(max_length=35, choices=TIPO_PERSONAL_CHOICES, blank=True, null=True)
    cedula_profesional = models.CharField(max_length=20, unique=True, blank=True, null=True)
    especialidad = models.CharField(max_length=50, blank=True, null=True)
    nombre_completo = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    fecha_ingreso = models.DateTimeField()
    numero_telefonico = models.CharField(max_length=20)
    direccion = models.CharField(max_length=100)
    turno = models.CharField(max_length=2, choices=TURNO_CHOICES)
    horario = models.CharField(max_length=10, choices=HORARIO_CHOICES)
    salario_neto = models.DecimalField(max_digits=10, decimal_places=2)
    rfc = models.CharField(max_length=13, unique=True)
    curp = models.CharField(max_length=18, unique=True)
    class Meta:
        managed = False  # This line tells Django not to manage this table
        db_table = 'PERSONAL'  # This line tells Django the name of the existing table
    def __str__(self):
        return self.nombre_completo
    


class Nomina(models.Model):
    ID_nomina = models.AutoField(primary_key=True)
    ID_personal = models.ForeignKey(Personal, on_delete=models.CASCADE, db_column='ID_personal') 
    Horas_trabajadas = models.IntegerField()
    Horas_extras = models.IntegerField(default=0)
    Retardos = models.IntegerField(default=0)
    Faltas = models.IntegerField(default=0)
    Empleado_del_mes = models.BooleanField(default=False)
    Fecha_pago = models.DateTimeField()
    Tipo_pago = models.CharField(max_length=20)
    
    Salario_NETO = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False  # No queremos que Django gestione esta tabla
        db_table = 'NOMINA'  # Esto es el nombre exacto de la tabla en la base de datos

    def __str__(self):
        return self.ID_personal



class Propietarios(models.Model):
    ID_propietario = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)
    Apellido = models.CharField(max_length=50)
    Telefono = models.CharField(max_length=20)
    Direccion = models.CharField(max_length=100)
    Mascotas = models.IntegerField(null=True, blank=True)
    Correo_electronico = models.EmailField(max_length=50)
    class Meta:
        managed = False
        db_table = "PROPIETARIOS"



class Proveedores(models.Model):
    ID_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    # articulos_que_provee = models.TextField()  # Utilizamos TextField para mapear el tipo de datos CLOB de Oracle
    class Meta:
        managed = False  # No queremos que Django gestione esta tabla
        db_table = 'PROVEEDORES'  # Esto es el nombre exacto de la tabla en la base de datos
    def __str__(self):
        return self.nombre
    

class Inventario(models.Model):
    ID_producto = models.AutoField(primary_key=True)
    Nombre_producto = models.CharField(max_length=50)
    Area = models.CharField(max_length=30)
    Caracteristicas = models.TextField()
    Precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    Cantidad_inventario = models.IntegerField()
    Fecha_caducidad = models.TextField()
    Productos_descuento = models.IntegerField()
    Marca_producto = models.CharField(max_length=50, blank=True, null=True)
    Presentacion = models.CharField(max_length=30, blank=True, null=True)
    Fecha_compra = models.TextField()
    class Meta:
        managed = False  # No queremos que Django gestione esta tabla
        db_table = 'INVENTARIO'  # Esto es el nombre exacto de la tabla en la base de datos
    def __str__(self):
        return self.Nombre_producto

class ProveedoresProductos(models.Model):
    ID_proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, db_column='ID_proveedor')
    ID_producto = models.ForeignKey(Inventario, on_delete=models.CASCADE, db_column='ID_producto')
    class Meta:
        managed = False
        db_table = 'PROVEEDORESPRODUCTOS'
        unique_together = (('ID_proveedor', 'ID_producto'),)  # La combinación de ID_proveedor y ID_producto debe ser única
    def __str__(self):
        return f'{self.ID_proveedor} - {self.ID_producto}'
    


class Mascotas(models.Model):
    ID_mascota = models.AutoField(primary_key=True)
    ID_propietario = models.ForeignKey(Propietarios, on_delete=models.CASCADE, db_column='ID_propietario')
    Nombre = models.CharField(max_length=30)
    Tipo = models.CharField(max_length=30)
    Raza = models.CharField(max_length=30)
    Fecha_nacimiento = models.DateField()
    Color = models.CharField(max_length=20, null=True, blank=True)
    Sexo = models.CharField(max_length=1)
    Imagen = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        managed = False
        db_table = "MASCOTAS"



class Expedientes(models.Model):
    SEXO_OPCIONES = [("M", "Macho"), ("H", "Hembra")]
    ID_expediente = models.AutoField(db_column="ID_expediente", primary_key=True)
    ID_mascota = models.ForeignKey( Mascotas, on_delete=models.CASCADE, db_column="ID_mascota")
    ID_personal = models.ForeignKey( Personal, on_delete=models.CASCADE, db_column="ID_personal")
    Edad = models.IntegerField()
    Historial_clinico = models.TextField(null=True, blank=True)
    Cirugias = models.TextField(null=True, blank=True)
    Tratamientos = models.TextField(null=True, blank=True)
    Fecha_ingreso = models.DateTimeField()
    Fecha_egreso = models.DateTimeField(null=True, blank=True)
    Diagnostico = models.TextField(null=True, blank=True)
    Esquema_vacunacion = models.TextField(null=True, blank=True)
    Alergias = models.TextField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = "EXPEDIENTES"




class RecetasMedicas(models.Model):
    ID_receta = models.AutoField(primary_key=True)
    ID_mascota = models.ForeignKey(Mascotas, on_delete=models.CASCADE, db_column='ID_mascota')
    ID_personal = models.ForeignKey(Personal, on_delete=models.CASCADE, db_column='ID_personal') 
    Peso = models.DecimalField(max_digits=5, decimal_places=2)
    Medicamentos_recetados = models.TextField()
    Indicaciones_generales = models.TextField(blank=True, null=True)
    Fecha = models.DateTimeField()
    class Meta:
        managed = False  # No queremos que Django gestione esta tabla
        db_table = 'RECETASMEDICAS'  # Esto es el nombre exacto de la tabla en la base de datos
    def __str__(self):
        return str(self.ID_receta)



class Ventas(models.Model):
    ID_venta = models.AutoField(primary_key=True)
    ID_producto = models.ForeignKey(Inventario, on_delete=models.CASCADE, db_column='ID_producto')
    ID_personal = models.ForeignKey(Personal, on_delete=models.CASCADE, db_column='ID_personal')
    Cantidad_vendida = models.IntegerField()
    Total = models.DecimalField(max_digits=10, decimal_places=2) #  cambiamos el AutoField por un DecimalField
    Fecha_venta = models.DateTimeField()
    class Meta:
        managed = False  # No queremos que Django gestione esta tabla
        db_table = 'VENTAS'  # Esto es el nombre exacto de la tabla en la base de datos
    def __str__(self):
        return str(self.ID_venta)




























# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " - by " + self.user.username


class Pet(models.Model):
    nombre = models.CharField(max_length=100)  # campos existente
    edad = models.IntegerField()
    sexo = models.CharField(max_length=100)
    raza = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    nombre_propietario = models.CharField(max_length=100)
    telefono_propietario = models.CharField(max_length=100)
    direccion_propietario = models.CharField(max_length=100)
    historial = models.CharField(max_length=100)
    cirugias = models.CharField(max_length=100)
    tratamientos = models.CharField(max_length=100)
    fechas_egreso = models.CharField(max_length=100)
    diagnostico = models.CharField(max_length=100)
    esquema_vacunas = models.CharField(max_length=100)
    alergias = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.nombre