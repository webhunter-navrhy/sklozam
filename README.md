# sklozam.cz — technická modernizace

Návrh nového webu pro Michala Zahradníka (Sklozam). Klient chtěl zachovat rámec starého webu z Webnode a jen ho technicky zmodernizovat.

- Obsah a struktura stránek jsou v `build.py`, `python3 build.py` vygeneruje všechny `*/index.html` (a ?v= hashe k CSS/JS)
- Adresy stránek jsou stejné jako na starém webu (`/rodokmen/`, `/sklenene-modely/hvezdice/` …), takže staré odkazy po přesunu domény fungují
- Styly `assets/style.css`, skript `assets/main.js` (menu na mobilu, galerie, videa po kliknutí, mapa po rozbalení)
- Fotky jsou originály ze starého webu (nejvýš 640 px, víc tam není)

## Co se změnilo proti starému webu
- Responzivní (mobil), čitelné písmo, galerie se zvětšením, videa YouTube přímo na stránce (youtube-nocookie, načítají se až po kliknutí)
- Přehled modelů s náhledy, rodokmen jako časová osa po generacích, u modelů odkaz na předchozí/další
- Odstraněno: počítadlo TOPlist, starý Google Analytics (UA), RSS, vyhledávání
- Texty jsou autorovy, opravené jen překlepy (jesli, shopny, sestrojill, chamie, zdoj, hnotnost, neůměrně, Guinessovy, Stephensenova → Stephensonova …)

## K doladění s klientem
- Weby Petra Bílka (remeslo-do-skol.webnode.cz, bilekpetr-rytesklo.cz) už neexistují, odkaz je zatím bez adresy
- Odkazy na ČT iVysílání mohou vést na staré adresy
- Plánovací kalendář zůstává na folkcraft.eu/zahradnik (má captchu)
