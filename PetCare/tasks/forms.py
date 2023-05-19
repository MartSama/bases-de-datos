from django import forms
from .models import (
    Pet,
    Task,
    Personal,
    Nomina,
    Propietarios,
    Expedientes,
    Mascotas,
    Proveedores,
    ProveedoresProductos,
    Inventario,
    RecetasMedicas,
    Ventas,)



class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = [
            "tipo_personal",
            "cedula_profesional",
            "especialidad",
            "nombre_completo",
            "fecha_nacimiento",
            "fecha_ingreso",
            "numero_telefonico",
            "direccion",
            "turno",
            "horario",
            "salario_neto",
            "rfc",
            "curp",]
        widgets = {
            "tipo_personal": forms.Select(attrs={"class": "form-control", "id": "id_tipo_personal"}),
            "cedula_profesional": forms.TextInput(attrs={"class": "form-control", "id": "id_cedula_profesional"}),
            "especialidad": forms.TextInput(attrs={"class": "form-control", "id": "id_especialidad"}),
            "nombre_completo": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_nacimiento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"} ),
            "fecha_ingreso": forms.DateInput(
                attrs={"class": "form-control", "type": "date"} ),
            "numero_telefonico": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "turno": forms.Select(attrs={"class": "form-control"}),
            "horario": forms.Select(attrs={"class": "form-control"}),
            "salario_neto": forms.TextInput(attrs={"class": "form-control"}),
            "rfc": forms.TextInput(attrs={"class": "form-control"}),
            "curp": forms.TextInput(attrs={"class": "form-control"}),}
        
    def clean(self):
        cleaned_data = super().clean()
        tipo_personal = cleaned_data.get('tipo_personal')
        cedula_profesional = cleaned_data.get('cedula_profesional')
        especialidad = cleaned_data.get('especialidad')

        if tipo_personal == 'Medicos veterinarios':
            if not cedula_profesional or not especialidad:
                raise forms.ValidationError('Para médicos veterinarios se requiere cedula profesional y especialidad.')
        else:
            if cedula_profesional or especialidad:
                raise forms.ValidationError('Los campos cedula profesional y especialidad deben ser nulos para otros roles.')

        

        



class PropietarioForm(forms.ModelForm):
    class Meta:
        model = Propietarios
        fields = ["Nombre", "Apellido", "Telefono", "Direccion", "Correo_electronico"]
        widgets = {
            "Nombre": forms.TextInput(attrs={"class": "form-control"}),
            "Apellido": forms.TextInput(attrs={"class": "form-control"}),
            "Telefono": forms.TextInput(attrs={"class": "form-control"}),
            "Direccion": forms.TextInput(attrs={"class": "form-control"}),
            "Correo_electronico": forms.EmailInput(attrs={"class": "form-control"}),}
        labels = {
            "Nombre": "Nombre",
            "Apellido": "Apellido",
            "Telefono": "Teléfono",
            "Direccion": "Dirección",
            "Correo_electronico": "Correo Electrónico",}



class ProveedoresForm(forms.ModelForm):
    class Meta:
        model = Proveedores
        fields = ["nombre", "direccion", "telefono",]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            }
        labels = {
            "nombre": "Nombre",
            "direccion": "Dirección",
            "telefono": "Teléfono",
            }

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = [
            "Nombre_producto", #--
            "Area",             #--
            "Caracteristicas", #--
            "Precio_unitario",  #--
            "Cantidad_inventario", #--
            "Fecha_caducidad",
            "Productos_descuento", #--
            "Marca_producto", #--
            "Presentacion",
            "Fecha_compra",]
        widgets = {
            "Nombre_producto": forms.TextInput(attrs={"class": "form-control"}),
            "Area": forms.TextInput(attrs={"class": "form-control"}),
            
            "Caracteristicas": forms.Textarea(attrs={"class": "form-control"}),
            "Precio_unitario": forms.NumberInput(attrs={"class": "form-control"}),
            "Cantidad_inventario": forms.NumberInput(attrs={"class": "form-control"}),
            "Fecha_caducidad": forms.Textarea(attrs={"class": "form-control"}),
            "Productos_descuento": forms.NumberInput(attrs={"class": "form-control"}),
            "Marca_producto": forms.TextInput(attrs={"class": "form-control"}),
            "Presentacion": forms.TextInput(attrs={"class": "form-control"}),
            "Fecha_compra": forms.Textarea(attrs={"class": "form-control"}),}
        labels = {
            
            "Nombre_producto": "Nombre del Producto",
            "Area": "Area",
            "Caracteristicas": "Características",
            "Precio_unitario": "Precio Unitario",
            "Cantidad_inventario": "Cantidad en Inventario",
            "Fecha_caducidad": "Fecha de Caducidad",
            "Productos_descuento": "Productos en Descuento",
            "Marca_producto": "Marca del Producto",
            "Presentacion": "Presentación",
            "Fecha_compra": "Fecha de Compra",}



