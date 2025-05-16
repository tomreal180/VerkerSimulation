import random
import math
from typing import List

from Fehler import StrassenichtVorhandenError


class Punkt:
    """
    Diese Klasse repräsentiert einen Punkt in einem zweidimensionalen Raum
    mit X- und Y-Koordinaten und optional einem Namen.
    """
    def __init__(self,x : float,y : float,Name : str = None):
        """
        Konstruktor initialisiert eine neue Instanz der Punkt-Klasse.

        Args:
            x (float): Die X-Koordinate des Punktes.
            y (float): Die Y-Koordinate des Punktes.
            Name (str, optional): Ein optionaler Name für den Punkt. Standardmäßig None.
        """
        self.x : float = x
        self.y : float= y
        self.name :str = Name

    """
    #Erweiterung 1 - Mindestand zum vorausfahrenden Fahrzeug einhalten::
    Vegleichmethode wird entwickelt, die 2 Punkte abhängig von der Vektor vergleicht werden.
    Entwickeln eine Setter-Methode, die die neue Position und Geschwindigkeit einsetzt.
    """
    def get_Name(self) -> str:
        """
        Getter-Methode gibt den Namen des Punktes zurück.

        Returns:
            str: Der Name des Punktes.
        """
        return self.name
    
    def get_X(self) -> float:
        """
        Getter-Methode gibt die X-Koordinate des Punktes zurück.

        Returns:
            float: Die X-Koordinate.
        """
        return self.x
    
    def get_Y(self)-> float:
        """
        Getter-Methode gibt die Y-Koordinate des Punktes zurück.

        Returns:
            float: Die Y-Koordinate.
        """
        return self.y
    
    def get_Abstand(self,punkt) -> float:
        """
       Methode berechnet des euklidischen Abstandes zwischen diesem Punkt und einem anderen Punkt.

        Args:
            punkt (Punkt): Der andere Punkt, zu dem der Abstand berechnet werden soll.

        Returns:
            float: Der Abstand zwischen den beiden Punkten.
        """
        vectorX = self.x - punkt.get_X()
        vectorY = self.y - punkt.get_Y()
        return math.sqrt(vectorX**2 + vectorY**2)
    
    def berechnen_Vektor(self, punkt) ->tuple[float]:
        """
        Methode berechnet des Vektors von diesem Punkt zu einem anderen Punkt.

        Args:
            punkt (Punkt): Der Zielpunkt, zu dem der Vektor berechnet werden soll.

        Returns:
            tuple[float]: Ein Tupel (delta_x, delta_y), das den Vektor repräsentiert.
        """
        return (punkt.get_X()-self.x, punkt.get_Y()-self.y)
    
    def __str__(self):
        """
        Methode gibt eine String-Repräsentation des Punktes zurück, typischerweise als (x, y).

        Returns:
            str: Die String-Repräsentation des Punktes.
        """
        return f"({self.x}, {self.y})"

