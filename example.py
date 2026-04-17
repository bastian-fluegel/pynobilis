# example.py
from core.app import App
from components.window import Window

def startup():
    """Diese Funktion wird erst aufgerufen, wenn im Splash OK geklickt wurde."""
    print("Lade Haupt-App-Komponenten...")
    win = Window(title="Mein nobles Hauptfenster", posX=200, posY=200, width=800, height=600)
    # Hier könnten weitere UI Elemente geladen werden

def main():
    app = App()
    
    # Wir übergeben die 'startup' Funktion. 
    # WICHTIG: Nur 'startup' schreiben, nicht 'startup()' (wir rufen sie noch nicht auf!)
    app.run(startup_callback=startup)

if __name__ == "__main__":
    main()