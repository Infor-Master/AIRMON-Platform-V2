from network import WLAN
import binascii
wl = WLAN()
print("Gateway EUI: {}".format(binascii.hexlify(wl.mac())[:6] + 'fffe' + binascii.hexlify(wl.mac())[6:]))
