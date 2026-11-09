# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 20:43:30 2026

@author: Anderson
"""

"""Sistema de Gestión de Inventario y Ventas para una microempresa.

Aplicación en consola que permite registrar productos, consultarlos,
actualizar el inventario, realizar ventas con descuento y emitir un
reporte de ventas, validando todos los datos ingresados por el usuario.
"""

# Constantes

CATEGORIAS = ("Accesorios", "Periféricos", "Monitores", "Componentes", "Redes")
MONEDA = "S/"
ANCHO_LINEA = 66

# Funciones de validación de entrada

def leer_texto(mensaje):
    """Pide un texto no vacío y lo devuelve sin espacios sobrantes."""
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("  Error: el campo no puede estar vacío.")


def leer_entero(mensaje, minimo=0, maximo=None):
    """Pide un número entero dentro de un rango y lo devuelve."""
    while True:
        try:
            valor = int(input(mensaje))
        except ValueError:
            print("  Error: ingrese un número entero válido.")
            continue
        if valor < minimo:
            print(f"  Error: el valor debe ser mayor o igual a {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"  Error: el valor debe ser menor o igual a {maximo}.")
        else:
            return valor


def leer_decimal(mensaje, minimo=0.0):
    """Pide un número decimal mayor que el mínimo y lo devuelve."""
    while True:
        try:
            valor = float(input(mensaje))
        except ValueError:
            print("  Error: ingrese un número válido (ejemplo: 45.99).")
            continue
        if valor <= minimo:
            print(f"  Error: el valor debe ser mayor que {minimo:g}.")
        else:
            return valor


def leer_categoria():
    """Muestra las categorías disponibles y devuelve la elegida."""
    print("  Categorías disponibles:")
    for numero, nombre in enumerate(CATEGORIAS, start=1):
        print(f"    {numero}. {nombre}")
    opcion = leer_entero("  Seleccione la categoría: ", 1, len(CATEGORIAS))
    return CATEGORIAS[opcion - 1]


# Funciones auxiliares de lógica

def buscar_por_id(productos, id_producto):
    """Devuelve el producto con ese ID o None si no existe."""
    for producto in productos:
        if producto["id"] == id_producto:
            return producto
    return None


def generar_id(productos):
    """Calcula el siguiente ID disponible."""
    if not productos:
        return 1
    return max(producto["id"] for producto in productos) + 1


def calcular_descuento(cantidad):
    """Devuelve el porcentaje de descuento según la cantidad vendida."""
    if cantidad >= 10:
        return 0.10
    elif cantidad >= 5:
        return 0.05
    else:
        return 0.0


def titulo(texto):
    """Imprime un encabezado de sección."""
    print()
    print(f"=== {texto} ".ljust(ANCHO_LINEA, "="))


# Operaciones del menú

def registrar_producto(productos):
    """Registra un nuevo producto en el inventario."""
    titulo("Registrar Nuevo Producto")
    nombre = leer_texto("Nombre: ")
    categoria = leer_categoria()
    precio = leer_decimal("Precio: ")
    stock = leer_entero("Stock: ", 0)
    producto = {
        "id": generar_id(productos),
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock,
    }
    productos.append(producto)
    print(f"Producto registrado con éxito (ID {producto['id']}).")


def mostrar_productos(productos):
    """Muestra el inventario completo en forma de tabla."""
    titulo("Lista de Productos")
    if not productos:
        print("No hay productos registrados.")
        return
    print(f"{'ID':<4}{'Nombre':<24}{'Categoría':<14}"
          f"{'Precio':>10}{'Stock':>7}")
    print("-" * ANCHO_LINEA)
    for p in productos:
        print(f"{p['id']:<4}{p['nombre']:<24}{p['categoria']:<14}"
              f"{p['precio']:>10.2f}{p['stock']:>7}")


def buscar_producto(productos):
    """Busca productos por ID o por parte del nombre."""
    titulo("Buscar Producto")
    print("  1. Buscar por ID")
    print("  2. Buscar por nombre")
    modo = leer_entero("Seleccione el tipo de búsqueda: ", 1, 2)
    encontrados = []
    if modo == 1:
        id_producto = leer_entero("ID del producto: ", 1)
        producto = buscar_por_id(productos, id_producto)
        if producto is not None:
            encontrados.append(producto)
    else:
        texto = leer_texto("Nombre (o parte): ").lower()
        for p in productos:
            if texto in p["nombre"].lower():
                encontrados.append(p)
    if not encontrados:
        print("No se encontraron productos con ese criterio.")
        return
    for p in encontrados:
        print(f"ID {p['id']} | {p['nombre']} | {p['categoria']} | "
              f"{MONEDA} {p['precio']:.2f} | Stock: {p['stock']}")


def actualizar_inventario(productos):
    """Suma o corrige el stock de un producto existente."""
    titulo("Actualizar Inventario")
    if not productos:
        print("No hay productos registrados.")
        return
    id_producto = leer_entero("ID del producto: ", 1)
    producto = buscar_por_id(productos, id_producto)
    if producto is None:
        print("Error: no existe un producto con ese ID.")
        return
    print(f"Producto: {producto['nombre']} "
          f"(stock actual: {producto['stock']})")
    print("  1. Agregar unidades (reposición)")
    print("  2. Establecer un nuevo stock")
    modo = leer_entero("Seleccione una opción: ", 1, 2)
    if modo == 1:
        cantidad = leer_entero("Unidades a agregar: ", 1)
        producto["stock"] += cantidad
    else:
        producto["stock"] = leer_entero("Nuevo stock: ", 0)
    print(f"Inventario actualizado. Stock actual: {producto['stock']}")


def realizar_venta(productos, ventas):
    """Registra una venta calculando subtotal, descuento y total."""
    titulo("Realizar Venta")
    if not productos:
        print("No hay productos registrados.")
        return
    id_producto = leer_entero("ID del producto: ", 1)
    producto = buscar_por_id(productos, id_producto)
    if producto is None:
        print("Error: no existe un producto con ese ID.")
        return
    if producto["stock"] == 0:
        print(f"Error: '{producto['nombre']}' no tiene stock disponible.")
        return
    cantidad = leer_entero("Cantidad a vender: ", 1)
    if cantidad > producto["stock"]:
        print(f"Error: stock insuficiente (disponible: {producto['stock']}).")
        return
    subtotal = producto["precio"] * cantidad
    porcentaje = calcular_descuento(cantidad)
    descuento = subtotal * porcentaje
    total = subtotal - descuento
    producto["stock"] -= cantidad
    ventas.append({
        "producto": producto["nombre"],
        "cantidad": cantidad,
        "subtotal": subtotal,
        "descuento": descuento,
        "total": total,
    })
    print(f"Subtotal: {MONEDA} {subtotal:.2f}")
    print(f"Descuento ({porcentaje * 100:.0f}%): {MONEDA} {descuento:.2f}")
    print(f"Venta realizada. Total: {MONEDA} {total:.2f}")


def reporte_ventas(ventas):
    """Muestra el detalle de las ventas y los totales acumulados."""
    titulo("Reporte de Ventas")
    if not ventas:
        print("Aún no se han realizado ventas.")
        return
    total_general = 0.0
    unidades = 0
    for numero, venta in enumerate(ventas, start=1):
        print(f"Venta {numero}: {venta['producto']} | "
              f"Cantidad: {venta['cantidad']} | "
              f"Descuento: {MONEDA} {venta['descuento']:.2f} | "
              f"Total: {MONEDA} {venta['total']:.2f}")
        total_general += venta["total"]
        unidades += venta["cantidad"]
    print("-" * ANCHO_LINEA)
    print(f"Ventas realizadas: {len(ventas)} | Unidades vendidas: {unidades}")
    print(f"Total general: {MONEDA} {total_general:.2f}")


# Control del programa

def mostrar_menu():
    """Imprime el menú principal."""
    print()
    print(" Sistema de Gestión de Inventario ".center(ANCHO_LINEA, "="))
    print("  1. Registrar Producto")
    print("  2. Mostrar Productos")
    print("  3. Buscar Producto")
    print("  4. Actualizar Inventario")
    print("  5. Realizar Venta")
    print("  6. Reporte de Ventas")
    print("  7. Salir")


def main():
    """Ciclo principal del programa."""
    productos = []
    ventas = []
    try:
        while True:
            mostrar_menu()
            opcion = leer_entero("Seleccione una opción: ", 1, 7)
            if opcion == 1:
                registrar_producto(productos)
            elif opcion == 2:
                mostrar_productos(productos)
            elif opcion == 3:
                buscar_producto(productos)
            elif opcion == 4:
                actualizar_inventario(productos)
            elif opcion == 5:
                realizar_venta(productos, ventas)
            elif opcion == 6:
                reporte_ventas(ventas)
            else:
                break
    except (KeyboardInterrupt, EOFError):
        print()
        print("Entrada interrumpida.")
    print("Saliendo del sistema... ¡Hasta pronto!")


if __name__ == "__main__":
    main()