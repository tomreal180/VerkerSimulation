class FormatError(RuntimeError):
   """
   Diese benutzerdefinierte Fehlerklasse wird ausgelöst, wenn ein Problem mit dem
   Format der Eingabedatei erkannt wird. 
   """
   pass

class StrassenichtVorhandenError(RuntimeError):
   """
    Diese benutzerdefinierte Fehlerklasse wird ausgelöst, wenn eine Referenz auf
    eine Straße gemacht wird, die im simulierten Netz nicht existiert oder nicht gefunden wurde.
    """
   pass

class EingabedateinichtVorhandenError(RuntimeError):
    """
    Diese benutzerdefinierte Fehlerklasse wird ausgelöst, wenn die angegebene
    Eingabedatei nicht gefunden werden kann.
    """
    pass

class UngultigEingabeError(RuntimeError):
    """
    Diese benutzerdefinierte Fehlerklasse wird ausgelöst, wenn Daten in der
    Eingabedatei zwar vorhanden sind, aber inhaltlich ungültig sind.
    """
    pass
