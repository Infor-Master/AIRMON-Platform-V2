from network import WLAN
from network import LoRa
from machine import RTC
import machine
import socket
import utime

class C_Wifi:

    def __init__(self, network):
        print('[Wifi] Wifi starting...')
        self.wlan = WLAN(mode=WLAN.STA)
        self.wlan.antenna(WLAN.EXT_ANT) #por defeito escolhe sempre a interna
        # Versão da Documentação Oficial:
        self.wlan.connect(ssid=network["SSID"], auth=(WLAN.WPA2_ENT, network["USER"],network["PASS"]), identity=network["USER"])

        # Versão documentada no github da pycom pelo autor no ficheiro de coneção WLAN:

        # self.wlan.connect(ssid=network["SSID"], auth=(WLAN.WPA2_ENT,""), wpa2_ent_method=WLAN.EAP_PEAP, wpa2_ent_auth=(network["USER"],network["PASS"]), identity=network["USER"], timeout=5000)

        while not self.wlan.isconnected():
            utime.sleep_ms(50)
        print('[Wifi] Wifi connected to '+network["SSID"])

    # def __init__(self, networks):
    #     print('[Wifi] Wifi starting...')
    #     self.wlan = WLAN(mode=WLAN.STA)
    #     nets = self.wlan.scan()
    #     for net in nets:
    #         print('[Wifi] Found ['+net.ssid+'] network')
    #         if self.wlan.isconnected():
    #             break
    #         for network in networks:
    #             if net.ssid == network[1]:
    #                 print('[Wifi] Attempting to connect to ['+network[1]+']...')
    #                 if network[0] == 'WPA2':
    #                     self.wlan.connect(network[1], auth=(WLAN.WPA2, network[2]), timeout=10000)
    #                 elif network[0] == 'WPA2E':
    #                     self.wlan.connect(network[1], auth=(WLAN.WPA2_ENT, network[3], network[2]), identity=network[3], timeout=10000)
    #                 utime.sleep(20)
    #                 break
    #     if not self.wlan.isconnected():
    #         machine.reset()
    #     print('[Wifi] Wifi started')

    # def __init__(self, networks):
    #     print('[Wifi] Wifi starting...')
    #     self.wlan = WLAN(mode=WLAN.STA, antenna=WLAN.EXT_ANT)
    #     for network in networks:
    #         print('[Wifi] Attempting to connect to ['+network[1]+']...')
    #         try:
    #             if network[0] == 'WPA2':
    #                 self.wlan.connect(network[1], auth=(WLAN.WPA2, network[2]), timeout=10000)
    #             elif network[0] == 'WPA2E':
    #                 self.wlan.connect(network[1], auth=(WLAN.WPA2_ENT, network[3], network[2]), identity=network[3])
    #             while not self.wlan.isconnected():
    #                 machine.idle()
    #             break
    #         except Exception as e:
    #             print("[Wifi] Failed to connect to ["+network[1]+"], possible timeout")
    #     if not self.wlan.isconnected():
    #         machine.reset()
    #     print('[Wifi] Wifi started')

class C_LoRa:

    def __init__(self):
        print('[LoRa] LoRa socket starting...')
        self.lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
        self.lora_socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        self.lora_socket.setblocking(False)
        print('[LoRa] LoRa socket started')

class C_RTC:

    def __init__(self):
        print('[RTC] RTC sync in progress...')
        self.rtc = RTC()
        self.rtc.ntp_sync("pool.ntp.org")
        print('[RTC] RTC synced')
