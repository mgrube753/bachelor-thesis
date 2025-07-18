# Überblick des Experimente 2 -- Malte Grube

Dieses Experiment testet die Qualität von automatisiert-generierten Fragen durch vier Large Language Models und deren Fähigkeit, verschiedene Fragetypen entsprechend spezifischer Bloom's Taxonomy-Level zu generieren. Dabei wurden drei verschiedene Prompting-Strategien verwendet, mit denen die Modelle Fragen generieren sollten. Details zu diesen Prompts werden aufgrund des Blindtests nicht gegeben. Das Thema der Fragen ist das ISO OSI Modell, welches in der Informatik eine wichtige Rolle spielt.

Das Experiment fokussiert sich auf die Beziehung zwischen Frageformaten (Multiple-Choice vs. Open-Ended) und kognitiven Anforderungsniveaus nach Bloom's revised Taxonomy. Es wird untersucht, wie verschiedene Spezifikationen in den Prompts (Angabe von Fragetyp, Bloom-Level, oder beidem zusammen) die pädagogische Effektivität der generierten Fragen beeinflussen.

Es folgen die Beschreibungen der drei Subexperimente, sowie eine Anleitung, wie Sie die Bewertungen vornehmen können.

## Experiment 2a (`exp2a.csv`) - Fragetyp-fokussiert

Es wurde eine Prompting-Strategie genutzt, die sich ausschließlich auf die Spezifikation des Fragetyps konzentriert:

-   **Eingabequelle:** Entnommene Auszüge aus Vorlesungsskript
-   **Generiert:** Fragen wurden mit Fokus auf spezifische Frageformate erstellt
-   **Strategie:**
    -   Vorgabe des Fragetyps (Multiple-Choice oder Open-Ended)
    -   Keine Vorgabe des kognitiven Levels
    -   Das final bestimmte kognitive Level jeder Frage ist entscheidend für die pädagogische Effektivität

## Experiment 2b (`exp2b.csv`) - Bloom-Level-fokussiert

Es wurde eine Prompting-Strategie genutzt, die sich auf spezifische kognitive Level nach Bloom's Taxonomy konzentriert:

-   **Eingabequelle:** Entnommene Auszüge aus Vorlesungsskript
-   **Generiert:** Fragen wurden mit Fokus auf spezifische Bloom-Levels erstellt
-   **Strategie:**
    -   Vorgabe des gewünschten Bloom-Levels (1-6)
    -   Kein festes Frageformat vorgegeben
    -   Fokus auf Alignment mit dem vorgegebenen kognitiven Level
    -   Das durch Prompting vorgegebene Bloom-Level wird zudem den Bewertern vorenthalten

## Experiment 2c (`exp2c.csv`) - Kombinierte Spezifikation

Es wurde eine Prompting-Strategie genutzt, die beide Anforderungen integriert:

-   **Eingabequelle:** Entnommene Auszüge aus Vorlesungsskript
-   **Generiert:** Fragen wurden mit kombinierter Spezifikation erstellt
-   **Strategie:**
    -   Vorgabe sowohl des Fragetyps als auch des Bloom-Levels
    -   Untersuchung von Beziehungen zwischen Frageformat und kognitivem Level
    -   Umfassende Analyse der pädagogischen Effektivität

## Anleitung für Experten

### Schritt 1: Verständnis der Bewertungskriterien

Lesen Sie die Experiment-spezifische Rubrik, um die Bewertungskriterien zu verstehen.

Diese Rubrik fokussiert sich auf die Bewertung der Fragen hinsichtlich ihrer pädagogischen Qualität und dem erreichten Bloom's Taxonomy-Level. **Bloom's Level** wird bewertet, um die kognitive Anspruchsebene der generierten Fragen zu analysieren.

Primär war der Plan gewesen, dass die Fragen durch Large Language Models ebenso ausgewertet werden sollen, jedoch wurde dies durch die Experten-Verfügbarkeit verworfen. Deshalb steht in der Experten-Rubrik zu jedem Bloom's Level auch eine kurze Beschreibung, was die jeweilige Stufe umfasst, und Trigger-Verben, die auf diese Stufe hinweisen.

### Schritt 2: Verständnis der CSV-Struktur

Die `exp2a.csv` (16 Fragen), `exp2b.csv` (8 Fragen) und `exp2c.csv` (16 Fragen) enthalten:

-   `sample_id`: Eine eindeutige ID für jede Frage, die Ihnen hilft, die Fragen zu identifizieren
-   Die jeweiligen 7 Kategorien zur Bewertung von 0-10 (beziehungsweise 1-6 für Bloom's Level):
    -   `relevance` (Relevanz)
    -   `clarity` (Klarheit)
    -   `answerability` (Beantwortbarkeit)
    -   `challenging` (Herausfordernd)
    -   `value` (Wertigkeit)
    -   `language` (Sprache)
    -   `bloom_rating` (Erreichtes Bloom-Level, Bewertung 1-6)
-   Eine `answer_problems`-Spalte, in der Sie LLM-basierte Antworten angeben können, bei denen beispielsweise der Wahrheitsgehalt der Antworten angezweifelt wird oder weiteres
-   Eine `comments`-Spalte für weitere Anmerkungen. Dies könnten beispielsweise Indizien sein, wie: Die Frage ist ein Ankerbeispiel, indem sie besonders gut oder schlecht abschneidet, oder auch, dass die Frage nicht beantwortbar ist, weil sie zu unklar formuliert ist, oder zu stark vom Text abweicht. Dies kann geschehen, sobald höhere Bloom-Level erreicht werden, da diese Fragen über den Kontext hinausgehen können.

Anhand der CSV-Dateien können Sie die Fragen und deren Spezifikationen nachvollziehen, um diese Zeile für Zeile zu bewerten.
Die Dateien der einzelnen Fragen sind durch `sample_id` nummeriert, sodass die Zuordnung erleichtert wird.
Der Zähler für die Fragen fängt für jedes Subexperiment (2a, 2b, 2c) jeweils bei 1 an.

### Schritt 3: Bewertung von Experiment 2a (Fragetyp-fokussiert)

1. Öffnen Sie die jeweilige Experiment-CSV-Datei
2. Für jede Zeile:
    - Schauen Sie sich die entsprechende Frage an.
    - Bewerten Sie nach den Kategorien der Rubrik.
    - Notieren Sie diverse Anmerkungen in der `comments`-Spalte, sofern passend.

## Notiz für Fragenanzahl pro Student

Es kann passieren, dass die gegebene Zeit für Sie nicht ausreicht, um alle Fragen zu bewerten (muss aber nicht der Fall sein). Wenn dies recht schnell jedoch erkennbar ist, dann ist das Ziel, dass Sie jeweils zumindest 20 Fragen bewerten. Geplant sei dann eine 50%-Überlappung (10/20 Fragen) zwischen den Studenten, die wie folgt entsteht:

-   **Student 1:** Fragen 1-16 von Exp2a, 1-4 von Exp2b
-   **Student 2:** Fragen 11-16 von Exp2a, 1-8 von Exp2b, 1-6 von Exp2c
-   **Student 3:** Fragen 5-8 von Exp2b, 1-16 von Exp2c

## Dankbarkeit für Ihre Unterstützung

Vielen Dank, dass Sie sich die Zeit nehmen, die Qualität der generierten Fragen meines Experimentes zu bewerten.
