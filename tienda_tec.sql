-- Rodrigo Antonio Estrada Orantes 23270051
-- 01/04/2025
-- practica15_23270051
-- \. C:\Users\rodan\OneDrive\Documentos\documentos de la escuela\mysql\notepad\tienda_tec.sql

DROP DATABASE IF EXISTS practica15_23270051;
CREATE DATABASE IF NOT EXISTS practica15_23270051;
USE practica15_23270051;

CREATE TABLE IF NOT EXISTS clientes (
  id_cliente INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  telefono VARCHAR(10));

CREATE TABLE IF NOT EXISTS empleado (
  id_empleado INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  correo VARCHAR(100) NULL DEFAULT NULL,
  contrasena char(5) NULL DEFAULT NULL,
  puesto VARCHAR(45) NULL DEFAULT NULL);

CREATE TABLE IF NOT EXISTS ventas (
  id_venta INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  id_cliente INT NOT NULL,
  fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  total DECIMAL(10,2) NOT NULL,
  empleado_id_empleado INT NOT NULL,
  INDEX debe (id_cliente ASC) VISIBLE,
  INDEX fk_ventas_empleado1_idx (empleado_id_empleado ASC) VISIBLE,
  CONSTRAINT debe
    FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
  CONSTRAINT fk_ventas_empleado1
    FOREIGN KEY (empleado_id_empleado) REFERENCES empleado (id_empleado)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE IF NOT EXISTS proveedor (
  id_proveedor INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  telefono VARCHAR(15) NULL DEFAULT NULL,
  direccion TEXT NULL DEFAULT NULL,
  correo VARCHAR(100) NULL DEFAULT NULL);

CREATE TABLE IF NOT EXISTS productos (
  id_producto INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT NOT NULL,
  precio DECIMAL(10,2) NOT NULL,
  stock INT NOT NULL DEFAULT '0',
  id_proveedor INT NULL DEFAULT NULL,
  INDEX vienen (id_proveedor ASC) VISIBLE,
  CONSTRAINT vienen
    FOREIGN KEY (id_proveedor)REFERENCES proveedor (id_proveedor)
    ON DELETE SET NULL
    ON UPDATE CASCADE);

CREATE TABLE IF NOT EXISTS detalle_venta (
  id_detalle INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  id_venta INT NOT NULL,
  id_producto INT NOT NULL,
  cantidad INT NOT NULL,
  precio_unitario DECIMAL(10,2) NOT NULL,
  importe DECIMAL(10,2) NOT NULL,
  INDEX id_venta (id_venta ASC) VISIBLE,
  INDEX id_producto (id_producto ASC) VISIBLE,
  CONSTRAINT esta
    FOREIGN KEY (id_venta)REFERENCES ventas (id_venta),
  CONSTRAINT vendra
    FOREIGN KEY (id_producto)REFERENCES productos (id_producto));

CREATE TABLE IF NOT EXISTS inventario (
  id_inventario INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  cantidad INT NOT NULL,
  fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  productos_id_producto INT NOT NULL,
  proveedor_id_proveedor INT NOT NULL,
  INDEX tendra (productos_id_producto ASC) VISIBLE,
  INDEX estara (proveedor_id_proveedor ASC) VISIBLE,
  CONSTRAINT tendra
    FOREIGN KEY (productos_id_producto)REFERENCES productos (id_producto),
  CONSTRAINT estara
    FOREIGN KEY (proveedor_id_proveedor)REFERENCES proveedor (id_proveedor)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE IF NOT EXISTS empleado_has_inventario (
  empleado_id_empleado INT NOT NULL,
  inventario_id_inventario INT NOT NULL,
  PRIMARY KEY (empleado_id_empleado, inventario_id_inventario),
  INDEX saldra (inventario_id_inventario ASC) VISIBLE,
  CONSTRAINT ira
    FOREIGN KEY (empleado_id_empleado) REFERENCES empleado (id_empleado),
  CONSTRAINT saldra
    FOREIGN KEY (inventario_id_inventario) REFERENCES inventario (id_inventario));