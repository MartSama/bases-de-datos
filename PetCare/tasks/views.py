
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import (
    TaskForm, PetForm, PersonalForm, PropietarioForm, ExpedienteForm, NominaForm, VentasForm,)
from .models import Task, Pet, Personal, Propietarios, Expedientes, Nomina, Ventas
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from tasks.views import Pet
from .models import Mascotas, Proveedores, Inventario, RecetasMedicas, ProveedoresProductos
from .forms import MascotaForm, ProveedoresForm, InventarioForm, RecetasMedicasForm, ProveedoresProductosForm
from django.db import connection,transaction

###     Home   ######################
def home(request):
    return render(request, "home.html")

###     Registrarse   ####################
def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_superuser(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("/")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Usuario ya existe."},
                )
        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "Contraseñas no coinciden"},
        )


###     Personal   ######################
@login_required
def personal(request):
    if request.method == "POST":
        form = PersonalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("personal")
        else:
            print(form.errors)  # Imprimir los errores de validación
    else:
        form = PersonalForm()
    personal = Personal.objects.all().order_by("id_personal")
    return render(request, "personal.html", {"personal": personal, "form": form})
#
@login_required
def personals_view(request):
    if request.method == 'POST':
        form = PersonalForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Personal (Tipo_personal, Cedula_profesional, Especialidad, Nombre_completo,
                    Fecha_nacimiento, Fecha_ingreso, Numero_telefonico, Direccion, Turno, Horario, Salario_neto, RFC, CURP)
                    VALUES (:Tipo_personal, :Cedula_profesional, :Especialidad, :Nombre_completo,
                    :Fecha_nacimiento, :Fecha_ingreso, :Numero_telefonico, :Direccion, :Turno, :Horario, :Salario_neto, :RFC, :CURP)
                """, {
                    'Tipo_personal': form.cleaned_data['tipo_personal'],
                    'Cedula_profesional': form.cleaned_data['cedula_profesional'],
                    'Especialidad': form.cleaned_data['especialidad'],
                    'Nombre_completo': form.cleaned_data['nombre_completo'],
                    'Fecha_nacimiento': form.cleaned_data['fecha_nacimiento'],
                    'Fecha_ingreso': form.cleaned_data['fecha_ingreso'],
                    'Numero_telefonico': form.cleaned_data['numero_telefonico'],
                    'Direccion': form.cleaned_data['direccion'],
                    'Turno': form.cleaned_data['turno'],
                    'Horario': form.cleaned_data['horario'],
                    'Salario_neto': form.cleaned_data['salario_neto'],
                    'RFC': form.cleaned_data['rfc'],
                    'CURP': form.cleaned_data['curp'],})
            form = PersonalForm()  # Limpiar el formulario después de guardar los datos
    else:
        form = PersonalForm()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Personal ORDER BY id_personal")
        rows = cursor.fetchall()
        # Obtén los nombres de las columnas de la tabla
        columns = [col[0] for col in cursor.description]
        print(columns)  # Imprime los nombres de las columnas
        # Convierte cada fila en un diccionario
        personals = [dict(zip(columns, row)) for row in rows]
    return render(request, 'personals.html', {'personals': personals, 'form': form})


###     Nomina      #####################
@login_required
def nomina(request):
    if request.method == "POST":
        form = NominaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("nomina")
        else:
            print(form.errors)  # Imprimir los errores de validación
    else:
        form = NominaForm()
    nomina = Nomina.objects.all().order_by("ID_nomina")
    return render(request, "nomina.html", {"nomina": nomina, "form": form})
##
@login_required
def nomina_s(request):
    if request.method == "POST":
        form = NominaForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                print({
                    'ID_personal': form.cleaned_data['ID_personal'],
                    'Horas_trabajadas': form.cleaned_data['Horas_trabajadas'],
                    'Horas_extras': form.cleaned_data['Horas_extras'],
                    'Retardos': form.cleaned_data['Retardos'],
                    'Faltas': form.cleaned_data['Faltas'],
                    'Empleado_del_mes': form.cleaned_data['Empleado_del_mes'],
                    'Fecha_pago': form.cleaned_data['Fecha_pago'],
                    'Tipo_pago': form.cleaned_data['Tipo_pago']

                })
                cursor.execute("""
                    INSERT INTO Nomina (ID_personal, Horas_trabajadas, Horas_extras, Retardos, Faltas, Empleado_del_mes, Fecha_pago, Tipo_pago)
                    VALUES (:ID_personal, :Horas_trabajadas, :Horas_extras, :Retardos, :Faltas, :Empleado_del_mes, :Fecha_pago, :Tipo_pago)
                """, {
                    'ID_personal': form.cleaned_data['ID_personal'].id_personal,
                    'Horas_trabajadas': form.cleaned_data['Horas_trabajadas'],
                    'Horas_extras': form.cleaned_data['Horas_extras'],
                    'Retardos': form.cleaned_data['Retardos'],
                    'Faltas': form.cleaned_data['Faltas'],
                    'Empleado_del_mes': form.cleaned_data['Empleado_del_mes'],
                    'Fecha_pago': form.cleaned_data['Fecha_pago'],
                    'Tipo_pago': form.cleaned_data['Tipo_pago'],})
            form = NominaForm()  # Clear form after saving data
    else:
        form = NominaForm()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Nomina.*, Personal.Nombre_completo 
            FROM Nomina 
            INNER JOIN Personal ON Nomina.ID_personal = Personal.ID_personal
            ORDER BY Nomina.ID_nomina
        """)
        rows = cursor.fetchall()
        # Get table column names
        columns = [col[0] for col in cursor.description]
        print(columns)  # Print column names
        # Convert each row into a dictionary
        nomina = [dict(zip(columns, row)) for row in rows]
    return render(request, 'nomina_s.html', {'nomina': nomina, 'form': form})
