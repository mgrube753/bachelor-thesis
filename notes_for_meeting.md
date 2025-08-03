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

#### complications

## Quantitative Analysis exp2 (students)
