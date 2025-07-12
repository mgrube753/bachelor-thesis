Verhalte dich wie ein erfahrener Experte im Generieren von kognitiv anspruchsvollen Fragen, welche nicht triviales und analytisches Denken fordern.
Deine Aufgabe ist es, eine Frage vom Typ {question_type} zu dem folgenden Text über das ISO-OSI-Modell zu formulieren.

---

Befolge dabei die folgenden Anweisungen, um eine qualitativ hochwertige Frage zu generieren:

1. Untersuche den gegebenen Instruktionstext sorgfältig.
2. Formuliere eine klare, präzise und kognitiv anspruchsvolle Frage vom Typ {question_type}, die zum kritischen Nachdenken anregt.
3. Erstelle passend zur Frage mindestens eine Antwort.
4. Füge am Ende einer korrekten Antwort `(Richtig)` hinzu.
5. Füge am Ende jeder falschen Antwort `(Falsch)` hinzu.
6. Verwende für Listen ausschließlich alphabetische Aufzählungen wie `a) `, `b) `, `c) `, etc., und beginne die Aufzählung mit `a) `.
7. Gib nur die Frage und die Antwort(en) im vorgegebenen Format als Fließtext aus. Schreibe keinen zusätzlichen Text und vermeide jegliche Markdown-basierte Formatierung.

---

Fokussiere dich auf den folgenden Text bei der Fragengenerierung:

"""
{text}
"""

---

Verwende für die Ausgabe der Frage und der Antwort(en) das folgende Format zwischen den folgenden Docstring-Symbolen:

"""
{question_type_format}
"""

Beachte dabei, dass auch mehrere korrekte Antworten möglich sind, die dann ebenfalls mit (Richtig) markiert werden sollten.