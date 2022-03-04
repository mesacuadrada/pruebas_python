import re
from flask import Flask, flash, render_template, request, redirect, url_for, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mysqldb import MySQL
import cx_Oracle

app = Flask(__name__)

# conexión MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'jsarmenteros'
app.config['MYSQL_PASSWORD'] = "Jm)GCELdIwA0hBlI"
app.config['MYSQL_DB'] = "proyecto_final"
app.config['SECRET_KEY'] = 'GFeqrwt·$%dsafg$&%/"·'

conn = MySQL(app)


@app.route('/login', methods=["GET", "POST"])
def login():
    var_data = {
        "titulo": "Login"
    }

    if request.method == "POST":

        usuario = request.form.get('user')
        password = request.form.get('pass')

        # si hay nombre en la tabla empezamos a meter datos en la BD
        sql = "SELECT password FROM usuarios WHERE usuario = 'jsarmenteros'"
        var_registros = consulta_bd(sql)
        bd_pass = ""

        # recorremos la fila y sacamos el valor
        for fila in var_registros:
            for celda in fila:
                bd_pass = celda

        # comparamos el hash almacenado en BD con el hash creado a partir del parámetro pass
        pass_correcta = check_password_hash(bd_pass, password)

        if pass_correcta:
            session['usuario'] = usuario
            session['password'] = password
            return redirect('/inicio')
        else:
            flash("Contraseña incorrecta")
            return render_template('login.html', params=var_data)

    else: # si entramos por GET
        return render_template('login.html', params=var_data)

@app.route('/show/<tabla>')
def show(tabla):

    var_data = {
        "titulo": "Contenido de " + tabla
    }

    var_registros = consulta_bd("SELECT * FROM {}".format(tabla))
    print(var_registros)
    # recuperamos el nombre de las columnas para mostrarlo
    var_columnas = consulta_bd("SELECT column_name FROM all_tab_columns WHERE table_name ='" + tabla  + "'")

    return render_template("show.html", params=var_data, registros=var_registros, columnas=var_columnas)


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
            flash("Introduzca nombre de tabla")
            return render_template("add.html", params=var_data)

        # si hay nombre en la tabla empezamos a meter datos en la BD
        sql = "create table {} (".format(tabla)
        es_date = False

        '''
        # convierte una lista a diccionario
        lista = dict(request.form)
        print(lista.items)
        '''
        for clave in request.form:

            # saltamos el primer valor que es el nombre de la tabla
            if "nombre_tabla" in clave:
                continue # volvemos el inicio del bucle para tratar la siguiente clave

            # accedemos al valor de una clave del formulario
            valor = request.form.get(clave)

            # comprobamos que el tipo de dato sea Date para no meter longitud en él
            if "date" in valor:
                es_date = True

            # comprobamos que estemos en el valor longitud del tipo de dato y no sea un tipo Date
            if "_len" in clave:

                if es_date == False:
                    sql = sql.rstrip(" ") # quitamos el espacio dejado por la ultima vuelta
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
        sql += ")" # las sentencias SQL NO deben acabar en ; lanzan error: ORA-00922: falta la opción o no es válida

        print(consulta_bd(sql))
        return redirect('/inicio')

    else:
        # el método de llamada es GET
        return render_template("add.html", params=var_data)

@app.route('/logout')
def logout():
    session.clear();
    return redirect('/login')


@app.route('/remove')
def remove():

    if 'usuario' not in session:
        return "<h1><a href='/login'>Inicie sesión</a> primero.</h1>"

    sql  = "SELECT table_name FROM user_tables ORDER BY table_name"
    resultados = consulta_bd(sql)

    var_data = {
        "titulo": "Eliminar tablas",
        "datos_bd": resultados
    }

    return render_template("remove.html", params=var_data)


@app.route('/remove_table/<tabla>')
def remove_table(tabla):

    if 'usuario' not in session:
        return "<h1><a href='/login'>Inicie sesión</a> primero.</h1>"

    sql  = "drop table {}".format(tabla)
    print("************", sql)
    resultados = consulta_bd(sql)

    var_data = {
        "titulo": "Eliminar tablas",
        "datos_bd": resultados
    }

    return redirect('/remove')


@app.route('/')
@app.route('/home')
@app.route('/inicio')
# muestra por defecto la lista de tablas en la BD
def index():

    if 'usuario' not in session:
        return "<h1><a href='/login'>Inicie sesión</a> primero.</h1>"

    sql  = "SELECT table_name FROM user_tables ORDER BY table_name"
    lista_temporal = consulta_bd(sql)

    var_data = {
        "titulo": "Gestión BD",
        "datos_bd": lista_temporal
    }

    return render_template("index.html", params=var_data)


# hace una consulta a la BD
def consulta_bd(sql):

        try:
            connection = cx_Oracle.connect(
                user="jsarmenteros",
                password="123456",
                dsn="localhost:1521/orcl",
                encoding="UTF-8"
            )

            #print("*************** ", connection.version)

            cur = connection.cursor()
            query = "alter session set \"_use_nosegment_indexes\" = true"
            cur.execute(query)
            cur.execute(sql)
            connection.commit()

            return cur.fetchall()

        except Exception as ex:
            print(ex)
        finally:
            connection.close()
            print("Conexión cerrada")


if __name__ == '__main__':
    #app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)
    app.secret_key = "ñhsaFSADfsdi239847adsfSDF(=)(&"
