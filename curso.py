# bucles
for i in ["primavera", "verano", "otoño", "invierno"]:  # el contador es el número de elementos en la tupla
    print(i, end=" ")  # imprime contenido tupla sin retorno de carro con espacio al final

for i in range(5):  # pasa 5 veces por el bucle
    print(f"valor del contador {i}", end=" ")  # formateo de cadenas sin concatenación

for i in range(5, 10):  # el contador empieza en 5 y acaba en 9
    print(f"valor del contador {i}", end=" ")
    print("Valor del contador: " + str(i))  # método tradicional

for i in range(5, 50, 3):  # el contador empieza en 5 y acaba en 50, pero va de 3 en 3
    print(f"valor del contador {i}", end=" ")

i = 0
while i <= 10:
    print(f"bucle while {i}")
    i += 1
    break  # sale del bucle while
    continue  # vuelve al inicio del bucle while

# condicionales
email = False
punto = False
for i in "hola@caracola.es":  # imprime tantas veces como caracteres haya

    if i == "@":
        email = True

    if i == ".":
        punto = True

if email and punto:
    print("correo correcto")


# funciones generador

def devuelve_ciudades(*ciudades):  # número indeterminado de parámetros en formato tupla
    for elemento in ciudades:
        yield elemento  # devuelve elemento (Madrid)
        yield from elemento  # devuelve subelementos (M) (a) (d) (r) (i) (d)


ciudades_devueltas = devuelve_ciudades("Madrid", "Barcelona")  # llama a función y guarda en contenedor val devueltos

print(next(ciudades_devueltas))

# EXCEPCIONES

try:
    resultado = 8 / 0
except ZeroDivisionError as e:
    print(f"No se puede dividir entre cero ({e})")
except ValueError as e:
    print(f"Datos incorrectos ({e})")
except:  # todas las excepciones
    e = sys.exc_info()[0]
    print("Error no tratado ", e)
finally:  # se ejecuta siempre
    print("fin del programa", "adios")


# raise ValueError("No se permite este tipo")  # lanzamos una excepción

#  C L A S E S

class Vehiculos():  # super clase

    def __init__(self, numero_ruedas):
        self.ruedas = numero_ruedas

    def __str__(self):  # lo que se devuelve al usar print sobre la función
        return str(self.ruedas)


class Coche(Vehiculos):  # entre paréntesis la super clase
    pass


mi_coche = Coche(4)
print(mi_coche)

# C A D E N A S

" hola ".strip()  # trim

# I M P O R T A R
import io  # se importan todas las funciones, pero obliga a usar las funciones precedidas del nombre archivo
from io import open  # se importa una función y no obliga a usar el nombre archivo delante
from io import *  # se importan todas las funciones y no obliga a poner nombre archivo delante

# A R C H I V O S

from io import open

archivo = open("archivo.txt", "w")  # abre en modo W escritura, R  lectura, A  append, R+ lectura/escritura
archivo.write("contenido del archivo")  # guardamos contenido, .read para leerlo
archivo.close()

archivo2 = open("archivo.txt", "r")
# linea_texto = archivo2.readlines()  # guarda en una lista las líneas del texto leido, writeLines guarda en archivo
archivo2.seek(
    int(
        len(
            archivo2.read()
        ) / 2  # posiciona el cursor en medio del texto
    )
)
print(archivo2.read())  # un entero indicaría hasta donde tiene que leer read
archivo2.close()

# S E R I A L I Z A C I Ó N

import pickle

lista_nombres = [
    "Pedro Moreno",
    "Luis Martínez",
    "Marcos Sánchez",
    "Leticia Sanchez",
    "María de la Vega",
    "Isabel Robledo",
    "Victor Méndez",
    "Teresa Mendoza",
    "1024 Mendoza",
    "Jesús 2048",
    "Jesús López",
    "Sandra Salomé"
]

fichero_binario = open("lista_nombres", "wb")  # abierto en modo escritura binaria
pickle.dump(lista_nombres, fichero_binario)  # guarda la colección en archivo
fichero_binario.close()

fichero = open("lista_nombres", "rb")  # read binary
lista = pickle.load(fichero)
print(lista)
fichero.close()
del fichero  # lo elimina de memoria

# B A S E S   D E   D A T O S  -  S Q L i t e

import sqlite3

conn = sqlite3.connect("bd.db")
cur = conn.cursor()
cur.execute('''
    create table if not exists productos (
    id integer primary key autoincrement,
    articulo varchar(50) unique, 
    precio integer, 
    seccion varchar(20),
    stock integer)
    ''')
# cur.execute("drop table productos")
conn.commit()

import random

