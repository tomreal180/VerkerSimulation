import os
from Interaktion import DataIn, DataOut
from Logik import Netze

class ProgrammSteuerung:
    """
    Klasse fuer die Programm-Steuerung, die die Daten aus der Interaktion entgegenimmt,
    die Simulation durchgeführt und das Ergebnis an die Interaktion zurueckgibt, damit es
    mit Hilfe von Interaktionen notwendige Daten und Simulation erstellen kann 

     Attribute:
        filepath (string): Adresse von path
        Datain (DataIn): Input-Handler
        Dataout (DataOut): Output-Handler
        Fehlerlog (FehlerLog): .log Datei- Handler
        netze (Netze): Verkehrsystem enthält alle Einfallspunkte und Kreuzungen
    """
    def __init__(self,datei, filepath):
        self.filepath = filepath
        self.Datain = DataIn(datei,filepath)
        self.Dataout = DataOut(filepath)
        self.Fehlerlog = FehlerLog(datei,filepath)
        self.netze = Netze(self.Datain.get_einfallspunkte(),self.Datain.get_kreuzungen())
        self.Dataout.create_Plan(self.netze)
        
    def run(self):
        for i in range(self.Datain.get_zeitraum()[0]):
            self.netze.Simulieren(i)
            if(i%self.Datain.get_zeitraum()[1] == 0):
                self.Dataout.write_Process(self.netze,i)
            
        
        self.Dataout.create_Statistik(self.netze)

        os.system(f"python Plot.py {self.filepath}")

        self.Fehlerlog.schreiben_In_log_Datei(f"Die Simulation wurde erfolgreich ausgeführt. Das Ergebnis ist in Ordner{self.filepath}.")
        self.beenden()
    
    def beenden(self):
        self.Fehlerlog.schreiben_In_log_Datei("Das Programm wurde beendet.")
        os._exit(0)

class FehlerLog:
    def __init__(self, datei, filepath):
        name = datei.split(".")[0]
        self.file = os.path.join(filepath,f"{name}.log")

    def schreiben_In_log_Datei(self, Message):
        with open(self.file,"a") as f:
            f.write(Message)

    

    