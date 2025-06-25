# Überblick der Experimente -- Malte Grube

Dieses Experiment (bestehend aus 1a und 1b) testet die Qualität von automatisiert-generierten Fragen durch vier Large Language Models und deren Fähigkeit, sich an diverse gegebene Quellinhalte zu halten. Dabei wurden zwei verschiedene Prompts verwendet, mit denen die Modelle Fragen generieren sollten. Details zu diesen Prompts werden aufgrund des Blindtests nicht gegeben.

Als Sonderfall wird in Experiment 1b getestet, ob die Modelle in der Lage sind, Manipulationen im Text zu erkennen, oder ob genau diese straight-forward für die Fragengenerierung genutzt werden. Manipulation beschreibt hier, dass gewisse Informationen im Text bewusst verfälscht wurden, um zu prüfen, ob die Modelle diese erkennen und entsprechend Fragen generieren können.

Es folgen die Beschreibungen der beiden Subexperimente, welche Materialien genutzt und welche zusätzlich manipuliert wurden, sowie eine Anleitung, wie Sie die Bewertungen vornehmen können.

## Experiment 1a (`exp1a.csv`)

Es wurden folgende Materialien genutzt, um Fragen bei Experiment 1a zu generieren:

-   **Eingabequelle:** Originalinhalte aus drei verschiedenen Quellen zum Thema ISO-OSI-Modell
-   **Generiert:** Fragen wurden aus folgenden Materialien jeweils erstellt
-   **Material:**
    -   `script`: Extrahierte Textauszüge von Prof. Caps Vorlesungs-PDF "Referenzarchitekturen"
    -   `transcript`: Audio-Text-Fassung (TXT) dieser Vorlesung, von Doritt Linke bereitgestellt
    -   `tanenbaum`: Auszüge aus der "Computer Networks"-PDF von Andrew S. Tanenbaum, bspw. [hier](https://csc-knu.github.io/sys-prog/books/Andrew%20S.%20Tanenbaum%20-%20Computer%20Networks.pdf) einsehbar

Die Materialien wurden von mir extrahiert und aufbereitet durch

- Auteilen der Layer in einzelne TXT-Files und
- gegebenenfalls Kürzung,

sodass sie eine angemessene Länge für die Fragengenerierung haben.

## Experiment 1b (`exp1b.csv`)

Dieses Subexperiment, welches auf Experiment 1a aufbaut, fokussiert sich auf die Manipulation einer Inhaltsquelle.

-   **Eingabequelle:** Manipulierte Inhalte (TXT)
-   **Generiert:** Fragen wurden aus absichtlich verfälschten Texten erstellt
-   **Material:**
    -   `script (manipulated)`: Extrahierte Textauszüge von Prof. Caps Vorlesungs-PDF "Referenzarchitekturen", jedoch manipuliert

Die Layer-Dateien, basierend auf den Vorlesungsfolien, wurden durch einmaliges LLM-Prompting so verändert, dass sie inhaltlich keinen Sinn mehr ergeben, aber dennoch die stichpunktartige Struktur des Vorlesungstextes beibehalten.

Durch diese Manipulation wird getestet, ob die Modelle in der Lage sind, die Unstimmigkeiten gegenüber dem ISO-OSI-Modell zu erkennen, oder ob sie diese Informationen für die Fragengenerierung nutzen.

## Anleitung für Experten

### Schritt 1: Verständnis der Bewertungskriterien

Lesen Sie Subexperiment-spezifischen Rubriken:

-   `exp1a_rubric.md`
-   `exp1b_rubric.md`

Diese unterscheiden sich in den Bewertungskriterien innerhalb der letzten Kategorie jedes Subexperiments. Im ersten Subexperiment (1a) wird die **Korrektheit** der Fragen bewertet, während im zweiten Subexperiment (1b) der **Umgang mit Manipulation** im Fokus steht.

### Schritt 2: Verständnis der CSV-Struktur

Die `exp1a.csv` und `exp1b.csv` enthalten:

-   `input_source`: Die Quelle des Textes, aus dem die Frage generiert wurde (z.B. `script`, `transcript`, `tanenbaum`, `script_manipulated`).
-   `layer`: Der jeweilige Schichttext, aus der die Frage generiert wurde.
-   Die jeweiligen 5 Kategorien zur Bewertung von 0-10
-   Eine `comments`-Spalte für Ihre Anmerkungen. Dies könnten beispielsweise Indizien sein, wie: Die Frage ist ein Ankerbeispiel für eine bestimmte Kategorie, sodass diese auffällig gut oder schlecht abschneidet, oder auch, dass die Frage nicht beantwortbar ist, weil sie zu unklar formuliert ist.

Anhand der CSV-Dateien können Sie die Fragen und deren Quellen nachvollziehen, um diese Zeile für Zeile zu bewerten.
Die Dateien der einzelnen Fragen sind so nummeriert, mit der `input_source` und der `layer`-Nummer versehen, um die Zuordnung zu erleichtern.
Wenn Sie Frage $n$ bewerten, muss das Ergebnis in Zeile $n+1$ der CSV-Datei eingetragen werden, da die erste Zeile den Header enthält, usw. für die weiteren Fragen.
Der Zähler für die Fragen ist für Experiment 1a und 1b fangen jeweils bei 1 an.

### Schritt 3: Bewertung von Experiment 1a

1. Öffnen Sie `exp1a.csv`.
2. Für jede Zeile:
    - Schauen Sie sich die entsprechende Frage in `questions/exp1a/` an.
    - Prüfen Sie den zur Fragengenerierung genutzten Quelltext in `source/[input_source]/layer[X].txt`.
    - Bewerten Sie nach den 5 Kategorien der Rubrik `exp1a_rubric.md` und geben Sie ggf. Ihre Kommentare in die `comments`-Spalte ein.

### Schritt 4: Bewertung von Experiment 1b

1. Öffnen Sie `exp1b.csv`.
2. Für jede Zeile mit `script_manipulated`:
    - Schauen Sie sich die Frage in `questions/exp1b/` an.
    - Vergleichen Sie mit dem manipulierten Text in `source/script_manipulated/layer[X].txt`.
    - Bewerten Sie nach den 5 Kategorien der Rubrik `exp1b_rubric.md`, wobei die `manipulation_handling`-Bewertung für dieses Subexperiment das Hauptaugenmerk ist. Da können Kommentare hilfreich sein.

### Schritt 5: CSV-Dokumentation

Tragen Sie Ihre Bewertungen (0-10) in die jeweiligen CSV-Spalten, basierend auf der jeweiligen Bewertungsrubrik, ein:

-   `relevance` (Relevanz)
-   `clarity` (Klarheit)
-   `answerability` (Beantwortbarkeit)
-   `challenging` (Herausfordernd)
-   `correctness` (Korrektheit) -- Für Experiment 1a
-   `manipulation_handling` (Umgang mit Manipulationen) -- Für Experiment 1b
-   `comments` -- Dort können Sie Ihre Anmerkungen zu jeder Frage eintragen, um Ihre Bewertungen ggf. zu erläutern oder auf Besonderheiten hinzuweisen.

## Dankbarkeit für Ihre Unterstützung

Vielen Dank, dass Sie sich die Zeit nehmen, die Qualität der generierten Fragen meines Experimentes zu bewerten.