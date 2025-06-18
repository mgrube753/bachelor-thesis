# Überblick der Experimente

## Experiment 1a (`exp1a.csv`)

-   **Quelle:** Originalinhalte (TXT) aus drei verschiedenen Quellen zum Thema ISO-OSI-Modell
-   **Generiert:** Fragen wurden aus unverändertem Material erstellt
-   **Material:**
    -   `script`: Extrahierte Texte aus Prof. Caps Vorlesung "Referenzarchitekturen"
    -   `transcript`: Audio-Text-Fassung der Vorlesung
    -   `tanenbaum`: Auszüge aus "Computer Networks" von Andrew S. Tanenbaum

## Experiment 1b (`exp1b.csv`)

-   **Quelle:** Manipulierte Inhalte (TXT)
-   **Generiert:** Fragen wurden aus absichtlich verfälschten Texten erstellt
-   **Material:**
    -   `script (manipulated)`: Bewusst manipulierte Vorlesungstexte

---

## Anleitung für Experten

### Schritt 1: Verständnis der Bewertungskriterien

Lesen Sie Subexperiment-spezifischen Rubriken:

-   `exp1a_rubric.md`:
-   `exp1b_rubric.md`:

### Schritt 2: Verständnis der CSV-Struktur

Die `exp1a.csv` und `exp1b.csv` enthalten:

-   `input_source`: Die Quelle des Textes, aus dem die Frage generiert wurde (z.B. `script`, `transcript`, `tanenbaum`, `script_manipulated`).
-   `layer`: Der jeweilige Schichttext, aus der die Frage generiert wurde.
-   Die 5 Kategorien zur Bewertung von 0-10
-   Anhand der CSV-Dateien können Sie die Fragen und deren Quellen nachvollziehen, um diese Zeile für Zeile zu bewerten.
-   Deswegen sind die Dateien der einzelnen Fragen nummeriert, mit der `input_source` und der `layer`-Nummer versehen, um die Zuordnung zu erleichtern.
-   Wenn Sie Frage 1 bewerten, muss das Ergebnis in Zeile 2 der CSV-Datei eingetragen werden, da die erste Zeile den Header enthält, usw. für die weiteren Fragen.

### Schritt 2: Bewertung von Experiment 1a

1. Öffnen Sie `exp1a.csv`.
2. Für jede Zeile:
    - Schauen Sie sich die entsprechende Frage in `questions/exp1a/` an.
    - Prüfen Sie den zur Fragengenerierung genutzten Quelltext in `source/[input_source]/layer[X].txt`.
    - Bewerten Sie nach den 5 Kategorien der Rubrik `exp1a_rubric.md`

### Schritt 3: Bewertung von Experiment 1b

1. Öffnen Sie `exp1b.csv`.
2. Für jede Zeile mit `script_manipulated`:
    - Schauen Sie sich die Frage in `questions/exp1b/` an.
    - Vergleichen Sie mit dem manipulierten Text in `source/script_manipulated/layer[X].txt`.
    - Bewerten Sie nach den 5 Kategorien der Rubrik `exp1b_rubric.md`, wobei die `Correctness`-Bewertung für dieses Subexperiment das Hauptaugenmerk ist

### Schritt 4: Dokumentation

Tragen Sie Ihre Bewertungen (0-10) in die jeweiligen CSV-Spalten ein:

-   `relevance`
-   `clarity`
-   `answerability`
-   `challenging`
-   `correctness`

---

## Ziel der Auswertung

Das Experiment testet die Qualität von LLM-generierten Fragen und deren Fähigkeit, sich an gegebene Quellinhalte zu halten. Als Sonderfall wird im Experiment 1b getestet, ob die Modelle in der Lage sind, Manipulationen zu erkennen, oder ob diese straight-forward für die Fragengenerierung genutzt werden.
