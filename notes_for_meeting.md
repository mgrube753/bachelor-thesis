## Quantitative Analysis exp1

### exp1a

-   exp1 quantitativ: cosine similarity nicht zureichend. adherence score besser hierbei, vor allem nützlicher bei exp1b
    -   adherence score zeigt in exp1a jedoch nicht streng genug ob man sich an den inhalt gehalten hat
    -   beide metriken zeigen keine sinnvollen trends bei input source, jedoch deepseek und openai etwas hoeher als anthropic und google
    -   prompt type aber auch trend zu common prompt bei adherence score, sinnvoll da in qualitativer analyse auch dargelegt worden, nur bei AS geringer sichtbar, complex prompt ist bei adherence score geringer gewesen

### exp1b

-   in exp1b cossim noch nutzloser, aber adherence score zeigt hier deutlicher und korrekt an, dass deepseek und openai besser sich von den manipulierten inhalten distanzieren, vor allem deepseek
    -   vor allem der complex prompt hat hierzu beigetragen, da deepseek und openai dort am besten abgeschnitten haben

## Qualitative Analysis exp1 (supervisor vs. staff)

### supervisor

#### exp1a

-   openai als klarer favorit in fragengenerierung, nah gefolgt von deepseek bzgl. relevance, clarity, answerability
-   openai bei value bedeutend besser als konkurrenz, deepseek und openai in language auffällig gut
-   correctness zu source text bei openai top, deepseek und anthropic nicht schlecht, aber google überraschend breit gefächert im scoring
-   challenging sind oft vor allem die fragen von deepseek und openai eher weniger; google breites spektrum aber eben besser; anthropic beste datenverteilung
-   total score ist openai klar im vorteil, deepseek und anthropic auf einem level, google deutlich schlechter.
-   es fiel aber auf, dass anthropic und google besonders schlechte emotionen bei supervisor hervorrufen
-   correctness nochmal separat betrachtet: openai überzeugend bei allen sources + prompts
    -   google auffallend schlecht bei beiden prompts, besonders ausgelöst durch script, tanenbaum besser, transcript bestes bei google
    -   deepseek common prompt sehr gut, script nicht soooo gut, tanenbaum besser, transcript am besten wieder
    -   anthropic eher durcheinander, script und transcript gut, common prompt auch besser als complex
-   nach input source gefiltert ist transcript oftmals erkennbar am besten (gelegentlich script knapp dahinter), die vom script sind viel mehr challenging, gefolgt von tanenbaum. durch schwäche bei challenging für transcript ist total score knapp im mean schlechter als script
-   common prompt signifikant besser abgeschnitten als complex, ausser challenging, da complex prompt hier besser war

#### exp1b

-   anders bewertet als die staffs es getan haben, somit hier mit weniger ratings (1 rater vs 4 bei staff) wenig signifikante trends
-   grundsätzlicher struggle der modelle bei der fragenmenge erkennbar bei manipulation handling
-   common prompt im grunde noch schlechter als complex prompt
-   werte grundlegend gering, aber deepseek bei beiden prompts gelegentliche erkennung dessen
-   anthropic und google nur bei complex prompt; openai bei der sampling-menge gar nicht
-   deepseek und openai sind hier keine favoriten bei manipuliertem inhalt, was nicht ganz einhergeht mit der quantitativen analyse, da hier openai und deepseek besser waren!

#### complications

-   bei exp1b nur manipulation handling bewertet, da andere kategorien da nicht sinnvoll
-   auch mit rubrik-vergrößerung sind gewisse fragen mit NaN-Werten behaftet
-   complex prompt (e.g. anthropic) führte zu ungenügenden werten bei challenging, value und correctness. gelegentlich dann auch inkorrekte antwortmöglichkeiten oder waren abseits des gegebenen contents
-   deepseek und google hatten sehr oft "basierend auf dem text" drin
-   googles fragen waren oft zu lang, sehr weitschweifend, gelegentlich auch antwortmöglichkeiten inkorrekt, gelegentlich fragen überaus unklar gestellt
-   deepseek und openai fragen waren eben nicht allzu fordernd

### staff

-   schlechtes agreement bei exp 1 vor allem durch zwischenwert-bewertung bei staff members

#### exp1a

- openai und deepseek an sich die leading models in vielen kriterien wie clarity, answerability, language
- der vorteil von openai bei staff nicht so stark vertreten wie bei supervisor, die modelle waren alle relativ nah beieinander
- auch hier ist challenging kriterium geringer als die anderen kriterien, aber grundlegend strenger bei den staff members hier
- challenging auch bei staff mit anthropic und google besser als deepseek und openai
- language auch strenger bei staff, cap hat 10/10 für openai und deepseek, aber staff sind 8.6/10 jeweils
- anthropic und google sind eher schwerfällig ebenso, erkennbar in language
- value etwas strenger auch an sich, openai als klarer favorit entfällt ein wenig hier, statt 10/10 wie bei supervisor, stattdessen 6.48
- correctness grundsätzlich auch am besten bei openai und dann deepseek, gewisse niedrig-ratings gibts dort aber auch
- anthropic und google sind tiefer angesiedelt, inkorrektheiten und ausgedachtes abseits vom source text
- an sich ähnlich zum supervisor, aber dieser hat nur 0,5,10 benutzt bei correctness, die anderen auch werte dazwischen
- total score auch openai am besten knapp, gefolgt von deepseek, aber differenz ist nicht so groß wie bei supervisor
- correctness nach input source: sehr verschieden, die llms performen sehr verschieden, aber per prompt type eindeutig der common prompt wieder besser
- alle metriken nach input source: script an sich knapp am durchsetzen. transcript nah dahinter, und sogar besser bei clarity, ganz knapp answerability und language
- alles nach prompt type: common prompt besser als complex, ausser bei challenging, da complex prompt besser war. im value aber waren die staff members besonders streng ggü. supervisor, auch etwas bei clarity und language
- dafür in correctness sehr aehnlich zu supervisor, in beiden prompts

