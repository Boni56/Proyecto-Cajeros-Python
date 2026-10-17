import customtkinter as ctk  
from tkcalendar import DateEntry
import pyodbc
from PIL import Image
from tkinter import messagebox
from CapaNegocio import iniciar_sesion
from datetime import datetime


#funciones reutilizables 
def crear_titulo(contenedor, texto, tamano, color):
    return ctk.CTkLabel(
        contenedor,
        text=texto,
        font=("Arial", tamano, "bold"),
        text_color=color
    )

def crear_boton(contenedor, texto, comando=None):
    return ctk.CTkButton(
        contenedor,
        text=texto,
        text_color="#000000",
        fg_color="#54BEF0",
        hover_color="#2C7DF6",
        command=comando
    )
#variable global 
usuario_actual = None
operacion_actual = ""
id_cajero_actual = None
usuario_sql = None
password_sql = None

#Configuracion estetica y creacion de la ventana 
VentanaP = ctk.CTk() #crea la ventana 
VentanaP.geometry("800x600")
VentanaP.title("Cajero Automatico")
VentanaP.iconbitmap("IconoCajeroICO.ico")
VentanaP.resizable(False,False) #esto es para tener el tamano fijo 
VentanaP.configure(fg_color="#D76BF2")
ctk.set_appearance_mode("dark")

 #Ceacion de frames para la parte estetica del cajero 
 #Frame superior 
frame_superior = ctk.CTkFrame(
  VentanaP,
  height=80,
  fg_color="#4A4545"
  
 )

frame_superior.pack(side="top", fill = "x")

titulo = crear_titulo(
    frame_superior,
    "Cajeros Automaticos Cartago",
    24,
    "white"
)
titulo.pack(pady=20)

#Frame de logo del cajero 
frame_logo = ctk.CTkFrame(
    VentanaP,
    width=320,
    height=520,
    fg_color="#59BBC2"
    
)

frame_logo.pack(side="left", fill="y")

logo = ctk.CTkImage(
    light_image=Image.open("IconoCajero.PNG"),
    dark_image=Image.open("IconoCajero.PNG"),
    size=(200, 200)
)
label_logo = ctk.CTkLabel(
    frame_logo,
    image=logo,
    text=""
)
label_logo.place(x=50, y=150)

titulo = ctk.CTkLabel(
    frame_logo,
    text="Bienvenidos",
    font=("Arial", 32, "bold"),
    text_color="black"
)
titulo.place(x=50,y=45)

titulo = ctk.CTkLabel(
    frame_logo,
    text="Proyecto Realizado Por:\n Eymi Bonilla y Sebastian Sanchez" ,
    font=("Arial", 18, "normal"),
    text_color="black"
)
titulo.place(x=20,y=450)

#frame del inicio de seccion 
frame_login = ctk.CTkFrame(
    VentanaP,
    fg_color="#D76BF2"
)

frame_login.pack(side="right", fill="both", expand=True)

lbllogin = crear_titulo(
    frame_login,
    "INICIO DE SESION",
    28,
    "black"
)

lbllogin.pack(pady=40)

lbl_cuenta = ctk.CTkLabel(
    frame_login,
    text="Número de Cuenta"
)

lbl_cuenta.pack()

entry_cuenta = ctk.CTkEntry(
    frame_login,
    width=250,
    fg_color="#FFFFFF",      
    text_color="#000000",   
    border_color="#687A94"
)

entry_cuenta.pack(pady=10)


lbl_pin = ctk.CTkLabel(
    frame_login,
    text="PIN de Seguridad"
)

lbl_pin.pack()

entry_pin = ctk.CTkEntry(
    frame_login,
    width=250,
    fg_color="#FFFFFF",      
    text_color="#000000",    
     border_color="#687A94",
    show="*" 
)

entry_pin.pack(pady=10)
#funcion para cambiar entre pantallas 
def cambiar_frame(frame_ocultar, frame_mostrar):
    frame_ocultar.pack_forget()
    frame_mostrar.pack(
        side="right",
        fill="both",
        expand=True
    )

def seleccionar_cajero(id_cajero):
    global id_cajero_actual
    id_cajero_actual = id_cajero
    abrir_menu()

def abrir_menu():

    lbl_bienvenida.configure(
        text=f"Bienvenido {usuario_actual.nombre}"
    )
    cambiar_frame(
        frame_cajeros,
        frame_menu
    )
