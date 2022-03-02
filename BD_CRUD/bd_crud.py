import re
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
import cx_Oracle

app = Flask(__name__)

# conexión MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'jsarmenteros'
app.config['MYSQL_PASSWORD'] = "Jm)GCELdIwA0hBlI"
app.config['MYSQL_DB'] = "proyecto_final"

conn = MySQL(app)

@app.route('/add', methods=["GET", "POST"])
def add():

    var_data = {
        "titulo": "Añadir tabla"
    }

    if request.method == "POST":
        # request.args['nombre_tabla'] para acceder al parámetro a través del GET
        # request.form['nombre_tabla'] para acceder al parámetro a través del POST

        tabla = request.form.get('nombre_tabla')

        # comprobamos que haya nombre en la tabla
        if tabla == "":
            return render_template("add.html", params=var_data)
        
        # si hay nombre en la tabla empezamos a meter datos en la BD
        sql = "create table {} (".format(tabla)
        es_date = False

        #print(request.form)

        for clave in request.form:
            
            # saltamos el primer valor que es el nombre de la tabla
            if "nombre_tabla" in clave:
                continue

            valor = request.form.get(clave)

            # comprobamos que el tipo de dato sea Date para no meter longitud en el
            if "date" in valor:
                es_date = True

            # comprobamos que estemos en el valor longitud del tipo de dato y no sea un tipo Date
            if "_len" in clave:
                
                if es_date == False:
                    valor = "({}),".format(valor)
                else:
                    # si es fecha no se imprime el valor actual
                    sql = sql.rstrip(" ") # quitamos el espacio dejado por la ultima vuelta
                    sql += ", ".format(valor) # imprimimos coma y omitimos el valor actual de longitud del dato
                    es_date = False
                    continue

            sql += "{} ".format(valor)        

        # eliminamos ", " dejado por la última pasada del bucle
        sql = sql.rstrip(", ")
        sql += ");"

        print(sql)
        
        return render_template("add.html", params=var_data)

    else:

        return render_template("add.html", params=var_data)




@app.route('/')
@app.route('/home')
@app.route('/inicio')
def index():

    try:
        connection = cx_Oracle.connect(
            user="jsarmenteros",
            password="123456",
            dsn="localhost:1521/orcl",
            encoding="UTF-8"
        )

        print("*************** ", connection.version)

        cur = connection.cursor()
        cur.execute("SELECT table_name FROM user_tables ORDER BY table_name")
  
        rows = cur.fetchall()
        lista_temporal = []

        for filas in rows:
            for celdas in filas:
                lista_temporal.append(celdas)

    except Exception as e:
        print(e)
    finally:
        connection.close()
        print("Conexión cerrada")

    var_data = {
        "titulo": "Gestión BD",
        "datos_bd": lista_temporal
    }

    return render_template("index.html", params=var_data)

# hace una consulta a la BD
def consulta_bd(sql):
    return  "datos devueltos"

    

if __name__ == '__main__':
    #app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)
