# Überblick des Experimentes 2 -- Malte Grube

Dieses Experiment testet die Qualität von automatisiert-generierten Fragen durch vier Large Language Models und deren Fähigkeit, verschiedene Fragetypen entsprechend spezifischer Bloom's Taxonomy-Level zu generieren. Dabei wurden drei verschiedene Prompting-Strategien verwendet, mit denen die Modelle Fragen generieren sollten. Details zu diesen Prompts werden aufgrund des Blindtests nicht gegeben.

Das Experiment fokussiert sich auf die Beziehung zwischen Frageformaten (Multiple-Choice vs. Open-Ended) und kognitiven Anforderungsniveaus nach Bloom's revised Taxonomy. Es wird untersucht, wie verschiedene Spezifikationen in den Prompts (Angabe von Fragetyp, Bloom-Level, oder beidem zusammen) die pädagogische Effektivität der generierten Fragen beeinflussen.

Es folgen die Beschreibungen der drei Subexperimente, welche Prompting-Strategien genutzt wurden, sowie eine Anleitung, wie Sie die Bewertungen vornehmen können.

## Experiment 2a (`exp2a.csv`) - Fragetyp-fokussiert

Es wurde eine Prompting-Strategie genutzt, die sich ausschließlich auf die Spezifikation des Fragetyps konzentriert:

-   **Eingabequelle:** Unbekannte Quellen (noch nicht spezifiziert)
-   **Generiert:** Fragen wurden mit Fokus auf spezifische Frageformate erstellt
-   **Strategie:** 
    -   Vorgabe des Fragetyps (Multiple-Choice oder Open-Ended)
    -   Keine Vorgabe des kognitiven Levels
    -   Das final bestimmte kognitive Level jeder Frage ist entscheidend für die pädagogische Effektivität

## Experiment 2b (`exp2b.csv`) - Bloom-Level-fokussiert

Es wurde eine Prompting-Strategie genutzt, die sich auf spezifische kognitive Level nach Bloom's Taxonomy konzentriert:

-   **Eingabequelle:** Unbekannte Quellen
-   **Generiert:** Fragen wurden mit Fokus auf spezifische Bloom-Level erstellt
-   **Strategie:**
    -   Vorgabe des gewünschten Bloom-Levels (1-6)
    -   Kein festes Frageformat vorgegeben
    -   Fokus auf Alignment mit dem vorgegebenen kognitiven Level
    -   Gefordertes Bloom-Level wird zudem den Bewertern vorenthalten

## Experiment 2c (`exp2c.csv`) - Kombinierte Spezifikation

Es wurde eine Prompting-Strategie genutzt, die beide Anforderungen integriert:

-   **Eingabequelle:** Unbekannte Quellen
-   **Generiert:** Fragen wurden mit kombinierter Spezifikation erstellt
-   **Strategie:**
    -   Vorgabe sowohl des Fragetyps als auch des Bloom-Levels
    -   Untersuchung von Beziehungen zwischen Frageformat und kognitivem Level
    -   Umfassende Analyse der pädagogischen Effektivität

## Anleitung für Experten

### Schritt 1: Verständnis der Bewertungskriterien

Lesen Sie die Experiment 2-spezifische Rubrik:

-   `exp2_rubric.md`

Diese Rubrik fokussiert sich auf die Bewertung der Fragen hinsichtlich ihrer pädagogischen Qualität und dem erreichten Bloom's Taxonomy-Level. Im Gegensatz zu Experiment 1 wird hier anstelle der **Korrektheit** bzw. **Umgang mit Manipulation** das **Bloom's Level** bewertet, um die kognitive Anspruchsebene der generierten Fragen zu analysieren.

### Schritt 2: Verständnis der CSV-Struktur

Die `exp2a.csv`, `exp2b.csv` und `exp2c.csv` enthalten:

