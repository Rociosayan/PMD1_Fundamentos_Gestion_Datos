PRAGMA foreign_keys = ON;

CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    segmento TEXT,
    fecha_registro TEXT
);

CREATE TABLE productos (
    id_producto INTEGER PRIMARY KEY,
    nombre TEXT,
    categoria TEXT,
    proveedor TEXT,
    costo_unitario REAL,
    precio_lista REAL
);

CREATE TABLE tiendas (
    id_tienda INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    zona TEXT,
    tipo_local TEXT
);

CREATE TABLE ventas (
    id_venta INTEGER PRIMARY KEY,
    id_cliente INTEGER,
    id_producto INTEGER,
    id_tienda INTEGER,
    fecha_operacion TEXT,
    cantidad_unidades TEXT,
    precio_venta_unitario TEXT,
    costo_unitario TEXT,
    descuento_pct TEXT,
    stock_inicial TEXT,
    stock_final TEXT,
    merma_unidades TEXT,
    canal TEXT,
    metodo_pago TEXT,
    monto_venta_soles TEXT,
    margen_venta_soles TEXT,
    observacion TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_tienda) REFERENCES tiendas(id_tienda)
);
