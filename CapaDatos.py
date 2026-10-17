#para la conexccion de py con sql
import pyodbc


def conectar(usuario, password):
    print(usuario,password)
    conexion = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-DO5UK67\\SQLEXPRESS;"
        "DATABASE=CajerosProc;"
        f"UID={usuario};"
        f"PWD={password};"
        "TrustServerCertificate=yes;" 
    )
    #print(usuario,password)
            
    
    return conexion

#llama al procedimiento almacenado de inicio de seccion 
def obtener_cliente(usuario, password, numero_cuenta):
    try:
        conexion = conectar(
            usuario,
            password
        )
        cursor = conexion.cursor()
        cursor.execute(
            "EXEC sp_ObtenerCliente ?",
            numero_cuenta
        )
        datos = cursor.fetchone()
        conexion.close()
        return datos
    except Exception as e:
        print("Error SQL:", e)
        return None

def consultar_saldo(
    usuario,
    password,
    numero_cuenta
):
    try:
        conexion = conectar(
            usuario,
            password
        )
        cursor = conexion.cursor()
        cursor.execute(
            "EXEC sp_ConsultarSaldo ?",
            numero_cuenta
        )
        resultado = cursor.fetchone()
        conexion.close()
        if resultado:
            return resultado[0]
        return None
    except Exception as e:
        print("Error SQL:", e)
        return None

def retirar(
    usuario,
    password,
    numero_cuenta,
    id_cajero,
    monto
):
    try:
        conexion = conectar(
            usuario,
            password
        )
        cursor = conexion.cursor()
        cursor.execute(
            "EXEC sp_Retirar ?, ?, ?",
            numero_cuenta,
            id_cajero,
            monto
        )
        resultado = cursor.fetchone()
        conexion.commit()
        conexion.close()
        if resultado:
            return resultado[0]
        return None
    except Exception as e:
        print("Error SQL:", e)
        return None

def depositar(
    usuario,
    password,
    numero_cuenta,
    id_cajero,
    monto
):
    try:
        conexion = conectar(
            usuario,
            password
        )
        cursor = conexion.cursor()
        cursor.execute(
            "EXEC sp_Depositar ?, ?, ?",
            numero_cuenta,
            id_cajero,
            monto
        )
        while cursor.description is None:
            cursor.nextset()
        resultado = cursor.fetchone()
        conexion.commit()
        conexion.close()
        if resultado:
            return resultado[0]
        return None
    except Exception as e:
        print("Error SQL:", e)
        return None

def transferir(
    usuario,
    password,
    cuenta_origen,
    cuenta_destino,
    id_cajero,
    monto
):
    try:
        conexion = conectar(
            usuario,
            password
        )
        cursor = conexion.cursor()
        cursor.execute(
            "EXEC sp_Transferir ?, ?, ?, ?",
            cuenta_origen,
            cuenta_destino,
            id_cajero,
            monto
        )
        while cursor.description is None:
            cursor.nextset()
        resultado = cursor.fetchone()
        conexion.commit()
        conexion.close()
        if resultado:
            return resultado[0]
        return None
    except Exception as e:
        print("Error SQL:", e)
        return None

def registrar_pago(
    usuario,
    password,
    numero_cuenta,
    id_cajero,
    categoria,
    servicio,
    monto
):
    try:
        conexion = conectar(
            usuario,
            password
        )
        cursor = conexion.cursor()
        cursor.execute(
            "EXEC sp_RegistrarPago ?, ?, ?, ?, ?",
            numero_cuenta,
            id_cajero,
            categoria,
            servicio,
            monto
        )
        while cursor.description is None:
            cursor.nextset()
        resultado = cursor.fetchone()
        conexion.commit()
        conexion.close()
        if resultado:
            return resultado[0]
        return None
    except Exception as e:
        print("Error SQL:", e)
        return None

def obtener_historial(
    usuario,
    password,
    numero_cuenta,
    fecha_inicio,
    fecha_fin
):
    try:
        conexion = conectar(
            usuario,
            password
        )
        cursor = conexion.cursor()
        cursor.execute(
            "EXEC sp_HistorialMovimientos ?, ?, ?",
            numero_cuenta,
            fecha_inicio,
            fecha_fin
        )
        movimientos = cursor.fetchall()
        conexion.close()
        return movimientos
    except Exception as e:
        print("Error SQL:", e)
        return []

