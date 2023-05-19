DROP TABLE VENTAS; --
DROP TABLE RECETASMEDICAS; --
DROP TABLE EXPEDIENTES; --
DROP TABLE NOMINA; -- 
DROP TABLE INVENTARIO; -- 
DROP TABLE PROVEDOREES;--
DROP TABLE PERSONAL; --
DROP TABLE MASCOTAS; --
DROP TABLE PROPIETARIOS;




--
-- TABLA
-- PERSONAL
--

CREATE TABLE Personal (
    ID_personal NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    Tipo_personal VARCHAR2(30) CHECK (
        Tipo_personal IN (
            'Medicos veterinarios', 
            'Recepcionista', 
            'Encargado de acuario', 
            'Encargado de accesorios', 
            'Encargado de articulos generales', 
            'Encargado de estetica'
        )
    ),
    Cedula_profesional VARCHAR2(20) NULL,
    Especialidad VARCHAR2(50) NULL,
    Nombre_completo VARCHAR2(50) NOT NULL,
    Fecha_nacimiento DATE NOT NULL,
    Fecha_ingreso DATE NOT NULL,
    Numero_telefonico VARCHAR2(20) NOT NULL,
    Direccion VARCHAR2(100) NOT NULL,
    Turno VARCHAR2(2) CHECK (
        Turno IN ('M', 'V')
    ),
    Horario VARCHAR2(10) CHECK (
        Horario IN ('8-4','1-9')
    ),
    Salario_neto DECIMAL(10, 2) NOT NULL,
    RFC VARCHAR2(13) UNIQUE NOT NULL,
    CURP VARCHAR2(18) UNIQUE NOT NULL
);


--
-- TABLA
-- NOMINA
--

CREATE TABLE Nomina (
    ID_Nomina NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
    ID_personal NUMBER NOT NULL,
    Horas_trabajadas NUMBER NOT NULL,
    Horas_extras NUMBER DEFAULT 0,
    Retardos NUMBER DEFAULT 0,
    Faltas NUMBER DEFAULT 0,
    Empleado_del_mes NUMBER DEFAULT 0 CHECK (Empleado_del_mes IN (0, 1)),
    Fecha_pago TIMESTAMP,
    Tipo_pago VARCHAR2(20),
    Salario_neto DECIMAL(10, 2),
    FOREIGN KEY (ID_personal) REFERENCES Personal(ID_personal)
);



CREATE OR REPLACE TRIGGER calcular_nomina
BEFORE INSERT OR UPDATE ON Nomina
FOR EACH ROW
DECLARE 
    v_salario_neto DECIMAL(10, 2);
    v_tipo_personal VARCHAR2(30);
    v_salario_base DECIMAL(10, 2);
BEGIN
    SELECT Tipo_personal, Salario_neto
    INTO v_tipo_personal, v_salario_base
    FROM Personal
    WHERE ID_personal = :NEW.ID_personal;

    v_salario_neto := CASE
        WHEN v_tipo_personal = 'Medicos veterinarios' THEN :NEW.Horas_trabajadas * 300
        WHEN v_tipo_personal = 'Encargado de estetica' THEN :NEW.Horas_trabajadas * 200
        ELSE :NEW.Horas_trabajadas * 100
    END;
    v_salario_neto := v_salario_neto + v_salario_base;
    IF :NEW.Horas_extras > 0 THEN
        v_salario_neto := v_salario_neto + v_salario_neto * 0.15;
    END IF;
    IF :NEW.Retardos >= 3 THEN
        v_salario_neto := v_salario_neto - v_salario_neto * 0.05;
    END IF;
    IF :NEW.Faltas >= 3 THEN
        v_salario_neto := v_salario_neto - v_salario_neto * 0.10;
    END IF;
    IF :NEW.Empleado_del_mes = 1 THEN
        v_salario_neto := v_salario_neto + 100;
    END IF;
    :NEW.Salario_neto := v_salario_neto;
END;
/





--
-- TABLA
-- PROPIETARIOS
--


-- Crear la tabla
CREATE TABLE Propietarios (
    ID_propietario NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
    Nombre VARCHAR2(50) NOT NULL,
    Apellido VARCHAR2(50) NOT NULL,
    Telefono VARCHAR2(20) NOT NULL,
    Direccion VARCHAR2(100) NOT NULL,
    Mascotas NUMBER,
    Correo_electronico VARCHAR2(50)
);


