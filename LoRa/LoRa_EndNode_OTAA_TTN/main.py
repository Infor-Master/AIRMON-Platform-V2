""" Authors: João Campelo & Leandro Costa """

from network import LoRa
from pysense import Pysense
from SI7006A20 import SI7006A20
import socket
import binascii
import struct
import time
import config
import pycom

py = Pysense()
si = SI7006A20(py)
pycom.heartbeat(False)
pycom.rgbled(0x7f0000) # red

# definir a ligação LoRa do tipo LoRaWAN
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# cria parametros para autenticação OTAA
dev_eui = binascii.unhexlify('0084585A5CBF7AC2')
app_eui = binascii.unhexlify('70B3D57ED001B5CE')
app_key = binascii.unhexlify('BF912344057D2749DCB549C9F79FDD1E')

# definir 3 canais de comunicação com a mesma frequência
lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)

# definir o spreading factor/data rate para 125kHz de largura de banda
SF=config.LORA_NODE_DR0

while True:

    # cria ligação à internet usando OTAA
    lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=SF)

    # espera até o módulo esteja conetado à internet
    while not lora.has_joined():
       time.sleep(2.5)
       print('Not joined yet...')

    pycom.rgbled(0x007f00) # green

    # remove todos os canais não utilizados
    for i in range(3, 16):
        lora.remove_channel(i)

    # cria uma socket para LoRa
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    # definir a LoRaWAN com o data rate anteriormente estabelecido
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, SF)
    # definir o socket como non-blocking
    s.setblocking(False)

    time.sleep(5.0)

    while (True):
        t_ambient=si.temperature()
        humidity=si.humidity()

        pkt=b'PKT #'+int((t_ambient-7)*100).to_bytes(2, 'little')+int(humidity*100).to_bytes(2, 'little')
        print('Sending:', pkt)
        #socket envia a mensagem criada
        s.send(pkt)
        
        time.sleep(5)

        pycom.heartbeat(True)
        pycom.heartbeat(False)
        # coloca o módulo em modo deepsleep
        py.setup_sleep(7200)
        py.go_to_sleep()
        pycom.heartbeat(True)
        pycom.heartbeat(False)
        pycom.rgbled(0x007f00)
