import utime
import binascii
import urequests
import pycom
import machine
import sys
import CONFIG as config
from coms import C_Wifi
from coms import C_LoRa
from coms import C_RTC
from logger import Logger
from machine import WDT

pycom.heartbeat(False)
pycom.rgbled(0x000000) # off

##########################
#  Functions             #
##########################

def _parser(data):
    msg = str(binascii.b2a_base64(data))
    payload='{"msg": "'+msg[2:-1]+'"}'
    return payload

##########################
#  Communinations        #
##########################

log = Logger('debug.log')
c_wifi = C_Wifi(config.networks)
c_rtc = C_RTC((2022, 5, 10, 18, 26, 0, 0, 0))
c_lora = C_LoRa(block=True)
wdt = WDT(timeout=600000) #10 minutos

##########################
#  MAIN                  #
##########################

while True:
    try:
        if not c_wifi.wlan.isconnected():
            log._log('[Main] Wlan not connected. Going to reset')
            machine.reset()
        log._log('[Main] Waiting for data from Lora socket....')
        print('[Main] Waiting for data from Lora socket....')
        data = c_lora.lora_socket.recv(256)
        if data:
            data=str(data)[2:-1]
            log._log('[Main] Received data from Lora')
            payload=_parser(data)
            for i in range(5):  #5 attempts
                log._log('[Main] Attempt #' + str(i))
                log._log('[Main] Payload prepared, sending...')
                res = urequests.post(config.url,headers=config.headers, data=payload, _timeout=10)
                log._log('[Main] Response received as: ' + str(res.status_code))
                wdt.feed()
                log._log('[Main] WDT feed')
                if (res.status_code == 200 or res.status_code == 201):
                    res.close()
                    break
                else:
                    res.close()
    except Exception as e:
        log._log_exception(e)
