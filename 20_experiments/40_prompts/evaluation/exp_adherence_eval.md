Verhalte dich wie ein Experte im metrischen Bewerten von automatisch generierten Fragen bezüglich ihrer Übereinstimmung mit einem gegebenen Quelltext zum ISO-OSI-Modell.

Dein Ziel ist es, die folgende Frage sorgfältig zu studieren:

"""
{question_text}
"""

Diese Frage basiert auf folgendem Kontext zu einem Layer des ISO-OSI-Modells. Studiere diesen Text sorgfältig:

"""
{context_text}
"""

Um diese Frage nun professionell anhand ihrer Übereinstimmung zu bewerten, analysiere den Text und die Frage systematisch. Achte dabei auf die korrekte Verwendung von Fachbegriffen und die Nutzung der Funktionen zu den entsprechenden Schichten. Identifiziere Abweichungen vom Kontext und bewerte final den Grad der Übereinstimmung. Nutze dazu die folgende Bewertungsskala:

- Wert von 1.0: Alle Inhalte wurden korrekt und umfassend dargelegt
- Wert von 0.8-0.9: Geringfügige fachliche Abweichungen
- Wert von 0.6-0.7: Gewisse technische Ungenauigkeiten
- Wert von 0.4-0.5: Mehrere inhaltliche Abweichungen
- Wert von 0.2-0.3: Gravierende Missverständnisse
- Wert von 0.0-0.1: Inhalte entsprechen nicht dem Kontext

Für ein systematisches Verwenden der Daten soll das Ausgabeformat wie folgt aussehen:

"""
[adherence_score]
"""

Ein Beispiel-Output wäre: `0.73`

Nun bewerte die Frage anhand der Inhaltstreue zum gegebenen Kontext. Deine Antwort soll ausschließlich die Bewertung als Dezimalzahl zwischen 0.0 und 1.0 mit zwei Nachkommastellen sein, ohne zusätzliche Erklärungen oder Kommentare.