-   `question_type`: Der spezifizierte Fragetyp (Multiple-Choice oder Open-Ended), falls vorgegeben
-   `bloom_level`: Das angestrebte Bloom-Level (1-6), falls vorgegeben
-   `sample_id`: Eine eindeutige ID für jede Frage, die Ihnen hilft, die Fragen zu identifizieren
-   Die jeweiligen 5 Kategorien zur Bewertung von 0-10:
    -   `relevance` (Relevanz)
    -   `clarity` (Klarheit)
    -   `answerability` (Beantwortbarkeit)
    -   `challenging` (Herausfordernd)
    -   `value` (Wertigkeit)
    -   `language` (Sprache)
    -   `bloom_rating` (Erreichtes Bloom-Level, Bewertung 1-6)
-   Eine `answer_problems`-Spalte, in der Sie LLM-basierte Antworten angeben können, bei denen der Wahrheitsgehalt der Antworten angezweifelt wird
-   Eine `comments`-Spalte für weitere Anmerkungen. Dies könnten beispielsweise Indizien sein, wie: Die Frage ist ein Ankerbeispiel für eine bestimmte Bloom-Kategorie, die Frage entspricht nicht dem angestrebten Fragetyp, oder Diskrepanzen zwischen angestrebtem und erreichtem kognitiven Level.

. #TODO better comments description

Anhand der CSV-Dateien können Sie die Fragen und deren Spezifikationen nachvollziehen, um diese Zeile für Zeile zu bewerten.
Die Dateien der einzelnen Fragen sind durch `sample_id` nummeriert, sodass die Zuordnung erleichtert wird.
Der Zähler für die Fragen fängt für jedes Subexperiment (2a, 2b, 2c) jeweils bei 1 an.

### Schritt 3: Bewertung von Experiment 2a (Fragetyp-fokussiert)

1. Öffnen Sie `exp2a.csv`.
2. Für jede Zeile:
    - Schauen Sie sich die entsprechende Frage in `questions/exp2a/` an.
    - Bewerten Sie nach den Kategorien der Rubrik `exp2_rubric.md`.
    - Bestimmen Sie das tatsächlich erreichte Bloom-Level (1-6) unabhängig von Vorgaben.
    - Notieren Sie diverse Anmerkungen in der `comments`-Spalte

### Schritt 4: Bewertung von Experiment 2b (Bloom-Level-fokussiert)

1. Öffnen Sie `exp2b.csv`.
2. Für jede Zeile:
    - Schauen Sie sich die entsprechende Frage in `questions/exp2b/` an.
    - Bewerten Sie nach den Kategorien der Rubrik `exp2_rubric.md`.
    - Notieren Sie diverse Anmerkungen in der `comments`-Spalte

### Schritt 5: Bewertung von Experiment 2c (Kombinierte Spezifikation)

1. Öffnen Sie `exp2c.csv`.
2. Für jede Zeile:
    - Schauen Sie sich die entsprechende Frage in `questions/exp2c/` an.
    - Bewerten Sie nach den Kategorien der Rubrik `exp2_rubric.md`.
    - Notieren Sie diverse Anmerkungen in der `comments`-Spalte

### Schritt 6: CSV-Dokumentation

Tragen Sie Ihre Bewertungen in die jeweiligen CSV-Spalten ein:

- Relevanz, Klarheit, Beantwortbarkeit, Herausfordernd, Wertigkeit, Sprache: Bewertung von 0-10 Punkten
- Bloom's Level: Bewertung von 1-6 basierend auf der tatsächlich erreichten kognitiven Anforderung
- Je nach Subexperiment werden dann diese Bloom Ratings von mir geeignet punktuell ausgewertet
- Kommentare können Sie in der `comments`-Spalte hinterlassen, um Ihre Bewertungen zu erläutern oder auf Besonderheiten hinzuweisen.

## Dankbarkeit für Ihre Unterstützung

Vielen Dank, dass Sie sich die Zeit nehmen, die Qualität der generierten Fragen meines Experimentes zu bewerten.