#fin de la funcion cambiar pantallas 

#frame para mostar el comprobante 
def mostrar_comprobante(
    operacion,
    monto,
    saldo_anterior,
    saldo_actual
):
    ventana = ctk.CTkToplevel()
    ventana.title("Comprobante")
    ventana.geometry("450x350")
    ventana.resizable(False, False)
    frame = ctk.CTkFrame(
        ventana,
        fg_color="white"
    )
    frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )
    titulo = ctk.CTkLabel(
        frame,
        text="COMPROBANTE",
        font=("Arial", 20, "bold"),
        text_color="black"
    )
    titulo.pack(pady=10)
    texto = (
        f"Cliente: {usuario_actual.nombre}\n"
        f"Cuenta: {usuario_actual.numero_cuenta}\n"
        f"Cajero: {id_cajero_actual}\n\n"
        f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        f"Operación: {operacion.upper()}\n"
        f"Monto: ₡{monto:.2f}\n\n"
        f"Saldo anterior: ₡{saldo_anterior:.2f}\n"
        f"Saldo actual: ₡{saldo_actual:.2f}"
    )
    lbl_info = ctk.CTkLabel(
        frame,
        text=texto,
        text_color="black",
        justify="left",
        anchor="w",
        font=("Arial", 14)
    )
    lbl_info.pack(
        padx=20,
        pady=10,
        anchor="w"
    )
    btn_cerrar = ctk.CTkButton(
        frame,
        text="Cerrar",
        command=ventana.destroy
    )
    btn_cerrar.pack(pady=15)
#fin del comprobate 

#Creacion de la ventana de los cajeros 
frame_cajeros = ctk.CTkFrame(
    VentanaP,
    fg_color="#D76BF2"
)
titulo_cajero = ctk.CTkLabel(
    frame_cajeros,
    text="SELECCIONE UN CAJERO",
    font=("Arial", 24, "bold"),
    text_color="black"
)

titulo_cajero.pack(pady=30)

cajeros = [
    ("Cajero 1", "Ubicación: CUC", "ImagenCajero1.png"),
    ("Cajero 2", "Ubicación: Cartago Centro", "ImagenCajero2.png"),
    ("Cajero 3", "Ubicación: Paraíso, Cartago", "ImagenCajero3.png")
]

for i, (nombre, ubicacion, archivo) in enumerate(
    cajeros,
    start=1
):

    imagen = ctk.CTkImage(
        light_image=Image.open(archivo),
        dark_image=Image.open(archivo),
        size=(50, 50)
    )
    boton = ctk.CTkButton(
        frame_cajeros,
        image=imagen,
        compound="left",
        text=f"{nombre}\n{ubicacion}",
        width=300,
        height=70,
        command=lambda x=i: seleccionar_cajero(x)
    )
    boton.image = imagen
    boton.pack(pady=15)
#fin de la creacion de los cajeros 

#menu de los cajeros 
frame_menu = ctk.CTkFrame(
    VentanaP,
    fg_color="#D76BF2"
)

lbl_bienvenida = ctk.CTkLabel(
    frame_menu,
    text="Bienvenido",
    font=("Arial",24,"bold"),
    text_color="black"
)

lbl_bienvenida.pack(pady=20)
#fin del menu 
#frame de operaciones del cajero 
# frame para operaciones
# frame para operaciones
frame_operaciones = ctk.CTkFrame(
    VentanaP,
    fg_color="#D76BF2"
)

lbl_titulo_operacion = ctk.CTkLabel(
    frame_operaciones,
    text="OPERACIÓN",
    font=("Arial", 24, "bold"),
    text_color="black"
)
lbl_titulo_operacion.pack(pady=20)

# Campo 1
lbl_campo1 = ctk.CTkLabel(
    frame_operaciones,
    text="Monto"
)
lbl_campo1.pack()

entry_campo1 = ctk.CTkEntry(
    frame_operaciones,
    width=250
)
entry_campo1.pack(pady=10)

# Campo 2
lbl_campo2 = ctk.CTkLabel(
    frame_operaciones,
    text=""
)
lbl_campo2.pack()

entry_campo2 = ctk.CTkEntry(
    frame_operaciones,
    width=250
)
entry_campo2.pack(pady=10)


