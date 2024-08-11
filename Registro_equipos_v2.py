from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import sqlite3
import gen_Reporte
from tkcalendar import DateEntry
from datetime import datetime, timedelta, date
global estadoEq
global estadoFactura

# BORRAR REGISTROS
# CONSULTAS PARAMETRIZADAS USANDO INTERROGANTES para evitar la inyección SQL
# REALIZAR MODULOS PARA MEJORAR LA LECTURA DEL CÓDIGO, EJEMPLO UN MODULO DE CONEXIÓN

# --------- Funciones ------------ #

def conexionBBDD():
    # Funcion enlazada con el boton de conectar base de datos
    try:
        miConexion = sqlite3.connect("Equipos")
        miCursor = miConexion.cursor()

        miCursor.execute('''
                            CREATE TABLE DATOS_EQUIPOS (
                            SERIE VARCHAR PRIMARY KEY,
                            MARCA VARCHAR(40),
                            MODELO VARCHAR(50),
                            CONFIGURACION VARCHAR(50),
                            FECHA_CAL DATE,
                            SIG_FECHA_CAL DATE,     
                            RUC INTEGER(11),
                            EMPRESA VARCHAR(80),
                            ZONA VARCHAR (30),
                            CONTACTO VARCHAR (30),
                            CORREO VARCHAR (30),
                            CELULAR VARCHAR (30),
                            SENSOR1 INTEGER (15),
                            SENSOR2 INTEGER (15),
                            SENSOR3 INTEGER (15),
                            SENSOR4 INTEGER (15),
                            SENSOR5 INTEGER (15),
                            ESTADO VARCHAR (15),
                            COTIZACION VARCHAR (10),
                            ORDEN VARCHAR (20),
                            FACTURA INTEGER (1)
                            )'''
                         )

        messagebox.showinfo("BBDD", "BBDD creada con éxito")

    except:
        messagebox.showwarning("¡Atención!", "La BBDD ya existe")


def salirAplicacion():
    valor = messagebox.askquestion("Salir", "¿Deseas salir de la aplicación?")
    if valor == "yes":
        root.destroy()


def limpiarCampos():
    miSerie.set("")
    miMarca.set("")
    miModelo.set("")
    miConfig.set("")
    miCalibracion.set("")
    miSiguiente_Cal.set("")
    miRUC.set("")
    miEmpresa.set("")
    miZona.set("")
    miContacto.set("")
    miCorreo.set("")
    miCelular.set("")
    miSensor1.set("")
    miSensor2.set("")
    miSensor3.set("")
    miSensor4.set("")
    miSensor5.set("")
    miEstadoEquipo.set("")
    miNumeroCotizacion.set("")
    miOC.set("")
    # Para borrar un texto comentario usar *****.delete(1.0, END)


def crear():
    if miSerie.get() == "":
        messagebox.showinfo("Registrar equipo", "Ingresa un número de serie")
    else:
        # Crear nuevo registro en la BBDD
        miConexion = sqlite3.connect("Equipos")
        miCursor = miConexion.cursor()

        # Esto evita la inyección SQL
        datos = (
            miSerie.get(), miMarca.get().upper(), miModelo.get().upper(),
            miConfig.get().upper(), miCalibracion.get(),
            miSiguiente_Cal.get(), miRUC.get(), miEmpresa.get().upper(), miZona.get().upper()
        )

        # Añadir valores nulos para las columnas restantes
        datos += ("", "", "", "", "", "", "", "", estadoEq[0], "", "", estadoFactura[0])

        miCursor.execute("INSERT INTO DATOS_EQUIPOS VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", datos)
        miEstadoEquipo.set(estadoEq[0])

        miConexion.commit()
        miConexion.close()
        messagebox.showinfo("BBDD", "Registro insertado con éxito")