############################





###     PROPIETARIOS    #####################
@login_required
def propietarios(request):
    if request.method == "POST":
        form = PropietarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("propietarios")
    else:
        form = PropietarioForm()

    propietarios = Propietarios.objects.all()
    return render(
        request, "propietarios.html", {"propietarios": propietarios, "form": form})
###     SQL


@login_required
def propietarios_s(request):
    if request.method == 'POST':
        form = PropietarioForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
					INSERT INTO Propietarios (Nombre, Apellido, Telefono, Direccion, Correo_electronico)
					VALUES (:Nombre, :Apellido, :Telefono, :Direccion, :Correo_electronico)
                """,{
			        'Nombre': form.cleaned_data['Nombre'], 
                    'Apellido': form.cleaned_data['Apellido'],
			        'Telefono': form.cleaned_data['Telefono'],
			        'Direccion': form.cleaned_data['Direccion'],
			        'Correo_electronico': form.cleaned_data['Correo_electronico'],})
                form = PropietarioForm()    
    else:
        form = PropietarioForm()

    with connection.cursor() as cursor:
        cursor.execute(""" 
        SELECT * FROM Propietarios ORDER BY ID_PROPIETARIO""")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        print(columns)
        propietarios_s = [dict(zip(columns,row)) for row in rows]
    return render(request, 'propietarios_s.html',{'propietarios_s':propietarios_s, 'form': form})



###     Proveedores   ######################
@login_required
def proveedores(request):
    if request.method == "POST":
        form = ProveedoresForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("proveedores")
        else:
            print(form.errors)  # Imprimir los errores de validación
    else:
        form = ProveedoresForm()
    proveedores = Proveedores.objects.all().order_by("ID_proveedor")
    return render(
        request, "proveedores.html", {"proveedores": proveedores, "form": form}
    )
###     Sql     ###
@login_required
def proveedores_s(request):
    if request.method == 'POST':
        form = ProveedoresForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Proveedores (Nombre, Direccion, Telefono)
                    VALUES (:Nombre, :Direccion, :Telefono)
                """, {
                    'Nombre': form.cleaned_data['nombre'],
                    'Direccion': form.cleaned_data['direccion'],
                    'Telefono': form.cleaned_data['telefono'],})
            form = ProveedoresForm()  # Limpiar el formulario después de guardar los datos
    else:
        form = ProveedoresForm()
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_PROVEEDOR, NOMBRE, DIRECCION, TELEFONO FROM Proveedores ORDER BY ID_PROVEEDOR")
        rows = cursor.fetchall()
        # Obtén los nombres de las columnas de la tabla
        columns = [col[0] for col in cursor.description]
        print(columns)  # Imprime los nombres de las columnas
        # Convierte cada fila en un diccionario
        proveedores = [dict(zip(columns, row)) for row in rows]
        print(proveedores)  # Añadido para depurar
    return render(request, 'proveedores_s.html', {'proveedores_s': proveedores, 'form': form})