class ProveedoresProductosForm(forms.ModelForm):
    class Meta:
        model = ProveedoresProductos
        fields = ['ID_proveedor', 'ID_producto']
        widgets = {
            'ID_proveedor': forms.Select(attrs={'class': 'form-control'}),
            'ID_producto': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'ID_proveedor': 'ID Proveedor',
            'ID_producto': 'ID Producto',
        }





class NominaForm(forms.ModelForm):
    class Meta:
        model = Nomina
        fields = [
            "ID_personal",
            "Fecha_pago",
            "Tipo_pago",
            "Horas_trabajadas",
            "Horas_extras",
            "Retardos",
            "Faltas",
            "Empleado_del_mes",]
        widgets = {
            "ID_personal": forms.Select(attrs={"class": "form-control"}),
            "Fecha_pago": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "date"}),
            "Tipo_pago": forms.TextInput(attrs={"class": "form-control"}),
            "Horas_trabajadas": forms.NumberInput(attrs={"class": "form-control"}),
            "Horas_extras": forms.NumberInput(attrs={"class": "form-control"}),
            "Retardos": forms.NumberInput(attrs={"class": "form-control"}),
            "Faltas": forms.NumberInput(attrs={"class": "form-control"}),
            "Empleado_del_mes": forms.CheckboxInput(attrs={"class": "form-check"}),}
        labels = {
            "ID_personal": "Personal",
            "Fecha_pago": "Fecha de Pago",
            "Tipo_pago": "Tipo de Pago",
            "Horas_trabajadas": "Horas Trabajadas",
            "Horas_extras": "Horas Extras",
            "Retardos": "Retardos",
            "Faltas": "Faltas",
            "Empleado_del_mes": "¿Empleado del Mes?", }

class MascotaForm(forms.ModelForm):
    SEXO_CHOICES = [("M", "M"), ("H", "H")]
    Sexo = forms.ChoiceField( choices=SEXO_CHOICES, widget=forms.Select(attrs={"class": "form-control"}))
    class Meta:
        model = Mascotas
        fields = [
            "ID_propietario",
            "Nombre",
            "Tipo",
            "Raza",
            "Fecha_nacimiento",
            "Color",
            "Sexo",
            "Imagen", ]
        widgets = {
            "ID_propietario": forms.Select(attrs={"class": "form-control"}),
            "Nombre": forms.TextInput(attrs={"class": "form-control"}),
            "Tipo": forms.TextInput(attrs={"class": "form-control"}),
            "Raza": forms.TextInput(attrs={"class": "form-control"}),
            "Fecha_nacimiento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"} ),
            "Color": forms.TextInput(attrs={"class": "form-control"}),
            "Sexo": forms.Select(attrs={"class": "form-control"}),
            "Imagen": forms.FileInput(attrs={"class": "form-control"}), }
        labels = {
            "ID_propietario": "Propietario",
            "Nombre": "Nombre de la Mascota",
            "Tipo": "Tipo",
            "Raza": "Raza",
            "Fecha_nacimiento": "Fecha de Nacimiento",
            "Color": "Color",
            "Sexo": "Sexo",
            "Imagen": "Imagen",}

