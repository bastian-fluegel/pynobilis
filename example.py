# (c) 2024 Bastian Flügel. All rights reserved.
# example.py
from core.app import App
from components.window import Window

def main():
    app = App()
    
    # Dieses Fenster wird nun faktisch zum "Root", 
    # da es das einzige ist.
    win = Window()
    
    print("System started. Admin presence active.")
    app.run()

if __name__ == "__main__":
    main()