###     Inventario    ######################
@login_required
def inventario(request):
    if request.method == "POST":
        form = InventarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventario")
        else:
            print(form.errors)  # Imprimir los errores de validación
    else:
        form = InventarioForm()
    inventario = Inventario.objects.all().order_by("ID_producto")
    return render(request, "inventario.html", {"inventario": inventario, "form": form})
# ###     SQL         ###
@login_required
def inventario_s(request):
    form = InventarioForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                     INSERT INTO Inventario (Nombre_producto, Area, Caracteristicas, Precio_unitario, Cantidad_inventario, Fecha_caducidad, Productos_descuento, Marca_producto, Presentacion, Fecha_compra)
                    VALUES (:Nombre_producto, :Area, :Caracteristicas, :Precio_unitario, :Cantidad_inventario, :Fecha_caducidad, :Productos_descuento, :Marca_producto, :Presentacion, :Fecha_compra)
                """, {
                     'Nombre_producto': form.cleaned_data['Nombre_producto'],
                    'Area': form.cleaned_data['Area'],
                    'Caracteristicas': form.cleaned_data['Caracteristicas'],
                    'Precio_unitario': form.cleaned_data['Precio_unitario'],
                    'Cantidad_inventario': form.cleaned_data['Cantidad_inventario'],
                    'Fecha_caducidad': form.cleaned_data['Fecha_caducidad'],
                    'Productos_descuento': form.cleaned_data['Productos_descuento'],
                    'Marca_producto': form.cleaned_data['Marca_producto'],
                    'Presentacion': form.cleaned_data['Presentacion'],
                    'Fecha_compra': form.cleaned_data['Fecha_compra'],
                })
                transaction.commit()
                id_producto = cursor.lastrowid
                print(f"ID_producto generado: {id_producto}")
            form = InventarioForm()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Inventario ORDER BY ID_producto")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        inventario = [dict(zip(columns, row)) for row in rows]
    if request.method != 'POST':
        form = InventarioForm()
    return render(request, 'inventario_s.html', {'inventario': inventario, 'form': form})


#############################################################

@login_required
def proveedores_productos_s(request):
    form_pp = ProveedoresProductosForm(request.POST or None)
    if request.method == 'POST':
        if form_pp.is_valid():
            with connection.cursor() as cursor:
                id_proveedor = form_pp.cleaned_data['ID_proveedor'].ID_proveedor
                id_producto = form_pp.cleaned_data['ID_producto'].ID_producto
                try:
                    cursor.execute("""
                        INSERT INTO ProveedoresProductos (ID_proveedor, ID_producto)
                        VALUES (:ID_proveedor, :ID_producto)
                    """, {
                        'ID_proveedor': id_proveedor,
                        'ID_producto': id_producto,
                    })
                    transaction.commit()
                except Exception as e:
                    print(f"Error al insertar en proveedores productos {e}")
                form_pp = ProveedoresProductosForm()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT pp.ID_proveedor, p.Nombre, pp.ID_producto, pr.Nombre_producto
            FROM ProveedoresProductos pp
            INNER JOIN Proveedores p ON pp.ID_proveedor = p.ID_proveedor
            INNER JOIN Inventario pr ON pp.ID_producto = pr.ID_producto
            """)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        proveedores_productos = [dict(zip(columns, row)) for row in rows]
    if request.method != 'POST':
        form_pp = ProveedoresProductosForm()
    return render(request, 'proveedores_productos_s.html', {'proveedores_productos': proveedores_productos, 'form_pp': form_pp})