class Fahrzeug:
    """
    Diese Klasse repräsentiert ein Fahrzeug in der Simulation.
    """
    def __init__(self, anfang: Punkt, id: int):
        """
        Konstruktor initialisiert eine neue Instanz der Fahrzeug-Klasse.

        Args:
            anfang (Punkt): Der Startpunkt des Fahrzeugs.
            id (int): Eine eindeutige Identifikationsnummer für das Fahrzeug.
        """
        self.Position: Punkt = Punkt(anfang.get_X(), anfang.get_Y())
        self.Geschwindigkeit:float= self.get_random_Geschwindigkeit()
        self.id: int = id
    
    def get_ID(self) -> int:
        """
        Getter-Methode gibt die ID des Fahrzeugs zurück.

        Returns:
            int: Die eindeutige Identifikationsnummer des Fahrzeugs.
        """
        return self.id;

    def get_random_Geschwindigkeit(self) -> float:
        """
        Methode generiert. die eine zufällige Geschwindigkeit für das Fahrzeug 

        Returns:
            float: Die zufällig generierte Geschwindigkeit des Fahrzeugs.
        """
        rnd = random.Random()
        geschwindigkeit = max(0, rnd.gauss(45,10)) /360
        return geschwindigkeit
    
    def get_Position(self) -> Punkt:
        """
        Getter-Methode gibt die aktuelle Position des Fahrzeugs zurück.

        Returns:
            Punkt: Ein Punkt-Objekt, das die aktuelle X- und Y-Koordinate des Fahrzeugs darstellt.
        """
        return self.Position
    
    def get_Geswindigkeit(self) -> float:
        """
        Getter-Methode gibt die aktuelle Geschwindigkeit des Fahrzeugs zurück.

        Returns:
            float: Die aktuelle Geschwindigkeit des Fahrzeugs.
        """
        return self.Geschwindigkeit
    
    def __str__(self):
        """
        Methode gibt eine String-Repräsentation der Position des Fahrzeugs zurück.
        """
        return self.Position
    
    def set_new_Point(self, punkt: Punkt):
        """
        Setter-Methode setzt eine neue Position für das Fahrzeug.

        Args:
            punkt (Punkt): Das neue Punkt-Objekt, das die Position des Fahrzeugs darstellen soll.
        """
        self.Position = punkt

    def berechnen_next_Point(self, vektor: tuple[float],lange : float) -> Punkt:
        """
        Methode berechnet den nächsten Punkt, zu dem sich das Fahrzeug bewegen würde,
        basierend auf einem gegebenen Vektor, dessen Länge und der Geschwindigkeit des Fahrzeugs.

        Args:
            vektor (tuple[float]): Der Richtungsvektor der Bewegung (delta_x, delta_y).
            lange (float): Die Länge (Betrag) des Vektors.

        Returns:
            Punkt: Ein neues Punkt-Objekt, das den potenziellen nächsten Standort des Fahrzeugs darstellt.
        """
        alpha = self.berechnen_Einheit(vektor, lange, self.Geschwindigkeit)
        new_x = self.Position.get_X() + alpha[0]
        new_y = self.Position.get_Y() + alpha[1]
        return Punkt(new_x,new_y)
    
    def berechnen_Einheit(self,vektor : tuple[float], lange : float, Abstand : float) -> tuple[float]:
        """
        Methode berechnet die Komponenten eines Vektors, der die Bewegung in einer bestimmten Länge
        entlang eines gegebenen Richtungsvektors darstellt.

        Args:
            vektor (tuple[float]): Der ursprüngliche Richtungsvektor (delta_x, delta_y).
            lange (float): Die Länge (Betrag) des ursprünglichen Vektors.
            Abstand (float): Die gewünschte Länge des resultierenden Bewegungsvektors (z.B. Geschwindigkeit).

        Returns:
            tuple[float]: Ein Tupel (bewegter_delta_x, bewegter_delta_y), das den
                          Bewegungsvektor für den gegebenen Abstand darstellt.
        """   
        return (Abstand*vektor[0]/lange, Abstand*vektor[1]/lange)
    
    def berechnen_Point(self,anfang: Punkt, vektor: tuple[float], lange : float, rest :float):
        """
        Methode berechnet und setzt die neue Position des Fahrzeugs, wenn es einen Teil
        einer Strecke bereits zurückgelegt hat.

        Args:
            anfang (Punkt): Der Startpunkt der aktuellen Strecke.
            vektor (tuple[float]): Der Richtungsvektor der aktuellen Strecke.
            lange (float): Die Gesamtlänge der aktuellen Strecke.
            rest (float): Der bereits zurückgelegte Weg auf der letzten Strecke in diesem Simulationsschritt.
        """
        alpha = self.berechnen_Einheit(vektor,lange, self.Geschwindigkeit-rest)
        new_x = anfang.get_X() + alpha[0]
        new_y = anfang.get_Y() + alpha[1]
        self.Position = Punkt(new_x,new_y) 


