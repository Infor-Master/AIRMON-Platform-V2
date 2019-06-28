""" Authors: João Campelo & Leandro Costa """

import machine
import binascii

WIFI_MAC = binascii.hexlify(machine.unique_id()).upper()

# for EU868
LORA_FREQUENCY = 868100000
LORA_NODE_DR0 = 0
LORA_NODE_DR1 = 1
LORA_NODE_DR2 = 2
LORA_NODE_DR3 = 3
LORA_NODE_DR4 = 4
LORA_NODE_DR5 = 5

#DATA_RATE   |   configuration   |
#DR_0        |      SF12BW125    |
#DR_1        |      SF11BW125    |
#DR_2        |      SF10BW125    |
#DR_3        |      SF9BW125     |
#DR_4        |      SF8BW125     |
#DR_5        |      SF7BW125     |