###     Mascotas    ######################
def mascotas(request):
    if request.method == "POST":
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = MascotaForm()
    mascotas = Mascotas.objects.all()
    return render(request, "mascotas.html", {"form": form, "mascotas": mascotas})
###     SQL      ################
@login_required
def mascotas_s(request):
    form = MascotaForm(request.POST, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            with connection.cursor() as cursor:
                # Manejo de la imagen
                imagen = request.FILES['Imagen']
                fs = FileSystemStorage()
                filename = fs.save(imagen.name, imagen)
                upload_file_url = fs.url(filename)

                print({
                    'ID_propietario': form.cleaned_data['ID_propietario'],  
                    'Nombre': form.cleaned_data['Nombre'],
                    'Tipo': form.cleaned_data['Tipo'],
                    'Raza': form.cleaned_data['Raza'],
                    'Fecha_nacimiento': form.cleaned_data['Fecha_nacimiento'],
                    'Color': form.cleaned_data['Color'],
                    'Sexo': form.cleaned_data['Sexo'],
                    'Imagen': upload_file_url,
                })

                cursor.execute("""
                    INSERT INTO Mascotas (ID_propietario, Nombre, Tipo, Raza, Fecha_nacimiento, Color, Sexo, Imagen)
                    VALUES (:ID_propietario, :Nombre, :Tipo, :Raza, :Fecha_nacimiento, :Color, :Sexo, :Imagen)
                """, {
                    'ID_propietario': form.cleaned_data['ID_propietario'].ID_propietario,
                    'Nombre': form.cleaned_data['Nombre'],
                    'Tipo': form.cleaned_data['Tipo'],
                    'Raza': form.cleaned_data['Raza'],
                    'Fecha_nacimiento': form.cleaned_data['Fecha_nacimiento'],
                    'Color': form.cleaned_data['Color'],
                    'Sexo': form.cleaned_data['Sexo'],
                    'Imagen': upload_file_url,
                })
                transaction.commit()
                id_mascota = cursor.lastrowid
                print(f"ID_mascota generado: {id_mascota}")
            form = MascotaForm()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT m.ID_mascota, m.Nombre, p.Nombre AS nombre_propietario, p.Apellido AS apellido_propietario, m.Tipo, m.Raza, m.Fecha_nacimiento, m.Color, m.Sexo, m.Imagen 
            FROM Mascotas m
            INNER JOIN Propietarios p ON m.ID_propietario = p.ID_propietario
            ORDER BY m.ID_mascota
        """)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        mascotas = [dict(zip(columns, row)) for row in rows]
    if request.method != 'POST':
        form = MascotaForm()
    return render(request, 'mascotas_s.html', {'mascotas': mascotas, 'form': form})












###     Expedientes     ############################3
@login_required
def expedientes(request):
    expedientes = Expedientes.objects.all()
    if request.method == "POST":
        form = ExpedienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("expedientes")
    else:
        form = ExpedienteForm()
    return render(
        request, "expedientes.html", {"expedientes": expedientes, "form": form}
    )
###     SQL     ####
@login_required
def expedientes_s(request):
    form = ExpedienteForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Expedientes (
                        ID_mascota,
                        ID_personal,
                        Edad,
                        Historial_clinico,
                        Cirugias,
                        Tratamientos,
                        Fecha_ingreso,
                        Fecha_egreso,
                        Diagnostico,
                        Esquema_vacunacion,
                        Alergias
                    ) VALUES (
                        :ID_mascota,
                        :ID_personal,
                        :Edad,
                        :Historial_clinico,
                        :Cirugias,
                        :Tratamientos,
                        :Fecha_ingreso,
                        :Fecha_egreso,
                        :Diagnostico,
                        :Esquema_vacunacion,
                        :Alergias
                    )
                """, {
                    'ID_mascota': form.cleaned_data['ID_mascota'].ID_mascota,
                    'ID_personal': form.cleaned_data['ID_personal'].id_personal,
                    'Edad': form.cleaned_data['Edad'],
                    'Historial_clinico': form.cleaned_data['Historial_clinico'],
                    'Cirugias': form.cleaned_data['Cirugias'],
                    'Tratamientos': form.cleaned_data['Tratamientos'],
                    'Fecha_ingreso': form.cleaned_data['Fecha_ingreso'],
                    'Fecha_egreso': form.cleaned_data['Fecha_egreso'],
                    'Diagnostico': form.cleaned_data['Diagnostico'],
                    'Esquema_vacunacion': form.cleaned_data['Esquema_vacunacion'],
                    'Alergias': form.cleaned_data['Alergias'],
                })
                transaction.commit()
                id_expediente = cursor.lastrowid
                print(f"ID_expediente generado: {id_expediente}")
            form = ExpedienteForm()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT e.*, m.Nombre as nombre_mascota, p.Nombre_completo as nombre_personal,
            m.Sexo as sexo_mascota, m.Raza as raza_mascota, m.Color as color_mascota
            FROM Expedientes e
            INNER JOIN Mascotas m ON e.ID_mascota = m.ID_mascota
            INNER JOIN Personal p ON e.ID_personal = p.ID_personal
            ORDER BY e.ID_expediente
        """)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        expedientes = [dict(zip(columns, row)) for row in rows]
    if request.method != 'POST':
        form = ExpedienteForm()
    return render(request, 'expedientes_s.html', {'expedientes': expedientes, 'form': form})








###     Recetas     ##############
@login_required
def recetasMedicas(request):
    if request.method == "POST":
        form = RecetasMedicasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("recetasMedicas")
        else:
            print(form.errors)  # Imprimir los errores de validación
    else:
        form = RecetasMedicasForm()
    recetasMedicas = RecetasMedicas.objects.all().order_by("ID_receta")
    return render(
        request, "recetasMedicas.html", {"recetasMedicas": recetasMedicas, "form": form}
    )
###     SQL     #######################
@login_required
def recetasMedicas_s(request):
    form = RecetasMedicasForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            with connection.cursor() as cursor:
                print({
                    'ID_mascota': form.cleaned_data['ID_mascota'],  
                    'ID_personal': form.cleaned_data['ID_personal'],
                    'Peso': form.cleaned_data['Peso'],
                    'Medicamentos_recetados': form.cleaned_data['Medicamentos_recetados'],
                    'Indicaciones_generales': form.cleaned_data['Indicaciones_generales'],
                    'Fecha': form.cleaned_data['Fecha'],
                })

                cursor.execute("""
                    INSERT INTO RecetasMedicas (ID_mascota, ID_personal, Peso, Medicamentos_recetados, Indicaciones_generales, Fecha)
                    VALUES (:ID_mascota, :ID_personal, :Peso, :Medicamentos_recetados, :Indicaciones_generales, :Fecha)
                """, {
                    'ID_mascota': form.cleaned_data['ID_mascota'].ID_mascota,
                    'ID_personal': form.cleaned_data['ID_personal'].id_personal,
                    'Peso': form.cleaned_data['Peso'],
                    'Medicamentos_recetados': form.cleaned_data['Medicamentos_recetados'],
                    'Indicaciones_generales': form.cleaned_data['Indicaciones_generales'],
                    'Fecha': form.cleaned_data['Fecha'],
                })
                transaction.commit()
                id_receta = cursor.lastrowid
                print(f"ID_receta generado: {id_receta}")
            form = RecetasMedicasForm()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.ID_receta, r.Peso, r.Medicamentos_recetados, r.Indicaciones_generales, r.Fecha, m.ID_mascota, m.Nombre AS nombre_mascota, p.ID_personal, p.Nombre_completo AS nombre_personal 
            FROM RecetasMedicas r
            INNER JOIN Mascotas m ON r.ID_mascota = m.ID_mascota
            INNER JOIN Personal p ON r.ID_personal = p.ID_personal
            ORDER BY r.ID_receta
        """)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        recetasMedicas = [dict(zip(columns, row)) for row in rows]
    if request.method != 'POST':
        form = RecetasMedicasForm()
    return render(request, 'recetasMedicas_s.html', {'recetasMedicas': recetasMedicas, 'form': form})














