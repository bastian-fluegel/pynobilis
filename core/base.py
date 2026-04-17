# (c) 2024 Bastian Flügel. All rights reserved.
# core/base.py
import uuid
import logging

# Setup eines Framework-weiten Loggers
logger = logging.getLogger("pynobilis")

class NobilisBase:
    """Die architektonische Basis für alle pynobilis Komponenten."""
    
    _is_licensed = False  # Globaler Lizenzstatus

    def __init__(self):
        self._id = uuid.uuid4()
        self._log = logger.getChild(self.__class__.__name__)
        self._log.debug(f"Instanz initialisiert: {self._id}")

    @classmethod
    def set_license_key(cls, key: str):
        """
        Validiert den Lizenzschlüssel.
        Wenn gültig, wird das Wasserzeichen deaktiviert.
        """
        # Hier käme die Validierungslogik rein
        if key == "ADMIN-PRO-2024": # Beispiel-Validierung
            cls._is_licensed = True
            logger.info("Kommerzielle Lizenz aktiviert. Wasserzeichen entfernt.")
        else:
            cls._is_licensed = False
            logger.warning("Ungültiger Lizenzschlüssel.")

    @property
    def needs_watermark(self) -> bool:
        """Gibt an, ob ein Wasserzeichen gerendert werden muss."""
        return not self._is_licensed