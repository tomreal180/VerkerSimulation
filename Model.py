import random
import math
from typing import List

from Fehler import StrassenichtVorhandenError


class Punkt:
    def __init__(self,x : float,y : float,Name : str = None):
        self.x : float = x
        self.y : float= y
        self.name :str = Name


    def get_Name(self) -> str:
        return self.name
    
    def get_X(self) -> float:
        return self.x
    
    def get_Y(self)-> float:
        return self.y
    
    def get_Abstand(self,punkt) -> float:
        vectorX = self.x - punkt.get_X()
        vectorY = self.y - punkt.get_Y()
        return math.sqrt(vectorX**2 + vectorY**2)
    
    def berechnen_Vektor(self, punkt) ->tuple[float]:
        return (punkt.get_X()-self.x, punkt.get_Y()-self.y)
    
    def __str__(self):
        return f"({self.x}, {self.y})"

class Fahrzeug:
    
    def __init__(self, anfang: Punkt, id: int):
        self.Position: Punkt = Punkt(anfang.get_X(), anfang.get_Y())
        self.Geschwindigkeit:float= self.get_random_Geschwindigkeit()
        self.id: int = id
    
    def get_ID(self) -> int:
        return self.id;

    def get_random_Geschwindigkeit(self) -> float:
        rnd = random.Random()
        geschwindigkeit = max(0, rnd.gauss(45,10)) /360
        return geschwindigkeit
    
    def get_Position(self) -> Punkt:
        return self.Position
    
    def get_Geswindigkeit(self) -> float:
        return self.Geschwindigkeit
    
    def __str__(self):
        return self.Position
    
    def set_new_Point(self, punkt: Punkt):
        self.Position = punkt

    def berechnen_next_Point(self, vektor: tuple[float],lange : float) -> Punkt:
        alpha = self.berechnen_Einheit(vektor, lange, self.Geschwindigkeit)
        new_x = self.Position.get_X() + alpha[0]
        new_y = self.Position.get_Y() + alpha[1]
        return Punkt(new_x,new_y)
    
    def berechnen_Einheit(self,vektor : tuple[float], lange : float, Abstand : float) -> tuple[float]:   
        return (Abstand*vektor[0]/lange, Abstand*vektor[1]/lange)
    
    def berechnen_Point(self,anfang: Punkt, vektor: tuple[float], lange : float, rest :float):
        alpha = self.berechnen_Einheit(vektor,lange, self.Geschwindigkeit-rest)
        new_x = anfang.get_X() + alpha[0]
        new_y = anfang.get_Y() + alpha[1]
        self.Position = Punkt(new_x,new_y) 


class Strasse:
    def __init__(self,Anfang : Punkt,Ziel: Punkt ):
       self.Anfang : Punkt = Anfang
       self.Ziel : Punkt = Ziel
       self.Vektor: tuple[float] = Anfang.berechnen_Vektor(Ziel)
       self.Length: float =  Anfang.get_Abstand(Ziel)
       self.Fahrzeugen: List[Fahrzeug] = []
       self.Max: float = 0
       self.Gesamt: float = 0

    def get_Anfang(self) -> Punkt:
        return self.Anfang
    
    def get_Fahrzeugen(self) -> List[Fahrzeug]:
        return self.Fahrzeugen
    
    def get_Length(self) -> float:
        return self.Length
    
    def get_Vektor(self) -> tuple[float]:
        return self.Vektor
    
    def get_Ziel(self) -> Punkt:
        return self.Ziel
    
    def add_Fahrzeug(self, newCar : Fahrzeug):
        self.Fahrzeugen.append(newCar)
        self.Gesamt+=len(self.Fahrzeugen)
        if len(self.Fahrzeugen )> self.Max:
            self.Max = len(self.Fahrzeugen)
    
    def check_Fahrzeug(self):
        for i, fahrzeug in enumerate(self.Fahrzeugen):
            nextPosition = fahrzeug.berechnen_next_Point(self.Vektor, self.Length)
            vectorMitZiel = self.Ziel.berechnen_Vektor(nextPosition)
            check = [self.Vektor[0]*vectorMitZiel[0], self.Vektor[1]*vectorMitZiel[1]]
            if not(check[0] >= -1e-9 and check[1]>= -1e-9):
                fahrzeug.set_new_Point(nextPosition)
            else:
                ziel = self.Ziel
                if isinstance(ziel,Kreuzung):
                    tempZiel = ziel
                    anfangName = self.Anfang.get_Name()
                    nextStrasse = tempZiel.waehlen_naechsten_Ziel(anfangName)
                    LengthvonFahrzeugbisZiel = fahrzeug.get_Position().get_Abstand(self.Ziel)
                    fahrzeug.berechnen_Point(nextStrasse.get_Anfang(), nextStrasse.get_Vektor(),nextStrasse.get_Length() ,LengthvonFahrzeugbisZiel)
                    nextStrasse.add_Fahrzeug(fahrzeug)
                
                self.Fahrzeugen.pop(i)

    # def print_Fahrzeugen(self):
    #     str = ""
    #     for fahrzeug in self.Fahrzeugen:
    #         str+= f", {fahrzeug.__str__()}"
    #     print(f"{self} : {str}")
        

    def get_Statistik(self) -> tuple[float]:
        return (self.Gesamt, self.Max, self.Length)

    def get_Point(self) -> str:
        return f"{round(self.Anfang.get_X(),1)} {round(self.Anfang.get_Y(),1)} {round(self.Ziel.get_X(),1)} {round(self.Ziel.get_Y(),1)}"

    def __str__(self):
        return f"{self.Anfang}-->{self.Ziel}"