def confirmar_operacion():

    global operacion_actual
    global usuario_sql
    global password_sql
    global id_cajero_actual

    try:
        exito = False
        mensaje = ""

        if operacion_actual == "deposito":
                
            texto_monto = entry_campo1.get().strip()
            if texto_monto == "":
                messagebox.showerror(
                "Error",
                "Debe ingresar un monto."
            )
                return
            
            monto = float(texto_monto) 
            saldo_anterior = usuario_actual.saldo
            exito = usuario_actual.depositar(
                usuario_sql,
                password_sql,
                id_cajero_actual,
                monto
            )
            if exito:
                mensaje = (
                    f"Depósito realizado correctamente.\n"
                    f"Saldo actual: ₡{usuario_actual.saldo}"
                )
                detalle = "Depósito en cuenta"
            else:
                mensaje = ("No fue posible realizar el depósito.")

        elif operacion_actual == "retiro":              
            texto_monto = entry_campo1.get().strip()
            if texto_monto == "":
                messagebox.showerror(
                "Error",
                "Debe ingresar un monto."
                )
                return
            monto = float(texto_monto)
            saldo_anterior = usuario_actual.saldo
            exito = usuario_actual.retirar(
                usuario_sql,
                password_sql,
                id_cajero_actual,
                monto
            )
            if exito:
                mensaje = (
                f"Retiro realizado correctamente.\n"
                f"Saldo actual: ₡{usuario_actual.saldo}"
                )
                detalle = "Retiro de efectivo"
            else:
                mensaje = ( "No fue posible realizar el retiro."
            )
                    
        elif operacion_actual == "transferencia":
            cuenta = entry_campo1.get().strip()
            texto_monto = entry_campo2.get().strip()
            if cuenta == "" or texto_monto == "":
                messagebox.showerror(
                "Error",
                "Debe completar todos los campos."
                )
                return

            monto = float(texto_monto)
            saldo_anterior = usuario_actual.saldo
            exito = usuario_actual.transferir(
                usuario_sql,
                password_sql,
                id_cajero_actual,
                cuenta,
                monto
            )
            if exito:
                mensaje = (
                    f"Transferencia realizada correctamente.\n"
                    f"Saldo actual: ₡{usuario_actual.saldo}"
                )
                detalle = f"Transferencia a cuenta {cuenta}"
            else:
                mensaje = (
                    "No fue posible realizar la transferencia."
                )

        elif operacion_actual == "hogar":
            servicio = entry_campo1.get().strip()
            if servicio == "":
                messagebox.showerror(
                    "Error",
                    "Debe ingresar un servicio."
                )
                return
            texto_monto = entry_campo2.get().strip()
            if texto_monto == "":
                messagebox.showerror(
                    "Error",
                    "Debe ingresar un monto."
                )
                return
            monto = float(texto_monto)
            saldo_anterior = usuario_actual.saldo
            exito = usuario_actual.registrar_pago(
                usuario_sql,
                password_sql,
                id_cajero_actual,
                "Hogar",
                servicio,
                monto
            )
            if exito:
                mensaje = (
                    f"Pago realizado correctamente.\n"
                    f"Saldo actual: ₡{usuario_actual.saldo}"
                )
                detalle = servicio
            else:
                mensaje = (
                    "No fue posible realizar el pago."
                )

        elif operacion_actual == "telefonia":
            servicio = entry_campo1.get().strip()
            if servicio == "":
                messagebox.showerror(
                    "Error",
                    "Debe ingresar un servicio."
                )
                return
            texto_monto = entry_campo2.get().strip()
            if texto_monto == "":
                messagebox.showerror(
                    "Error",
                    "Debe ingresar un monto."
                )
                return
            monto = float(texto_monto)
            saldo_anterior = usuario_actual.saldo
            exito = usuario_actual.registrar_pago(
                usuario_sql,
                password_sql,
                id_cajero_actual,
                "Telefonía",
                servicio,
                monto
            )
            if exito:
                mensaje = (
                    f"Pago realizado correctamente.\n"
                    f"Saldo actual: ₡{usuario_actual.saldo}"
                )
                detalle = servicio
            else:
                mensaje = (
                    "No fue posible realizar el pago."
                )

        elif operacion_actual == "entretenimiento":
            servicio = entry_campo1.get().strip()
            if servicio == "":
                messagebox.showerror(
                    "Error",
                    "Debe ingresar un servicio."
                )
                return
            texto_monto = entry_campo2.get().strip()
            if texto_monto == "":
                messagebox.showerror(
                    "Error",
                    "Debe ingresar un monto."
                )
                return
            monto = float(texto_monto)
            saldo_anterior = usuario_actual.saldo
            exito = usuario_actual.registrar_pago(
                usuario_sql,
                password_sql,
                id_cajero_actual,
                "Entretenimiento",
                servicio,
                monto
            )
            if exito:
                mensaje = (
                    f"Pago realizado correctamente.\n"
                    f"Saldo actual: ₡{usuario_actual.saldo}"
                )
                detalle = servicio
            else:
                mensaje = (
                "No fue posible realizar el pago."
            )
                
        operacion = operacion_actual
        saldo_actual = usuario_actual.saldo
        if exito:
            cambiar_frame(
                frame_operaciones,
                frame_menu
            )
            mostrar_comprobante(
                operacion,
                monto,
                saldo_anterior,
                saldo_actual,
                detalle
            )
        else:
            messagebox.showerror(
                "Error",
                mensaje
            )
    except Exception as e:
        print("ERROR:", e)
        messagebox.showerror(
            "Error",
            str(e)
        )

