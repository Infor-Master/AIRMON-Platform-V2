""" Authors: João Campelo & Leandro Costa """

import machine
import ubinascii

WIFI_MAC = ubinascii.hexlify(machine.unique_id()).upper()

# definir a Gateway ID pelos primeiros 3 bytes do endereço MAC + 'FFFE' + os últimos 3 bytes do endereço MAC
GATEWAY_ID = WIFI_MAC[:6] + "FFFE" + WIFI_MAC[6:12]

SERVER = 'router.eu.thethings.network'
PORT = 1700

NTP = "pool.ntp.org"
NTP_PERIOD_S = 7300

#WIFI_SSID = 'WLAN1-0LJ0N2'
#WIFI_PASS = '0LJ0N21M3G1'

WIFI_SSID = 'NOS-4EC0'
WIFI_PASS = '102de71f6cc8'

# for EU868
LORA_FREQUENCY = 868100000
LORA_GW_DR = "SF12BW125" # DR_0

#DATA_RATE   |   configuration   |
#DR_0        |      SF12BW125    |
#DR_1        |      SF11BW125    |
#DR_2        |      SF10BW125    |
#DR_3        |      SF9BW125     |
#DR_4        |      SF8BW125     |
#DR_5        |      SF7BW125     |
