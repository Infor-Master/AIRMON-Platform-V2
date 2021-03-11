from network import LoRa
import socket
import crypto
import utime
import _thread
import pycom
import os
import machine
from machine import SD
import CONFIG as cfg
from MQ131_O3_Sensor import MQ131
from MiCs6814_MultiChannel_Sensor import MiCS6814
from SEN0219_CO2_Sensor import SEN0219_SERIAL
from PMS5003ST_Sensor import PMS5003ST

keycode = cfg.keycode
R0_MQ131 = cfg.R0_MQ131
sleep_lenght = const(480000)

sd = SD()
os.mount(sd, '/sd')

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

def th_send(data, id):
    while True:
        try:
            # Pinos 0, 1, 4, 5, 6, 7, 8, 12, 22, 23 reservados para sistema

            pycom.rgbled(0x0000ff) #Blue

            print('[PMS] heating up...')
            PMS = PMS5003ST(TX='P2', RX='P3')
            utime.sleep(30)
            print('[PMS] reading...')
            PMSdata = PMS.PMSReadActive()
            PMS.deinit()
            if(PMSdata==False):
                pycom.rgbled(0xffff00)
                print('[PMS] failed to read')
                continue
            CH2O_PPM=(24.45 * PMSdata[12]) / 30.026
            CH2O=str(CH2O_PPM)
            Temp=str(PMSdata[13])
            Humd=str(PMSdata[14])
            print('[PMS] finished')

            print('[MiCS] starting...')
            MiCS = MiCS6814(SDA='P10',SCL='P11')
            utime.sleep(1)
            gases=MiCS.calcAllGases()
            MiCS.deinit()
            NO2=str(gases[1]); #Possui mais gases mas só queremos o NO2
            print('[MiCS] finished')

            print('[MQ] starting...')
            MQ = MQ131(pin='P16', R0=R0_MQ131)
            utime.sleep(1)
            MQvolts = MQ.MQRead()
            MQPPB = MQ.MQGet_PPB(MQvolts)
            MQ.deinit()
            O3=str(MQPPB)
            print('[MQ] finished')

            print('[SEN] starting...')
            SEN_S = SEN0219_SERIAL(TX='P20', RX='P21')
            #SEN_S.SEN_Serial_ABCOn()
            utime.sleep(1)
            print('[SEN] reading...')
            SENdata = SEN_S.SEN_Serial_read()
            SEN_S.deinit()
            if(SENdata==False):
                pycom.rgbled(0xffff00)
                print('[SEN] failed to read')
                continue
            SENPPM = (256*SENdata[2]) + SENdata[3]
            CO2=str(SENPPM)
            print('[SEN] finished')

            data = '{"keycode": "'+keycode+'","CO2": '+CO2+',"NO2": '+NO2+',"O3": '+O3+',"CH2O": '+CH2O+',"Temp": '+Temp+',"Humd": '+Humd+'}'

            print('[Data] sending...')
            s.send(data)
            print("[DATA] saving localy...")
            f = open('/sd/DataLog.csv', 'a')
            f.write("\";"+data+"\"\n")
            f.close()
            print("[DATA] : "+data)
            print("[DATA] finished")

            pycom.rgbled(0x000000) # off
            machine.sleep(sleep_lenght)
        except Exception as e:
            import sys
            pycom.rgbled(0xff0000) # red
            print("[Error] ")
            with open("error.log", "a") as f:
                sys.print_exception(e, f)

pycom.heartbeat(False)
_thread.start_new_thread(th_send, (0, 0))