def leer():   # Consultar
    if miSerie.get() == "":
        pass
    else:
        miConexion = sqlite3.connect("Equipos")
        miCursor = miConexion.cursor()

        # Realizar una consulta para obtener el registro que se tiene almacenado en la tabla correspondiente con el Numero de serie introducido
        # miCursor.execute("SELECT * FROM DATOS_EQUIPOS WHERE SERIE=" + miSerie.get()) Salia error con numeros de series alfanumericos
        # cODIGO ARREGLADO PORQUE NO PERMITIA LECTURAS CON SEGMENTOS ALFANUMERICOS
        miCursor.execute("SELECT * FROM DATOS_EQUIPOS WHERE SERIE='" + miSerie.get() + "'")

        # Se cocantena la consulta dentro de execute.

        elUsuario = miCursor.fetchall()  # La función fetchall devuelve un array de todos los registros de la consulta
        if len(elUsuario) == 0:
            messagebox.showinfo("BBDD", "Equipo no registrado en la base de datos")
        else:
            for usuario in elUsuario:  # Se consulta los datos de array que contiene toda la data relacionada con ese numero de serie
                miSerie.set(usuario[0])
                miMarca.set(usuario[1])
                miModelo.set(usuario[2])
                miConfig.set(usuario[3])
                miCalibracion.set(usuario[4])
                miSiguiente_Cal.set(usuario[5])
                miRUC.set(usuario[6])
                miEmpresa.set(usuario[7])
                miZona.set(usuario[8])
                miContacto.set(usuario[9])
                miCorreo.set(usuario[10])
                miCelular.set(usuario[11])
                miSensor1.set(usuario[12])
                miSensor2.set(usuario[13])
                miSensor3.set(usuario[14])
                miSensor4.set(usuario[15])
                miSensor5.set(usuario[16])
                miEstadoEquipo.set(usuario[17])
                miNumeroCotizacion.set(usuario[18])
                miOC.set(usuario[19])

        miConexion.commit()
        miConexion.close()

def eliminar():
    try:
        repuesta = messagebox.askquestion("Eliminar registro", "¿Deseas eliminar el registro?")
        if repuesta == "yes":
            miConexion = sqlite3.connect("Equipos")
            miCursor = miConexion.cursor()
            miCursor.execute("DELETE FROM DATOS_EQUIPOS WHERE SERIE=" + miSerie.get())

            miConexion.commit()
            miConexion.close()
            messagebox.showinfo("BBDD", "Registro eliminado con éxito")
            limpiarCampos()
    except sqlite3.OperationalError:
        messagebox.showinfo("BBDD", "Ingresa un número de serie valido")

