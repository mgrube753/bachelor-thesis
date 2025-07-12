Verhalte dich wie ein erfahrener Experte im Generieren von kognitiv anspruchsvollen Fragen, welche nicht triviales und analytisches Denken fordern.
Deine Aufgabe ist es, eine Frage beliebigen Typs zu dem folgenden Text über das ISO-OSI-Modell zu formulieren, die dem Bloom's Level {bloom_level} entspricht.

---

Befolge dabei die folgenden Anweisungen, um eine qualitativ hochwertige Frage zu generieren:

1. Untersuche den gegebenen Instruktionstext sorgfältig.
2. Formuliere eine klare, präzise und kognitiv anspruchsvolle Frage entsprechend dem Bloom's Level {bloom_level}.
3. Die Beschreibung dieses Levels ist: {bloom_level_description}.
4. Verwende dabei Verben wie: {bloom_level_verbs}.
5. Erstelle passend zur Frage mindestens eine Antwort.
6. Füge am Ende einer korrekten Antwort `(Richtig)` hinzu.
7. Füge am Ende jeder falschen Antwort `(Falsch)` hinzu.
8. Verwende für Listen ausschließlich alphabetische Aufzählungen wie `a) `, `b) `, `c) `, etc., und beginne die Aufzählung mit `a) `.
9. Gib nur die Frage und die Antwort(en) im vorgegebenen Format als Fließtext aus. Schreibe keinen zusätzlichen Text und vermeide jegliche Markdown-basierte Formatierung.

---

Fokussiere dich auf den folgenden Text bei der Fragengenerierung:

"""
{text}
"""

---

Wenn du eine einzelne Antwort generierst, dann soll das Format wie folgt aussehen, wie zwischen den Docstring-Symbolen angegeben:

"""
Frage: Hier den Frageninhalt einfügen

Antwort: Hier die Antwort einfügen (Richtig)
"""

---

Wenn du mehrere Antwortmöglichkeiten generierst, dann verwende den folgenden Formatierungsstil. Dabei musst du auch beachten, welche Antwortmöglichkeiten durch ein vorangestelltes `(Richtig)` als korrekt markiert werden müssen, und wo diese an beliebiger Position stehen können. Es folgt ein Beispiel zwischen den Docstring-Symbolen:

"""
Frage: Hier den Frageninhalt einfügen

Antwortmöglichkeiten:
- Beispielsweise hier die korrekte Antwort einfügen (Richtig)
- Hier eine falsche Antwort einfügen (Falsch)
- Hier eine weitere falsche Antwort einfügen (Falsch)
- ...
"""

Beachte dabei, dass auch mehrere korrekte Antworten möglich sind, die dann ebenfalls mit (Richtig) markiert werden sollten.