btn_confirmar = ctk.CTkButton(
    frame_operaciones,
    text="Confirmar",
    command=confirmar_operacion
)
btn_confirmar.pack(pady=10)

btn_volver = ctk.CTkButton(
    frame_operaciones,
    text="Volver",
    command=lambda: cambiar_frame(
        frame_operaciones,
        frame_menu
    )
)

btn_volver.pack(pady=10)
#fin de operaciones 

# funcion de consultar saldo 
def consultar_saldo():
    global usuario_actual

    saldo = usuario_actual.consultar_saldo()

    messagebox.showinfo(
        "Saldo Disponible",
        f"Su saldo actual es:\n₡{saldo:,}"
    )
# fin de la consulta de saldo 
def abrir_deposito():

    global operacion_actual

    operacion_actual = "deposito"

    lbl_titulo_operacion.configure(
        text="DEPÓSITO"
    )

    lbl_campo1.configure(
        text="Monto"
    )

    entry_campo1.delete(0, "end")

    lbl_campo2.pack_forget()
    entry_campo2.pack_forget()

    cambiar_frame(
        frame_menu,
        frame_operaciones
    )
def abrir_retiro():

    global operacion_actual

    operacion_actual = "retiro"

    lbl_titulo_operacion.configure(
        text="RETIRO"
    )

    lbl_campo1.configure(
        text="Monto"
    )

    entry_campo1.delete(0, "end")

    lbl_campo2.pack_forget()
    entry_campo2.pack_forget()

    cambiar_frame(
        frame_menu,
        frame_operaciones
    )
def abrir_transferencia():

    global operacion_actual

    operacion_actual = "transferencia"

    lbl_titulo_operacion.configure(
        text="TRANSFERENCIA"
    )

    lbl_campo1.configure(
        text="Cuenta destino"
    )

    entry_campo1.delete(0, "end")

    lbl_campo2.configure(
        text="Monto"
    )

    lbl_campo2.pack()

    entry_campo2.delete(0, "end")
    entry_campo2.pack(pady=10)

    btn_confirmar.pack_forget()
    btn_volver.pack_forget()

    btn_confirmar.pack(pady=10)
    btn_volver.pack(pady=10)
    cambiar_frame(
        frame_menu,
        frame_operaciones
    )

def abrir_pago(tipo, titulo, etiqueta):

    global operacion_actual

    operacion_actual = tipo

    lbl_titulo_operacion.configure(
        text=titulo
    )

    lbl_campo1.configure(
        text=etiqueta
    )

    entry_campo1.delete(0, "end")

    lbl_campo2.configure(
        text="Monto"
    )

    entry_campo2.delete(0, "end")

    lbl_campo2.pack_forget()
    entry_campo2.pack_forget()

    lbl_campo2.pack(before=btn_confirmar)
    entry_campo2.pack(pady=10, before=btn_confirmar)

    cambiar_frame(
        frame_pagos,
        frame_operaciones
    )

#funcion de pagos 
def pagos():
    cambiar_frame(
        frame_menu,
        frame_pagos
    )
#fin de la funcion pagos 
# frame de pagos del hogar, telefonia ....
frame_pagos = ctk.CTkFrame(
    VentanaP,
    fg_color="#D76BF2"
)

