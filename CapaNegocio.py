#imports 
from datetime import datetime
from CapaDatos import obtener_cliente
from CapaDatos import consultar_saldo
from CapaDatos import retirar as retirar_sql
from CapaDatos import depositar as depositar_sql
from CapaDatos import transferir as transferir_sql
from CapaDatos import registrar_pago as registrar_pago_sql
from CapaDatos import obtener_historial

def iniciar_sesion(cuenta, pin):
    
    datos = obtener_cliente(
        cuenta,
        pin,
        cuenta
    )
  
    if datos is None:
        return None

    return Usuario(
        datos.IDCliente,
        datos.NombreCliente,
        datos.NumeroCuenta,
        datos.IDCuenta,
        datos.Saldo
    )



class Usuario:

    def __init__(
        self,
        id_cliente,
        nombre,
        numero_cuenta,
        id_cuenta,
        saldo
    ):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.numero_cuenta = numero_cuenta
        self.id_cuenta = id_cuenta
        self.saldo = saldo
        self.id_cajero =None
        self.historial = []
   
    def consultar_saldo(self):

        return self.saldo
    
    def retirar(
        self,
        usuario,
        pin,
        id_cajero,
        monto
    ):
        if monto <= 0:
            return False
        nuevo_saldo = retirar_sql(
            usuario,
            pin,
            self.numero_cuenta,
            id_cajero,
            monto
        )
        if nuevo_saldo is not None:
            self.saldo = nuevo_saldo
            return True
        return False

    
    def depositar(
        self,
        usuario,
        pin,
        id_cajero,
        monto
    ):
        if monto <= 0:
            return False

        nuevo_saldo = depositar_sql(
            usuario,
            pin,
            self.numero_cuenta,
            id_cajero,
            monto
        )

        if nuevo_saldo is not None:
            self.saldo = nuevo_saldo
            return True
        return False

    def retirar(
        self,
        usuario,
        pin,
        id_cajero,
        monto
    ):
        if monto <= 0:
            return False
        nuevo_saldo = retirar_sql(
            usuario,
            pin,
            self.numero_cuenta,
            id_cajero,
            monto
        )
        if nuevo_saldo is not None:
            self.saldo = nuevo_saldo
            return True
        return False

    def transferir(
        self,
        usuario,
        pin,
        id_cajero,
        cuenta_destino,
        monto
    ):
        if monto <= 0:
            return False
        nuevo_saldo = transferir_sql(
            usuario,
            pin,
            self.numero_cuenta,
            cuenta_destino,
            id_cajero,
            monto
        )
        if nuevo_saldo is not None:
            self.saldo = nuevo_saldo
            return True
        return False

    def registrar_pago(
        self,
        usuario,
        pin,
        id_cajero,
        categoria,
        detalle,
        monto
    ):
        nuevo_saldo = registrar_pago_sql(
            usuario,
            pin,
            self.numero_cuenta,
            id_cajero,
            categoria,
            detalle,
            monto
        )
        if nuevo_saldo is not None:
            self.saldo = nuevo_saldo
            return True
        return False

    def obtener_historial_sql(
        self,
        usuario,
        password,
        fecha_inicio,
        fecha_fin
    ):
        return obtener_historial(
            usuario,
            password,
            self.numero_cuenta,
            fecha_inicio,
            fecha_fin
        )      

