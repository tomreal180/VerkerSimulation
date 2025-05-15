import os
from typing import List

from Fehler import EingabedateinichtVorhandenError, FormatError, UngultigEingabeError
from Model import Kreuzung, Netze
from Model import EinfallsPunkt

class DataIn:
    def __init__(self, datei : str, filepath : str):
        self.Filepath :str = filepath
        self.Datei :str = os.path.join(self.Filepath, datei)
        self.titel: str = None
        self.zeitraum: List[int] = [None, None]
        self.einfallspunkte : List[EinfallsPunkt]= []
        self.kreuzungen : List[Kreuzung] = []
        self.parse_file()

    def parse_file(self):
        try:
            with open(self.Datei, 'r') as f:
                # Titel
                zeile1 = f.readline().strip()
                if zeile1.startswith("#"):
                    self.titel = zeile1[1:].strip()
                else:
                    raise FormatError("Die erste Zeile fomatiert falsch.")

                # Zeitraum
                zeile2 = f.readline().strip()
                if zeile2 == "Zeitraum:":
                    zeit_var = f.readline().strip()
                    temp1 = zeit_var.split()
                    if len(temp1) == 2:
                        self.zeitraum[0] = int(temp1[0])
                        self.zeitraum[1] = int(temp1[1])
                    else:
                        raise UngultigEingabeError("Die Eingabe des Zeitraums ist ungultig.")
                    if f.readline():
                        pass
                    else:
                        raise FormatError("Die Eingabe des Zeitraums ist nicht richtig geschlossen.")
                else: 
                    raise FormatError("Die Eingabe enthält keine Anfang des Zeitraums.")

                # Einfallspunkte
                einfallspunkt_titel = f.readline().strip()
                if einfallspunkt_titel == "Einfallspunkte:":
                    while True:
                        raw_punkt = f.readline().strip()
                        if not raw_punkt:
                            break
                        temp1 = raw_punkt.split()
                        if len(temp1) == 5:
                            name = temp1[0]
                            x = float(temp1[1])
                            y = float(temp1[2])
                            ziel = temp1[3]
                            takt = int(temp1[4])
                            self.einfallspunkte.append(EinfallsPunkt(x, y, name, takt, ziel))
                        else:
                            raise UngultigEingabeError("Die Eingabe des Einfallspunkts ist ungültig ")
                else: 
                    raise FormatError("Der Anfang des Einfallspunkts enthält falsche Format ")
                # Kreuzungen
                kreuzungen_titel = f.readline().strip()
                if kreuzungen_titel == "Kreuzungen:":
                    for line in f:
                        kreuzung = line.strip().split()
                        if len(kreuzung) >= 3 and (len(kreuzung) - 3) % 2 == 0:
                            name = kreuzung[0]
                            x = float(kreuzung[1])
                            y = float(kreuzung[2])
                            punkte = []
                            anteile = []
                            for i in range(3, len(kreuzung), 2):
                                punkte.append(kreuzung[i])
                                anteile.append(float(kreuzung[i+1]))
                            self.kreuzungen.append(Kreuzung(x, y, name, punkte, anteile))
                        else:
                            raise UngultigEingabeError("Die Eingabe des Kreuzungs ist ungueltig ")
                else:
                    raise FormatError("Die Anfangs der Kreuzungen enthält falsche Format ")
        except FileNotFoundError:
            raise EingabedateinichtVorhandenError(f"Error: File {self.Datei} is not found ")
        except ValueError as e:
            raise ValueError("Eingabedatei ist ungultig.")

    def get_zeitraum(self) -> List[int]:
        return self.zeitraum

    def get_einfallspunkte(self) -> List[EinfallsPunkt]:
        return self.einfallspunkte

    def get_kreuzungen(self) -> List[Kreuzung]:
        return self.kreuzungen


class DataOut:
        def __init__(self, filepath : str):
            self.filepath : str = filepath
        
        def create_Plan(self,netze : Netze):
            file = os.path.join(self.filepath,"Plan.txt")
            Strassen = netze.get_alle_Strassen()
            with open(file, "w") as f:
                for i,strasse in enumerate(Strassen):
                    if i== len(Strassen)-1:
                        f.write(strasse.get_Point())
                    else:
                        f.write(strasse.get_Point()+"\n")
        
        def create_Statistik(self, netze : Netze):
            file = os.path.join(self.filepath,"Statistik.txt")
            with open(file ,"w") as f:
                Strassen = netze.get_alle_Strassen()
                f.write("Gesamtanzahl Fahrzeuge pro 100m:\n")
                for strasse in Strassen:
                    statistik = strasse.get_Statistik()
                    f.write(f"{strasse}: {statistik[0]/statistik[2]}\n")
                f.write("Maximale Anzahl Fahrzeuge pro 100m:\n")
                for i,strasse in enumerate(Strassen):
                    statistik = strasse.get_Statistik()
                    if i== len(Strassen)-1:
                        f.write(f"{strasse}: {statistik[1]/statistik[2]}")
                    else:
                        f.write(f"{strasse}: {statistik[1]/statistik[2]}\n")
        
        def write_Process(self, netze: Netze, ZeitPunkt: int):
            file = os.path.join(self.filepath,"Fahrzeuge.txt")
            with open(file, "a") as f:
                Strassen = netze.get_alle_Strassen()
                f.write(f"*** t = {ZeitPunkt}\n")
                for strasse in Strassen:
                    ziel = strasse.get_Ziel()
                    fahrzeugen = strasse.get_Fahrzeugen()
                    for fahrzeug in fahrzeugen:
                        position = fahrzeug.get_Position()
                        zahl = fahrzeug.get_ID()
                        f.write(f"{position.get_X()} {position.get_Y()} {ziel.get_X()} {ziel.get_Y()} {zahl}\n")