CREATE TABLE Personal (
    ID_personal NUMBER PRIMARY KEY,
    Tipo_personal VARCHAR2(30),
    Cedula_profesional VARCHAR2(20) UNIQUE,
    Especialidad VARCHAR2(50),
    Nombre_completo VARCHAR2(50) NOT NULL,
    Fecha_nacimiento DATE NOT NULL,
    Fecha_ingreso TIMESTAMP NOT NULL,
    Numero_telefonico VARCHAR2(20) NOT NULL,
    Direccion VARCHAR2(100) NOT NULL,
    Turno VARCHAR2(20) NOT NULL,
    Horario VARCHAR2(20) NOT NULL,
    Salario_neto NUMBER(10, 2) NOT NULL,
    RFC VARCHAR2(13) UNIQUE NOT NULL,
    CURP VARCHAR2(18) UNIQUE NOT NULL);

CREATE TABLE Proveedores (
    ID_proveedor NUMBER PRIMARY KEY,
    Nombre VARCHAR2(50) NOT NULL,
    Direccion VARCHAR2(100) NOT NULL,
    Telefono VARCHAR2(20) NOT NULL,
    Articulos_que_provee CLOB );  

CREATE TABLE Propietarios (
    ID_propietario NUMBER PRIMARY KEY,
    Nombre VARCHAR2(50) NOT NULL,
    Apellido VARCHAR2(50) NOT NULL,
    Telefono VARCHAR2(20) NOT NULL,
    Direccion VARCHAR2(100) NOT NULL,
    Numero_cliente NUMBER,
    Correo_electronico VARCHAR2(50));    

CREATE TABLE Inventario (
    ID_producto NUMBER PRIMARY KEY,
    ID_proveedor NUMBER,
    Clasificacion VARCHAR2(30) NOT NULL,
    Nombre_producto VARCHAR2(50) NOT NULL,
    Caracteristicas CLOB,
    Precio_unitario NUMBER(10, 2) NOT NULL,
    Cantidad_inventario NUMBER NOT NULL,
    Fecha_caducidad TIMESTAMP,
    Productos_descuento NUMBER(1),
    Marca_producto VARCHAR2(50),
    Presentacion VARCHAR2(30),
    Fecha_compra TIMESTAMP,
    FOREIGN KEY (ID_proveedor) REFERENCES Proveedores(ID_proveedor));

CREATE TABLE Nomina (
    ID_nomina NUMBER PRIMARY KEY,
    ID_personal NUMBER,
    Fecha_pago TIMESTAMP NOT NULL,
    Tipo_pago VARCHAR2(20) NOT NULL,
    Horas_trabajadas NUMBER NOT NULL,
    Horas_extras NUMBER DEFAULT 0,
    Retardos NUMBER DEFAULT 0,
    Faltas NUMBER DEFAULT 0,
    Empleado_del_mes NUMBER(1),
    Salario_total NUMBER(10, 2),
    FOREIGN KEY (ID_personal) REFERENCES Personal(ID_personal));

CREATE TABLE Mascotas (
    ID_mascota NUMBER PRIMARY KEY,
    ID_propietario NUMBER,
    Nombre_mascota VARCHAR2(30) NOT NULL,
    Edad NUMBER NOT NULL,
    Sexo CHAR(1) NOT NULL,
    Raza VARCHAR2(30) NOT NULL,
    Color VARCHAR2(20) NOT NULL,
    Historial_clinico CLOB,
    Cirugias CLOB,
    Tratamientos CLOB,
    Fecha_ingreso TIMESTAMP NOT NULL,
    Fecha_egreso TIMESTAMP,
    Diagnostico CLOB,
    Esquema_vacunacion CLOB,
    Alergias CLOB,
    FOREIGN KEY (ID_propietario) REFERENCES Propietarios(ID_propietario));

CREATE TABLE RecetasMedicas (
    ID_receta NUMBER PRIMARY KEY,
    ID_mascota NUMBER,
    ID_personal NUMBER,
    Peso NUMBER(5,2) NOT NULL,
    Medicamentos_recetados CLOB NOT NULL,
    Indicaciones_generales CLOB,
    Fecha TIMESTAMP NOT NULL,
    FOREIGN KEY (ID_mascota) REFERENCES Mascotas(ID_mascota),
    FOREIGN KEY (ID_personal) REFERENCES Personal(ID_personal) );

CREATE TABLE Ventas (
    ID_venta NUMBER PRIMARY KEY,
    ID_producto NUMBER,
    ID_personal NUMBER,
    Cantidad_vendida NUMBER NOT NULL,
    Subtotal NUMBER(10, 2),
    Total NUMBER(10, 2),
    Fecha_venta TIMESTAMP NOT NULL,
    FOREIGN KEY (ID_producto) REFERENCES Inventario(ID_producto),
    FOREIGN KEY (ID_personal) REFERENCES Personal(ID_personal) );