###     Ventas      ############
@login_required
def ventas(request):
    if request.method == "POST":
        form = VentasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ventas")
        else:
            print(form.errors)  # Imprimir los errores de validación
    else:
        form = VentasForm()
    ventas = Ventas.objects.all().order_by("ID_venta")
    return render(request, "ventas.html", {"ventas": ventas, "form": form})
###     SQL        ###############
@login_required
def ventas_s(request):
    form = VentasForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Ventas (ID_producto, ID_personal, Cantidad_vendida, Fecha_venta)
                    VALUES (:ID_producto, :ID_personal, :Cantidad_vendida, :Fecha_venta)
                """, {
                    'ID_producto': form.cleaned_data['ID_producto'].ID_producto,
                    'ID_personal': request.user.id,  # Asegúrate de tener un campo de usuario que corresponda
                    'Cantidad_vendida': form.cleaned_data['Cantidad_vendida'],
                    'Fecha_venta': form.cleaned_data['Fecha_venta'],
                })
                transaction.commit()
                id_venta = cursor.lastrowid
                print(f"ID_venta generado: {id_venta}")
            form = VentasForm()
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT v.ID_VENTA, v.CANTIDAD_VENDIDA, v.TOTAL, v.FECHA_VENTA, i.ID_PRODUCTO, i.NOMBRE_PRODUCTO, p.ID_PERSONAL
            FROM Ventas v
            INNER JOIN Inventario i ON v.ID_PRODUCTO = i.ID_PRODUCTO
            INNER JOIN Personal p ON v.ID_PERSONAL = p.ID_PERSONAL
            ORDER BY v.ID_VENTA
        """)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        ventas = [dict(zip(columns, row)) for row in rows]

    
    if request.method != 'POST':
        form = VentasForm()
    return render(request, 'ventas_s.html', {'ventas': ventas, 'form': form})















