import random
import math


class Punkt:
    def __init__(self,x,y,Name = None):
        self.x = x
        self.y = y
        self.name = Name


    def get_Name(self):
        return self.name
    
    def get_X(self):
        return self.x
    
    def get_Y(self):
        return self.y
    
    def get_Abstand(self,punkt):
        vectorX = self.x - punkt.get_X()
        vectorY = self.y - punkt.get_Y()
        return math.sqrt(vectorX**2 + vectorY**2)
    
    def berechnen_Vektor(self, punkt):
        erg = [None, None]
        erg[0] = punkt.get_X()-self.x
        erg[1] = punkt.get_Y()-self.y
        return erg
    
    def set_X(self, newX):
        self.x = newX;

    def set_Y(self, newY):
        self.y = newY

    def __str__(self):
        return f"({self.x}, {self.y})"

class EinfallsPunkt(Punkt):
    def __init__(self,x,y,name,Takt,Ziel):
        super().__init__(x,y,name)
        self.Takt = Takt
        self.Ziel = Ziel
        self.Strasse = None

    def __str__(self):
        return self.name
    
    def set_Strasse(self, strasse):
        self.Strasse = strasse
    
    def get_Strasse(self):
        return self.Strasse

    def get_Ziel(self):
        return self.Ziel
    
    def get_Takt(self):
        return self.Takt

class Kreuzung(Punkt):
    def __init__(self,x, y,name,Ziele,Anteile):
        super().__init__(x,y, name)
        self.Ziele = Ziele
        self.Anteile = Anteile
        self.Strassen = []
    
    def get_Strassen(self):
        return self.Strassen
    
    def add_Strassen(self,strass):
        self.Strassen.append(strass)

    def get_Ziele(self):
        return self.Ziele

    def waehlen_naechsten_Ziel(self,letzteAnfang):
        indexofletzteAnfang = self.Ziele.index(letzteAnfang)
        gesamt = 0
        tempWahl = []
        tempCheck= []
        for i in range(len(self.Ziele)):
            if (i == indexofletzteAnfang):
                continue

            gesamt+= self.Anteile[i]
            tempCheck.append(gesamt)
            tempWahl.append(self.Strassen[i])

        wahl = random.random()*gesamt

        for j in range(len(tempCheck)):
            if(wahl<tempCheck[j]):
                return tempWahl[j]
        
        return tempWahl[0]
    

    def __str__(self):
        return self.name
    


class Fahrzeug:
    
    def __init__(self, anfang: Punkt, Zahl):
        self.Position = Punkt(anfang.get_X(), anfang.get_Y())
        self.Geschwindigkeit = self.get_random_Geschwindigkeit()
        self.Zahl = Zahl
    
    def get_Zahl(self):
        return self.Zahl;

    def get_random_Geschwindigkeit(self):
        rnd = random.Random()
        geschwindigkeit = max(0, rnd.gauss(45,10)) /360
        return geschwindigkeit
    
    def get_Position(self):
        return self.Position
    
    def get_Geswindigkeit(self):
        return self.Geschwindigkeit
    
    def __str__(self):
        return self.Position
    def set_new_Point(self, punkt: Punkt):
        self.Position = punkt

    def berechnen_next_Point(self, vektor,lange):
        alpha = self.berechnen_alpha(vektor, lange, self.Geschwindigkeit)
        new_x = self.Position.get_X() + alpha[0]
        new_y = self.Position.get_Y() + alpha[1]
        return Punkt(new_x,new_y)
    
    def berechnen_alpha(self,vektor, lange, Abstand):
        einheit = [Abstand*vektor[0]/lange, Abstand*vektor[1]/lange ]   
        return einheit
    
    def berechnen_Point(self,anfang: Punkt, vektor, lange, alpha):
        alpha1 = self.berechnen_alpha(vektor,lange, self.Geschwindigkeit-alpha)
        new_x = anfang.get_X() + alpha1[0]
        new_y = anfang.get_Y() + alpha1[1]
        self.Position = Punkt(new_x,new_y) 

    def __str__(self):
        return self.Position


