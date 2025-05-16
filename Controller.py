import os
from Fehler import EingabedateinichtVorhandenError, FormatError, StrassenichtVorhandenError, UngultigEingabeError
from View import DataIn, DataOut
from Model import Netze

class ProgrammSteuerung:
    """
    Diese Klasse für die Programm-Steuerung, die die Daten aus der Interaktion entgegennimmt, 
    die Simulation durchführt und das Ergebnis an die Interaktion zurückgibt, 
    kann mithilfe von Interaktionen notwendige Daten und Simulation erstellen. 
    """
    def __init__(self,datei : str, filepath : str):
            """
            Konstruktor initialisiert eine neue Instanz der ProgrammSteuerung-Klasse.

            Args:
            datei (str): Der Name der Datei, für die die Log-Datei und die Verwendung von Datain erstellt wird.
                         Der Dateiname wird verwendet, um den Namen der Log-Datei zu generieren.
            filepath (str): Der Pfad, in dem die Log-Datei, DataIn, DataOut gespeichert werden soll.
            """
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
        """
        Methode startet die Simulation des Verkehrsnetzes.
        Führt die Simulation über einen definierten Zeitraum aus und speichert Zwischenergebnisse
        sowie finale Statistiken.
        """
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
        """
        Methode beendet das Programm und schreibt eine entsprechende Meldung in das Log.
        """
        self.Fehlerlog.schreiben_In_log_Datei("Das Programm wurde beendet.")
        os._exit(0)

class FehlerLog:
    """
    Diese Klasse verwaltet das Schreiben von Fehlermeldungen in eine Log-Datei.
    """
    def __init__(self, datei : str, filepath : str):
        """
        Konstruktor initialisiert eine neue Instanz der FehlerLog-Klasse.

        Args:
            datei (str): Der Name der Datei, für die das Log erstellt wird.
                         Der Dateiname wird verwendet, um den Namen der Log-Datei zu generieren.
            filepath (str): Der Pfad, in dem die Log-Datei gespeichert werden soll.
        """
        name = datei.split(".")[0]
        self.file :str = os.path.join(filepath,f"{name}.log")

    def schreiben_In_log_Datei(self, Message : str):
        """
        Methode schreibt eine Nachricht in die Log-Datei.
        Jede Nachricht wird in einer neuen Zeile hinzugefügt.

        Args:
            Message (str): Die Fehlermeldung oder Information, die geloggt werden soll.
        """
        with open(self.file,"a") as f:
            f.write(f"{Message}\n")

    

    