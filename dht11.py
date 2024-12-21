import time
from machine import Pin, I2C
import dht
from ssd1306 import SSD1306_I2C

# Configuración del OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # Configurar I2C
oled = SSD1306_I2C(128, 32, i2c)

# Configuración del DHT11
sensor = Pin(15)  # Pin GPIO donde está conectado el DHT11
dht_sensor = dht.DHT11(sensor)

# Configuración de pines de salida (relés)
ventilador = Pin(2, Pin.OUT, value=1)  # Relé inicialmente apagado (HIGH)
calefactor = Pin(4, Pin.OUT, value=1)  # Relé inicialmente apagado (HIGH)

# Estados iniciales
estado_calefactor = "off"
estado_ventilador = "off"

def leer_temperatura_humedad():
    """Lee la temperatura y humedad del DHT11."""
    try:
        dht_sensor.measure()
        return dht_sensor.temperature(), dht_sensor.humidity()
    except Exception as e:
        return None, None
#grabar
def controlar_dispositivos(temperatura):
    """Controla el ventilador y calefactor según la temperatura."""
    global estado_calefactor, estado_ventilador


#ventilador = Pin(2, Pin.OUT, value=1)  # Relé inicialmente apagado (HIGH)
#calefactor = Pin(4, Pin.OUT, value=1)  # Relé inicialmente apagado (HIGH)

# Solo un relé puede activarse a la vez
    if temperatura >= 22:  # Encender ventilador, apagar calefactor
        calefactor.value(0)  # Apagar calefactor (HIGH)
        ventilador.value(0)  # Encender ventilador (LOW)
        estado_calefactor = "off"
        estado_ventilador = "on"
    elif temperatura <= 21:  # Encender calefactor, apagar ventilador
        ventilador.value(1)  # Apagar ventilador (HIGH)
        calefactor.value(1)  # Encender calefactor (LOW)
        estado_calefactor = "on"
        estado_ventilador = "off"
    else:  # Ambos apagados
        calefactor.value(1)  # Apagar calefactor (HIGH)
        ventilador.value(1)  # Apagar ventilador (HIGH)
        estado_calefactor = "off"
        estado_ventilador = "off"

def mostrar_en_oled(temperatura, humedad):
    """Muestra la temperatura, humedad y estado en el OLED."""
    oled.fill(0)
    oled.text("Temp: {:.1f}C".format(temperatura), 0, 0)
    oled.text("Hum: {:.1f}%".format(humedad), 0, 10)
    oled.text("Cal: {}".format(estado_calefactor), 0, 20)
    oled.text("Ven: {}".format(estado_ventilador), 65, 20)
    oled.show()

def main():
    while True:
        # Leer temperatura y humedad
        temperatura, humedad = leer_temperatura_humedad()
        
        if temperatura is not None and humedad is not None:
            controlar_dispositivos(temperatura)
            mostrar_en_oled(temperatura, humedad)
        else:
            # Mostrar error en la pantalla OLED
            oled.fill(0)
            oled.text("Error DHT11", 0, 10)
            oled.show()
        
        time.sleep(2)

# Ejecutar el programa
main()