#### exp1b

- staff hat etwas anders bewertet als supervisor, was an den zwischen-ratings liegen könnte
- die sampling-menge war recht klein, spiegelt nicht den kompletten rahmen der fragen wider
- aber durch die 4 staff members mehr oder weniger ähnliche trends wie bei supervisor
- dieser war nur viel strenger.
- an sich complex prompt auch am besser performen was erkennung angeht.
- auch hier eher anthropic und v.a. google besser, deepseek und openai schwächer, was in quantitativer analyse nicht so war (alle fragen via adherence score)
- modell-struggles hierbei nicht so stark erkennbar wie bei supervisor, es zeigt sich jedoch auch im agreement, dass die bewertungen sehr divers ausfallen

#### complications

- gewisse fragen waren teils nicht related zum source text, wobei answerability und correctness sinken
- negationsfragen aufgetreten, was kritisiert wurde --> weniger clarity und value
- google und anthropic über complex prompt vor allem erkennbar lange komplexe fragen, welche so nicht gestellt werden sollten
- "based on the text" oft angekreidet --> value vermindert
- google und anthropic mit inkorrekten antwortmöglichkeiten / oder eben abseits des source textes oft gesehen
- openai und deepseek manchmal einfache fragen gestellt
- was grundlegend mit dem common prompt einhergeht, die complex prompt fragen waren mehr herausfordernd, aber dadurch litten die anderen kategorien darunter --> clarity und language
- openai stets am besten rund, aber bei cap viel besser sichtbar; grundsätzlich hatten die anderen modelle probleme hohe werte bei clarity, answerability und correctness zu erreichen
- inkonsistente bewertungen, vor allem durch zwischenwerte und verschiedene interpretationen der kriterien-abstufungen, führten zu einem schlechten agreement. es fiel mir schwer, diese abstufungen anzulegen, da die literatur eben nicht so viel dabei geholfen hat
- exp1b anders bewertet wie gesagt, und die sampling-menge bei 1b relativ klein 

## Quantitative Analysis exp2 (students)

### insights

- ratings an sich nicht so divers zwischen den modellen wie erwartet
    - fragen grundlegend relevant und klar für alle modelle. google und openai hierbei etwas schwächer
    - auch in der answerability alle recht ähnlich gut, aber google und openai schlechter, google hat eben viele überladene fragen, die über den text hinausgehen
    - dafür sind google und openai bei challenging weiter vorn
    - fragen oft auch wertvoll, openai und deepseek eben etwas höher vertreten
    - per language haben alle modelle jeweils diverse performance gehabt, aber grundlegend waren die fragen gut formuliert
    - bloom's level: auf den ersten blick hat deepseek schwächste performance, dann anthropic. auch wenn mean bei openai und google etwas gering sind, die mediane sind sehr weit oben
    - total score: kein klarer gewinner oder verlierer
- anhand der subexperimente:
    - fragen von type only sind am relevantesten
    - klarheit bei type only und type+bloom am besten gg. bloom only
    - answerability eher besser bei type only und type+bloom, bloom only schlechter
    - fragen von bloom only viel mehr challenging
    - alle subexperimente haben hohe value scores an sich, aber bloom only an sich am besten
    - per language type+bloom am besten
    - bloom only und type+bloom bei bloom score beide gut. type only ergebnisse weniger hoch
    - total score sind bei BO und TB ähnlich gut, TO etwas niedriger, was primär durch bloom score bedingt ist
- bloom scores zwischen llm und subexperiment:
    - anthropic bei 2a gewinnner, openai bei 2b, google bei 2c
- bloom scores pro question type und subexperiment:
    - 2c scoring grundsätzlich gut für MCQ und open ended, aber open ended bei beiden subexperimenten besser
- agreements:
    - answerability, challenging und bloom rating sind sehenswert, rest ist gering

### complications

- kein operator bei gewissen fragen, besonders in experiment 2a, was bloom's taxonomy wichtig macht
- value kriterium sei nicht so gut, sagt eine studentin, da sie eher bei fragen auf ein lernziel abbilden würde, das haben wir nicht eingebunden, sondern nur bloom level
   - "Wird die Frage vom Dozenten als fachlich / didaktisch / technisch sinnvoll erachtet?" ist schwierig, da fachlich und didaktisch etwas anderes ist
- agreement problem stets vorhanden, aber die haben sich ausdrücklich an die rubrik gehalten, statt zwischenratings wie bei staff members
- (von mir: deepseek hatte manchmal multiple-choice statt open-ended generiert)
- google und anthropic voller fachtermini, aber auch einmal openai bei 2a (mit mehreren operatoren, obwohl ich keine vorgegeben habe*)
- anthropic bei 2c keinen operator
- openai hatte bei bloom 6 auch MCQ generieren müssen. das gefiel der studentin nicht, da MCQ und hohes Bloom sich ausschließen...
- an sich google und anthropic explizit oft unschöne fragen.