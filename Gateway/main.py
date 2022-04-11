import utime
import binascii
import _thread
import urequests
import pycom
import machine
import sys
import CONFIG as config
from coms import C_Wifi
from coms import C_LoRa
from coms import C_RTC
from logger import Logger

pycom.heartbeat(False)
pycom.rgbled(0x000000) # off

##########################
#  Functions             #
##########################

def _encryptor(data):
    msg = str(binascii.b2a_base64(data))
    payload='{"msg": "'+msg[2:-1]+'"}'
    return payload

def th_send(data, id):
    for i in range(5):  #5 attempts
        log._log('[Thread] Attempt #' + str(i))
        try:
            payload=_encryptor(data)
            log._log('[Thread] Payload prepared, sending...')
            res = urequests.post(config.url,headers=config.headers, data=payload)
            log._log('[Thread] Response received as: ' + str(res.status_code))
            if (res.status_code == 200 or res.status_code == 201):
                res.close()
                return
            else:
                res.close()
        except Exception as e:
            log._log_exception(e)

##########################
#  Communinations        #
##########################

log = Logger('debug.log')
c_wifi = C_Wifi(config.networks)
c_rtc = C_RTC()
c_lora = C_LoRa()

##########################
#  MAIN                  #
##########################

while True:
    try:
        if not c_wifi.wlan.isconnected():
            log._log('[Main] Wlan not connected. Going to reset')
            machine.reset()
        data = c_lora.lora_socket.recv(256)
        if data:
            data=str(data)[2:-1]
            log._log('[Main] Received data from Lora, going to start new thread')
            _thread.start_new_thread(th_send, (data, 0))
        utime.sleep(1)
    except Exception as e:
        log._log_exception(e)
