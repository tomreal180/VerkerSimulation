from Interaktion import DataIn, DataOut
from Logik import Netze

class ProgrammSteuerung:
    def __init__(self,datei):
        self.Datain = DataIn(datei)
        self.Dataout = DataOut(datei)
        self.netze = Netze(self.Datain.get_einfallspunkte(),self.Datain.get_kreuzungen())
        self.Dataout.create_Plan(self.netze)
        
    def run(self):
        for i in range(self.Datain.get_zeitraum()[0]):
            self.netze.Simulieren(i)
            if(i%self.Datain.get_zeitraum()[1] == 0):
                self.Dataout.write_Process(self.netze,i)
            
        
        self.Dataout.create_Statistik(self.netze)

    