class Strasse:
    def __init__(self,Anfang : Punkt,Ziel: Punkt ):
       self.Anfang = Anfang
       self.Ziel = Ziel
       self.Vektor = Anfang.berechnen_Vektor(Ziel)
       self.Länge =  Anfang.get_Abstand(Ziel)
       self.Fahrzeugen = []
       self.Max = 0
       self.Gesamt = 0

    def get_Anfang(self):
        return self.Anfang
    
    def get_Fahrzeugen(self):
        return self.Fahrzeugen
    
    def get_Length(self):
        return self.Länge
    
    def get_Vektor(self):
        return self.Vektor
    
    def get_Ziel(self):
        return self.Ziel
    
    def add_Fahrzeug(self, newCar):
        self.Gesamt+=1
        self.Fahrzeugen.append(newCar)
        if len(self.Fahrzeugen )> self.Max:
            self.Max = len(self.Fahrzeugen)
    
    def check_Fahrzeug(self):
        for i, fahrzeug in enumerate(self.Fahrzeugen):
            nextPosition = fahrzeug.berechnen_next_Point(self.Vektor, self.Länge)
            vectorMitZiel = self.Ziel.berechnen_Vektor(nextPosition)
            längevonFahrzeugbisZiel = fahrzeug.get_Position().get_Abstand(self.Ziel)
            check = [self.Vektor[0]*vectorMitZiel[0], self.Vektor[1]*vectorMitZiel[1]]
            if not(check[0] >= -1e-9 and check[1]>= -1e-9):
                fahrzeug.set_new_Point(nextPosition)
            else:
                ziel = self.Ziel
                if isinstance(ziel,Kreuzung):
                    tempZiel = ziel
                    anfangName = self.Anfang.get_Name()
                    nextStrasse = tempZiel.waehlen_naechsten_Ziel(anfangName)
                    
                    fahrzeug.berechnen_Point(nextStrasse.get_Anfang(), nextStrasse.get_Vektor(),nextStrasse.get_Length() ,längevonFahrzeugbisZiel)
                    nextStrasse.add_Fahrzeug(fahrzeug)
                
                self.Fahrzeugen.pop(i)

    def print_Fahrzeugen(self):
        str = ""
        for fahrzeug in self.Fahrzeugen:
            str+= f", {fahrzeug.__str__()}"
        print(f"{self} : {str}")
        

    def get_Statistik(self):
        return (self.Gesamt, self.Max, self.Länge)

    def get_Point(self):
        return f"{round(self.Anfang.get_X(),1)} {round(self.Anfang.get_Y(),1)} {round(self.Ziel.get_X(),1)} {round(self.Ziel.get_Y(),1)}"

    def __str__(self):
        return f"{self.Anfang}-->{self.Ziel}"


class Netze:
    def __init__(self, Einfallspunkte, Kreuzugen):
        self.Einfallspunkte = Einfallspunkte
        self.Kreuzungen = Kreuzugen
        self.n = 0
        self.finden_Strassen()

    
    def finden_Strassen(self):
        for ep in self.Einfallspunkte:
            ziel = self.get_Punkt(ep.get_Ziel())
            if(ziel != None):
                ep.set_Strasse(Strasse(ep,ziel))

        for kp in self.Kreuzungen:
            Ziele = kp.get_Ziele()
            for z in Ziele:
                ziel = self.get_Punkt(z)
                kp.add_Strassen(Strasse(kp,ziel))

    def get_Punkt(self,name):
        for ep in self.Einfallspunkte:
            if(ep.get_Name() == name):
                return ep
        
        for kp in self.Kreuzungen:
            if (kp.get_Name() == name):
                return kp
            
        return None
    
    def get_alle_Strassen(self):
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
                newCar = Fahrzeug(ep,self.n)
                s.add_Fahrzeug(newCar)
                self.n += 1
            
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

