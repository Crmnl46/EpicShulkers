# Sales Agreement Management Application

Eine moderne Python-Anwendung zur Verwaltung von Verkaufsvereinbarungen (Verkaufsverträge für Elektronikgeräte).

## ✨ Funktionen

### Hauptfunktionen
- **Verkaufsvereinbarungen verwalten** mit 4-stelligen KV-Nummern (z.B. KV1234)
- **Automatische Datumsangabe** (aktuelles Datum vorausgefüllt, aber editierbar)
- **Kundendaten sammeln**: Vor-/Nachname, Adresse, Geburtsdatum, Ausweisart, Ausweisnummer
- **Ausweis-Scan Funktion** mit automatischer Bildintegration
- **Elektronikgeräte-Daten**: Marke, Typ, Preis (€), Seriennummer/IMEI, Sicherheitscode
- **Automatische Standardanmerkung** zur rechtlichen Bestätigung

### Export & Übersichten
- **PDF-Export** für einzelne Verkaufsvereinbarungen
- **CSV-Export** für alle Vereinbarungen oder gefilterte Übersichten
- **Monats- und Jahresübersichten** mit Exportmöglichkeit
- **Suchfunktion** nach KV-Nummer
- **Lokale Speicherung** aller Daten

## 🎨 Design

- **Hellblaue Schrift** auf weißem Hintergrund
- **Grüne Farben** für "Ja"/Bestätigungen 
- **Rote Farben** für "Nein"/Abbruch
- **Moderne und benutzerfreundliche** Oberfläche mit Tabs

## 📋 Installation

### Voraussetzungen
- Python 3.12+ (entwickelt für 3.13)
- tkinter für GUI (normalerweise mit Python vorinstalliert)

### Setup
1. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

2. Für GUI-Umgebungen:
   ```bash
   sudo apt-get install python3-tk  # Ubuntu/Debian
   ```

## 🚀 Ausführung

### GUI-Modus (empfohlen)
```bash
python3 sales_agreement_app.py
```

### CLI-Modus (für Headless-Umgebungen)
```bash
python3 launcher.py
```

### Tests ausführen
```bash
python3 test_sales_app.py
```

## 📁 Dateien

- `sales_agreement_app.py` - Hauptanwendung mit GUI
- `launcher.py` - CLI-Interface und Launcher
- `test_sales_app.py` - Testschuite für alle Funktionen
- `requirements.txt` - Python-Abhängigkeiten
- `sales_agreements.json` - Datenspeicher (wird automatisch erstellt)

## 🔧 Verwendung

### Neue Verkaufsvereinbarung erstellen
1. KV-Nummer eingeben (4 Ziffern, wird automatisch mit "KV" prefixiert)
2. Datum prüfen/anpassen
3. Kundendaten im ersten Tab eingeben
4. Elektronikgeräte-Daten im zweiten Tab eingeben
5. Optional: Ausweis-Bild scannen/hochladen
6. "Speichern" klicken

### Übersichten und Export
- **Menü → Datei → Monatsübersicht/Jahresübersicht**
- **Menü → Datei → Als CSV exportieren**
- **Menü → Datei → Als PDF speichern**

### Suche
- **Menü → Suchen → Nach KV-Nummer suchen**

## 📊 Datenformat

Alle Daten werden in JSON-Format gespeichert mit folgender Struktur:
```json
{
  "id": "eindeutige-uuid",
  "kv_number": "KV1234",
  "date": "12.09.2025",
  "customer": {
    "first_name": "Max",
    "last_name": "Mustermann",
    "address": "Straße 1\n12345 Stadt",
    "birth_date": "01.01.1990",
    "id_type": "Personalausweis",
    "id_number": "DE123456789"
  },
  "electronics": {
    "brand": "Apple",
    "model": "iPhone 15",
    "price": "800",
    "serial": "ABC123456789",
    "security_code": "1234",
    "notes": "Zusätzliche Anmerkungen"
  },
  "image_path": "pfad/zum/ausweis-bild.jpg",
  "created_at": "2025-09-12T09:07:02"
}
```

## 🛡️ Rechtliche Bestätigung

Jede Verkaufsvereinbarung enthält automatisch folgende Standardanmerkung:

> "Der Verkäufer versichert dem Käufer, dass die oben bezeichneten Geräte rechtmäßig erworben worden sind und nicht gestohlen wurden, und dem Verkäufer die Herkunft der Geräte bekannt sind."

## 📝 Lizenz

MIT License - siehe LICENSE Datei für Details.