def actualizar(TIPO):

    if miSerie.get() == "":
        messagebox.showinfo("Actualizar Equipo", "Ingresa un número de serie valido")
    # https://ellibrodepython.com/switch-python

    else:
        try:
            # Crear nuevo registro en la BBDD
            miConexion = sqlite3.connect("Equipos")
            miCursor = miConexion.cursor()
            if TIPO == "TODO":
                # CONSULTA PARAMETRIZADA QUE REEMPLAZA LO DE ARRIBA
                datos = miMarca.get(), miModelo.get(), miConfig.get(), miCalibracion.get(), miSiguiente_Cal.get(), miRUC.get(), miEmpresa.get(), miZona.get()
                datos += miEstadoEquipo.get(), estadoFactura[0]

                miCursor.execute(
                    "UPDATE DATOS_EQUIPOS SET MARCA=?, MODELO=?, CONFIGURACION=?, FECHA_CAL=?, SIG_FECHA_CAL=?, RUC=?, EMPRESA=?, ZONA=?, ESTADO=?, FACTURA=?" +
                    "WHERE SERIE=?", datos + (miSerie.get(),)   # La coma convierte a tupla tipo STR
                )

            elif TIPO == "COTIZACION":
                segundaVentana(0)
                Nro_Cot = miNumeroCotizacion.get()
                miCursor.execute(
                    "UPDATE DATOS_EQUIPOS SET ESTADO=?, COTIZACION=?, FACTURA=? WHERE SERIE=?",
                    (estadoEq[1], Nro_Cot, estadoFactura[0], miSerie.get())
                )
                miEstadoEquipo.set(estadoEq[1])
                miNumeroCotizacion.set(Nro_Cot)

            elif TIPO == "CALIBRAR":
                F_cal = miCalibracion.get()
                F_cal_siguiente = miSiguiente_Cal.get()
                miCursor.execute(
                    "UPDATE DATOS_EQUIPOS SET ESTADO=?, FECHA_CAL=?, SIG_FECHA_CAL=?, FACTURA=? WHERE SERIE=?",
                    (estadoEq[2], F_cal, F_cal_siguiente, estadoFactura[0], miSerie.get())
                )
                miEstadoEquipo.set(estadoEq[2])
                miCalibracion.set(F_cal)
                miSiguiente_Cal.set(F_cal_siguiente)

            elif TIPO == "ORDEN":
                segundaVentana(1)
                Nro_Orden = miOC.get()
                miCursor.execute(
                    "UPDATE DATOS_EQUIPOS SET ESTADO=?, ORDEN=?, FACTURA=? WHERE SERIE=?",
                    (estadoEq[3], Nro_Orden, estadoFactura[0], miSerie.get())
                )
                miEstadoEquipo.set(estadoEq[3])
                miNumeroCotizacion.set(Nro_Orden)

            elif TIPO == "SENSORES":
                miCursor.execute(
                    "UPDATE DATOS_EQUIPOS SET SENSOR1=?, SENSOR2=?, SENSOR3=?, SENSOR4=?, SENSOR5=? WHERE SERIE=?",
                    (miSensor1.get(), miSensor2.get(), miSensor3.get(), miSensor4.get(), miSensor5.get(), miSerie.get())
                                )
            elif TIPO == "NUEVO":
                miEstadoEquipo.set(estadoEq[5])
                messagebox.showinfo("Registro Equipo Nuevo", "Actualizar los datos de contacto")
                miCursor.execute(
                    "UPDATE DATOS_EQUIPOS SET ESTADO=?, CONTACTO=?, CORREO=?, CELULAR=? WHERE SERIE=?",
                    (estadoEq[5], miContacto.get().upper(), miCorreo.get().lower(), miContacto.get(), miSerie.get()))

            elif TIPO == "USADO":
                miCursor.execute(
                    "UPDATE DATOS_EQUIPOS SET CONTACTO=?, CORREO=?, CELULAR=? WHERE SERIE=?",
                    (miContacto.get().upper(), miCorreo.get().lower(), miContacto.get(), miSerie.get()))


            miConexion.commit()
            miConexion.close()
            messagebox.showinfo("BBDD", "Registro Actualizado con éxito")
        except sqlite3.OperationalError as errorLocal:
            messagebox.showerror("Error", f"Error de base de datos: {errorLocal}")

def segundaVentana(T):

    Titulo=["Registra tu cotización", "Registra tu Nro. OC / OS / PO", "Ingresa tu número de cotización", "Ingresa Nro. OC / OS / PO"]
    Valor = [miNumeroCotizacion, miOC]
    ventanaRegistro = tk.Toplevel(root)
    ventanaRegistro.title(Titulo[T])
    ventanaRegistro.geometry("300x150")
    etiqueta = tk.Label(ventanaRegistro, text=Titulo[T+2], pady=10)
    etiqueta.pack()
    ingresaNro = tk.Entry(ventanaRegistro, textvariable=Valor[T])
    ingresaNro.pack(pady=10)

    boton_aceptar = tk.Button(ventanaRegistro, text="Aceptar", command=lambda: ventanaRegistro.destroy())
    boton_aceptar.pack(pady=10)

    root.wait_window(ventanaRegistro)

