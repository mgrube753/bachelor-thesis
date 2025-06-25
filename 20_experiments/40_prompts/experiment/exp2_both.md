Verhalte dich wie ein erfahrener Experte im Generieren von kognitiv anspruchsvollen Fragen, welche nicht triviales und analytisches Denken fordern.
Deine Aufgabe ist es, eine Frage vom Typ {question_type} zu dem folgenden Text über das ISO-OSI-Modell zu formulieren, die dem Bloom's Level {bloom_level} entspricht.

---

Befolge dabei die folgenden Anweisungen, um eine qualitativ hochwertige Frage zu generieren:

1. Untersuche den gegebenen Instruktionstext sorgfältig.
2. Erfasse alles, was für die ordnungsgemäße Fragengenerierung zum ISO-OSI-Modell wichtig ist.
3. Formuliere eine klare, präzise und kognitiv anspruchsvolle Frage vom Typ {question_type} entsprechend dem Bloom's Level {bloom_level}.
4. Die Beschreibung dieses Levels ist: {bloom_level_description}.
5. Verwende dabei Verben wie: {bloom_level_verbs}.
6. Erstelle passend zur Frage mindestens eine Antwort.
7. Füge am Ende einer korrekten Antwort `(Richtig)` hinzu.
8. Füge am Ende jeder falschen Antwort `(Falsch)` hinzu.
9. Verwende für Listen ausschließlich Gedankenstriche (`-`).
10. Gib nur die Frage und die Antwort(en) im vorgegebenen Format als Fließtext aus. Schreibe keinen zusätzlichen Text und vermeide jegliche Markdown-basierte Formatierung.

---

Fokussiere dich auf den folgenden Text bei der Fragengenerierung:

"""
{text}
"""

---

Wenn Multiple-Choice gefordert wird, dann musst du beachten, welche Antwortmöglichkeiten durch ein vorangestelltes `(Richtig)` als korrekt markiert werden müssen, und wo diese an beliebiger Position stehen können.

Verwende für die Ausgabe der Frage und der Antwort(en) das folgende Format zwischen den folgenden Docstring-Symbolen:

"""
{question_type_format}
"""

Beachte dabei, dass auch mehrere korrekte Antworten möglich sind, die dann ebenfalls mit (Richtig) markiert werden sollten.