class Strasse:
    """
    Diese Klasse repräsentiert eine Straße im Verkehrsnetz.
    """
    def __init__(self,Anfang : Punkt,Ziel: Punkt ):
        """
        Konstruktor Initialisiert eine neue Instanz der Strasse-Klasse.

        Args:
            Anfang (Punkt): Der Startpunkt der Straße.
            Ziel (Punkt): Der Endpunkt der Straße.
        """
        self.Anfang : Punkt = Anfang
        self.Ziel : Punkt = Ziel
        self.Vektor: tuple[float] = Anfang.berechnen_Vektor(Ziel)
        self.Length: float =  Anfang.get_Abstand(Ziel)
        self.Fahrzeugen: List[Fahrzeug] = []
        self.Max: float = 0
        self.Gesamt: float = 0
        """
        Erweiterung:
        #Erweiterung 4 - Die Geschwindigkeit ist abhängig von den Streckenabschnitten:
        Ein Attribut für die Geschwindigkeit kann auch definiert werden.=> Fahrzeug Geschwindigkeit ist abhängig von der Straße
        
        #Erweiterung 3 - Es gibt Strecken mit mehreren Fahrbahnen pro Richtung:
        Es gibt viele Felder in Fahrzuegen-Attribut => Viele Fahrbahnen

        #Erweiterung 1 - Mindestand zum vorausfahrenden Fahrzeug einhalten:
        Ein Attribut für das minimale Abstand zwischen 2 Fahrzuegen, das auch in Methode Check_Fahrzeug() geschickt wird.

        """

    """
    #Erweiterung 1 - Mindestand zum vorausfahrenden Fahrzeug einhalten:
    Entwickeln eine Methode, die Fahrzeug mithilfe die Positionvergleich-Methode der Punkt-Klasse in der Straße zu sortieren
    Entwickeln eine Setter-Methode, die neue Geschwindigkeit und Position einsetzt.
    """
    def get_Anfang(self) -> Punkt:
        """
        Getter-Methode gibt den Startpunkt der Straße zurück.

        Returns:
            Punkt: Das Punkt-Objekt, das den Anfang der Straße darstellt.
        """
        return self.Anfang
    
    def get_Fahrzeugen(self) -> List[Fahrzeug]:
        """
        Getter-Methode gibt die Liste der Fahrzeuge zurück, die sich derzeit auf dieser Straße befinden.

        Returns:
            List[Fahrzeug]: Eine Liste von Fahrzeug-Objekten.
        """
        return self.Fahrzeugen
    
    def get_Length(self) -> float:
        """
        Getter-Methode gibt die Länge der Straße zurück.

        Returns:
            float: Die Länge der Straße.
        """
        return self.Length
    
    def get_Vektor(self) -> tuple[float]:
        """
        Getter-Methode gibt den Richtungsvektor der Straße zurück.

        Returns:
            tuple[float]: Ein Tupel (delta_x, delta_y), das den Vektor darstellt.
        """
        return self.Vektor
    
    def get_Ziel(self) -> Punkt:
        """
        Getter-Methode gibt den Endpunkt der Straße zurück.

        Returns:
            Punkt: Das Punkt-Objekt, das das Ende der Straße darstellt.
        """
        return self.Ziel
    
    def add_Fahrzeug(self, newCar : Fahrzeug):
        """
        Methode fügt ein neues Fahrzeug zu dieser Straße hinzu.

        Args:
            newCar (Fahrzeug): Das Fahrzeug-Objekt, das hinzugefügt werden soll.
        """
        self.Fahrzeugen.append(newCar)
        self.Gesamt+=len(self.Fahrzeugen)
        if len(self.Fahrzeugen )> self.Max:
            self.Max = len(self.Fahrzeugen)
    
    def check_Fahrzeug(self):
        """
        Methode überprüft die Position aller Fahrzeuge auf dieser Straße und aktualisiert sie.
        """
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
        """
         #Erweiterung 4 - Die Geschwindigkeit ist abhängig von den Streckenabschnitten:
         Die Attribut Geschwindigkeit kann in der neue Methode findende Methode geschickt
        """
    
    def get_Statistik(self) -> tuple[float]:
        """
        Methode gibt statistische Daten über die Straße zurück.

        Returns:
            tuple[float]: Ein Tupel, das (Gesamtzahl der Fahrzeuge, Maximale Anzahl der Fahrzeuge, Länge der Straße) enthält.
        """
        return (self.Gesamt, self.Max, self.Length)

    def get_Point(self) -> str:
        """
        Methode gibt eine String-Repräsentation der Koordinaten des Anfangs- und Endpunkts
        der Straße zurück.

        Returns:
            str: Ein String im Format "AnfangX AnfangY ZielX ZielY".
        """
        return f"{round(self.Anfang.get_X(),1)} {round(self.Anfang.get_Y(),1)} {round(self.Ziel.get_X(),1)} {round(self.Ziel.get_Y(),1)}"

    def __str__(self):
        """
        Methode gibt eine String-Repräsentation der Straße zurück

        Returns:
            str: Eine String-Repräsentation der Straße im Format "Anfangspunkt-->Zielpunkt".
        """
        return f"{self.Anfang}-->{self.Ziel}"