lbl_pago = ctk.CTkLabel(
    frame_pagos,
    text="SELECCIONE EL TIPO DE PAGO",
    font=("Arial",24,"bold"),
    text_color="black"
)
lbl_pago.pack(pady=20)
#fin del frame pagos de hogar, telefonia... 
tipos_pago = [
    (
        "Hogar",
        lambda: abrir_pago(
            "hogar",
            "PAGO HOGAR",
            "Servicio (Agua, Luz, Internet)"
        )
    ),

    (
        "Telefonía",
        lambda: abrir_pago(
            "telefonia",
            "PAGO TELEFONÍA",
            "Compañía (Kolbi, Claro, Liberty)"
        )
    ),

    (
        "Entretenimiento",
        lambda: abrir_pago(
            "entretenimiento",
            "PAGO ENTRETENIMIENTO",
            "Servicio (Netflix, Spotify, Disney+)"
        )
    )
]

for texto, funcion in tipos_pago:

    ctk.CTkButton(
        frame_pagos,
        text=texto,
        command=funcion
    ).pack(pady=10)
#boton para regresar 
btn_volver_pagos = ctk.CTkButton(
    frame_pagos,
    text="Volver",
    command=lambda: cambiar_frame(
        frame_pagos,
        frame_menu
    )
)
btn_volver_pagos.pack(pady=20)
#finde del boton volver  
#funcion de ver el historial 
#frame historial 
frame_historial = ctk.CTkFrame(
    VentanaP,
    fg_color="#D76BF2"
)
lbl_historial = ctk.CTkLabel(
    frame_historial,
    text="CONSULTAR HISTORIAL",
    font=("Arial", 24, "bold"),
    text_color="black"
)
lbl_historial.pack(pady=20)

lbl_inicio = ctk.CTkLabel(
    frame_historial,
    text="Fecha Inicial"
)
lbl_inicio.pack()

calendario_inicio = DateEntry(
    frame_historial,
    date_pattern="dd/mm/yyyy"
)
calendario_inicio.pack(pady=10)

lbl_final = ctk.CTkLabel(
    frame_historial,
    text="Fecha Final"
)
lbl_final.pack()

calendario_final = DateEntry(
    frame_historial,
    date_pattern="dd/mm/yyyy"
)
calendario_final.pack(pady=10)
textbox_historial = ctk.CTkTextbox(
    frame_historial,
    width=400,
    height=200
)

textbox_historial.pack(pady=10)
#fin del frame historial 
def buscar_historial():
    global usuario_sql
    global password_sql
    fecha_inicio = datetime.strptime(
        calendario_inicio.get(),
        "%d/%m/%Y"
    ).strftime("%Y-%m-%d")
    fecha_final = datetime.strptime(
        calendario_final.get(),
        "%d/%m/%Y"
    ).strftime("%Y-%m-%d")
    movimientos = usuario_actual.obtener_historial_sql(
        usuario_sql,
        password_sql,
        fecha_inicio,
        fecha_final
    )
    textbox_historial.delete(
        "1.0",
        "end"
    )
    if len(movimientos) == 0:
        textbox_historial.insert(
            "end",
            "No existen movimientos."
        )
    else:
        for movimiento in movimientos:
            texto = (
                f"Fecha: {movimiento.FechaMov}\n"
                f"Tipo: {movimiento.Tipo}\n"
                f"Descripción: {movimiento.Descripcion}\n"
                f"Monto: ₡{movimiento.Monto}\n"
                f"Saldo Anterior: ₡{movimiento.SaldoAnterior}\n"
                f"Saldo Actual: ₡{movimiento.SaldoActual}\n"
                f"Cajero: {movimiento.NombreCajero}\n"
                f"{'-'*40}\n"
            )
            textbox_historial.insert(
                "end",
                texto
            )

btn_buscar_historial = ctk.CTkButton(
    frame_historial,
    text="Buscar",
    command=buscar_historial
)
btn_buscar_historial.pack(pady=10)

btn_volver_historial = ctk.CTkButton(
    frame_historial,
    text="Volver",
    command=lambda: cambiar_frame(
        frame_historial,
        frame_menu
    )
)
btn_volver_historial.pack(pady=10)
#fin de buscar historial

