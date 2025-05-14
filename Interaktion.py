import os

from Logik import Kreuzung, Netze
from Logik import EinfallsPunkt

class DataIn:
    def __init__(self, datei, filepath):
        self.Filepath = filepath
        self.Datei = os.path.join(self.Filepath, datei)
        self.titel = None
        self.zeitraum = [None, None]
        self.einfallspunkte = []
        self.kreuzungen = []
        self.parse_file()

    def parse_file(self):
        try:
            with open(self.Datei, 'r') as f:
                # Titel
                zeile1 = f.readline().strip()
                if zeile1.startswith("#"):
                    self.titel = zeile1[1:].strip()

                # Zeitraum
                zeile2 = f.readline().strip()
                if zeile2 == "Zeitraum:":
                    zeit_var = f.readline().strip()
                    temp1 = zeit_var.split()
                    if len(temp1) == 2:
                        self.zeitraum[0] = int(temp1[0])
                        self.zeitraum[1] = int(temp1[1])
                    if f.readline(): # Consume the empty line after Zeitraum
                        pass

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

        except FileNotFoundError:
            print(f"Error: File not found at {self.in_file}")
        except Exception as e:
            print(f"An error occurred during parsing: {e}")

    def get_zeitraum(self):
        return self.zeitraum

    def get_einfallspunkte(self):
        return self.einfallspunkte

    def get_kreuzungen(self):
        return self.kreuzungen


class DataOut:
        def __init__(self, filepath):
            self.filepath = filepath
        
        def create_Plan(self,netze : Netze):
            file = os.path.join(self.filepath,"plan.txt")
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
                    f.write(f"{strasse}: {round(statistik[0]/statistik[2],1)}\n")
                f.write("Maximale Anzahl Fahrzeuge pro 100m:\n")
                for i,strasse in enumerate(Strassen):
                    statistik = strasse.get_Statistik()
                    if i== len(Strassen)-1:
                        f.write(f"{strasse}: {round(statistik[1]/statistik[2],1)}")
                    else:
                        f.write(f"{strasse}: {round(statistik[1]/statistik[2],1)}\n")
        
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
                        zahl = fahrzeug.get_Zahl()
                        f.write(f"{position.get_X()} {position.get_Y()} {ziel.get_X()} {ziel.get_Y()} {zahl}\n")