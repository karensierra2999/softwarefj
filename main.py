from abc import ABC, abstractmethod
import logging
from datetime import datetime

# =====================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGS
# =====================================================

logging.basicConfig(
    filename="softwarefj_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =====================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================

class ClienteError(Exception):
    pass


class ServicioError(Exception):
    pass


class ReservaError(Exception):
    pass


# =====================================================
# CLASE ABSTRACTA PERSONA
# =====================================================

class Persona(ABC):

    @abstractmethod
    def mostrar_datos(self):
        pass


# =====================================================
# CLASE CLIENTE
# =====================================================

class Cliente(Persona):

    def __init__(self, nombre, identificacion, correo):

        # VALIDACIONES

        if not nombre.strip():
            raise ClienteError(
                "El nombre no puede estar vacío"
            )

        if len(str(identificacion)) < 5:
            raise ClienteError(
                "La identificación debe tener mínimo 5 caracteres"
            )

        if "@" not in correo:
            raise ClienteError(
                "El correo electrónico no es válido"
            )

        # ATRIBUTOS PRIVADOS (ENCAPSULACIÓN)

        self.__nombre = nombre
        self.__identificacion = identificacion
        self.__correo = correo

    # ==========================================
    # GETTERS
    # ==========================================

    def get_nombre(self):
        return self.__nombre

    def get_identificacion(self):
        return self.__identificacion

    def get_correo(self):
        return self.__correo

    # ==========================================
    # SETTERS
    # ==========================================

    def set_correo(self, nuevo_correo):

        if "@" not in nuevo_correo:
            raise ClienteError(
                "El nuevo correo no es válido"
            )

        self.__correo = nuevo_correo

    # ==========================================
    # MÉTODO ABSTRACTO IMPLEMENTADO
    # ==========================================

    def mostrar_datos(self):

        return (
            f"Cliente: {self.__nombre} "
            f"- ID: {self.__identificacion}"
        )


# =====================================================
# CLASE ABSTRACTA SERVICIO
# =====================================================

class Servicio(ABC):

    def __init__(self, nombre, tarifa_base):

        if tarifa_base <= 0:
            raise ServicioError(
                "La tarifa base debe ser mayor que cero"
            )

        self.nombre = nombre
        self.tarifa_base = tarifa_base

    @abstractmethod
    def calcular_costo(self, horas):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# =====================================================
# SERVICIO RESERVA DE SALAS
# =====================================================

class ReservaSala(Servicio):

    def __init__(self, capacidad, tarifa_base):

        super().__init__(
            "Reserva de Sala",
            tarifa_base
        )

        if capacidad <= 0:
            raise ServicioError(
                "La capacidad debe ser positiva"
            )

        self.capacidad = capacidad

    def calcular_costo(self, horas, impuesto=0):

        costo = self.tarifa_base * horas
        costo += costo * impuesto

        return costo

    def descripcion(self):

        return (
            f"Sala para "
            f"{self.capacidad} personas"
        )


# =====================================================
# SERVICIO ALQUILER DE EQUIPOS
# =====================================================

class AlquilerEquipo(Servicio):

    def __init__(self, tipo_equipo, tarifa_base):

        super().__init__(
            "Alquiler de Equipo",
            tarifa_base
        )

        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, horas, descuento=0):

        costo = self.tarifa_base * horas
        costo -= costo * descuento

        return costo

    def descripcion(self):

        return (
            f"Alquiler de "
            f"{self.tipo_equipo}"
        )


# =====================================================
# SERVICIO ASESORÍA ESPECIALIZADA
# =====================================================

class AsesoriaEspecializada(Servicio):

    def __init__(self, especialidad, tarifa_base):

        super().__init__(
            "Asesoría Especializada",
            tarifa_base
        )

        self.especialidad = especialidad

    def calcular_costo(self, horas, recargo=0):

        costo = self.tarifa_base * horas
        costo += costo * recargo

        return costo

    def descripcion(self):

        return (
            f"Asesoría en "
            f"{self.especialidad}"
        )


# =====================================================
# CLASE RESERVA
# =====================================================

