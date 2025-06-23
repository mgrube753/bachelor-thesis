Verhalte dich wie ein erfahrener Experte im Generieren von kognitiv anspruchsvollen Fragen, welche nicht triviales und analytisches Denken fordern. Untersuche den gegebenen Instruktionstext sorgfältig und erfasse alles, was für die ordnungsgemäße Fragengenerierung zum ISO-OSI-Modell wichtig ist.

Deine Aufgabe ist es, eine Frage beliebigen Typs zu formulieren, die auf dem bereitgestellten Text basiert und dem Bloom's Level {bloom_level} entspricht.
Die Beschreibung dieses Levels ist: {bloom_level_description}.
Verwende dabei Verben wie: {bloom_level_verbs}.
Die Frage soll klar und präzise sein und den Leser dazu anregen, kritisch über den Inhalt nachzudenken.

Fokussiere dich auf den folgenden Text bei der Fragengenerierung:

"""
{text}
"""

Die korrekte Antwort -- oder Antwortmöglichkeit, sofern mehrere Möglichkeiten generiert werden -- soll zu Beginn klar mit einem "~" gekennzeichnet werden.

Wenn eine Antwortmöglichkeit generiert wird, soll das Antwortformat somit wie folgt, zwischen den folgenden Docstring-Symbolen, aussehen:

"""
Frage: Hier den Frageninhalt einfügen

Antwort: ~Hier die Antwort einfügen
"""

Wenn mehrere Antwortmöglichkeiten generiert werden, verwende stattdessen den folgenden Formatierungsstil, wobei du überlegen musst, welche Antwortmöglichkeiten durch ein vorangestelltes "~" als korrekt markiert werden müssen, und wo diese an beliebiger Position stehen können. Hier ein Beispiel zwischen den folgenden Docstring-Symbolen:

"""
Frage: Hier den Frageninhalt einfügen

Antwortmöglichkeiten:
- ~Beispielsweise hier die korrekte Antwort einfügen
- Hier die erste falsche Antwort einfügen
- Hier die zweite falsche Antwort einfügen
- Hier die dritte falsche Antwort einfügen
"""

Verwende klaren Fließtext. Bei Listen nutzte ausschließlich die Gedankenstriche "-" als Formatierung und vermeide jegliche andere Markdown-basierte Formatierung.

Nun starte mit der Generierung unter Berücksichtigung der oben genannten Punkte. Gib nur die Frage und die zugehörige(n) Antwort(en) aus. Achte final auf Korrektheit in Format und Formulierung.