def serie_sensores():
    ventanaSensores = tk.Toplevel(root)
    ventanaSensores.title("Núm Serie Sensores")

    etiqueta = tk.Label(ventanaSensores, text="Registra o actualiza los números de serie de los sensores.\n"
                                              " Tener en cuenta el orden recomendado para los modelos multigases")
    etiqueta.grid(row=0, column=0, columnspan=2, pady=10)

    sensores_etiqueta = ["Sensor 1 (O2)", "Sensor 2 (GC)", "Sensor 3(Gases duales)", "Sensor 4 (Gases exóticos)", "Sensor 5 (PID o IR)"]
    sensores_variable = [miSensor1, miSensor2, miSensor3, miSensor4, miSensor5]

    boton_guardar = tk.Button(ventanaSensores, text="Guardar o actualizar", command=lambda: [actualizar("SENSORES"), ventanaSensores.destroy()])
    boton_guardar.grid(row=6, column=0, pady=20)

    boton_cerrar = tk.Button(ventanaSensores, text="cerrar", command=lambda: ventanaSensores.destroy())
    boton_cerrar.grid(row=6, column=1, pady=20)

    # Usar grid para organizar las etiquetas en una matriz 2x5
    for i, sensores_variable in enumerate(sensores_variable):
        cuadroSensor_etiqueta = tk.Label(ventanaSensores, text=sensores_etiqueta[i])
        cuadroSensor_etiqueta.grid(row=i+1, column=0, padx=10, pady=10)

        cuadroSensor_variable = tk.Entry(ventanaSensores, textvariable=sensores_variable)
        cuadroSensor_variable.grid(row=i+1, column=1, padx=10, pady=10)


def listaGases():
    miConexion = sqlite3.connect("Equipos")
    miCursor = miConexion.cursor()

    varOpcion = StringVar()
    ventana = Toplevel(root)
    ventana1 = Frame(ventana)
    ventana1.pack(side="top")  # Para empaquetar
    consulta_lista_gases = "SELECT CONFIGURACION FROM DATOS_EQUIPOS"
    miCursor.execute(consulta_lista_gases)
    configuracion_temporal = miCursor.fetchall()
    configuracion = sorted(set(row[0] for row in configuracion_temporal if row[0]))

    varOpcion.set(configuracion[0])  # Valor predeterminado
    Mensaje = Label(ventana1, text="Selecciona la configuración del detector")
    Mensaje.grid(row=1, column=0, sticky="e", padx=10, pady=10)
    miConexion.close()

    def seleccionar_configuracion(conf):
        miConfig.set(conf)

    for i, conf in enumerate(configuracion):
        Texto_Config = Radiobutton(ventana1, text=conf, variable=varOpcion, value=conf, command=lambda conf=conf: seleccionar_configuracion(conf))
        Texto_Config.grid(row=i + 2, column=0, sticky="s", padx=10, pady=0)

    ventana2 = Frame(ventana)
    ventana2.pack(side="bottom")  # Para empaquetar.

    botonCerrar = Button(ventana2, text="Cerrar", command=lambda: ventana.destroy())
    botonCerrar.grid(row=0, column=1, sticky="s", padx=10, pady=10)

