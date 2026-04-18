# (c) 2026 Bastian Flügel. All rights reserved.
# example.py - Das Zen-Meisterstück

from core.app import App
from components.layout import VStack, HStack, Spacer
from components.widgets import Label, Button

def startup(app):
    """
    Diese Funktion wird aufgerufen, sobald der Splash-Screen bestätigt wurde.
    Sie dient als Konstruktor für das eigentliche User-Interface.
    """
    
    # 1. Hauptfenster definieren
    # .window() gibt das Window-Objekt zurück
    # .content() füllt es mit dem Root-Layout
    app.window(title="AnthroEditor", size=(700, 500)).content(
        
        # 2. Das Root-Layout (Vertikaler Stapel)
        VStack(padding=60, spacing=20).children(
            
            # Ein großes, edles Label (Headline)
            Label("AnthroEditor")
                .font(size=48, weight="bold")
                .color("primary"),
            
            # Ein dezenter Untertitel
            Label("Erstelle Großartiges in absoluter Stille.")
                .font(size=16)
                .color("secondary"),
            
            # Ein Spacer drückt die Buttons nach unten
            Spacer(),
            
            # 3. Eine horizontale Reihe für die Interaktion
            HStack(spacing=12).children(
                
                Button("Einstellungen")
                    .width(140)
                    .action(lambda: print("Öffne Settings...")),
                
                Button("Projekt Starten")
                    .width(160)
                    .primary()  # Markiert dies als Hauptaktion (Enter-Taste)
                    .action(lambda: print("Lade Editor...")),
                
                # Der Beenden-Button nutzt direkt die Methode der App-Klasse
                Button("Exit")
                    .width(80)
                    .action(app.stop)
            )
        )
    )

def main():
    # Erstellt die App-Instanz mit deinem Branding
    app = App(name="AnthroEditor")
    
    # Startet den Lifecycle:
    # 1. Zeigt den Splash-Screen
    # 2. Wartet auf "Start App"
    # 3. Führt startup(app) aus
    # 4. Zeigt das Hauptfenster
    app.run(startup_callback=startup)

if __name__ == "__main__":
    main()