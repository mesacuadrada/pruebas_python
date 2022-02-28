# I N T E R F A Z   G R Á F I C A

# https://docs.python.org/es/3/library/tkinter.html
from tkinter import *

raiz = Tk()
raiz.attributes('-toolwindow', True)  # quita botones de maximizar y minimizar
raiz.config(padx=5, pady=5)
raiz.title("Pruebas GUI")
raiz.resizable(True, True)
raiz.iconbitmap("sopa.ico")
# raiz.wm_attributes('-transparentcolor', raiz['bg'])
# raiz.geometry("640x480") # tamaño de la ventana

frame = Frame()
frame.pack(fill="both",
           expand=True)  # mete el frame en la raíz, side="top, left, right, bottom" alineación, anchor="n, s, e, w"
#  fill se adapta al padre
frame.config(bg="silver", width="640", height="480", pady=5, padx=5)

valor_texto = StringVar()

Label(frame, text="Hola mundo", font=("arial", 18)).grid(row=0, column=0)

imagen = PhotoImage(file="imagen.png")
Label(frame, image=imagen).grid(row=1, column=0)

texto = Entry(frame, font=('arial', 10), fg='gray', textvariable=valor_texto)
texto.grid(row=2, column=0)

passw = Entry(frame, font=('arial', 11), fg='gray', show='*')
passw.insert(0, 'password')
passw.grid(row=3, column=0, columnspan=1, rowspan=1)

import tkinter.scrolledtext as scrolledtext

miTexto = scrolledtext.ScrolledText(frame, width=20, height=8, font=("arial", 16))
miTexto.grid(row=4, column=0)

# RADIO BUTTONS
opciones = IntVar()


def get_genero():
    print(opciones.get())


Radiobutton(raiz, text="Masculino", variable=opciones, value=1, command=get_genero).pack()
Radiobutton(raiz, text="Femenino", variable=opciones, value=2, command=get_genero).pack()

# CHECK BUTTONS
playa = IntVar()
montana = IntVar()
mar = IntVar()


def opcion_escogida():
    opciones = ""

    if playa.get() == 1:
        opciones += " playa"

    if mar.get() == 1:
        opciones += " mar"

    if montana.get() == 1:
        opciones += " montaña"

    print(opciones)


Checkbutton(raiz, text="Playa", variable=playa, onvalue=1, offvalue=0, command=opcion_escogida).pack()
Checkbutton(raiz, text="Mar", variable=mar, onvalue=1, offvalue=0, command=opcion_escogida).pack()
Checkbutton(raiz, text="Montaña", variable=montana, onvalue=1, offvalue=0, command=opcion_escogida).pack()

# VENTANAS EMERGENTES

from tkinter import messagebox


def opcion_salir():
    valor = messagebox.askquestion("Salir", "¿Desea salir?")
    if valor == "yes":
        raiz.destroy()


# BARRA MENÚ SUPERIOR

barra_menu = Menu(raiz)
raiz.config(menu=barra_menu)

menu_archivo = Menu(barra_menu, tearoff=0)
menu_archivo.add_command(label="Nuevo")
menu_archivo.add_command(label="Guardar")
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=opcion_salir)

menu_edicion = Menu(barra_menu)
menu_herramientas = Menu(barra_menu)
menu_ayuda = Menu(barra_menu)

barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
barra_menu.add_cascade(label="Edición", menu=menu_edicion)
barra_menu.add_cascade(label="Herramientas", menu=menu_herramientas)
barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

#  coge fecha actual
from datetime import datetime


def codigo_boton():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    valor_texto.set(current_time)


boton_envio = Button(raiz, text=" E N V I A R ", command=codigo_boton)
boton_envio.pack()

# aplica a todos los widget los mismos parámetros
for widget in frame.winfo_children():

    if "frame" in str(widget.widgetName):  # el texto con scroll se llama frame... lo omitimos, no admite FG=
        continue

    widget.grid(padx=(5, 0), pady=(8, 0))
    widget.configure(fg='red', font=('arial', 16))
    print(widget.widgetName)


#  maneja evento onlcik para limpiar texto campo
def on_click(event):
    texto.configure(state=NORMAL)
    texto.delete(0, END)

    # make the callback only work once
    texto.unbind('<Button-1>', on_click_id)


on_click_id = texto.bind('<Button-1>', on_click)

# DIÁLOGO APERTURA FICHERO
from tkinter import filedialog


def abre_fichero():
    fichero = filedialog.askopenfilename(
        title="Abrir", initialdir="C:", filetypes=(
            ("Excel", ".xlsx"),
            ("Texto", ".txt"),
            ("Images", ".png")
        )
    )
    print(fichero)


Button(raiz, text=" Abrir fichero ", command=abre_fichero).pack()

raiz.mainloop()
