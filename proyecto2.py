import pandas as pd
import os

UMBRAL_STOCK_BAJO = 20  

#Clase Producto
class Producto:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = int(cantidad) 

    def descuento(self):
       
        return self.precio * 0.9


def ver_producto(inventario): #Muestra los detalles de un producto que se necesite revisar
    nombre = input("Ingrese el nombre del producto a ver:").strip().title()
   #los prints Muestran 1 el nombre,2 el precio, 3 el stock  y 4 el descuento (si se uso el metodo descuento)
    if nombre in inventario:
        producto = inventario[nombre]
        
        print(f"\n -- Detalles de {nombre} --")
        
        print(f"Precio: ${producto.precio:n}") 
        
        print(f"Stock: {producto.cantidad} unidades")
        
        print(f"Precio con 10% de Descuento: ${producto.descuento(): n}")
    else:
        print(f"Producto {nombre} no encontrado en el inventario")

def agregar_producto(inventario): #Añade un producto nuevo al inventario
    
    nombre = input("Ingrese el nombre del producto: ").strip().title()
    if nombre in inventario:
        print(f"El producto {nombre} ya existe. Use 'Actualizar Stock' o 'Actualizar Precio'.")
        return

    while True:
        try:
            precio = float(input("Ingrese el precio del producto: $"))
            cantidad = int(input("Ingrese la cantidad (stock):"))
            if precio < 0 or cantidad < 0:
                print("El precio y la cantidad deben ser válidos y positivos")
                continue
            break
        except ValueError:
            print("Error: Por favor, ingrese un número válido para precio y cantidad")
#valida que el producto no exista y maneja el error si el usuario ingresa un precio o cantidad numerica erronea
    nuevo_producto = Producto(nombre, precio, cantidad)
    inventario[nombre] = nuevo_producto
    print(f"Producto '{nombre}' agregado correctamente")

def vender_producto(inventario):
    
    nombre_producto = input("Ingrese el nombre del producto a vender:").strip().title()
    if nombre_producto in inventario:
        producto = inventario[nombre_producto]
        while True:
            try:
                cantidad = int(input(f"Stock actual: {producto.cantidad}. ¿Cuántas unidades de {nombre_producto} desea vender?: "))
                if cantidad <= 0:
                    print("La cantidad a vender debe ser mayor a cero.")
                    continue
                break
            except ValueError:
                print("Error: Por favor, ingrese un número entero para la cantidad.")

        if producto.cantidad >= cantidad:
            producto.cantidad -= cantidad
            print(f"Se vendieron {cantidad} unidades de {nombre_producto}. Stock restante {producto.cantidad}")
        else:
            print(f"No hay suficiente stock de {nombre_producto}. Stock disponible: {producto.cantidad}")
    else:
        print(f"No se encontró el producto {nombre_producto} en el inventario")

def listar_inventario(inventario, umbral):
    
    if not inventario:
        print("\n -- Inventario Vacío --")
        return
    print("\n -- Inventario Actual -- ")
    productos_con_alerta = 0
    for nombre, producto in inventario.items():
        alerta = ""
        if producto.cantidad < umbral:
            alerta = " (Stock Bajo)"
            productos_con_alerta += 1
        print(f"{nombre}: Stock: {producto.cantidad}, Precio: ${producto.precio:,.2f}{alerta}")

    if productos_con_alerta > 0:
        print(f"\nHay {productos_con_alerta} productos con stock bajo el umbral de {umbral}.")

def actualizar_stock(inventario):
    
    nombre = input("Ingrese el nombre del producto a actualizar:").strip().title()
    if nombre in inventario:
        producto = inventario[nombre]
        print(f"Stock actual de {nombre}: {producto.cantidad}")
        while True:
            try:
                ajuste = int(input("Ingrese el ajuste de stock (+ para agregar, - para quitar):"))
                nuevo_stock = producto.cantidad + ajuste
                if nuevo_stock < 0:
                    print(f"Error: El stock ({nuevo_stock}) no puede ser negativo")
                    return
                else:
                    producto.cantidad = nuevo_stock
                    print(f"Stock de {nombre} actualizado. Nuevo stock: {nuevo_stock}")
                    return
            except ValueError:
                print("Ingrese un número válido para el ajuste")
    else:
        print(f"Producto {nombre} no encontrado")
def actualizar_precio(inventario):
    nombre = input("Ingrese el nombre del producto para actualizar el precio")
    if nombre in inventario:
        producto = inventario[nombre]
        print(f"Precio actual de {nombre}: ${producto.precio: n}")
        while True:
            try:
                nuevo_precio = float(input("Ingrese el nuevo precio: $"))
                if nuevo_precio < 0:
                    print("El precio debe ser un valor positivo")
                    continue
                producto.precio = nuevo_precio
                print(f"Precio de {nombre} actualizado Nuevo precio: ${nuevo_precio: n}")
                return
            except ValueError:
                print("Error: Por favor, ingrese un numero valido")
    else:
            print(f"Producto {nombre} no encontrado")

def guardar_inventario(inventario):
    
    datos_para_csv = []
    for nombre, producto in inventario.items():
        datos_para_csv.append({
            'nombre': producto.nombre,
            'precio': producto.precio,
            'cantidad': producto.cantidad
        })
    df_actualizado = pd.DataFrame(datos_para_csv)
    df_actualizado.to_csv("productos.csv", index=False)
    print("Inventario guardado exitosamente.")



def main():
    inventario = {}
    df_productos = None 

    
    try:
        df_productos = pd.read_csv("productos.csv")
        print("Carga de 'productos.csv' exitosa.")
    except FileNotFoundError:
        print("Error: no se encontró el archivo 'productos.csv'. Inventario vacío.")
        df_productos = pd.DataFrame(columns=['nombre', 'precio', 'cantidad'])
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        df_productos = pd.DataFrame(columns=['nombre', 'precio', 'cantidad'])

    for index, row in df_productos.iterrows():
        try:
            nombre = str(row['nombre']).strip().title()
            precio = float(row['precio'])
            cantidad = int(row['cantidad'])
            inventario[nombre] = Producto(nombre, precio, cantidad)
        except (KeyError, ValueError, TypeError) as e:
            print(f"Error al procesar la fila {index} del CSV: {e}. Fila Incorrecta. Producto omitido.")

    
    while True:
        print("\n -- Menú Inventario --")
        print("1. Ver Producto")
        print("2. Agregar Producto")
        print("3. Vender Producto")
        print("4. Listar Inventario")
        print("5. Actualizar Stock")
        print("6. Actualizar precio")
        print("7. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            ver_producto(inventario) 
        elif opcion == "2":
            agregar_producto(inventario)
        elif opcion == "3":
            vender_producto(inventario)
        elif opcion == "4":
            listar_inventario(inventario, UMBRAL_STOCK_BAJO)
        elif opcion == "5":
            actualizar_stock(inventario)
        elif opcion == "6":
            actualizar_precio(inventario)
        elif opcion == "7":
            guardar_inventario(inventario) 
            print("Saliendo del inventario")
            break 
        else:
            print(" Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()