lista_productos = [
    ("Camiseta" + str(random.randint(1000, 9999)), random.randint(6, 20), "Deportes", str(random.randint(0, 99))),
    ("Jarrón" + str(random.randint(1000, 9999)), random.randint(20, 80), "Cerámica", str(random.randint(0, 99))),
    ("Camión" + str(random.randint(1000, 9999)), random.randint(20, 35), "Juguetería", str(random.randint(0, 99)))
]
'''
cur.executemany("INSERT INTO PRODUCTOS VALUES(null,?,?,?,?)",
                lista_productos)  # poner null y no ? en campo autoincrementable
conn.commit()
'''
cur.execute("SELECT * FROM productos")
resultado = cur.fetchall()

for producto in resultado:
    print("Artículo: ", producto[0], " Sección: ", producto[2], " Precio: ", producto[1])

conn.close()

# FUNCIONES LAMBDA, ANÓNIMAS, ON THE GO, ON DEMAND, ONLINE

# no se pueden usar bucles/condicionales, : es el return, el nombre de la función es la variable area_triangulo
area_triangulo = lambda base, altura: (base * altura) / 2
# se llama a la función llamando a la variable y pasándole parámetros
print(area_triangulo(3, 2))


class Empleado:
    def __init__(self, nombre, cargo, salario):
        self.nombre = nombre
        self.cargo = cargo
        self.salario = salario

    def __str__(self):
        return "{} que trabaja como {} con un salario de {} €".format(self.nombre, self.cargo, self.salario)


lista_empleados = [
    Empleado("Juan", "Director", 75000),
    Empleado("Ana", "Presidenta", 85000),
    Empleado("Antonio", "Administrativo", 25000),
    Empleado("Sara", "Secretaria", 27000),
    Empleado("Mario", "Botones", 21000),
    Empleado("Junajo", "Botones", 21000),
    Empleado("Santiago", "Camarero", 2000),
    Empleado("Iñaqui", "Limpiador", 15000),
    Empleado("Irene", "Limpiadora", 15000),
    Empleado("Sandra", "Cuidadora", 15000)
]

# devuelve elementos que cumplen con la condición > 50.000 en la lista_empleados
salarios_altos = filter(lambda empleado: empleado.salario > 50000, lista_empleados)

for salario in salarios_altos:
    print(salario)


#  F U N C I Ó N   M A P

def calculo_comision(trabajador):
    if trabajador.salario <= 25000:
        trabajador.salario = trabajador.salario * 1.03

    return trabajador


lista_empleados_bonus = map(calculo_comision, lista_empleados)

for emp in lista_empleados_bonus:
    print(emp)

#  E X P R E S I O N E S   R E S G U L A R E S

import re

cadena = "vamos a aprender python"
texto_encontrado = re.search("aprender", cadena)
rango_valores = texto_encontrado.span()  # devuelve una tupla con posIni y posFin (.start y .end por junto)

for elemento in lista_nombres:
    '''
    if re.findall('^Isabel', elemento):  # ^ devuelve elemento de una lista encontrado por el principio
        print(elemento)

    if re.findall('ez$', elemento):  # $ devuelve elemento de una lista encontrado por el final
        print(elemento)

    if re.findall('S[aá]nchez', elemento):  # [aá] busca á o a en una palabra
        print(elemento)

    # ^ dentro de un rango significa NO, lo contrario
    if re.findall('^[L-M P-S]', elemento):  # Devuelve lo que empiece desde L hasta M (o no si se usa ^ dentro de [])
        print(elemento)

    # MATCH siempre busca al principio
    if re.match(".andra", elemento, re.IGNORECASE):  # el . sirve de comodín de 1 carácter
        print(elemento)

    if re.match("\d", elemento):  # busca dígitos
        print(elemento)
    '''
    # SEARCH busca en toda la cadena
    if re.search("\d", elemento, re.IGNORECASE):  # devuelve elementos con dígitos
        print(elemento)


#  D E C O R A D O R E S

# admite como parámetros variables o diccionarios
def decorador(funcion):
    def funcion_interior(*args, **kwargs):  # número indeterminado de parámetros
        print("adorno al inicio")
        funcion(*args, **kwargs)  # la función que va a ser decorada
        print("adorno al final")

    return funcion_interior


@decorador
def suma(num1, num2, num3):  # función a decorar
    """
    Formato de documentación de funciones y métodos con su pruebas
    """
    print(num1 + num2 + num3)


suma(num1=1, num2=12, num3=2)
suma(1, 2, 3)


# D O C U M E N T A C I Ó N   Y   P R U E B A S  M Ó D U L O   D O C T E S T

def resta(num1, num2):
    """
    Función que devuelve el resultado de una resta de 2 parámetros recibidos
    >>> for i in range(3):
    ...     resta(i, i)
    0
    """
    print(num1 - num2)


resta(3, 1)
import doctest

doctest.testmod()

#  E J E C U T A B L E S
#   En CMD pyinstaller --windowed --onefile --icon=sopa.ico archivo.py
