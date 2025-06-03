Verhalte dich wie ein erfahrener Experte im Generieren von kognitiv anspruchsvollen Fragen, welche nicht triviales und analytisches Denken fordern. Untersuche den gegebenen Instruktionstext sorgfältig und erfasse alles, was für die ordnungsgemäße Fragengenerierung zum ISO-OSI-Modell wichtig ist.

Deine Aufgabe ist es, eine Frage beliebigen Typs zu formulieren, die auf dem bereitgestellten Text basiert und dem Bloom's Level {bloom_level} entspricht.
Es folgt eine Beschreibung des Levels: {bloom_level_description}.
Bekannte Verben, die dem Level zugehörig sind, sind unter anderem: {bloom_level_verbs}.
Die Frage soll klar und präzise sein und den Leser dazu anregen, kritisch über den Inhalt nachzudenken.

Fokussiere dich auf den folgenden Text bei der Fragengenerierung:

"""
{text}
"""

Die korrekte Antwort -- oder Antwortmöglichkeit, sofern mehrere Möglichkeiten generiert werden -- soll zu Beginn klar mit einem "~" gekennzeichnet werden.

Wenn eine Antwortmöglichkeit generiert wird, soll das Antwortformat somit wie folgt aussehen:

"""
Frage: Hier den Frageninhalt einfügen

Antwort: ~Hier die Antwort einfügen
"""

Wenn mehrere Antwortmöglichkeiten generiert werden, verwende stattdessen den folgenden Formatierungsstil, wobei eine oder mehrere Antworten durch ein vorangestelltes korrekt markiert werden und an beliebiger Position stehen können:

"""
Frage: Hier den Frageninhalt einfügen

Antwortmöglichkeiten:
- ~Beispielsweise hier die korrekte Antwort einfügen
- Hier die erste falsche Antwort einfügen
- Hier die zweite falsche Antwort einfügen
- Hier die dritte falsche Antwort einfügen
"""

Verwende klaren Fließtext. Bei Listen nutzte ausschließlich die Gedankenstriche "-" als Formatierung.

Nun starte mit der Generierung unter Berücksichtigung der oben genannten Punkte. Gib nur die Frage und die zugehörige(n) Antwort(en) aus. Achte final auf Korrektheit in Format und Formulierung.