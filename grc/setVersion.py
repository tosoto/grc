import time

currentVer = str(time.time()).split('.')[0]

f = open('VERSION', 'w')
f.write('0.0.%s'%currentVer)
f.close()