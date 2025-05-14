import sys
from Interaktion import DataOut
from ProgrammSteuerung import ProgrammSteuerung

'''
Einstiegspunkt fuer das Programm
@author: Minh Duc Ha
'''

if(len(sys.argv) == 3 and sys.argv[1] != None and sys.argv[2]!= None):
    datei= sys.argv[2]
    filepath= sys.argv[1]
    ps = ProgrammSteuerung(datei,filepath)
    ps.run()