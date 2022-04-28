from network import WLAN
from network import LoRa
from machine import RTC
from logger import Logger
import machine
import socket
import utime

class C_Wifi:

    def __init__(self, networks):
        self.log = Logger('debug.log')

        try:
            # Usar Firmware do canal "Development". Versão 1.20.3.b4 funciona
            print('[Wifi] Wifi starting...')
            self.log._log('[Wifi] Wifi starting...')
            self.wlan = WLAN(mode=WLAN.STA)
            self.wlan.antenna(WLAN.EXT_ANT) #por defeito escolhe sempre a interna

            _timeout = 10000
            nets = self.wlan.scan()
            for net in nets:
                if self.wlan.isconnected():
                    break
                print('[Wifi] Found ['+net.ssid+'] network')
                for network in networks:
                    if net.ssid == network["SSID"]:
                        print('[Wifi] Attempting to connect to ['+network["SSID"]+']...')
                        self.log._log('[Wifi] Attempting to connect to ['+network["SSID"]+']...')
                        if network["AUTH"] == 'WPA2':
                            self.wlan.connect(ssid=network["SSID"], auth=(WLAN.WPA2, network["PASS"]), timeout=_timeout)
                        elif network["AUTH"] == 'WPA2E':
                            self.wlan.connect(ssid=network["SSID"], auth=(WLAN.WPA2_ENT, network["USER"], network["PASS"]), identity=network["USER"], hostname='Lopy Gateway', timeout=_timeout)
                        utime.sleep_ms(_timeout)
                        break
            # Versão da Documentação Oficial: (FUNCIONA)
            # self.wlan.connect(ssid=network["SSID"], auth=(WLAN.WPA2_ENT, network["USER"], network["PASS"]), identity=network["USER"], hostname='Lopy Gateway')
            if not self.wlan.isconnected():
                self.log._log('[Wifi] Failed to connect. Going to reset machine...')
                machine.reset()
            print('[Wifi] Wifi connected to '+network["SSID"])
            self.log._log('[Wifi] Wifi connected to '+network["SSID"])
        except Exception as e:
            self.log._log_exception(e)

class C_LoRa:

    def __init__(self):
        self.log = Logger('debug.log')
        print('[LoRa] LoRa socket starting...')
        self.log._log('[LoRa] LoRa socket starting...')
        self.lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
        self.lora_socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        self.lora_socket.setblocking(False)
        print('[LoRa] LoRa socket started')
        self.log._log('[LoRa] LoRa socket started')

class C_RTC:

    def __init__(self, init_time):
        self.log = Logger('debug.log')
        print('[RTC] RTC initiating...')
        self.log._log('[RTC] RTC initiating...')
        self.rtc = RTC()
        self.rtc.ntp_sync("pool.ntp.org", 360)            #pool.ntp.org
        print('[RTC] RTC sync in progress...')
        self.log._log('[RTC] RTC sync in progress...')
        sync_loop = 100
        while not self.rtc.synced() and sync_loop > 0:
            utime.sleep_ms(100)
            sync_loop = sync_loop - 1
        if not self.rtc.synced():
            print('[RTC] RTC failed to sync, using given')
            self.log._log('[RTC] RTC failed to sync, using given')
            self.rtc.init(init_time)
        else:
            print('[RTC] RTC synced')
            self.log._log('[RTC] RTC synced')