class EinfallsPunkt(Punkt):
    """
    Diese Klasse repräsentiert einen EinfallsPunkt (Entry Point) in das Verkehrsnetz.
    Er erbt von der 'Punkt'-Klasse 
    """
    def __init__(self,x : float,y: float,name : str,Takt : int,Ziel : str):
        """
        Konstruktor initialisiert eine neue Instanz des EinfallsPunktes.

        Args:
            x (float): Die X-Koordinate des EinfallsPunktes.
            y (float): Die Y-Koordinate des EinfallsPunktes.
            name (str): Der Name des EinfallsPunktes.
            Takt (int): Die Taktfrequenz, mit der Fahrzeuge an diesem Punkt generiert werden (z.B. alle 'Takt' Simulationsschritte).
            Ziel (str): Der Name des Ziels (Kreuzung oder Einfallspunkt), zu dem Fahrzeuge von diesem Punkt aus fahren sollen.
        """
        super().__init__(x,y,name)
        self.Takt : int = Takt
        self.Ziel : str= Ziel
        self.Strasse : Strasse= None

    def __str__(self):
        """
        Methode gibt eine String-Repräsentation des EinfallsPunktes zurück.

        Returns:
            str: Der Name des EinfallsPunktes.
        """
        return self.name
    
    def set_Strasse(self, strasse : Strasse):
        """
        Setter-Methode setzt die Straße, die von diesem EinfallsPunkt ausgeht.

        Args:
            strasse (Strasse): Das Strasse-Objekt, das mit diesem EinfallsPunkt verbunden ist.
        """
        self.Strasse = strasse
    
    def get_Strasse(self) -> Strasse:
        """
        Getter-Methode gibt die Straße zurück, die von diesem EinfallsPunkt ausgeht.

        Returns:
            Strasse: Das Strasse-Objekt, das mit diesem EinfallsPunkt verbunden ist.
        """
        return self.Strasse

    def get_Ziel(self) -> Punkt:
        """
        Getter-Methode gibt den Namen des Ziels zurück

        Returns:
            str: Der Name des Zielpunktes.
        """
        return self.Ziel
    
    def get_Takt(self) -> int:
        """
        Getter-Methode gibt die Takt zurück, mit der Fahrzeuge an diesem Punkt generiert werden.

        Returns:
            int: Die Taktfrequenz.
        """
        return self.Takt

class Kreuzung(Punkt):
    """
    Diese Klasse repräsentiert eine Kreuzung im Verkehrsnetz.
    Sie erbt von der 'Punkt'-Klasse.
    """
    def __init__(self,x : float, y : float,name : str,Ziele : List[str],Anteile: List[float]):
        """
        Konstruktor initialisiert eine neue Instanz der Kreuzung-Klasse.

        Args:
            x (float): Die X-Koordinate der Kreuzung.
            y (float): Die Y-Koordinate der Kreuzung.
            name (str): Der Name der Kreuzung.
            Ziele (List[str]): Eine Liste von Namen der Zielpunkte (andere Kreuzungen oder Einfallspunkte),
                                die von dieser Kreuzung aus erreichbar sind.
            Anteile (List[float]): Eine Liste von Wahrscheinlichkeiten (Anteilen), die angeben,
                                   wie wahrscheinlich ein Fahrzeug jedes der 'Ziele' wählt.
        """
        super().__init__(x,y, name)
        self.Ziele : List[str]= Ziele
        self.Anteile : List[float] = Anteile
        self.Strassen : List[Strasse] = []

        """
        #Erweiterung 2: Der Vekehrfluss ans den Kreuzungen wird geregel:
        Die Straßen-Feld kann in 2 Felder unterteilen, die ein Paare der Straße mit der umgekehrten Richtung enthaelt.
        Das Attribut für Ampeln wird in der Klasse Kreuzung definiert. 
        Der Wert dieses Attributs wird im bestimmten Zeitpunkt umgekehrt geändert.
        Für jeden Wert des Ampel-Attributs können nur die Fahrzeuge in den Straßen auf einem ausgewiesenen Feld bewegen
        """
    
    def get_Strassen(self):
        """
        Getter-Methode gibt die Liste der Straßen zurück, die von dieser Kreuzung ausgehen.

        Returns:
            List[Strasse]: Eine Liste von Strasse-Objekten.
        """
        return self.Strassen
    
    def add_Strassen(self,strasse: Strasse):
        """
        Setter-Methode fügt der Kreuzung eine ausgehende Straße hinzu.

        Args:
            strasse (Strasse): Das Strasse-Objekt, das von dieser Kreuzung ausgeht.
        """
        self.Strassen.append(strasse)

    def get_Ziele(self) -> Punkt:
        """
        Getter-Methode gibt die Liste der Namen der erreichbaren Ziele von dieser Kreuzung zurück.

        Returns:
            List[str]: Eine Liste von String-Namen der Ziele.
        """
        return self.Ziele

    def waehlen_naechsten_Ziel(self,letzteAnfang : Punkt) -> Strasse:
        """
        Methode wählt zufällig die nächste Straße aus, die ein Fahrzeug von dieser Kreuzung nehmen wird.
        Args:
            letzteAnfang (str): Der Name des Anfangspunkts der vorherigen Straße.

        Returns:
            Strasse: Das ausgewählte Strasse-Objekt, das die nächste Route für das Fahrzeug darstellt.
        """
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
        """
        Methode gibt eine String-Repräsentation der Kreuzung zurück.

        Returns:
            str: Der Name der Kreuzung.
        """
        return self.name
    