#ver el historial
def ver_historial():
    textbox_historial.delete(
        "1.0",
        "end"
    )
    cambiar_frame(
        frame_menu,
        frame_historial
    )
    
#fin del historial 


#funcion para mostar comprobante
def mostrar_comprobante(
    operacion,
    monto,
    saldo_anterior,
    saldo_actual,
    detalle=""
):
    ventana = ctk.CTkToplevel()
    ventana.title("Comprobante")
    ventana.geometry("500x500")
    ventana.iconbitmap("IconoCajeroICO.ico")
    frame_comprobante = ctk.CTkFrame(
        ventana,
        fg_color="#52AAC0"
    )
    frame_comprobante.pack(
        fill="both",
        expand=True
    )
    img_logo = ctk.CTkImage(
        Image.open("IconoCajero.png"),
        size=(60, 60)
    )
    lbl_logo = ctk.CTkLabel(
        frame_comprobante,
        image=img_logo,
        text=""
    )
    lbl_logo.pack(pady=10)
    lbl_titulo = ctk.CTkLabel(
        frame_comprobante,
        text="COMPROBANTE",
        font=("Arial", 24, "bold"),
        text_color="black"
    )
    lbl_titulo.pack(pady=10)
    texto = f"""
Cliente: {usuario_actual.nombre}
Cuenta: {usuario_actual.numero_cuenta}
Cajero: {id_cajero_actual}

Fecha:
{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

Operación:
{operacion.upper()}

Detalle:
{detalle}

Monto:
₡{monto}

Saldo anterior:
₡{saldo_anterior}

Saldo actual:
₡{saldo_actual}
"""
    textbox_info = ctk.CTkTextbox(
        frame_comprobante,
        width=420,
        height=250,
        fg_color="#DDEDF1",       
        text_color="black",
        border_width=0
    )
    textbox_info.pack(
        padx=20,
        pady=10,
        fill="both",
        expand=True
    )
    textbox_info.insert(
        "1.0",
        texto
    )
    textbox_info.configure(
        state="disabled"
    )
    btn_cerrar = ctk.CTkButton(
        frame_comprobante,
        text="Cerrar",
        command=ventana.destroy,
        width=150
    )
    btn_cerrar.pack(pady=15)

#fin de mostrar el comprobante 

#cerrar seccion
def cerrar_sesion():
    global usuario_actual
    global usuario_sql
    global password_sql
    global id_cajero_actual
    usuario_actual = None
    usuario_sql = ""
    password_sql = ""
    id_cajero_actual = None
    entry_cuenta.delete(0, "end")
    entry_pin.delete(0, "end")
    cambiar_frame(
        frame_menu,
        frame_login
    )
#fin de cerrar seccion 

#funicon del inicio de seccion 
def login():
    global usuario_actual
    global usuario_sql
    global password_sql
    cuenta = entry_cuenta.get().strip()
    pin = entry_pin.get().strip()
    if cuenta == "" or pin == "":
        messagebox.showerror(
            "Error",
            "Debe completar todos los campos."
        )
        return
    usuario_actual = iniciar_sesion(cuenta, pin)
    usuario_sql = cuenta
    password_sql = pin
    print(usuario_sql,password_sql)
    if usuario_actual:
        messagebox.showinfo(
            "Bienvenido",
            "Inicio de sesión exitoso."
        )
        cambiar_frame(frame_login, frame_cajeros)
    else:
        messagebox.showerror(
            "Error",
            "Cuenta o PIN incorrectos."
        )
#find de la funicon del login
#boton de los cajeros automaticos 
btn_ingresar = crear_boton(
    frame_login,
    "Ingresar",
    login
    )
btn_ingresar.pack(pady=30)
# fin del boton de ingresar de los cajeros
#botones del menu de los cajeros (deposito,retirar...)
opciones_menu = [
    ("Consultar Saldo", consultar_saldo),
    ("Depositar", abrir_deposito),
    ("Retirar", abrir_retiro),
    ("Transferir", abrir_transferencia),
    ("Pagos", pagos),
    ("Historial", ver_historial),
    ("Cerrar Sesión", cerrar_sesion)
]
for texto, funcion in opciones_menu:
    ctk.CTkButton(
        frame_menu,
        text=texto,
        command=funcion
    ).pack(pady=10)
#fin de los botones de los cajeros (retirar, depositar...)
#Hace que la ventana no se cierre 
VentanaP.mainloop()

