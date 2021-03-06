from collections import defaultdict
from pickle import POP_MARK
import re
from flask import Flask, flash, render_template, request, redirect, url_for, jsonify, session
from markupsafe import Markup
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mysqldb import MySQL
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient")

app = Flask(__name__)

# conexión MySQL
app.config['SECRET_KEY'] = 'GFeqrwt·$%dsafg$&%/"·'

conn = MySQL(app)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/login', methods=["GET", "POST"])
def login():
    var_data = {
        "titulo": "Login"
    }

    #print(">>" + generate_password_hash("123456")+ "<<")

    if request.method == "POST":

        usuario = request.form.get('user')
        password = request.form.get('pass')

        # si hay nombre en la tabla empezamos a meter datos en la BD
        sql = "SELECT password FROM usuarios WHERE username = 'jsarmenteros'"
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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/remove_row', methods=["GET", "POST"])
def remove_row():

    # si no se ha iniciado sesión, lo mandamos al login
    if inicio_sesion() == False:
        return redirect('/login');

    if request.method=='POST':
        row = request.form['dic']
        tabla = request.form['tabla']
    else:
        return redirect('/inicio');

    dic = eval(row)
    print(dic)

    var_columnas = consulta_bd("SELECT column_name FROM all_tab_columns WHERE table_name ='" + tabla  + "'")
    lista_columnas = []

    # recuepramos los nombres de las columnas para montar el delete
    for filas in var_columnas:
        for celdas in filas:
            lista_columnas.append(celdas)

    sql = "DELETE FROM {} WHERE ".format(tabla);

    # montamos la consulta con las columnas y valores de sendas listas
    i = 0;
    for fila in dic:
        sql += "{} = '{}' AND ".format(lista_columnas[i], dic[fila])
        i += 1

    sql = sql[:-4]
    #print(sql)
    consulta_bd(sql)

    #return redirect('/show/' + tabla);
    var_data = {
        "titulo": tabla
    }

    return redirect('/show/' + tabla)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/update_row', methods=["GET", "POST"])
def update_row():

    # si no se ha iniciado sesión, lo mandamos al login
    if inicio_sesion() == False:
        return redirect('/login');

    if request.method=='POST':
        row = request.form['dic']
        pk = request.form['pk']
        tabla = request.form['tabla']
    else:
        row = request.args['dic']
        pk = request.args['pk']
        tabla = request.args['tabla']

    # pasamos de string a diccionario
    dic = eval(row)
    """ Warnings when using eval():
    Consider a situation where you are using a Unix system (macOS, Linux, etc) and you
    have imported the os module. The os module provides a portable way to use operating
    system functionalities like reading or writing to a file.
    If you allow users to input a value using eval(input()), the user may issue
    commands to change file or even delete all the files using the command:
    os.system('rm -rf *')."""

    # print("primary key: " +  pk)
    var_columnas = consulta_bd("SELECT column_name FROM all_tab_columns WHERE table_name ='" + tabla  + "'")
    lista_columnas = []
    pos_pk = 0

    # para hacer el update necesitamos identificar la columna con el PK.
    # para saber qué columna es la PK primero obtenemos los nombres de las columnas
    # recorremos la lista con los nombres en busca de la palabra que sabemos que es la PK
    # cuando encontremos la palabra, nos quedamos con la posición, que será la misma
    # que tenga el listado con los valores a modificar

    # ritual para acceder a los datos de la lista sin (' ')
    for col in var_columnas:
        for dato in col:
            # creamos una lista a partir de los datos de la tupla
            lista_columnas.append(dato)
            # si coincide el dato con la pk nos quedamos con la posición en la lista
            # porque coincidirá con la posición del dato en la tabla q es clave primaria
            if pk in dato:
                pos_pk = lista_columnas.index(dato)

    contador = 0
    for fila in dic:
        contador = 0
        sql="UPDATE {} SET ".format(tabla)
        campo_where = ""
        for celda in fila:
            # si coincide el ídnice del PK con el actual, estamos ante el campo PK de la tabla
            if contador == pos_pk:
                sql += "{}='{}', ".format(lista_columnas[contador], fila[celda])
                campo_pk = lista_columnas[contador]
                campo_where = fila[celda]
            else:
                sql += "{}='{}', ".format(lista_columnas[contador], fila[celda])
            contador += 1
        # quitamos los 2 úlitmos carácteres añadidos en el bucle
        sql = sql[:-2]
        sql += " WHERE {} = '{}'".format(campo_pk, campo_where)
        print(sql)
        consulta_bd(sql)

    #print(type(row))
    return redirect('/show/' + tabla);


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/show/<tabla>')
def show(tabla):

    if inicio_sesion() == False:
        return redirect('/login');

    var_data = {
        "titulo": tabla
    }

    var_registros = consulta_bd("SELECT * FROM {}".format(tabla))

    # recuperamos el nombre de las columnas para mostrarlo
    var_columnas = consulta_bd("SELECT column_name FROM all_tab_columns WHERE table_name ='" + tabla  + "'")
    var_sql = """
            SELECT cols.column_name
            FROM all_constraints cons, all_cons_columns cols
            WHERE cols.table_name = '{}'
            AND cons.constraint_type = 'P'
            AND cons.constraint_name = cols.constraint_name
            AND cons.owner = cols.owner
            ORDER BY cols.table_name, cols.position
        """.format(tabla)

    var_pk = consulta_bd(var_sql)

    # ritual para quitar los carácteres que devuelve Oracle en sus resultados = (' ')
    for fila in var_pk:
        for celda in fila:
            var_pk = celda

    if len(var_pk) == 0:
        # enviamos un mensaje flask con contenido HTML
        flash(
            Markup("Esta tabla no tiene <i><b>primary key</b></i>, se tomará la primera columna como identificador")
        )

    return render_template("show.html", params=var_data, pk=var_pk, registros=var_registros, columnas=var_columnas)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/add_table', methods=["GET", "POST"])
