import utime
import binascii
import crypto
import _thread
import urequests
import pycom
import machine
import CONFIG as config
from coms import C_Wifi
from coms import C_LoRa
from coms import C_RTC

##########################
#  Communinations        #
##########################

c_wifi = C_Wifi(config.networks[0])
c_rtc = C_RTC()
c_lora = C_LoRa()

##########################
#  MAIN                  #
##########################

def _encryptor(data):
    #RSA Encryption - 2048 bits & PKCS8 followed by base64 binary to ascii convertion
    f = open(config.publicKeyCert)
    pk = f.read()
    f.close()
    #payload='{"msg": "'+str(binascii.b2a_base64(crypto.rsa_encrypt(data, pk)))+'"}'
    payload='{"msg": "'+str(binascii.b2a_base64(data))+'"}'
    return payload

def th_send(data, id):
    for i in range(5):  #5 attempts
        try:
            pycom.rgbled(0x0000ff) # blue
            payload=_encryptor(data)
            payload='{"msg": "'+data+'"}'
            print(payload)
            res = urequests.post(config.url,headers=config.headers, data=payload)
            print(res.status_code)
            if res.status_code == 200:
                res.close()
                pycom.rgbled(0x000000) # off
                return
            else:
                res.close()
        except Exception as e:
            import sys
            pycom.rgbled(0xff0000) # red
            with open("error.log", "a") as f:
                print(e)
                sys.print_exception(e, f)

#def th_rtc(data, id):
#    s.send('{"RTC": "'+str(rtc.now())+'"}')

pycom.heartbeat(False)
while True:
    try:
        if not c_wifi.wlan.isconnected():
            machine.reset()
        data = c_lora.lora_socket.recv(256)
        if data:
            pycom.rgbled(0x00ff00) # green
            data=str(data)[2:-1]

            _thread.start_new_thread(th_send, (data, 0))
        utime.sleep(1)
    except Exception as e:
        import sys
        pycom.rgbled(0xff0000) # red
        with open("error.log", "a") as f:
            print(e)
            sys.print_exception(e, f)