class Netze:
    """
    Diese Klasse repräsentiert das gesamte Verkehrsnetz, bestehend aus
    Einfallspunkten und Kreuzungen.
    """
    def __init__(self, Einfallspunkte:List[EinfallsPunkt], Kreuzugen: List[Kreuzung]):
        """
        Konstruktor initialisiert eine neue Instanz der Netze-Klasse.

        Args:
            Einfallspunkte (List[EinfallsPunkt]): Eine Liste aller EinfallsPunkt-Objekte im Netz.
            Kreuzugen (List[Kreuzung]): Eine Liste aller Kreuzung-Objekte im Netz.
        """
        self.Einfallspunkte : List[EinfallsPunkt] = Einfallspunkte
        self.Kreuzungen : List[Kreuzung] = Kreuzugen
        self.Zahl : int= 0
        self.finden_Strassen()

    
    def finden_Strassen(self):
        """
        Methode durchsucht alle Einfallspunkte und Kreuzungen, um die
        zugehörigen Straßen im Netz zu erstellen.

        Error:
        StrassenichtVorhandenError, wenn ein Zielpunkt nicht gefunden wird.
        """
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
        """
        Methode sucht und gibt ein Punkt-Objekt (EinfallsPunkt oder Kreuzung) anhand seines Namens zurück.

        Args:
            name (str): Der Name des gesuchten Punktes.

        Returns:
            Punkt: Das gefundene Punkt-Objekt oder None, wenn kein Punkt mit dem gegebenen Namen existiert.
        """
        for ep in self.Einfallspunkte:
            if(ep.get_Name() == name):
                return ep
        
        for kp in self.Kreuzungen:
            if (kp.get_Name() == name):
                return kp
            
        return None
    
    def get_alle_Strassen(self) -> List[Strasse]:
        """
        Methode sammelt und gibt eine Liste aller Straßen im gesamten Netz zurück.

        Returns:
            List[Strasse]: Eine Liste aller Strasse-Objekte im Netz.
        """
        erg = []
        for ep in self.Einfallspunkte:
            erg.append(ep.get_Strasse())
        for kp in self.Kreuzungen:
            Strassen = kp.get_Strassen()
            for strasse in Strassen:
                erg.append(strasse)
        return erg
    
    def Simulieren(self,ZeitPunkt: int):
        """
        Methode führt einen Simulationsschritt für das gesamte Verkehrsnetz durch.

        Args:
            ZeitPunkt (int): Der aktuelle Zeitpunkt der Simulation.
        """
        for ep in self.Einfallspunkte:
            s = ep.get_Strasse()
            s.check_Fahrzeug()
            Takt = ep.get_Takt()
            if (ZeitPunkt != 0) and (ZeitPunkt % Takt == 0):
                newCar = Fahrzeug(ep,self.Zahl)
                s.add_Fahrzeug(newCar)
                self.Zahl += 1
            
        for kp in self.Kreuzungen:
            s = kp.get_Strassen()
            for t in s:
                t.check_Fahrzeug()