def add():

    if inicio_sesion() == False:
        return redirect('/login');

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
        contador = 0
        pk = ""

        for clave in request.form:

            # saltamos el primer valor que es el nombre de la tabla
            if "nombre_tabla" in clave:
                continue # volvemos el inicio del bucle para tratar la siguiente clave

            # accedemos al valor de una clave del formulario
            valor = request.form.get(clave)

            #print("contador {} clave {} valor {}".format(contador, clave, valor))
            if contador == 0:
                pk = valor

            # comprobamos que el tipo de dato sea Date para no meter longitud en él
            if "date" in valor:
                es_date = True

            # comprobamos que estemos en el valor longitud del tipo de dato y no sea un tipo Date
            if "_len" in clave:

                if es_date == False:
                    sql = sql.rstrip(" ") # quitamos el espacio dejado por la ultima vuelta

                    # hacemos la primera columna not null y guardamos su valor para hacerla PK
                    if contador == 2:
                            valor = "({}) NOT NULL, ".format(valor)
                    else:
                            valor = "({}),".format(valor)

                else:
                    # si es fecha no se imprime el valor actual
                    sql = sql.rstrip(" ") # quitamos el espacio dejado por la ultima vuelta
                    sql += ", ".format(valor) # imprimimos coma y omitimos el valor actual de longitud del dato
                    es_date = False
                    continue

            contador +=1

            sql += "{} ".format(valor)


        # eliminamos ", " dejado por la última pasada del bucle
        sql += "primary key ({})".format(pk)
        #sql = sql.rstrip(", ")
        sql += ")" # las sentencias SQL NO deben acabar en ; lanzan error: ORA-00922: falta la opción o no es válida
        print(sql)
        consulta_bd(sql)
        return redirect('/inicio')

    else:
        # el método de llamada es GET
        return render_template("add.html", params=var_data)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/logout')
def logout():
    session.clear();
    return redirect('/login')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/remove')
def remove():

    if inicio_sesion() == False:
        return redirect('/login');

    sql  = "SELECT table_name FROM user_tables ORDER BY table_name"
    resultados = consulta_bd(sql)

    var_data = {
        "titulo": "Eliminar tablas",
        "datos_bd": resultados
    }

    return render_template("remove.html", params=var_data)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

@app.route('/insert', methods=['POST', 'GET'])
def insert():

    # si no se ha iniciado sesión, lo mandamos al login
    if inicio_sesion() == False:
        return redirect('/login');

    var_data = {
        "titulo": "Mostrando tabla"
    }

    if request.method != "POST":
        return render_template("show.html", params=var_data)

    parametros = request.form

    tabla = ""
    valores = ""

    for clave in parametros:

        if clave == "tabla":
            tabla = parametros[clave]
            continue

        valores += "'" + parametros[clave] + "', "

    valores = valores.rstrip(", ")
    sql = "insert into {} values({})".format(tabla, valores);
    consulta_bd(sql)

    return redirect("show/" + tabla)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/remove_table/<tabla>')
def remove_table(tabla):

    if inicio_sesion() == False:
        return redirect('/login');

    if tabla == "USUARIOS":
        flash("No se puede eliminar la tabla USUARIOS")
        return redirect('/remove')

    sql  = "drop table {}".format(tabla)
    resultados = consulta_bd(sql)

    var_data = {
        "titulo": "Eliminar tablas",
        "datos_bd": resultados
    }

    return redirect('/remove')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/')
@app.route('/home')
@app.route('/inicio')
# muestra por defecto la lista de tablas en la BD
def index():

    if inicio_sesion() == False:
        return redirect('/login');

    sql  = "SELECT table_name FROM user_tables ORDER BY table_name"
    lista_temporal = consulta_bd(sql)

    var_data = {
        "titulo": "Gestión BD",
        "datos_bd": lista_temporal
    }

    return render_template("index.html", params=var_data)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def inicio_sesion():

    if 'usuario' in session:
        return True
    else:
        flash ("Inicie sesión para continuar")
        return False

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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

            if str((ex)).lower() != "not a query":
                flash(str(ex))

        finally:
            connection.close()
            # print("Conexión cerrada")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


if __name__ == '__main__':
    #app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)
    app.secret_key = "ñhsaFSADfsdi239847adsfSDF(=)(&"
