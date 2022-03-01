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

@app.route('/add')
def add():
    var_data = {
        "titulo": "Añadir tabla"
    }
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

        print(connection.version)

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



if __name__ == '__main__':
    #app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)