class ExpedienteForm(forms.ModelForm):
    class Meta:
        model = Expedientes
        fields = [\
            "ID_mascota",
            "ID_personal",
            "Edad",
            "Historial_clinico",
            "Cirugias",
            "Tratamientos",
            "Fecha_ingreso",
            "Fecha_egreso",
            "Diagnostico",
            "Esquema_vacunacion",
            "Alergias" 
            ]
        widgets = {
            "ID_mascota": forms.Select(attrs={"class": "form-control"}),
            "ID_personal": forms.Select(attrs={"class": "form-control"}),
            "Edad": forms.NumberInput(attrs={"class": "form-control"}),
            "Historial_clinico": forms.Textarea(attrs={"class": "form-control"}),
            "Cirugias": forms.Textarea(attrs={"class": "form-control"}),
            "Tratamientos": forms.Textarea(attrs={"class": "form-control"}),
            "Fecha_ingreso": forms.DateInput(
                attrs={"class": "form-control", "type": "date"} ),
            "Fecha_egreso": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "date"}),
            "Diagnostico": forms.Textarea(attrs={"class": "form-control"}),
            "Esquema_vacunacion": forms.Textarea(attrs={"class": "form-control"}),
            "Alergias": forms.Textarea(attrs={"class": "form-control"}),}
        labels = {
            "ID_mascota": "Nombre de la Mascota",
            "ID_personal": "Personal",
            "Edad": "Edad",
            "Historial_clinico": "Historial Clínico",
            "Cirugias": "Cirugías",
            "Tratamientos": "Tratamientos",
            "Fecha_ingreso": "Fecha de Ingreso",
            "Fecha_egreso": "Fecha de Egreso",
            "Diagnostico": "Diagnóstico",
            "Esquema_vacunacion": "Esquema de Vacunación",
            "Alergias": "Alergias", }

class RecetasMedicasForm(forms.ModelForm):
    class Meta:
        model = RecetasMedicas
        fields = [
            "ID_mascota",
            "ID_personal",
            "Peso",
            "Medicamentos_recetados",
            "Indicaciones_generales",
            "Fecha", ]
        widgets = {
            "ID_mascota": forms.Select(attrs={"class": "form-control"}),
            "ID_personal": forms.Select(attrs={"class": "form-control"}),
            "Peso": forms.NumberInput(attrs={"class": "form-control"}),
            "Medicamentos_recetados": forms.Textarea(attrs={"class": "form-control"}),
            "Indicaciones_generales": forms.Textarea(attrs={"class": "form-control"}),
            "Fecha": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "date"} ),}
        labels = {
            "ID_mascota": "ID Mascota",
            "ID_personal": "ID Personal",
            "Peso": "Peso",
            "Medicamentos_recetados": "Medicamentos Recetados",
            "Indicaciones_generales": "Indicaciones Generales",
            "Fecha": "Fecha",}


class VentasForm(forms.ModelForm):
    class Meta:
        model = Ventas
        fields = [
            "ID_producto",
            "ID_personal",
            "Cantidad_vendida",
            "Fecha_venta", 
        ]
        widgets = {
            "ID_producto": forms.Select(attrs={"class": "form-control"}),
            "ID_personal": forms.Select(attrs={"class": "form-control"}),
            "Cantidad_vendida": forms.NumberInput(attrs={"class": "form-control"}),
            "Fecha_venta": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "date"} ), 
        }
        labels = {
            "ID_producto": "Producto",
            "ID_personal": "Personal",
            "Cantidad_vendida": "Cantidad Vendida",
            "Fecha_venta": "Fecha de Venta",
        }







#   Extras  #

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "important"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Escribe un titulo"} ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escribe una descripcion",}),
            "important": forms.CheckboxInput(
                attrs={"class": "form-check-input m-auto"} ),}

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            "nombre",
            "edad",
            "sexo",
            "raza",
            "color",
            "nombre_propietario",
            "telefono_propietario",
            "direccion_propietario",
            "historial",
            "cirugias",
            "tratamientos",
            "fechas_egreso",
            "diagnostico",
            "esquema_vacunas",
            "alergias",]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre de la mascota"}
            ),
            "edad": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Edad de la mascota"}
            ),
            "sexo": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Sexo de la mascota"}
            ),
            "raza": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Raza de la mascota"}
            ),
            "color": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Color de la mascota"}
            ),
            "nombre_propietario": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre del Propietario"}
            ),
            "telefono_propietario": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Raza de la mascota"}
            ),
            "direccion_propietario": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Color de la mascota"}
            ),
            "historial": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Color de la mascota"}
            ),
            "cirugias": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Color de la mascota"}
            ),
            "tratamientos": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Color de la mascota"}
            ),
            "fechas_egreso": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Color de la mascota"}
            ),
            "diagnostico": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Color de la mascota"}
            ),
            "esquema_vacunas": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Color de la mascota"}
            ),
            "alergias": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Color de la mascota"}
            ),}
