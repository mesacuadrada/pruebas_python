from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# conexión MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'jsarmenteros'
app.config['MYSQL_PASSWORD'] = "Jm)GCELdIwA0hBlI"
app.config['MYSQL_DB'] = "proyecto_final"

conn = MySQL(app)


@app.before_request
def before_request():
    print("antes de la petición...")


@app.after_request
def after_request(response):
    print("después de la petición...")
    return response


@app.route('/')
@app.route('/home')
@app.route('/inicio')
def index():
    cursos = ["PHP", "Python", "Java", "Kotlin", "Dart", "Javascript"]
    var_data = {
        "titulo": "index",
        "bienvenida": "saludos",
        "cursos": cursos,
        "numero_cursos": len(cursos)
    }
    return render_template("index.html", params=var_data)


@app.route('/contacto/<nombre>/<int:edad>')  # <nombre> indica q se espera parámetro nombre
def contacto(nombre, edad):
    var_data = {
        'titulo': 'Contacto',
        'nombre': nombre,
        'edad': edad
    }
    return render_template("contacto.html", params=var_data)


@app.route('/correo')
def correo():
    var_data = {
        'titulo': "Correo"
    }
    return render_template("correo.html", params=var_data)


def query_string():
    print(request)
    print(request.args)
    return "<h2>ok: {}, {}, {}</h2>".format(
        request.args.get('nombre'),
        request.args.get('edad'),
        request.args.get('correo')
    )


@app.route('/cursos')
def listar_cursos():
    data = {}

    try:
        cur = conn.connection.cursor()
        sql = "select * from dgt"
        cur.execute(sql)
        datos = cur.fetchall()
        # print(datos)
        data['datos'] = datos
        data['mensaje'] = 'Éxito'

    except Exception as e:
        data['mensaje'] = 'Error'

    return jsonify(data)


def pagina_no_encontrada(error):
    # return render_template('404.html'), 404  # muestra 404 personalizado
    return redirect(url_for('index'))  # redirige a index.html


if __name__ == '__main__':
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)
