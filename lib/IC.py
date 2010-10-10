##    Copyright (C) 2010 Miguel Gonzalez <enoelrocotiv@gmail.com>
##    Copyright (C) 2010 Oscar Iglesias  <osc.iglesias@gmail.com>
##
##    This file is part of rs232-obd-sim.py.
##
##    rs232-obd-sim.py is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation; either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program; if not, write to the Free Software Foundation,
##    Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

import string
import re
import serial
import threading
from utils import debug

def strhex_to_int(s):
    try:
        h = int(s,16)
    except ValueError:
        return None
    return h


class Elm(threading.Thread):
    """Emulates a ELM323 integrated circuit."""
    ID = "Fake ELM323 v1.0.0"
    ECHO = 0
    IDLE = 0
    SHOWTIME = 1
    sensors = []

    def __init__(self, port = r"\\.\CNCB0"):
        super(Elm, self).__init__(name="ELM")
        self.is_exit = False
        self.ser = serial.Serial(port, timeout=1)
        self.ECHO = 1
        self.status = self.IDLE
        self.sensors = []
        return

    def run(self):
        while self.is_exit == False:
            self.read()

    def exit(self):
        self.is_exit = True

    def read(self):
        b = []
        flag = True
        while flag:
            c = self.ser.read()
            if self.is_exit == True:
                return
            if c != '':
                if self.ECHO:
                    self.ser.write(c)
                b += c
                if c == '\n':
                    flag = False
        command = "".join(b[:-2]).upper()
        self.notify(command)

    def spacify(self, str):
        """ Introduces a space between eand 2 characters"""
        flag = False
        output = ''
        for char in str:
            output += char
            if flag == True:
                output += ' '
                flag = False
            else:
                flag = True
        return output

    def write(self, s):
        debug('Sent response "%s" '%s)
        self.ser.write(s+'\r\n')
        self.ser.write('>')

    def ok(self):
        self.write('OK')

    def error(self):
        self.write('ERROR')

    def nodata(self):
        self.write('NO DATA')

    def unknown(self):
        self.write('?')

    def doReset(self):
        self.ECHO = 1
        self.status = self.IDLE
        self.ok()

    def doInit(self):
        self.status = self.SHOWTIME
        self.write('BUSINIT: ...OK')

    def setEcho(self, s = 0):
        self.ECHO = s
        self.ok()

    def checkHexadecimal(self, s):
        return re.match('[0-9A-F ]+' , s.upper())

        return True

    def notify(self, command):
        debug('Received command %s'%repr(command))
        if command[:2] == 'AT':
            atcommand = command[2:].strip()
            if atcommand == 'Z':
                self.doReset()
            elif atcommand == 'I':
                self.write(self.ID)
            elif atcommand == 'E0':
                self.setEcho(0)
            elif atcommand == 'E1':
                self.setEcho(1)
            else:
                self.unknown()
        else:
            if self.checkHexadecimal(command):
                if self.status == self.IDLE:
                    self.doInit()
                svc = strhex_to_int(command[:2])
                pid = strhex_to_int(command[2:])
                self.notifySensor(svc, pid)
            else:
                self.error()


    def registerSensor(self, fSensor):
        self.sensors += [{
            'sensor':fSensor,
            'svc': fSensor.getService(),
            'pid': fSensor.getPID(),
        }]

    def notifySensor(self, svc, pid = None):
        debug('Searching sensor %s %s'%(svc, pid))
        for s in self.sensors:
            debug('    Checking sensor %s %s'%(s['svc'],s['pid']))
            if s['svc'] == svc and s['pid']== pid:
                debug('Found registered sensor %s%s'%(s['svc'],s['pid']))
                self.write(self.spacify(s['sensor'].response()))
                return
        self.nodata()
        debug('WARNING: %s %s not found'%(svc, pid))

