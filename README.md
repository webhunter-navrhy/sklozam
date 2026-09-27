# sklozam.cz — nový web

Návrh nového webu pro Michala Zahradníka (Sklozam). Zachovává obsah, strukturu a adresy starého webu z Webnode, ale design je nový: světlý papír, tmavá „vitrína“ pro skleněné modely, akcent v barvě plamene kahanu (Newsreader + Schibsted Grotesk). Klient nechce agresivní prodejní web — proto klidný tón, žádné pop-upy ani velké animace.

První verze (věrná kopie starého rámce) je v historii gitu, commit „Modernizace webu sklozam.cz se zachováním původního rámce“.

- Obsah a struktura stránek jsou v `build.py`, `python3 build.py` vygeneruje všechny `*/index.html` (a ?v= hashe k CSS/JS)
- Adresy stránek jsou stejné jako na starém webu (`/rodokmen/`, `/sklenene-modely/hvezdice/` …), takže staré odkazy po přesunu domény fungují
- Styly `assets/style.css`, skript `assets/main.js` (menu, galerie, videa po kliknutí, jemné odhalení při scrollu)
- Úvod: hero s Hvězdicí, čísla, pět generací (portréty vyříznuté z původního pásu v hlavičce), vitrína 10 modelů, video, školy s běžícím seznamem navštívených škol, rekordy a média
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