###     Task Manager    ################
@login_required
def task_manager(request):
    # Obtener tareas incompletas y completadas del usuario actual
    incomplete_tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=True
    )
    completed_tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False
    ).order_by("-datecompleted")
    # Procesar el formulario si se envió
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
    else:
        form = TaskForm()
    # Renderizar la plantilla y pasar las tareas y el formulario al contexto
    context = {
        "incomplete_tasks": incomplete_tasks,
        "completed_tasks": completed_tasks,
        "form": form,
    }
    return render(request, "all_tasks.html", context)


###     Pet page        ####################
@login_required
def pet_page(request):
    if request.method == "POST":
        form = PetForm(request.POST)
        if form.is_valid():
            new_pet = form.save(commit=False)
            new_pet.user = request.user
            new_pet.save()
            return redirect(".")
    else:
        form = PetForm()

    pets = Pet.objects.filter(user=request.user)
    context = {"pets": pets, "form": form}

    return render(request, "pet.html", context)


###     Task detail   ######################
@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, "task_detail.html", {"task": task, "form": form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("task_manager")
        except ValueError:
            return render(
                request,
                "task_detail.html",
                {"task": task, "form": form, "error": "Error updating task"},
            )


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("task_manager")
        except ValueError:
            return render(
                request,
                "create_task.html",
                {"form": TaskForm, "error": "Please provide valid information"},
            )


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("task_manager")


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("task_manager")


@login_required
def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Username or Password is INCORRECT",
                },
            )
        else:
            login(request, user)
            return redirect("/")













@login_required
def propietarios(request):
    if request.method == "POST":
        form = PropietarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("propietarios")
    else:
        form = PropietarioForm()

    propietarios = Propietarios.objects.all()
    return render(
        request, "propietarios.html", {"propietarios": propietarios, "form": form}
    )