class Reserva:

    def __init__(self, cliente, servicio, horas):

        if horas <= 0:
            raise ReservaError(
                "Las horas deben ser mayores que cero"
            )

        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "Pendiente"

    # ==========================================
    # CONFIRMAR RESERVA
    # ==========================================

    def confirmar_reserva(self):

        try:

            costo = self.servicio.calcular_costo(
                self.horas
            )

            self.estado = "Confirmada"

            mensaje = (
                f"Reserva confirmada para "
                f"{self.cliente.get_nombre()} "
                f"- Costo: ${costo}"
            )

            logging.info(mensaje)

            return mensaje

        except Exception as error:

            logging.error(
                f"Error al confirmar reserva: {error}"
            )

            raise ReservaError(
                "No fue posible confirmar la reserva"
            ) from error

    # ==========================================
    # CANCELAR RESERVA
    # ==========================================

    def cancelar_reserva(self):

        try:

            if self.estado == "Cancelada":

                raise ReservaError(
                    "La reserva ya estaba cancelada"
                )

            self.estado = "Cancelada"

            mensaje = (
                f"Reserva cancelada para "
                f"{self.cliente.get_nombre()}"
            )

            logging.warning(mensaje)

            return mensaje

        except ReservaError as error:

            logging.error(error)

            return str(error)

    # ==========================================
    # MOSTRAR RESUMEN
    # ==========================================

    def mostrar_resumen(self):

        return (
            f"Cliente: {self.cliente.get_nombre()} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Horas: {self.horas} | "
            f"Estado: {self.estado}"
        )


# =====================================================
# SIMULACIÓN DEL SISTEMA
# =====================================================

print("\n========== SOFTWARE FJ ==========\n")

# =====================================================
# OPERACIÓN 1
# CLIENTE VÁLIDO
# =====================================================

try:

    cliente1 = Cliente(
        "Karen Sierra",
        "12345",
        "karen@gmail.com"
    )

    print(cliente1.mostrar_datos())

except ClienteError as error:

    print(error)
    logging.error(error)

# =====================================================
# OPERACIÓN 2
# CLIENTE INVÁLIDO
# =====================================================

try:

    cliente2 = Cliente(
        "",
        "12",
        "correo_malo"
    )

except ClienteError as error:

    print(f"Error cliente: {error}")
    logging.error(error)

# =====================================================
# OPERACIÓN 3
# SERVICIO VÁLIDO
# =====================================================

try:

    sala = ReservaSala(
        20,
        50000
    )

    print(sala.descripcion())

except ServicioError as error:

    print(error)
    logging.error(error)

# =====================================================
# OPERACIÓN 4
# SERVICIO INVÁLIDO
# =====================================================

try:

    servicio_error = ReservaSala(
        -5,
        0
    )

except ServicioError as error:

    print(f"Error servicio: {error}")
    logging.error(error)

# =====================================================
# OPERACIÓN 5
# ALQUILER EQUIPO
# =====================================================

try:

    equipo = AlquilerEquipo(
        "Computador Gamer",
        30000
    )

    print(equipo.descripcion())

except ServicioError as error:

    print(error)

# =====================================================
# OPERACIÓN 6
# ASESORÍA
# =====================================================

try:

    asesoria = AsesoriaEspecializada(
        "Python",
        80000
    )

    print(asesoria.descripcion())

except ServicioError as error:

    print(error)

# =====================================================
# OPERACIÓN 7
# RESERVA EXITOSA
# =====================================================

try:

    reserva1 = Reserva(
        cliente1,
        sala,
        3
    )

    print(
        reserva1.confirmar_reserva()
    )

    print(
        reserva1.mostrar_resumen()
    )

except Exception as error:

    print(error)

# =====================================================
# OPERACIÓN 8
# RESERVA INVÁLIDA
# =====================================================

try:

    reserva2 = Reserva(
        cliente1,
        sala,
        -4
    )

except ReservaError as error:

    print(f"Error reserva: {error}")

# =====================================================
# OPERACIÓN 9
# CANCELACIÓN
# =====================================================

try:

    print(
        reserva1.cancelar_reserva()
    )

except ReservaError as error:

    print(error)

# =====================================================
# OPERACIÓN 10
# CANCELACIÓN REPETIDA
# =====================================================

try:

    print(
        reserva1.cancelar_reserva()
    )

except ReservaError as error:

    print(error)

# =====================================================
# FINALIZACIÓN
# =====================================================

print(
    "\nSistema ejecutado correctamente."
)

logging.info(
    "Ejecución finalizada correctamente"
)