def informacion_contacto(TIPO_EQUIPO):
    ventana_contacto = Toplevel(root)
    ancho = 40
    # ------- Creación de los cuadros de texto
    Mensaje = Label(ventana_contacto, text="Ingresa los datos necesarios.", justify="center")
    Mensaje.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    cuadroContacto = Entry(ventana_contacto, textvariable=miContacto, justify="center", width=ancho)
    cuadroContacto.grid(row=1, column=1, padx=10, pady=10)
    nombreContacto = Label(ventana_contacto, text="Nombre y apellidos: ")
    nombreContacto.grid(row=1, column=0, sticky="e", padx=10, pady=10)

    cuadroCorreo = Entry(ventana_contacto, textvariable=miCorreo, justify="center", width=ancho)
    cuadroCorreo.grid(row=2, column=1, padx=10, pady=10)
    nombreCorreo = Label(ventana_contacto, text="Correo: ")
    nombreCorreo.grid(row=2, column=0, sticky="e", padx=10, pady=10)

    cuadroCelular = Entry(ventana_contacto, textvariable=miCelular, justify="center", width=ancho)
    cuadroCelular.grid(row=3, column=1, padx=10, pady=10)
    nombreCelular = Label(ventana_contacto, text="Celular: ")
    nombreCelular.grid(row=3, column=0, sticky="e", padx=10, pady=10)

    boton_guardar = tk.Button(ventana_contacto, text="Guardar o actualizar", justify="center", command=lambda: [actualizar(TIPO_EQUIPO), ventana_contacto.destroy()])
    boton_guardar.grid(row=4, column=0, pady=20)

    boton_cerrar = tk.Button(ventana_contacto, text="cerrar", justify="center", command=lambda: ventana_contacto.destroy())
    boton_cerrar.grid(row=4, column=1, pady=20)

def lista_desplegable(columna):
    miConexion = sqlite3.connect("Equipos")
    miCursor = miConexion.cursor()
    consulta_lista_Modelos = f"SELECT {columna} FROM DATOS_EQUIPOS"
    miCursor.execute(consulta_lista_Modelos)

    lista_temporal = miCursor.fetchall()
    lista_columna = sorted(set(row[0] for row in lista_temporal if row[0]))

    return lista_columna

# _______________ Parte grafica
# Raiz del frame1

root = Tk()
# Una Raiz para la barra de menu
barraMenu = Menu(root)
root.config(menu=barraMenu, width=300, height=300)

bbddMenu = Menu(barraMenu, tearoff=0)
bbddMenu.add_command(label="Conectar", command=conexionBBDD)
bbddMenu.add_command(label="Abrir Clientes", command=lambda: CLIENTES_BBDD.abrir_ventana_clientes())
bbddMenu.add_command(label="Salir", command=salirAplicacion)

borrarMenu = Menu(barraMenu, tearoff=0)
borrarMenu.add_command(label="Borrar campos", command=limpiarCampos)

crudMenu = Menu(barraMenu, tearoff=0)
crudMenu.add_command(label="Nuevo", command=crear)
crudMenu.add_command(label="Leer", command=leer)
crudMenu.add_command(label="Actualizar", command=lambda: actualizar("TODO"))
crudMenu.add_command(label="Eliminar", command=eliminar)

ayudaMenu = Menu(barraMenu, tearoff=0)
ayudaMenu.add_command(label="Licencia")
ayudaMenu.add_command(label="Acerca de ...")

barraMenu.add_cascade(label="BBDD", menu=bbddMenu)
barraMenu.add_cascade(label="Borrar", menu=borrarMenu)
barraMenu.add_cascade(label="CRUD", menu=crudMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)

# ----------- Creacion de las variables para los campos de textos
miSerie = StringVar()
miMarca = StringVar()
miModelo = StringVar()
miConfig = StringVar()
miCalibracion = StringVar()
miSiguiente_Cal = StringVar()
miRUC = StringVar()
miEmpresa = StringVar()
miZona = StringVar()
miContacto = StringVar()
miCorreo = StringVar()
miCelular = StringVar()
miSensor1 = StringVar()
miSensor2 = StringVar()
miSensor3 = StringVar()
miSensor4 = StringVar()
miSensor5 = StringVar()
miEstadoEquipo = StringVar()
miNumeroCotizacion = StringVar()
miOC = StringVar()

#miEstadoFactura = stringVar()

estadoEq = ["Equipo Ingresado", "Equipo Cotizado", "Equipo Calibrado", "Equipo Despachado", "Equipo Facturado", "Equipo Venta Nuevo"]
estadoFactura = ["NO", "SI"]

# ------ Area para los campos de información NO EDITABLES -------
miFrame0 = Frame(root)
miFrame0.pack()

