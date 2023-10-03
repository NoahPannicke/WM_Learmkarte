# StadtKlang Learmkarte
Abgabeleistung Modul Wissensmanagement Sommersemester 2023 
Noah Pannicke (584166)
Adem Korkutan (571303)
Nele Sophie Engel (584172)


Eine detaillierte Dokumentation der Skripte und des Projekts erfolgt in einem seperaten Dokument.
Im Nachfolgenden soll lediglich auf die Verwendung der Skripte und dem Inhalt des Repositories eingegangen werden.

# Daten
Alle im Projekt verwendeten Daten sind im Repository abgelegt.
Die Shapefiles, welche zur Redution der Größe als .zip Dateien abgelegt sind, werden innerhalb der Skripte direkt von der ODIS-Berlin (https://daten.odis-berlin.de/) abgerufen.
Die dB-Beispieldaten sind als .csv Dateien im Repository abgelegt und werden aus ebenjenen eingeladen. Die Beispieldaten für die Berliner Straßen werden aufgrund des Umfangs im entsprechenden Skript erzeugt.

# Skripte
Zur Erstellung der Lärmkarte muss das Skript __app_laermkarte.py__ ausgeführt werden.
In diesem Skript befindet sich die Flask-App, welche direkt in der IDE oder durch Ausführung des 'python -m flask --app .\app_test.py run' Befehls, ausgeführt werden kann.

![image](https://github.com/NoahPannicke/WM_Learmkarte/assets/50919321/bd9289f5-44e7-4957-8470-d163d8fbfeba)

Innerhalb der geöffneten Website (obige Darstellung) lässt sich eine Uhrzeit oder ein Zeitraum eingeben, zu welchem eine Lärmkarte erstellt werden soll. Das Format muss entweder 00:00 oder 00:00-00:00 entsprechen. Falls keine Uhrzeit eingegeben wird, erfolgt die Darstellung der aktuellen dB-Werte.

![image](https://github.com/NoahPannicke/WM_Learmkarte/assets/50919321/ce8e9e1d-bcf0-4e9a-897c-01a0c9b6100d)

Die mittels Folium erzeugten Lärmkarten umfassen die Funktionalität der Darstellungsänderung mit verschiedenen Hintergründen, als auch die Anpassung der überlagernden Shapefiles, wodurch die Darstellung von Postleizahlen, lebensweltlich orientierte Räume als auch Straßen möglich ist. Alle Einstelungen können über den Reiter in der rechten oberen Ecke getätigt werden.
Weiterhin existiert eine Mouse-over Funktionalität, welche es ermöglicht für jedes Gebiet den entsprechenden Namen sowie den konkreten dB-Wert zu erhalten.

https://github.com/NoahPannicke/WM_Learmkarte/assets/50919321/4b4be8c5-6338-4bbe-9eed-b84e76b30a96

Unabhängig von der Live-Karte lässt sich eine historisierte Lärmkarte erstellen, welche die durchschnittliche dB-Entwicklung der vergangenen Tage abbildet. Durch einen Slider in der linken oberen Ecke lässt sich der Tag anpassen.

Alle Funktionalitäten der Karte, sowie die Karten an sich, werden im Skript __functions_laermkarte.py__ definiert. Die Funktionen werden bei Erzeugung der App aufgerufen.

Das Design der Website erfolgt im Skript __laermkarte.html__.

Für die reine Verwendung der Karte muss lediglich die __app_laermkarte.py__ verwendet werden. Die weiteren Skripte oder Dateien im Repository werden entweder automatisiert aufgerufen oder wurden lediglich zu Dokumentationszwecken abgelegt. 

# Pakete
Folgende Pakete müssen installiert sein (aktuellste Version, keine fehlerhaften Abhängigkeiten):
- Folium
- Flask
- Plotly
- Pandas
- Geopandas
- Numpy
- Shapely
- Datetime
- Time
- Serial
- Branca
