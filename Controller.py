import os
from Fehler import EingabedateinichtVorhandenError, FormatError, StrassenichtVorhandenError, UngultigEingabeError
from View import DataIn, DataOut
from Model import Netze

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
    def __init__(self,datei : str, filepath : str):
            self.filepath : str = filepath
            self.Fehlerlog : FehlerLog = FehlerLog(datei,filepath)
            try:
                self.Datain : DataIn= DataIn(datei,filepath)
            except FormatError as e:
                self.Fehlerlog.schreiben_In_log_Datei(str(e))
                self.beenden()
            except EingabedateinichtVorhandenError as e:
                self.Fehlerlog.schreiben_In_log_Datei(str(e))
                self.beenden()
            except UngultigEingabeError as e:
                self.Fehlerlog.schreiben_In_log_Datei(str(e))
                self.beenden()
            except ValueError as e:
                self.Fehlerlog.schreiben_In_log_Datei(str(e))
                self.beenden()

            self.Dataout : DataOut= DataOut(filepath)
            try:
                self.netze : Netze= Netze(self.Datain.get_einfallspunkte(),self.Datain.get_kreuzungen())
            except StrassenichtVorhandenError as e:
                self.Fehlerlog.schreiben_In_log_Datei(str(e))
                self.beenden()
                
            self.Dataout.create_Plan(self.netze)

        
    def run(self):
        try:
            for i in range(self.Datain.get_zeitraum()[0]):
                self.netze.Simulieren(i)
                if(i%self.Datain.get_zeitraum()[1] == 0):
                    self.Dataout.write_Process(self.netze,i)
                
            
            self.Dataout.create_Statistik(self.netze)

            os.system(f"python Plot.py {self.filepath}")
        except Exception as e:
            self.Fehlerlog.schreiben_In_log_Datei(str(e))
            self.beenden()
        self.Fehlerlog.schreiben_In_log_Datei(f"Die Simulation wurde erfolgreich ausgefuehrt. Das Ergebnis ist in Ordner {self.filepath} .")
        self.beenden()
    
    def beenden(self):
        self.Fehlerlog.schreiben_In_log_Datei("Das Programm wurde beendet.")
        os._exit(0)

class FehlerLog:
    def __init__(self, datei : str, filepath : str):
        name = datei.split(".")[0]
        self.file :str = os.path.join(filepath,f"{name}.log")

    def schreiben_In_log_Datei(self, Message : str):
            with open(self.file,"a") as f:
                f.write(f"{Message}\n")

    

    