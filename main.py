import sys
from Interaktion import DataOut
from ProgrammSteuerung import ProgrammSteuerung

# ps = ProgrammSteuerung("Eingabe.txt")

# ps.run()

if(len(sys.argv) == 3 and sys.argv[1] != None and sys.argv[2]!= None):
    datei= sys.argv[2]
    filepath= sys.argv[1]
    ps = ProgrammSteuerung(datei,filepath)
    ps.run()