nombre_estado_Equipo = Label(miFrame0, text="Estado")
nombre_estado_Equipo.grid(row=0, column=0, sticky="s", padx=2, pady=2)
estado_Equipo = Entry(miFrame0, textvariable=miEstadoEquipo, state="readonly")
estado_Equipo.grid(row=1, column=0, sticky="s", padx=2, pady=2)
estado_Equipo.configure(foreground="red", background="white")

nombre_cotizacion = Label(miFrame0, text="Nro. Cotización")
nombre_cotizacion.grid(row=0, column=1, sticky="s", padx=2, pady=2)
cotizacion = Entry(miFrame0, textvariable=miNumeroCotizacion, state="readonly")
cotizacion.grid(row=1, column=1, sticky="s", padx=2, pady=2)

nombre_orden = Label(miFrame0, text="Nro. OC / OS / PO")
nombre_orden.grid(row=0, column=2, sticky="s", padx=2, pady=2)
orden = Entry(miFrame0, textvariable=miOC, state="readonly")
orden.grid(row=1, column=2, sticky="s", padx=2, pady=2)

# ------ Botones para los cambios de estados -------

botonReg_Cotizacion = Button(miFrame0, text="Registrar Cotización", command=lambda: actualizar("COTIZACION"))
botonReg_Cotizacion.grid(row=2, column=0, sticky="s", padx=5, pady=5)

botonReg_Despacho = Button(miFrame0, text="Registrar Despacho", command=lambda: actualizar("ORDEN"))
botonReg_Despacho.grid(row=2, column=1, sticky="s", padx=5, pady=5)

botonReg_Factura = Button(miFrame0, text="Registrar Factura")
botonReg_Factura.grid(row=2, column=2, sticky="s", padx=5, pady=5)

boton_Generar_Reporte = Button(miFrame0, text="Generar Reporte", command=lambda: gen_Reporte.ventanaReporte(root))
boton_Generar_Reporte.grid(row=3, column=2, sticky="s", padx=5, pady=5)

boton_Registrar_EquipoNuevo = Button(miFrame0, text="Registrar Equipo Vendido", command=lambda: [crear(), informacion_contacto("NUEVO")])
boton_Registrar_EquipoNuevo.grid(row=3, column=0, sticky="s", padx=5, pady=5)

# ------ Area para los campos de información -------
miFrame = Frame(root)
miFrame.pack(side="top")  # Para empaquetar.

# ------- Creación de los cuadros de texto
cuadroSerie = Entry(miFrame, textvariable=miSerie)
cuadroSerie.grid(row=0, column=1, padx=10, pady=10)
cuadroSerie.config(justify="center")
nombreSerie = Label(miFrame, text="Serie")
nombreSerie.grid(row=0, column=0, sticky="e", padx=10, pady=10)

cuadroMarca = Combobox(miFrame, values=lista_desplegable("MARCA"), state="readonly", textvariable=miMarca, justify="center")
cuadroMarca.grid(row=1, column=1, padx=10, pady=10)
nombreMarca = Label(miFrame, text="Marca")
nombreMarca.grid(row=1, column=0, sticky="e", padx=10, pady=10)


#### Llamado de la base de datos para extraer datos.

cuadroModelo = Combobox(miFrame, values=lista_desplegable("MODELO"), state="readonly", textvariable=miModelo, justify="center")
cuadroModelo.grid(row=2, column=1, padx=10, pady=10)
nombreModelo = Label(miFrame, text="Modelo")
nombreModelo.grid(row=2, column=0, sticky="e", padx=10, pady=10)

cuadroConfig = Entry(miFrame, textvariable=miConfig)
cuadroConfig.grid(row=3, column=1, padx=10, pady=10)
cuadroConfig.config(justify="center")
nombreConfig = Label(miFrame, text="Configuración Gases")
nombreConfig.grid(row=3, column=0, sticky="e", padx=10, pady=10)

