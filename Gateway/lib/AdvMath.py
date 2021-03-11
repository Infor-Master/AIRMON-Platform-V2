import math
import crypto

def log10(val):
    return math.log(val)/math.log(10)

def _Random():
   r = crypto.getrandbits(32)
   return ((r[0]<<24)+(r[1]<<16)+(r[2]<<8)+r[3])/4294967295.0

def _RandomRange(rfrom, rto):
   return _Random()*(rto-rfrom)+rfrom