class EinfallsPunkt(Punkt):
    def __init__(self,x : float,y: float,name : str,Takt : int,Ziel : str):
        super().__init__(x,y,name)
        self.Takt : int = Takt
        self.Ziel : str= Ziel
        self.Strasse : Strasse= None

    def __str__(self):
        return self.name
    
    def set_Strasse(self, strasse : Strasse):
        self.Strasse = strasse
    
    def get_Strasse(self) -> Strasse:
        return self.Strasse

    def get_Ziel(self) -> Punkt:
        return self.Ziel
    
    def get_Takt(self) -> int:
        return self.Takt

class Kreuzung(Punkt):
    def __init__(self,x : float, y : float,name : str,Ziele : List[str],Anteile: List[float]):
        super().__init__(x,y, name)
        self.Ziele : List[str]= Ziele
        self.Anteile : List[float] = Anteile
        self.Strassen : List[Strasse] = []
    
    def get_Strassen(self):
        return self.Strassen
    
    def add_Strassen(self,strasse: Strasse):
        self.Strassen.append(strasse)

    def get_Ziele(self) -> Punkt:
        return self.Ziele

    def waehlen_naechsten_Ziel(self,letzteAnfang : Punkt) -> Strasse:
        indexofletzteAnfang = self.Ziele.index(letzteAnfang)
        gesamt = 0
        tempWahl = []
        tempAnteil= []
        for i in range(len(self.Ziele)):
            if (i == indexofletzteAnfang):
                continue

            gesamt+= self.Anteile[i]
            tempAnteil.append(self.Anteile[i])
            tempWahl.append(self.Strassen[i])

        tempAnteile = [anteil / gesamt for anteil in tempAnteil]

        return random.choices(tempWahl, weights=tempAnteile, k=1)[0]
    

    def __str__(self):
        return self.name
    

class Netze:
    def __init__(self, Einfallspunkte:List[EinfallsPunkt], Kreuzugen: List[Kreuzung]):
        self.Einfallspunkte : List[EinfallsPunkt] = Einfallspunkte
        self.Kreuzungen : List[Kreuzung] = Kreuzugen
        self.Zahl : int= 0
        self.finden_Strassen()

    
    def finden_Strassen(self):
        for ep in self.Einfallspunkte:
            ziel = self.get_Punkt(ep.get_Ziel())
            if(ziel):
                ep.set_Strasse(Strasse(ep,ziel))
            else:
                raise StrassenichtVorhandenError(f"Es gibt keine Punkt {ep.get_Ziel()}")
        for kp in self.Kreuzungen:
            Ziele = kp.get_Ziele()
            for z in Ziele:
                ziel = self.get_Punkt(z)
                if ziel:
                    kp.add_Strassen(Strasse(kp,ziel))
                else:
                   raise StrassenichtVorhandenError(f"Es gibt keine Punkt {z}") 

    def get_Punkt(self,name) -> Punkt:
        for ep in self.Einfallspunkte:
            if(ep.get_Name() == name):
                return ep
        
        for kp in self.Kreuzungen:
            if (kp.get_Name() == name):
                return kp
            
        return None
    
    def get_alle_Strassen(self) -> List[Strasse]:
        erg = []
        for ep in self.Einfallspunkte:
            erg.append(ep.get_Strasse())
        for kp in self.Kreuzungen:
            Strassen = kp.get_Strassen()
            for strasse in Strassen:
                erg.append(strasse)
        return erg
    
    def Simulieren(self,ZeitPunkt: int):
        # print(ZeitPunkt)
        # print("EinfallsPunkt")
        for ep in self.Einfallspunkte:
            s = ep.get_Strasse()
            s.check_Fahrzeug()
            Takt = ep.get_Takt()
            if (ZeitPunkt != 0) and (ZeitPunkt % Takt == 0):
                newCar = Fahrzeug(ep,self.Zahl)
                s.add_Fahrzeug(newCar)
                self.Zahl += 1
            
            # #test
            # s.print_Fahrzeugen()
        
        # print("Kreuzung: ")

        for kp in self.Kreuzungen:
            # print(kp)
            s = kp.get_Strassen()
            for t in s:
                t.check_Fahrzeug()
                # #test
                # t.print_Fahrzeugen()

