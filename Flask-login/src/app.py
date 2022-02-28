from flask import Flask, render_template, request, redirect, url_for
from config import config

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])
        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

''' lo dejamos en el minuto 16:34 del vídeo: 
https://www.youtube.com/watch?v=FX0lMm_Qj10
'''

@app.route("/")
def index():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
