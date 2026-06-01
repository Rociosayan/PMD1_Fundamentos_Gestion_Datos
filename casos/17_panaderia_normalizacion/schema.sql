CREATE TABLE "ventas_original" (
    "id_venta" INTEGER PRIMARY KEY,
    "fecha" TEXT,
    "cliente_nombre" TEXT,
    "cliente_distrito" TEXT,
    "producto_nombre" TEXT,
    "categoria_nombre" TEXT,
    "local_nombre" TEXT,
    "local_distrito" TEXT,
    "cantidad" INTEGER,
    "precio_unitario" REAL,
    "metodo_pago" TEXT,
    "total_venta" REAL
);
