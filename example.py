# (c) 2026 Bastian Flügel. All rights reserved.
# example.py - Das Zen-Meisterstück

from core.app import App
from components.layout import VStack, HStack, Spacer, Box
from components.widgets import Label, Button

def startup(app):
    (app.window()
        .title("AnthroEditor")
        .size(700, 500)
        .make_noble(level="subtle", intensity=1.0)
        .on_close(app.stop)
        .content(
            VStack(padding=60, spacing=30).content( # Haupt-Container

                # 1. Header Bereich
                VStack(spacing=5).content(
                    Label("AnthroEditor")
                        .font(size=48, weight="bold")
                        .color("primary"),
                    Label("Erstelle Großartiges in absoluter Stille.")
                        .font(size=16)
                        .color("secondary"),
                ),
                
                Spacer(),
                
                # 2. Aktions-Bereich in einer edlen Box
                # Wir nutzen jetzt einen HEX-Code für ein tiefes Anthrazit
                Box(padding=25)
                    .background("#1A1A1A", alpha=0.4) 
                    .corner_radius(16)
                    .content(
                        VStack(spacing=15).content(
                            Label("Projekt-Steuerung").font(size=12, weight="bold").color("secondary"),
                            HStack(spacing=12).content(
                                Button("Optionen").width(120),
                                Button("Projekt Starten").width(160).primary(),
                                Button("Exit").width(80).action(app.stop)
                            )
                        )
                    )
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