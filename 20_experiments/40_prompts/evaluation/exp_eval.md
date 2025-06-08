Verhalte dich wie ein Experte im Bewerten von automatisch generierten Fragen anhand eines gegebenen Kriterienkatalogs.

Dein Ziel ist es, die folgende Frage sorgfältig zu studieren, damit diese eine überaus menschenähnliche und vor allem objektive Beantwortung bekommt:

"""
{question_text}
"""

Diese Frage basiert auf folgendem Kontext zum einem Layer des ISO-OSI-Modells. Studiere diesen Text sorgfältig:

"""
{context_text}
"""

Um diese Frage nun professionell zu bewerten, nutze die folgende Rubrik:

"""
{rubric_text}
"""

Für ein systematisches Verwenden der Daten soll das Ausgabeformat wie folgt aussehen:

"""
[rubric1_score],[rubric2_score],[rubric3_score],[rubric4_score],[rubric5_score]
"""

Ein Beispiel dafür wäre: `0,10,5,6,3`

Nun bewerte die Frage anhand der Rubrik und gib deine Bewertung im angegebenen Format aus. Achte darauf, dass du die Kriterien der Rubrik einzeln und unabhängig voneinander bewertest. Deine Antwort soll ausschließlich die Bewertung enthalten, ohne zusätzliche Erklärungen oder Kommentare.