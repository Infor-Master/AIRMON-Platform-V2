import sys
import uos
import machine
from machine import RTC

class Logger:

    def __init__(self, filename):
        self.filename = filename

    def _log_exception(self, e):
        with open('error.log', "a") as f:
            sys.print_exception(e, f)
        self._check_size('error.log')
        machine.reset()

    def _log(self, msg):
        with open(self.filename, "a") as f:
            f.write(str('['+self._rtc()+'] '+msg+'\n'))
            f.close()
        self._check_size(self.filename)

    def _check_size(self, filename):
        statinfo = uos.stat(filename)
        if statinfo[6] > 10240: #10 kb, stat[6] = st_size
            uos.remove(str('OLD_' + filename))
            uos.rename(filename, str('OLD_' + filename))

    def _rtc(self):
        rtc = RTC()
        curr = rtc.now()
        return str(str(curr[0]) + '-' + str(curr[1]) + '-' + str(curr[2]) + ' ' + str(curr[3]) + ':' + str(curr[4]) + ':' + str(curr[5]))
