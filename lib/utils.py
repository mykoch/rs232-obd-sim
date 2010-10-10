import random
import string

def debug(msg):
     pass #print('-- ' + msg)

def sample(var):
    if var == 'VSS':
        self = hex (int(random.randrange(40,90)))[2:].upper()
    elif var == 'RPM':
        self = hex (int(random.randrange(750,4500)))[2:].upper()
    else:
        self = hex (int(random.randrange(0,255)))[2:].upper()
    if len(self)%2 == 1:
        self = '0' + self
    return self