cuadroCalibracion = DateEntry(miFrame, textvariable=miCalibracion, width=17, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
cuadroCalibracion.grid(row=4, column=1, padx=5, pady=5)
cuadroCalibracion.config(justify="center")
nombreCalibracion = Label(miFrame, text="Fecha de calibración")
nombreCalibracion.grid(row=4, column=0, sticky="e", padx=10, pady=10)

cuadroSiguiente_Cal = DateEntry(miFrame, textvariable=miSiguiente_Cal, width=17, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
cuadroSiguiente_Cal.grid(row=5, column=1, padx=5, pady=5)
cuadroSiguiente_Cal.config(justify="center")
nombreSiguiente_Cal = Label(miFrame, text="Prox. Calibración")
nombreSiguiente_Cal.grid(row=5, column=0, sticky="e", padx=10, pady=10)

cuadroRUC = Entry(miFrame, textvariable=miRUC)
cuadroRUC.grid(row=6, column=1, padx=10, pady=10)
cuadroRUC.config(justify="center")
nombreRUC = Label(miFrame, text="RUC")
nombreRUC.grid(row=6, column=0, sticky="e", padx=10, pady=10)

cuadroEmpresa = Entry(miFrame, textvariable=miEmpresa, width=35)
cuadroEmpresa.grid(row=7, column=1, padx=10, pady=10)
cuadroEmpresa.config(justify="center")
nombreEmpresa = Label(miFrame, text="Razón Social")
nombreEmpresa.grid(row=7, column=0, sticky="e", padx=10, pady=10)

cuadroZona = Entry(miFrame, textvariable=miZona, width=35)
cuadroZona.grid(row=8, column=1, padx=10, pady=10)
cuadroZona.config(justify="center")
nombreZona = Label(miFrame, text="Región / Zona")
nombreZona.grid(row=8, column=0, sticky="e", padx=10, pady=10)

# ----------- Frame para los botones de abrir, nuevo, etc --------

miFrame2 = Frame(root)
miFrame2.pack()

botonNuevo = Button(miFrame2, text="Nuevo", command=crear)
botonNuevo.grid(row=1, column=0, sticky="e", padx=10, pady=10)

botonConsulta = Button(miFrame2, text="Consultar", command=leer)
botonConsulta.grid(row=1, column=1, sticky="e", padx=10, pady=10)

botonActualizar = Button(miFrame2, text="Actualizar", command=lambda: actualizar("TODO"))
botonActualizar.grid(row=1, column=2, sticky="e", padx=10, pady=10)

botonBorrar = Button(miFrame2, text="Borrar", command=limpiarCampos)
botonBorrar.grid(row=1, column=3, sticky="e", padx=10, pady=10)

botonEliminar = Button(miFrame2, text="Eliminar", command=eliminar)
botonEliminar.grid(row=1, column=4, sticky="e", padx=10, pady=10)

# ----------- CONFIGURACION DEL FRAME1 para los botones LATERALES --------

botonConsultaSensores = Button(miFrame, text="Ver sensores", command=lambda: serie_sensores())
botonConsultaSensores.grid(row=0, column=2, sticky="s", padx=10, pady=10)

botonConsultaGases = Button(miFrame, text="Examinar", command=lambda: listaGases())
botonConsultaGases.grid(row=3, column=2, sticky="s", padx=10, pady=10)

botonConsultaRUC = Button(miFrame, text="Consultar RUC")
botonConsultaRUC.grid(row=6, column=2, sticky="s", padx=10, pady=10)

botonConsultaContacto = Button(miFrame, text="Consultar Contacto", command=lambda: informacion_contacto("USADO"))
botonConsultaContacto.grid(row=7, column=2, sticky="s", padx=10, pady=10)

botonReg_Cal = Button(miFrame, text="Registrar Calibración", command=lambda: actualizar("CALIBRAR"))
botonReg_Cal.grid(row=4, column=2, sticky="s", padx=10, pady=10)

root.mainloop()
