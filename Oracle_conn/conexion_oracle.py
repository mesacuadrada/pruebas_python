import cx_Oracle
from flask import Flask, render_template

cx_Oracle.init_oracle_client(lib_dir=r"F:\Downloads\WINDOWS.X64_193000_db_home\instantclient_21_3")

app = Flask("__main__")


@app.route("/calculadora/<operacion>/<int:num1>/<int:num2>")
def calculadora(operacion="", num1=0, num2=0):

    var_data = {
        'resultado': 0
    }

    if operacion == "suma":
        var_data["resultado"] = num1 + num2
        print("entra en suma que es ", var_data)
    elif operacion == "resta":
        var_data["resultado"] = num1 - num2
        print("entra en resta que es ", var_data)
    elif operacion == "multiplicacion":
        var_data["resultado"] = num1 * num2
    elif operacion == "division":
        var_data["resultado"] = num1 / num2
    else:
        var_data["resultado"] = "datos erróneos"

    return render_template("calculadora.html", var_data=var_data)


try:
    connection = cx_Oracle.connect(
        user="jsarmenteros",
        password="123456",
        dsn="localhost:1521/orcl",
        encoding="UTF-8"
    )
    print(connection.version)

    cur = connection.cursor()
    cur.execute("SELECT * FROM EMPLEADOS")
    rows = cur.fetchall()
    print("elementos: ", len(rows))

    for filas in rows:

        for celda in filas:
            print(celda)

        print("-------------------")

except Exception as e:
    print(e)
finally:
    connection.close()
    print("Conexión cerrada")

if __name__ == '__main__':
    app.run(port=8000, debug=True)