--
-- TABLA
-- PROVEEDORES
--


-- Crear la tabla
CREATE TABLE Proveedores (
    ID_proveedor NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
    Nombre VARCHAR2(50) NOT NULL,
    Direccion VARCHAR2(100) NOT NULL,
    Telefono VARCHAR2(20) NOT NULL,
    -- Articulos_que_provee CLOB 
);



--
-- TABLA
-- INVENTARIO
--

CREATE TABLE Inventario (
    ID_producto NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
    Nombre_producto VARCHAR2(50) NOT NULL,
    Area VARCHAR2(30) NOT NULL,    
    Caracteristicas CLOB,
    Precio_unitario NUMBER(10, 2) NOT NULL,
    Cantidad_inventario NUMBER NOT NULL,
    Fecha_caducidad CLOB,
    Productos_descuento NUMBER(3,2),
    Marca_producto VARCHAR2(50),
    Presentacion VARCHAR2(30),
    Fecha_compra CLOB );
    
-- Crear la tabla de relación ProveedoresProductos
CREATE TABLE ProveedoresProductos (
    ID_proveedor NUMBER,
    ID_producto NUMBER,
    PRIMARY KEY (ID_proveedor, ID_producto),
    FOREIGN KEY (ID_proveedor) REFERENCES Proveedores(ID_proveedor),
    FOREIGN KEY (ID_producto) REFERENCES Inventario(ID_producto)
);



--
-- TABLA
-- MASCOTAS
--

CREATE TABLE Mascotas (
    ID_mascota NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
    ID_propietario NUMBER,
    Nombre VARCHAR2(30) NOT NULL,
    Tipo VARCHAR2(30) NOT NULL,
    Raza VARCHAR2(30) NOT NULL,
    Fecha_nacimiento DATE NOT NULL,
    Color VARCHAR2(20) NOT NULL,
    Sexo CHAR(1) NOT NULL,
    Imagen VARCHAR2(255) NULL,
    FOREIGN KEY (ID_propietario) REFERENCES Propietarios(ID_propietario)
);

--
-- TABLA
-- ESPEDIENTES
--


CREATE TABLE Expedientes (
    ID_expediente NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
    ID_mascota NUMBER,
    ID_personal NUMBER,
    Edad NUMBER NOT NULL,
    Historial_clinico CLOB NULL,
    Cirugias CLOB NULL,
    Tratamientos CLOB NULL,
    Fecha_ingreso TIMESTAMP NOT NULL,
    Fecha_egreso TIMESTAMP,
    Diagnostico CLOB NULL,
    Esquema_vacunacion CLOB NULL,
    Alergias CLOB NULL,
    FOREIGN KEY (ID_mascota) REFERENCES Mascotas(ID_mascota),
    FOREIGN KEY (ID_personal) REFERENCES Personal(ID_personal)
);





--
-- TABLA
-- RECETAS
--


CREATE TABLE RecetasMedicas (
    ID_receta NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
    ID_mascota NUMBER,
    ID_personal NUMBER,
    Peso NUMBER(5,2) NOT NULL,
    Medicamentos_recetados CLOB NOT NULL,
    Indicaciones_generales CLOB,
    Fecha TIMESTAMP NOT NULL,
    FOREIGN KEY (ID_mascota) REFERENCES Mascotas(ID_mascota),
    FOREIGN KEY (ID_personal) REFERENCES Personal(ID_personal)
);

--
-- TABLA
-- VENTAS
--





CREATE TABLE Ventas (
    ID_venta NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
    ID_producto NUMBER,
    ID_personal NUMBER,
    Cantidad_vendida NUMBER NOT NULL,
    Total NUMBER(10, 2) NOT NULL,
    Fecha_venta TIMESTAMP NOT NULL,
    FOREIGN KEY (ID_producto) REFERENCES Inventario(ID_producto),
    FOREIGN KEY (ID_personal) REFERENCES Personal(ID_personal) );
    
CREATE OR REPLACE TRIGGER calcular_total_venta
BEFORE INSERT OR UPDATE ON Ventas
FOR EACH ROW
DECLARE 
    v_precio_unitario NUMBER(10, 2);
BEGIN
    SELECT Precio_unitario
    INTO v_precio_unitario
    FROM Inventario
    WHERE ID_producto = :NEW.ID_producto;

    :NEW.Total := :NEW.Cantidad_vendida * v_precio_unitario;
END;
/


