#!/usr/bin/env python3
"""Generátor webu sklozam.cz — Michal Zahradník, sklář.

Každá stránka = záznam v PAGES (cesta, titulek, obsah). Adresy jsou stejné
jako na původním webu, aby staré odkazy dál fungovaly.
Spuštění: python3 build.py  → vygeneruje */index.html s ?v= hashi assetů.
"""
import hashlib, html, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://www.sklozam.cz'


def ver(path):
    with open(os.path.join(ROOT, path), 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


# ---------- stavební bloky obsahu ----------

def img(name):
    return f'~/assets/img/{name}.jpg'


def gal(*items, cols=3, cls=''):
    """Galerie: položky (soubor, popisek). Klik otevře lightbox."""
    out = [f'<div class="gal gal--{cols} {cls}">']
    for name, cap in items:
        c = html.escape(cap, quote=True)
        out.append(
            f'<figure><a href="{img(name)}" class="lb" data-cap="{c}">'
            f'<img src="{img(name)}" alt="{c}" loading="lazy"></a>'
            + (f'<figcaption>{cap}</figcaption>' if cap else '') + '</figure>')
    out.append('</div>')
    return ''.join(out)


def fig(name, cap, cls=''):
    c = html.escape(cap, quote=True)
    return (f'<figure class="fig {cls}"><a href="{img(name)}" class="lb" data-cap="{c}">'
            f'<img src="{img(name)}" alt="{c}" loading="lazy"></a><figcaption>{cap}</figcaption></figure>')


def yt(vid, title):
    """Video z YouTube — načte se až po kliknutí (rychlost, soukromí)."""
    t = html.escape(title, quote=True)
    return (f'<div class="video"><button class="yt" data-id="{vid}" aria-label="Přehrát video: {t}">'
            f'<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy">'
            f'<span class="yt-play" aria-hidden="true"></span></button>'
            f'<p class="video-cap">{title} <a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">otevřít na YouTube</a></p></div>')


def ext(url, text=None):
    return f'<a href="{url}" target="_blank" rel="noopener">{text or url}</a>'


# ---------- obsah ----------

MODELS = [
    ('prvni-jednovalcovy-parni-stroj', 'První, jednoválcový parní stroj', 'prvni-jednovalec2',
     'Jednočinný parní stroj — můj první skleněný model.'),
    ('druhy-jednovalcovy-parni-stroj', 'Druhý, jednoválcový parní stroj', 'novy-jednovalec2',
     'Větší setrvačník, diamantem vybroušený válec. Běží i na páru.'),
    ('trivalcova-lokomotiva', 'Tříválcová lokomotiva', 'trivalec1',
     'Tři válce po 120° a zcela originální pohon šoupat.'),
    ('stephensenova-lokomotiva', 'Stephensonova lokomotiva', 'stefina1',
     'Lokomotiva z roku 1829 pro rozchod 127 mm. Český rekord.'),
    ('auto', 'Auto', 'paroauto',
     'Nejdřív na elektromotor, pak na páru. Diferenciál ze skla.'),
    ('boxer', 'Boxer', 'boxer',
     'Motor pro parní auto, který běží jako zdivočelé Kango.'),
    ('hvezdice', 'Hvězdice', 'hvezdice-detail',
     'Hvězdicový motor — osobně ho považuji za své vrcholné dílo.'),
    ('ctyrvalcovy-radovy-motor', 'Čtyřválcový řadový motor', 'ctyrvalec1',
     'Klikovka osmkrát zalomená. Vznikl v únoru 2015.'),
    ('letadlo', 'Letadlo', 'letadlo-vrch',
     'Rozpětí 1 m, let 7. června 2000 v Rakovníku. Český rekord.'),
    ('vsehochut', 'Všehochuť', 'kejvaci',
     'Skleněná pružina a pijící čáp, kterému říkám „Kejvák“.'),
]

HOME = f'''
<section class="intro">
  <p class="lead">navštívili jste stránky jednoho z nejstarších sklářských rodů v Čechách, kde se již od roku 1775, po osm generací, předává toto řemeslo z otce na syna. Nevím, jestli se i předcházející generace živily jako skláři, čas odvál jejich osudy na cestu zapomnění a nám nezbývá než věřit, že své geny trpělivosti a lásky k řemeslu vložili do generací dalších.</p>
  <p>O historii sklářského rodu Zahradníků se více dočtete v sekci <a href="~/rodokmen/">Rodokmen</a>.</p>
  <p class="aside-note">Na Facebooku a jiných sociálních sítích mě nehledejte, masturbaci svého ega provádím pouze zde.</p>
</section>

<div class="tiles">
  <a class="tile" href="~/sklenene-modely/">
    <img src="{img('hvezdice-detail')}" alt="Skleněný hvězdicový motor" loading="lazy">
    <span class="tile-t">Skleněné modely</span>
    <span class="tile-d">Parní stroje, lokomotivy, motory i letadlo — všechno ze skla a všechno se hýbe.</span>
  </a>
  <a class="tile" href="~/rodokmen/">
    <img src="{img('deda')}" alt="Děda Franz-Maria ve své dílně v Lipové ulici, 1926" loading="lazy">
    <span class="tile-t">Rodokmen</span>
    <span class="tile-d">Osm generací sklářů od roku 1775 — od Moravy přes Vídeň až do Prahy.</span>
  </a>
  <a class="tile" href="~/akce-pro-skoly/">
    <img src="{img('pri-praci2')}" alt="Přednáška o skle ve škole" loading="lazy">
    <span class="tile-t">Akce pro školy a školky</span>
    <span class="tile-d">Dvouhodinová přednáška s ukázkami a každé dítě si vyfoukne svou skleněnou kuličku.</span>
  </a>
</div>

<section class="box">
  <h2>Výroba parního stroje ze skla</h2>
  <p>Tříminutové video výroby parního stroje ze skla v sestříhané a zrychlené verzi.</p>
  {yt('pI90-S3egc8', 'Výroba parního stroje ze skla — zrychlená verze')}
</section>

<section class="news">
  <span class="news-tag">Nové</span>
  <a href="~/sklenene-modely/ctyrvalcovy-radovy-motor/" class="news-link">
    <img src="{img('ctyrvalec2')}" alt="Čtyřválcový řadový motor ze skla" loading="lazy">
    <span><strong>Čtyřválcový řadový motor</strong><br>Klikovka je osmkrát zalomena a její úhlení není až tak snadné, abych ho dělal „naostro“.</span>
  </a>
</section>

<section>
  <h2>Občas jsem byl hostem v televizi</h2>
  <ul class="links">
    <li>{ext('http://www.ceskatelevize.cz/ivysilani/1126666764-toulava-kamera/207411000321028/', 'Toulavá kamera')} <span>(čas od 17:17)</span></li>
    <li>{ext('http://www.ceskatelevize.cz/ivysilani/1095889602-barvy-zivota/210562221200010/obsah/110096-michal-zahradnik-sklar/', 'Barvy života')} <span>16. 4. 2010</span></li>
    <li>{ext('https://www.hornbach.cz/aktuality/machr-stories-045-parni-stroje-ze-skla/', 'Hornbach — Machr stories: Parní stroje ze skla')}</li>
  </ul>
</section>
'''

ZACATKY = '''
<p class="lead">Pro mě to všechno začalo v roce 1972, mnohem dříve, než se vůbec zrodil první skleněný parní stroj. Někdy v polovině sedmdesátých let, na učilišti, kdy jsem začal objevovat vlastnosti toho kouzelného materiálu — skla.</p>
<p>V té době, kdy se člověk učí vyrábět tvary a používat postupy při výrobě, které již vyzkoušel někdo jiný, tak v té době jsem začal zhmotňovat svoji fantazii. Pokud si vzpomínám, tak jeden z prvních výrobků zcela se vymykající směru technického skláře a do té doby snad ani jiným nevyroben, byla skleněná loutka. Přátelil jsem se tenkrát s jednou slečnou, která hrála loutkové divadlo, a já jsem ji chtěl obdarovat něčím výjimečným. A tak jsem jí vyrobil loutku, marionetu, která měla pohyblivé ruce a nohy a byla zavěšena na skleněných nitích. Paradoxem bylo, že samotná výroba byla otázkou jedné či dvou hodin, ale vymyslet způsob, jak ji zabalit a transportovat, na to jsem potřeboval několik dní.</p>
<p>K myšlence vyrobit si parní stroj jsem se dostal až o něco později. To už jsem byl po vyučení, plnil výsledky plánovitého rozvoje socialistického hospodářství a do mysli se mi vkrádala myšlenka, že té společnosti, ke štěstí a dokonalosti, cosi chybí. Ano, byl to skleněný parní stroj! …„ses asi zbláznil, to dohromady nedáš“…, …„ti to chodit nebude“…, …„Zahradník zase fušuje“…, tak asi takhle zněly věty podporující rozvoj mladého talentu a posunuly vznik parostroje o deset let. Až do roku 1988, kdy jsem s povolením Národního výboru začal soukromě podnikat, mít vlastní dílnu, čas a žádnou brzdu v podobě vedoucího.</p>
<p>Rozhodnete-li se dělat pohyblivé věci ze skla, tak největší konstrukční i výrobní komplikací je nemožnost použít šroubových, nýtovacích a dalších postupů, jinak zcela běžných a obvyklých při práci s kovem. Nedá se vzít hotová věc ze železa a okopírovat ji ze skla.</p>
<h2>Jak jsem dělal diferenciál</h2>
<p>Názorným příkladem je výroba diferenciálu pro mé skleněné <a href="~/sklenene-modely/auto/">auto</a>. To je taková ta oteklá roura, co mívají některá auta mezi zadníma kolama. Abych pochopil jeho funkci, tak jsem si jeden na vrakovišti sehnal. Doma jsem ho rozebral a ouha. Ono je to tady sešroubované a támhle sešroubované a tohle se točit musí, ale tohle zase nesmí, a musí to být v ose, a sakra, má to zuby. No, ozubené kolo ze skla, tak to nás teda v učilišti neučili. Ale já ten diferák chci!</p>
<p>Tak vezmu literaturu a zkoumám, jak se vyrábí ozubené kolo ze železa. Tady se píše, že zuby mají nějaký modul. Modul je takový souhrn požadavků, aby ty zuby byly dostatečně velké, aby něco vydržely a aby se po sobě odvalovaly, aby pasovaly do jiných zubů a aby…. No jo, ale strojnické tabulky vám přesně popisují zuby z oceli, bronzu, silonu a pro bůhví jaký materiál, ale o skle ani čárka. Čím to asi bude? Že by to nešlo? A nebo to nikdo ještě nepotřeboval? Tak jo, tak tedy zuby se frézují. Jak a čím já budu frézovat sklo? Asi to bude lepší vybrušovat. A jsme zase u toho. Technologie používané k zabrušování skla, co jsme se učili, jsou mi k ničemu.</p>
<p>Tak jinak. Chci, aby ten zub měl takový a takový tvar a aby byl tak a tak veliký. To bude sranda. To si takhle vezmu kousek mosazné kulatiny a vysoustružím si ten rádius a potom si udělám takový přípraveček, ten s tím bude točit a já na to nanesu volně vázané brusivo s vodou a zub bude na světě. Cink. Zub, ta mrcha, se vylomil. Tak tudy cesta nevede. Jak dál? Inu, nejlepší by byl diamantový brus. Koupit to nejde, Internet prakticky neexistuje (jsme v roce 1990).</p>
<blockquote class="quote">Diamantový bort se váže v niklové lázni pomocí elektrolytického vylučování niklu na elektricky vodivý povrch obráběcího nástroje, zmenšeného o předpokládaný rozměr diamantového zrna, jehož zárůst se řídí potřebou poměru rychlosti odebírání materiálu k pevnosti uchycení.</blockquote>
<p>No fuj tajbl. Věta, která mi doslova bere dech. Teprve s odstupem času zjišťuji, že pochopení té věty bylo na celé samovýrobě to nejjednodušší. Takže jdu shánět diamantový prach. Začínám v jednom zlatnictví a povídám tomu prodavači: „Dobrý den, potřeboval bych asi tak hrst malinkatých diamantů.“ „Víte, chci si udělat frézku na výrobu ozubeného kola ze skla,“ pokračuji, zatímco prodavač vytáčí číslo do blázince. Nakonec ale uvěřil a přislíbil pomoc, ať se prý zeptám tak za týden. Kupodivu hned druhý či třetí den mi volá a povídá, abych se zastavil, že Georgij mi tam trochu nechal. „Jo a kupte cestou někde tři masový konzervy, on je zbožňuje.“ A tak jsem se, za tři konzervy vepřového masa ve vlastní šťávě, stal majitelem asi 3 ccm umělého diamantového zrna z Ruska.</p>
<p>Pak už to jenom chtělo koupit niklovou lázeň, niklovou elektrodu, sehnat regulovatelný zdroj proudu, něco dalších chemikálií a zkoušet. Sláva, pokus se vydařil hned napoprvé. Upínám to do stroje, najíždím se skleněným kolečkem a… cink, kolečko prasklo. Sakra, vždyť vono to skoro vůbec nežere! Jak to? Proč? A znova hledám a ptám se. „Jo pane, ten dijámant se musí voživit,“ povídá mi jeden odborník. Asi ho mám polévat živou vodou, myslím si. „S tím se musí nejdřív zajet do karborunda, von vám vodrbe ten nikl, až začne čumět ten dijámant.“ Hotovo. Jednoduché, prosté, účinné. Radost pohledět, nástroj žere jak státní banka.</p>
<p>Brousím hlavní diferenciálové kolo. Počet zubů 57. U 55. zubu se mě zmocňuje euforie, přitlačím trochu víc a …cink. Zub je v… . No vlastně je tam celé kolo, všechna práce, protože to se nedá opravit, to musíte vyrobit celé znova. Co to znamená? Vzít rouru průměr 50 mm, pomocí speciálních kleští z grafitu (jasně, že mojí výroby, na tyhle srandičky se nic koupit nedá) vytočit polotovar budoucího kola. Připravit si osu s paprskama a vtavit ji do středu toho kola. Bacha, nesmí to, pokud možno, vůbec házet, a to ani ve směru radiálním, ani axiálním. A šup s tím do pece, aby se odstranilo pnutí. Temperační cyklus trvá 6 hodin. Když to vystydne, upne se to do stroje a obrousí na přesný vnější průměr. Pak se to upne jinak a pomocí dělícího kotouče se začnou brousit zuby znova. A hlavně klid, nic neuspěchat, a čím víc těch zubů je, tím pomaleji najíždět do záběru.</p>
<p>A pak? Sláva, potlesk, mám hotové ozubené kolečko. Na tom diferenciálu jich je, různě velkých, šest. Tak mnoho úspěchů, nebudeme vás rušit, a až to bude hotové, tak se přijďte pochlubit.</p>
''' + gal(('zadni-naprava', 'Zadní náprava auta s diferenciálem'), ('predni-naprava', 'Přední náprava'), ('paroauto', 'Hotové parní auto'), cols=3)


def gen(n, title, when, body, media=''):
    return (f'<li class="gen" id="generace-{n}"><div class="gen-no"><span>{n}.</span>generace</div>'
            f'<div class="gen-body"><h2>{title}</h2><p class="gen-when">{when}</p>{body}{media}</div></li>')


RODOKMEN = '''<p class="lead">Sklářské řemeslo se u nás v rodině dědilo nepřetržitě od roku 1775. Tady je devět generací Zahradníků tak, jak jsem je dohledal v matrikách a jak jsem je znal z vyprávění.</p>
<ol class="tree">''' + ''.join([
    gen(1, 'Franciscus Zahradnik', '1. polovina 18. století, Morava, okolí Buchlovic',
        '<p>Někdy v první polovině 18. století, v zemi Moravské, v okolí Buchlovic, žil jistý muž jménem Franciscus Zahradnik a byl… čím vlastně byl? O jeho existenci se dozvídám až z rodného listu jeho syna, kde se o něm píše: „socius ex officina“, čili „společník z dílny“.</p>'
        '<p>Tak tedy jemu a jeho ženě Francisce se v obci Altehütten, číslo 29, narodil syn Franciscus.</p>'),
    gen(2, 'Franciscus', 'narozen 17. 4. 1775, Altehütten',
        '<p>Stalo se tak 17. 4. 1775. A život šel dál. Franciscus se stal sklářem, vzal si za ženu, jistě krásnou a pracovitou, Agnes, dceru Paula Heppecka, a 20. 3. 1815 se jim narodil syn, jemuž dali jméno Benedikt.</p>',
        gal(('2-generace', 'Matriční záznam — 2. generace'), cols=4, cls='docs')),
    gen(3, 'Benedikt', 'narozen 20. 3. 1815',
        '<p>A historie se opakuje. Z Benedikta se stává sklář a za ženu pojme sličnou Julianu. Jim se pak ve Starých Hutích č. 11, dne 2. 4. 1843, narodil syn František.</p>',
        gal(('3-generace', 'Matriční záznam — 3. generace'), cols=4, cls='docs')),
    gen(4, 'František', 'narozen 2. 4. 1843, Staré Hutě',
        '<p>Jak šel čas, tak i František našel zalíbení nejen ve skle, ale i v moudrých ženách, seznámil se s Marií, dcerou hostinského ve Staré Huti, a přesídlili o kousek dál do Stupavy. A tam, 23. 12. 1869, se jim narodil syn Emanuel.</p>',
        gal(('4-generace', 'Matriční záznam — 4. generace'), cols=4, cls='docs')),
    gen(5, 'Emanuel', 'narozen 23. 12. 1869, Stupava',
        '<p>Jo, Emanuel. O něm jsem již něco zaslechl z vyprávění mého dědy. Protože sklárny ve Staré Huti krachovaly a práce bylo stále méně a méně, tak Emanuel se svojí ženou Marií, rozenou Šlauzarovou, přesídlili do Vídně. Ve Vídni si otevřel sklárnu a dokonce se v oboru sklofoukač stal i soudním znalcem.</p>'
        '<p>Na svou dobu byl vyšší postavy, vzpřímené chůze a s mohutným knírem. A jak mi děda vyprávěl, tak při nedělních vycházkách po Vídni vzbuzoval takový respekt, že mu i policisté salutovali.</p>'
        '<p>Na fotce je vyfocen se svým vnukem Pavlem (o něm se tu ještě také zmíním, je to totiž můj otec). Fotografie byla pořízena v roce 1943, kdy mu bylo již 74 roků. Vedle stojícímu Pavlovi bylo v té době 18 a byl právě vyučeným sklofoukačem.</p>'
        '<p>Rodičům se pak ve Vídni, dne 20. 8. 1896, narodil syn, jehož pokřtili Franz-Maria.</p>',
        gal(('praded', 'Emanuel s vnukem Pavlem, 1943'), ('5-generace', 'Matriční záznam — 5. generace'), cols=4, cls='docs')),
    gen(6, 'Franz-Maria', 'narozen 20. 8. 1896, Vídeň',
        '<p>Franz-Maria… pro mě to byl Spořilovský děda. V mých dětských očích laskavý děda, který mi vysvětloval, jak funguje parní stroj, jak se má štípat a sekat dříví, aby nebylo krvavé, a mnoho dalších, pro život potřebných věcí. Tak tenhle děda, v dobách, kdy ještě vůbec nebyl otcem a natož dědou, se jednoho dne nasytil té roztomilé despotické povahy svého otce Emanuela a utek do Prahy. Tady si v Lipové ulici otevřel sklářskou dílnu a jal se provozovat sklářské řemeslo.</p>'
        '<p>Na fotce z roku 1926 je právě ve své dílně v Lipové ulici v Praze. A tady je i článek z roku 1940, ve kterém děda vypráví o své práci.</p>',
        gal(('deda', 'Děda ve své dílně v Lipové ulici, 1926'), ('deda-v-novinach', 'Sklář ve službách lékařské vědy — článek z roku 1940'), ('6-generace', 'Matriční záznam — 6. generace'), cols=4, cls='docs')),
    gen(7, 'František a Pavel', 'narozeni 21. 11. 1924 a 8. 3. 1927',
        '<p>Zástupci sedmé generace jsou dva bratři. František, narozený 21. 11. 1924, zde na fotce z 19. 10. 1954, a Pavel, můj otec, narozený 8. 3. 1927. Ta fotka je někdy z roku 1957.</p>',
        gal(('strejda', 'František, 19. 10. 1954'), ('tata', 'Pavel, můj otec, kolem roku 1957'), ('7-generace', 'Rodný list — 7. generace'), cols=4, cls='docs')),
    gen(8, 'Michal', 'narozen 12. 4. 1957, Praha',
        '<p>No a tady jsem již já. Narozen 12. 4. 1957 v Praze. V letech 1972–1975 jsem se vyučil foukačem technického skla ve sklárnách Kavalier v Sázavě. Po vyučení jsem byl zaměstnán v Chiraně Modřany, ve Výzkumném ústavu makromolekulární chemie a v ČKD Polovodiče na Pankráci. Od roku 1988 jsem, s povolením Národního výboru, začal soukromě podnikat a činím tak dodnes. V letech 1984–1989 jsem absolvoval elektrotechnickou průmyslovku v Praze Nuslích, obor regulace a měření.</p>'
        '<p>Další informace naleznete v sekci <a href="~/jak-to-zacalo/">Mé sklářské začátky</a>.</p>',
        gal(('pri-praci3', 'Při práci nad kahanem'), cols=4, cls='docs')),
    gen(9, 'Jitka a Jan', 'narozeni 10. 2. 1987',
        '<p>Devátou generaci zastupují dvojčata Jitka a Jan, narození 10. 2. 1987. Ovšem jak se zdá, jejich zájmy jdou jinou cestou a se mnou pravděpodobně naše sklářská tradice končí…</p>'),
]) + '</ol>' + f'''
<p class="note">Zájemce o širší rozsah mého rodokmenu pak odkazuji na stránku MyHeritage: {ext('https://www.myheritage.cz/site-family-tree-22597601/zahradnik', 'myheritage.cz/site-family-tree-22597601/zahradnik')}</p>'''

SKOLY = f'''
<p class="kicker">Sklo kolem nás</p>
<p class="lead">Jmenuji se Michal Zahradník, jsem vyučený technický sklofoukač, představitel prakticky jednoho z nejstarších sklářských rodů v Čechách. Sklářské řemeslo se u nás v rodině dědilo nepřetržitě od roku 1775 a já jsem již osmou generací sklářů, s více než padesátiletou praxí. S některými svými výrobky jsem zapsán i v českém vydání Guinnessovy knihy rekordů.</p>
<p>Pro vaši školu vám nabízím dvouhodinovou přednášku o skle provázenou praktickými ukázkami tvarování skla nad kahanem. Přednáška je cílená pro žáky školek, základních škol, táborů a podobně.</p>

<div class="facts">
  <div><dt>Délka</dt><dd>2 × 45 minut na jednu třídu</dd></div>
  <div><dt>Za jeden den</dt><dd>až 4 cykly pro čtyři třídy</dd></div>
  <div><dt>Cena</dt><dd>do 40 dětí paušálně 5 000 Kč,<br>každé další dítě 100 Kč</dd></div>
  <div><dt>Cestovné</dt><dd>8 Kč/km</dd></div>
</div>

{gal(('pri-praci2', 'Přednáška ve třídě'), ('pri-praci1', 'Děti u pracoviště'), ('pri-praci3', 'Ukázka tvarování skla nad kahanem'), ('pracoviste', 'Mobilní pracoviště'), cols=4)}

<p>S obsazením samostatně jedné třídy na jednu dvouhodinovku (2 × 45 min). Takto je možné během jednoho dne provést na vaší škole až 4 cykly pro čtyři třídy.</p>
<p>Při částečném zredukování teoretické části lze přednášku realizovat i pro děti předškolního věku. Z praxe je zřejmé, že již děti od tří let věku jsou schopny si skleněnou kuličku nafouknout. U mladších pak bývá hlavním problémem utěsnění rtů okolo trubičky, takže funí sice pěkně, ale všude okolo…</p>
<p>Nespornou výhodou menšího kolektivu v rámci jedné třídy je individuální přístup ke každému žákovi.</p>
<p>Ovšem v případě, že je málo času a hodně dětí, lze provést i variantu, kdy moji přednášku, cca 35 minut, provedu pro všechny děti najednou, třeba v tělocvičně, a pak si chodí postupně foukat kuličky, bez ohledu na přestávky. Tak to pak za 60 minut stihne cca 35–45 dětí.</p>
<p>Zájem dětí o toto řemeslo je značný. Jejich pokusy o vyfouknutí skleněné kuličky jsou kvůli bezpečnosti prováděny tak, že sám sklo roztavím na patřičnou teplotu a oni pouze foukají. Protože vím, že se to leckdy na první pokus nepovede, tak si to zkusí znova, tak, aby si každý mohl svůj výtvor odnést domů.</p>

<div class="cols">
  <section>
    <h2>Stručný obsah přednášky</h2>
    <ul class="dash">
      <li>Historie skla, první nálezy, báje a pověsti.</li>
      <li>Definice a složení skla, jeho druhy a oblasti využití.</li>
      <li>Vlastnosti mechanické, chemické, optické.</li>
      <li>Sklo v přírodě. Vltavín, obsidián, fulgurity, pemza.</li>
    </ul>
  </section>
  <section>
    <h2>Praktické ukázky</h2>
    <ul class="dash dash--2">
      <li>Pnutí ve skle</li><li>Lepivost žhavého skla</li><li>Tepelná vodivost</li><li>Skleněná nit</li>
      <li>Skleněná pružina</li><li>Skleněný „papír“</li><li>Tažení</li><li>Foukání</li>
      <li>Mačkání</li><li>Stříhání nůžkami</li><li>Mimořádné vlastnosti křemenného skla</li><li>Broušení skla</li>
      <li>Praktické vyzkoušení foukání skla samotnými žáky</li>
    </ul>
  </section>
</div>

<p>Moje pracoviště je plně mobilní, jeho příprava trvá cca 20 minut a jsem zcela soběstačný. Můžu vystupovat přímo ve třídě a můj pracovní prostor zaujímá přibližně 2 × 2 m. Pro zajištění vyšší bezpečnosti používám maloobjemové lahve s PB a kyslíkem.</p>
<p>Z hygienických důvodů má každé dítě svoji vlastní trubičku k foukání, která byla předtím umyta v desinfekci.</p>
<p class="note">Školy nyní realizují své projekty v šablonách z Operačního programu Jan Amos Komenský. Záznamy z projektových dnů se už vyplňovat nebudou.</p>

<section class="box box--order">
  <h2>Pro objednání potřebuji vědět</h2>
  <ol class="check">
    <li>Adresu školy.</li>
    <li>Kontaktní osobu.</li>
    <li>Den konání (nutno dohodnout předem) — viz plánovací kalendář.</li>
    <li>Časový rozvrh (v kolik hodin má začít první přednáška).</li>
    <li>Počet tříd.</li>
    <li>Kde se učebna nachází. (Vybavení váží cca 70 kg, tak abych počítal s potřebným časem k jeho instalaci. 10. patro bez výtahu mě, pravda, potrénuje, ale když sotva dechu popadám, tak toho moc nenamluvím a nenafoukám… :D)</li>
    <li>Přibližný počet žáků.</li>
  </ol>
  <p>V plánovacím kalendáři si vyberete vám vyhovující volný termín. Máte-li zájem o více dní, prosím, označte si je všechny. Následně ode mě dostanete potvrzující e-mail.</p>
  <p class="btns"><a class="btn" href="http://folkcraft.eu/zahradnik/" target="_blank" rel="noopener">Otevřít plánovací kalendář</a> <a class="btn btn--ghost" href="mailto:sklozam@gmail.com?subject=P%C5%99edn%C3%A1%C5%A1ka%20o%20skle">Napsat e-mail</a></p>
</section>

<p><a href="~/akce-pro-skoly/reference-tabulka/">Seznam škol a školek, které jsem již navštívil →</a></p>
'''

KALENDAR = '''
<p class="lead">Zde máte k dispozici plánovací kalendář, kde si vyberete vám vyhovující volný termín pro konání přednášky. Máte-li zájem o více dní, prosím, označte si je všechny. Následně ode mě dostanete potvrzující e-mail.</p>
<section class="box box--order">
  <p>Kalendář běží na samostatné stránce. Před prvním vstupem vás požádá o jednoduché ověření (součet dvou čísel).</p>
  <p class="btns"><a class="btn" href="http://folkcraft.eu/zahradnik/" target="_blank" rel="noopener">Otevřít plánovací kalendář</a> <a class="btn btn--ghost" href="~/akce-pro-skoly/">Co potřebuji k objednání</a></p>
</section>
'''

SCHOOLS = [s.strip() for s in '''ZŠ Chodov, Praha 4|ZŠ Kostelec nad Černými lesy|ZŠ Český Brod|ZŠ Psáry|ZŠ Tupolevova, Praha 9|ZŠ Donovalská 1684|R-mosty|ZŠ Zbraslav-Hauptova|ZŠ Veliký Brázdim|ZŠ Nad Kavalírkou|ZŠ Nad Vodovodem 460, Praha 10|ZŠ Roztoky u Prahy|ZŠ Karla Klíče, Hostinné|ZŠ Jiřího z Lobkovic|ZŠ Bítovská|MŠ Semínko|ZŠ Bílá|ZŠ Na Planině|ZŠ Perunova|MŠ U Santošky|ZŠ Waldorfská, Butovická 228/9, Praha 5|ZŠ TGM Bělohorská, Praha 6|Anglická školka, Zbraslav|Rodinné centrum PEXESO, Zbraslav|ZŠ a MŠ Na Karlově, Benešov|ZŠ Hostivař, Praha 10|DALMATEENS|Dobrovolnické centrum Lékořice|MŠ Peroutkova, Praha 5|ZŠ a MŠ Mirošov|ZŠ Litvínovská 600|ZŠ Malostranská|ZŠ Kolín III|FZŠ profesora Otokara Chlupa|ZŠ Jesenice u Prahy|Stanice přírodovědců, Praha 5|ZŠ Ratibořická|ZŠ Unhošť|ZŠ Jeseniova|ZŠ Rudná, 5. května|ZŠ Montessori Kladno|ZŠ Pražačka|MŠ Stachova|ZŠ Petrovice|ZŠ Kolín IV|ZŠ Tuchlovice|MŠ Blatenská|ZŠ Kladno-Amálská 2511|ZŠ Mikulova|Hobby Centrum Pankrác, Praha 4|ZŠ Kladno, Vodárenská 2115|ZŠ Satalice|ZŠ praktická a ZŠ speciální - Lužiny|ZŠ Ke Kateřinkám 1400, Praha 4|ZŠ Vokovice|MŠ Hrabákova, Praha|ZŠ Dobřichovice|ZŠ Mníšek pod Brdy|ZŠ Jánošíkova, Praha 4|Knihovna Rakovník|ZŠ Tyršova, Nymburk|ZŠ Říčany|ZŠ a MŠ Červený vrch, Alžírská 680|ZŠ Neratovice|ZŠ Litoměřice|ZŠ a MŠ Kladno|ZŠ Dolany|ZŠ Šeberov|MŠ Hřibská|ZŠ Ruzyně|ZŠ Jílovská|ZK Aero Odolena Voda|ZŠ Nám. Českého povstání|ZŠ Nebušice|MŠ Sedlčanská|ZŠ a MŠ Lužec n. Vlt.|ZŠ Odolena Voda|3. ZŠ Slaný|Gymnázium Mikulov|ZŠ Kladská|ZŠ Lovosice|ZŠ Vrdy|ZŠ Břečťanová|ZŠ Průhonice|ZŠ Zvole|ZŠ Kolovraty|ZŠ Jánského|ZŠ Gutova|ZŠ Tuchlovice|ZŠ Angel|ZŠ Újezd nad Lesy|ZŠ Litoměřice B. Němcové|ZŠ Údlice u Chomutova|ZŠ Komenského Praha|ZŠ Komenského Karlovy Vary|MŠ Meziškolská|ZŠ Ústí nad Labem|ZŠ Všetaty|ZŠ Mnichovice|ZŠ Rakovník 2|ZŠ Sezimovo Ústí|MagicHill Říčany|MŠ Rohožník|MŠ Černošice|ZŠ Kadaň|MŠ Plamínkové|MŠ Kotorská|MŠ Voráčovská|ZŠ Žamberk|ZŠ Čakovice|ZŠ Písnická|ZŠ Jakutská|ZŠ Brandýsek|Křížová vila Žatec|ZŠ Palmovka|FZŠ Táborská|ZŠ Radim|ZŠ Poříčany|ZŠ Pchery|ZŠ Bráník, Školní 700|ZŠ Horáčkova|ZŠ TGM Velim|ZŠ Zlatníky|ZŠ Mráčkova Praha 4|ZŠ Kunratice|MŠ Babákova|ZŠ E. Přemyslovny Brno|ZŠ Bystřice|ZŠ Lyčkovo nám.|ZŠ Úvaly u Prahy|MŠ Vodnická|Centrum kultury Ostrava|MŠ Mikulov|ZŠ Resslova|ZŠ Libčice nad Vltavou|MŠ Pečky|ZŠ Jirny|Muzeum hl. m. Prahy|ZŠ Příbram - Jiráskovy sady|ZŠ Příbram - 28. října|ZŠ Příbram - Bratří Čapků|ZŠ Tatce|ZŠ Vratislavova, Praha 2|ZŠ Radotín|ZŠ Rynoltice|ZŠ Žíželice|ZŠ Pod Marjánkou, Praha 6|ZŠ Roudnice nad Labem|ZŠ Lipence|ZŠ Mirotice|MŠ Čestlice|MŠ Psáry|MŠ Přezletice|ZŠ Veltrusy|EducaNet Praha 4|ZŠ Kbely|ZŠ Velký Osek u Kolína|ZŠ Všenory|ZŠ Suchdol u Kutné Hory|Centrum kultury Ostrava|MŠ Záboří|MŠ Podlesí|ZŠ Vojtěšská|MŠ Janákova|ŠD JAK Louny|ZŠ a MŠ Fryčovická|ZŠ Meteorologická|ZŠ Jinočany|ZŠ U Obory|ZŠ Řevnice|ZŠ Botičská|ZŠ Kladno|ZŠ Skořenice|ZŠ Hlásná Třebáň|ZŠ Krupka|MŠ Riegrova, Děčín|ZŠ Vorlina, Vlašim|ZŠ Brno, Bosonožská|ZŠ Charlotty Masarykové, Chuchle|ZŠ Hradištko|ZŠ Písek - Svobodná|MŠ Libocká|ZŠ Waldorfská - Příbram|MŠ Malkovského|MŠ Jenštejn|MŠ Příbram, Školní|MŠ Volavkova|ZŠ Chroustníkovo Hradiště|ZŠ Jarov|MŠ Mratín'''.split('|')]

NAVSTIVENE = (f'<p class="lead">Školy, školky a další místa, kde jsem už povídal o skle a kde si děti foukaly své první kuličky. Celkem {len(SCHOOLS)} návštěv, seřazeno od nejstarší.</p>'
              '<ol class="schools">' + ''.join(f'<li>{html.escape(s)}</li>' for s in SCHOOLS) + '</ol>'
              '<p><a href="~/akce-pro-skoly/">← Zpět na nabídku pro školy</a></p>')

TRHY = '''
<p class="kicker">Prodejní stánek — pojízdná sklárna</p>
<p class="lead">Prakticky od počátku mého podnikání, od roku 1988, jsem své výrobky prodával na různých tržištích. Od roku 1992 jsem pak prodej rozšířil i o předvádění výroby.</p>
''' + gal(('stanek-1', 'Pojízdná sklárna — stánek jako přívěs za auto'), ('stanek-2', 'Předvádění výroby na trhu'), cols=2) + '''
<p>Nejprve v plátěném stánku, ale kvůli problémům s větrem a některými návštěvníky se stabilita plátěného stánku jevila jako nedostatečná. Proto jsem si navrhl a sestrojil dílnu jako přívěs za auto. Pro profesionální práci je potřeba i profesionálního zázemí stabilního a dobře vybaveného stánku.</p>
<p>Pro provoz sklářského pracoviště a zpracování skloviny SIMAX je zapotřebí kromě propan-butanu i kyslík a v některých situacích i stlačený vzduch. Dále, vzhledem k prašnosti prostředí na trhu, je pro mě nezbytné si z rukou smývat prach, aby mi sklo v rukou „neklouzalo“.</p>
<p>Celá konstrukce je podřízena požadavku, aby byla přijatelná i pro historické řemeslné trhy u nás i v zahraničí a zároveň umožňovala předvádět zpracování skla foukáním nad kahanem. Dalšími požadavky pak je dobrá stabilita ve větru, pracoviště v závětří a ochrana před deštěm. V neposlední řadě pak možnost ve stánku přebývat při vícedenních akcích.</p>
<p>Součástí mého předvádění práce sklofoukače je pak možnost sklářské dílny pro děti a dospělé. Ukážu jim, jak si mohou zkusit nafouknout skleněnou kuličku, a tu si pak odnesou s sebou domů.</p>

<section class="box">
  <h2>Pro pořadatele</h2>
  <div class="facts facts--plain">
    <div><dt>Stánek</dt><dd>3 × 2 m, s ojí potřebuji plochu 4 × 2 m</dd></div>
    <div><dt>Výška a váha</dt><dd>2,5 m, cca 750 kg</dd></div>
    <div><dt>Příjezd</dt><dd>přívěs za osobním autem — žádné schody na cestě, obrubník nevadí; prosím o co nejrovnější terén</dd></div>
    <div><dt>Elektřina</dt><dd>není nezbytná, je-li k dispozici, stačí 230 V / 100 W na osvětlení a malý kompresor</dd></div>
  </div>
</section>
'''

MODELY_INTRO = '''
<p class="lead">Na podzim roku 1991 jsem si začal hrát s konstrukcí pohyblivých skleněných modelů. Na rozdíl od klasické výroby laboratorního skla vyžaduje tato činnost hledání nových postupů při výrobě a zejména pak při přípravě různých přípravků, bez kterých se neobejdu.</p>
<p>Dnes mám plné šuple různého speciálního nářadí, od jednoduchých držáčků z duralu, pertinaxu, grafitu a podobně, až po poměrně složité grafitové tvarovací kleště a diamantové brusné nástroje. O jejich výrobě se zmiňuji v sekci <a href="~/jak-to-zacalo/">Mé sklářské začátky</a>. Dá se říci, že vymýšlení a výroba přípravků zabrala na některých modelech až 5× více času než samotná výroba. Jedinou výhodou ale je, že se ve většině případů dají použít i k výrobě dalších částí při konstrukci jiných modelů.</p>
<div class="models">''' + ''.join(
    f'<a class="model" href="~/sklenene-modely/{s}/"><span class="model-img"><img src="{img(i)}" alt="{t}" loading="lazy"></span>'
    f'<span class="model-t">{t}</span><span class="model-d">{d}</span></a>' for s, t, i, d in MODELS) + '</div>'

MODEL_BODY = {
'prvni-jednovalcovy-parni-stroj': '''
<p class="lead">První model, který jsem začal vyrábět, byl jednoválcový, jednočinný parní stroj. Při jeho výrobě jsem použil sklářské postupy, které jsem léta používal. Jak je vidět, daly se využít prakticky na celou konstrukci.</p>
''' + fig('prvni-jednovalec2', 'První jednoválcový parní stroj', 'fig--wide') + '''
<p>Trubice na píst a šoupě jsem vybral tak, aby do sebe nešly vzájemně zasunout, a to s co nejmenším přesahem. Pak jsem na soustruhu vytočil měděný trn, na začátku, asi v délce 5 mm, s mírným kuželem. Tímto přípravkem jsem pak s CITEM, za pomoci volně vázaného brusiva s vodou, postupně vybrušoval vnitřní plochu válce. Když bylo vybroušení válce hotové, tak jsem začal vyrábět píst. Nejdříve jsem si do tvarovacích grafitových kleští rozfoukl trubici na průměr o cca 0,5 mm větší, než byl otvor ve válci. Do této trubice jsem následně vtavil pístní čep s již předem připravenou ojnicí. Tento komplet jsem pak, nejdříve nahrubo, zabrousil za použití měděného trnu s přesným vnitřním průměrem. Následně jsem pak píst načisto za pomoci jemného brusného prášku zabrousil do válce. Když bylo zabroušeno, tak jsem píst odřízl na délku 30 mm.</p>
<p>Podobným způsobem jsem pak vyrobil i šoupě.</p>
<p>Po kompletaci jsem začal „ladit“. To znamená, že jsem přihýbáním excentru pro pohon šoupěte zkoušel optimální postavení oproti pístu, aby se válec začal plnit ve správný okamžik, ale zároveň, aby ve správný okamžik došlo k uzavření přívodu páry a naopak, aby ve správný okamžik došlo k uvolnění tlaku nad pístem. Tohle „ladění“ trvalo asi dvě hodiny, a bez úspěchu. Důvodem bylo, že jsem odvzdušňovací otvor udělal příliš krátký. Zkušenost získaná chybou konstrukce mě donutila celé šoupě udělat znova.</p>
<p>Hrál jsem si s tím asi do 2 hodin do rána, za vydatné podpory mých přátel radioamatérů, kteří mi na krátké i velké vzdálenosti drželi palce.</p>
<p>A pak přišel ten OKAMŽIK. Připojil jsem hadičku s tlakovým vzduchem, dal impulz setrvačníku a parostroj se rozběhl.</p>
''' + yt('o0zu4fraMlM', 'První funkční jednoválcový parní stroj'),

'druhy-jednovalcovy-parni-stroj': '''
<p class="lead">Poučen předcházejícími chybami, jsem začal přemýšlet o jiné konstrukci, která by byla „čistší“ jak z hlediska řemeslného, tak i funkčního.</p>
''' + gal(('novy-jednovalec2', 'Druhý jednoválcový parní stroj'), ('novy-jednovalec3', 'Detail'), ('novy-jednovalec1', 'Konstrukce'), cols=3) + '''
<p>Jednak jsem zvětšil velikost setrvačníku z původních 95 mm na 127 mm, abych získal větší hybnost. Také jsem zmenšil průměr šoupěte z 10 mm na 7 mm, abych snížil škodlivé protitlaky. Další změna byla v uložení klikovek od pístu a šoupěte. Obě jsem umístil co nejblíže k setrvačníku, aby se co nejvíce snížily krutné síly potřebné k jejich pohonu. Dále jsem předělal uchycení pístního čepu, takže již není pevně vtaven, ale do pístu jsou vyvrtány otvory, kudy čep prochází. Tím jsem získal i možnost ojnici v pístu vycentrovat pomocí krátkých trubiček, takže ta se tam již nemohla pohybovat ze strany na stranu.</p>
<p>Ovšem největší a podstatné změny jsem docílil tím, že jsem si vyrobil diamantové vybrušovací nástroje. O tom, jak jsem je vyráběl, se zmiňuji ve stati <a href="~/jak-to-zacalo/">Mé sklářské začátky</a>.</p>
''' + yt('V9DIPqyieXg', 'Tady je vidět, jak to běží na vzduch') + '''
<p>A jak již to tak bývá, každý pokrok musí být náležitě potrestán, a tak i broušení diamantem se ráčilo projevit. Bohužel až na závěr, kdy bylo vše sestaveno a na vzduch běhalo vše krásně lehce. Ovšem v okamžiku, kdy jsem použil páru, tak vlivem roztažnosti se začal píst roztahovat víc než válec, který byl zvenku ochlazován. Tím pádem se to začalo přidírat, až došlo k úplnému zastavení. Takže jsem byl nucen všechny pohybující se části ještě vzájemně dobrousit jemným brusivem hrubosti 600.</p>
''' + yt('73txXT21aZU', 'A tady to běhá již na páru') + '''
<p>Tříminutové video výroby parního stroje ze skla v sestříhané a zrychlené verzi najdete na <a href="~/">úvodní stránce</a>.</p>''',

'trivalcova-lokomotiva': '''
<p class="lead">Protože jednoválcový parní stroj ke své funkci potřebuje setrvačník k překonání „mrtvého“ chodu, tak při konstrukci skleněné lokomotivy jsem použil tří válců, jejichž pracovní úhly jsou posunuty po 120°.</p>
''' + gal(('trivalec-loko', 'Tříválcová lokomotiva'), ('trivalec1', 'Pohled z boku'), ('trivalec2', 'Pohled shora'), ('trivalec-detail-soupe', 'Detail pohonu šoupat'), ('trivalec3', 'Konstrukce'), cols=3) + '''
<p>A vzhledem k tomu, že napojení ojnic pístů a pohonu šoupat v jedné rovině by neúměrně prodloužilo délku hnané nápravy, zvolil jsem odvození pohybu šoupat zcela originálním způsobem. Mimochodem, tato konstrukce byla nejvíce obdivována na desítkách výstav parních strojů u nás i ve světě, protože na kovových modelech se s tímto řešením nikdo doposud nesetkal.</p>
<p>Ale opět se projevila závada. Tentokrát v tom, že kondenzující mokrá pára po několika okamžicích začne zvyšovat třecí odpor na vodítkách šoupat a lokomotiva se zastaví. Proto ji můžete vidět v běhu pouze na vzduch:</p>
''' + yt('zA0YYbQdwbE', 'Funkční tříválcová lokomotiva ze skla'),

'stephensenova-lokomotiva': '''
<p class="kicker">Stephensonova lokomotiva z roku 1829</p>
<p class="lead">Povzbuzen neúspěchy předchozích konstrukcí jsem se vrhl na další model. K jeho vytvoření mě vedla poznámka organizátora, na návštěvě výstavy parních strojů v Malchowě v Německu, že bych měl vyrobit nějaký funkční model pro rozchod modelové železnice 127 mm.</p>
''' + gal(('stefina1', 'Stephensonova lokomotiva'), ('stefina-parou', 'Lokomotiva v provozu'), ('stefina-spodek', 'Pohled zespodu — přední osa'), ('stefina2', 'Konstrukce'), cols=2) + '''
<p>Základem se mi staly osvědčené válce a šoupata z předchozích modelů. Kvůli přibližné podobě jsem tentokrát použil jenom dva válce. Nakonec se to projevilo jako dostačující, protože pohybová energie modelu zastoupila setrvačník. Větším konstrukčním problémem byla ale samotná přední osa. Vyosení excentrů je po 180° pro válce, dále po 180° pro šoupata, ale ty musí být zase úhlově posunuty o 45° vzhledem ke vzájemné nesouosé pozici. Navíc celá osa měla již přitavená kola, ojnice pro šoupata a ložiskovou přípravu pro rám lokomotivy. Ač se to nezdá, tak tento díl je ze všech mých modelů jeden z nejobtížnějších.</p>
<p>Protože konstrukce neumožňovala použít přehřívanou páru, kdy se čerstvá pára vede ještě jednou skrz topeniště, aby se docílilo vyšší teploty, a přívody k šoupátkům a následně k válcům byly dost dlouhé, vykazovala lokomotiva při provozu zajímavý efekt. Dokud na ni svítilo sluníčko, tak jela, ale ve stínu se díky kondenzaci vody zastavovala. Problém jsem pak vyřešil omotáním přívodního potrubí azbestovou šňůrou jako izolací. Po této úpravě již lokomotiva jezdila i ve stínu :D</p>
''' + yt('csHM0MuDwqo', 'Jízda skleněné Stephensonovy lokomotivy po kolejích') + '''
<div class="award">''' + fig('cert-lok', 'Certifikát o vytvoření českého rekordu') + '''<p>Lokomotivě byl dne 27. 11. 2002 vystaven <strong>certifikát o vytvoření českého rekordu</strong>.</p></div>''',

'auto': '''
<p class="lead">Na počátku byla snaha vyzkoušet nové konstrukční prvky a možnosti. Proto jsem se rozhodl, jako prototyp, nejdříve udělat auto na pohon elektromotorem. Na něm jsem si chtěl ověřit výrobu kulových čepů, skleněných pružin, kardanu (kvůli nutnému zalomení hřídele řízení) a diferenciálu. O výrobě diferenciálu se okrajově zmiňuji v části <a href="~/jak-to-zacalo/">Mé sklářské začátky</a>.</p>
''' + fig('elektroauto', 'Prototyp na elektromotor', 'fig--wide') + '''
<p>K ovládání jsem použil dvoukanálovou soupravu. Pro tlumení nárazů jsem si pneumatiky odlil z kaučuku. Auto na nich dosáhlo bez problému rychlosti asi 15 km/h.</p>
<h2>Přední náprava</h2>
''' + fig('predni-naprava', 'Přední náprava', 'fig--right') + '''
<p>Jako vzor jsem použil konstrukci modelu Buggy. Výroba nebyla ani moc složitá, protože jsem jenom kopíroval a mírně se přizpůsoboval originálu. První složitější věc byla výroba pružin. Zkoušel jsem je vinout z různě silných tyčinek na různé grafitové trny. Požadavkem bylo, aby měly dostatečnou pružnost a aby bez prasknutí šly stlačit o cca 15 mm. (V praxi jsem počítal se zdvihem 10 mm, tak aby byla spolehlivá rezerva.) No, navinul jsem jich asi 50, než jsem našel optimální poměr mezi průměrem tyčinky, průměrem trnu a schopností přežít těch 15 mm stlačení. Celkový zdvih na konci ramen je pak asi 20 mm a natáčení kol asi 40° na každou stranu.</p>
''' + yt('TaEAJ27Q0Lk', 'Jak funguje přední náprava') + '''
<h2>Zadní náprava</h2>
''' + fig('zadni-naprava', 'Zadní náprava s diferenciálem', 'fig--right') + '''
<p>Tak to již byl větší oříšek. Původně jsem ani diferenciál dělat nechtěl, ale pak mi došlo, že budu muset tak jak tak udělat převodovku, čili vyrábět ozubená kola ze skla, a tak proč nevyrobit rovnou k tomu ten diferenciál. Nemá cenu zde popisovat ty desítky hodin pokusů a omylů, vylomených zubů (naštěstí jen těch skleněných) a nových začátků. Nakonec se dílo podařilo.</p>
''' + yt('WS7p7NEUXes', 'Zadní náprava s diferenciálem') + '''
<p>A pak již jen zbývalo to všechno spasovat dohromady, zabrousit, co se vzájemně pohybuje, nabít baterky a vyjet. Tím byla hotova první část mé představy.</p>
<h2>Na páru</h2>
<p>Tou druhou bylo nahradit elektromotor parním strojem. K tomu jsem použil již spolehlivou konstrukci válce a šoupěte z předcházejících modelů. Dále jsem dodělal topeniště a mohlo se vyrazit.</p>
''' + fig('paroauto', 'Parní auto', 'fig--wide') + yt('4gOjP_cq0CM', 'Jízda parního auta'),

'boxer': '''
<p class="lead">Důvodem pro výrobu boxeru byla snaha zvýšit výkon pro parní auto, které popisuji v části <a href="~/sklenene-modely/auto/">Auto</a>. Výroba sama v sobě neskrývala žádné komplikace, ale výsledek nebyl nic moc.</p>
''' + gal(('boxer', 'Boxer'), ('boxer-bok1', 'Z boku'), ('boxer-strana', 'Ze strany'), ('boxer-vrch', 'Shora'), cols=2) + '''
<p>Motor se velmi obtížně vyvažuje a při běhu se chová jako zdivočelé Kango k bourání betonu. Ponechal jsem jej z čisté nostalgie, i když jsem párkrát uvažoval o tom, že jej rozeberu na náhradní díly. Tím bych vyzískal dva válce a dvě šoupata a nějakých 50 hodin práce.</p>
''' + yt('MqOh76PGfO0', 'Běh motoru Boxer'),

'hvezdice': '''
<p class="lead">Hvězdici já osobně považuji za své vrcholné dílo. Po zkušenostech s nevydařeným <a href="~/sklenene-modely/boxer/">Boxerem</a> jsem přemýšlel nad výrobou silného motoru pro nový typ parního auta II. generace. A tak vznikla Hvězdice.</p>
''' + fig('hvezdice-detail', 'Hvězdice', 'fig--wide') + '''
<p>Před tím, než jsem ji začal vyrábět, tak jsem si dlouho lámal hlavu nad tím, jak to ti konstruktéři vyřešili, že jim u těch hvězdicových motorů všechny ojnice směřují do jednoho bodu, a přesto jim to funguje. Teprve náhoda mi to osvětlila. Byl jsem na jednom předvádění sklářského řemesla v Bückeburgu v Německu. A tam je muzeum vrtulníků, kde mají krásný, funkční řez hvězdicovým motorem. Tak jsem to nastudoval a pustil se do díla. Celý trik s ojnicemi je tak prostý, že se divím, proč jsem na to nepřišel sám. Zkrátka hvězdicové motory mají jednu ojnici pevnou a všechny ostatní jsou k ní ukotveny kyvně. Jak prosté, že. No jo, ale o to složitější pro výrobu ze skla. Když tak o tom přemýšlím, tak výroba hvězdice byla jediným výrobkem, který jsem si musel rozkreslit. Na všechny ostatní konstrukce mi stačilo si je jenom představit v hlavě.</p>
<p>Principiálně se tedy jedná o tři válce ve vzájemném postavení po 120° a o tři šoupata, také ve vzájemném postavení po 120°, ale, pozor, časované ve zpoždění o 90° za pístem. (Kdybyste tomu někdo nerozuměl, tak si z toho nic nedělejte. Když tu větu po sobě čtu, tak ji taky nechápu.)</p>
''' + gal(('hvezda-predek', 'Zepředu'), ('hvezda-zadek', 'Zezadu'), ('hvezda-bok', 'Z boku'), ('hvezdice', 'Na podstavci'), cols=4) + '''
<p>Tím jsem tedy vyčerpal popis výroby a zde se můžete pokochat jejím chodem:</p>
''' + yt('rVOtieOciU8', 'Hvězdicový motor') + '''
<p>Pěkné, že? A teď si představte, že pro moje potřeby naprosto nepoužitelné! Ptáte se proč? Tedy vězte, že objem těch tří válců je nějakých 60 ccm a abych je párou uživil, tak bych musel mít kotel jako hrom, tím pádem zvětšit celkové rozměry auta a tím pádem zvětšit jeho váhu a tím pádem bych o celý navýšený výkon zase přišel. Takže hvězdice skončila jako výstavní exponát na prkýnku a mé konstrukční představy se začaly ubírat jiným směrem.</p>''',

'ctyrvalcovy-radovy-motor': '''
<p class="lead">V únoru 2015 mi zbyl týden volna, a tak jsem se pustil do výroby dalšího modelu, který jsem již delší dobu nosil v hlavě. Po tříválcové <a href="~/sklenene-modely/hvezdice/">hvězdici</a> to byl další model, jehož konstrukci jsem si musel trochu rozkreslit.</p>
''' + fig('ctyrvalec-vykres', 'Výkres fázování pístů a časování šoupat', 'fig--wide') + '''
<p>Hlavně jsem si musel ujasnit fázování pístů a časování šoupat. Přeci jenom, klikovka je osmkrát zalomena a její úhlení není až tak snadné, abych ho dělal „naostro“. A protože všechno souvisí se vším, musel jsem si ještě nakreslit rozkmit ojnice pístů, spočítat ideální délku, a to jak vzhledem k prostoru, který mi dával vnitřní průměr válců, tak k pozici šoupátek.</p>
<p>U těchto dvou částí je rozdíl v konstrukci kyvných čepů. Zatímco u pístů je v jejich středu, tak u šoupat je na jejich koncích. Z toho důvodu u šoupat, ač mají zdvih pouhých 10 mm, jsem celkovou délku zabroušení volil 45 mm, aby nedocházelo k nežádoucímu vzpříčení jádra v plášti.</p>
''' + gal(('ctyrvalec1', 'Čtyřválcový řadový motor'), ('ctyrvalec2', 'Pohled z boku'), ('ctyrvalec3', 'Detail'), ('ctyrvalec4', 'Pohled shora'), ('podstavec', 'Na podstavci'), cols=3) + '''
<p>Zatím se můžete podívat, jak motor běhá na pohon stlačeným vzduchem.</p>
''' + yt('EPq6JHREFYk', 'Čtyřválcový řadový motor na stlačený vzduch') + '''
<p>No a aby motor něco taky poháněl, tak k němu budu časem dodělávat různá zařízení. Prvním je gril na prasátko.</p>
''' + yt('evOol3tnbLs', 'Využití motoru ke grilování čuníka'),

'letadlo': '''
<p class="lead">Do výroby skleněného letadla jsem se pustil s mým přítelem ''' + ext('https://www.hacker-model.com/', 'Karlem Hackerem') + ''', čistě jenom z hecu. Přiznávám, že kdyby nebylo alkoholu, nebylo by ani letadlo.</p>
''' + gal(('letadlo-vrch', 'Skleněné letadlo shora'), ('letadlo-motor-detail', 'Detail motoru'), ('skelet', 'Skelet'), cols=3) + '''
<p>Vzorem byl letoun Lazy Bee (líná včela), který se nám svým poměrem nosné plochy křídla k předpokládané hmotnosti zdál být ideální. Kostra je vyrobena z tyčí o průměru 5 mm. Abych dosáhl co nejmenší vzletové hmotnosti, nedržel jsem se přísně výkresu, ale konstrukci bych nazval „volným pokračováním projektu“. Protože jsem neuvažoval o zavedení do sériové výroby, tak na žádný ohyb profilu křídla jsem nevyráběl šablonu, a tudíž je vše tvarováno od oka v ruce. To má ovšem za následek, že existují drobné odchylky mezi pravou a levou stranou křídla, čímž jsem následně ztížil práci pilotovi v udržení přímého letu.</p>
<p>Zprvu jsem zvažoval použít místo tyčí trubky a tím ještě více snížit konečnou hmotnost, dosti by tím ale vzrostla pracnost, a tak jsem podlehl svojí lenosti a zůstal u tyčí. Na vysvětlenou, obecně pro práci se sklem platí, že výroba z plného materiálu je jednodušší než z dutého. Jde totiž o to, že při zpracování dutých materiálů se značně projevuje teplotní roztažnost uvnitř uvězněného vzduchu, který se rozpíná a tím nafukuje zpracovávané místo. Aby se tomu zabránilo, je třeba mít někde otvor, ale pouze jediný, kterým se dá regulovat vnitřní tlak.</p>
<section class="box">
  <h2>Technické údaje</h2>
  <div class="facts facts--plain">
    <div><dt>Délka</dt><dd>800 mm</dd></div>
    <div><dt>Rozpětí</dt><dd>1 000 mm</dd></div>
    <div><dt>Hmotnost skeletu</dt><dd>965 g</dd></div>
    <div><dt>Vzletová hmotnost</dt><dd>1 000 g</dd></div>
  </div>
</section>
<p>Původně jsme zamýšleli vybavit letadlo modelářským spalovacím motorem, pak motorem na CO2, ale protože od myšlenky výroby letadla k jeho realizaci byly asi tři roky (nejsou lidi na práci), pokročil mezitím vývoj elektromotorů a baterií značně vpřed, a tak po drobných úpravách motorového lože jsme použili elektromotor Sprint 600 a baterie NiMH 750 mAh. Jak se později ukázalo, výkon motoru byl na spodní hranici výkonu.</p>
<h2>První let</h2>
<p>Po pečlivé předletové přípravě, kterou Karel provedl doma, jsme zvažovali, jak dál. Jestli provedeme zkušební let někde stranou a v tichosti, pak sebereme střepy a půjdem do hospody zapít žal, a nebo jestli to risknem a, přesvědčeni o kvalitě své práce, poletíme naostro.</p>
<p>Nakonec jsme se rozhodli, že je lepší vše vsadit na jednu kartu, a ohlásili jsme veřejný let na den 7. června 2000, konaný na letišti v Rakovníku. Přizvali jsme zástupce agentury ''' + ext('https://www.dobryden.cz/', '„Dobrý den“') + ''' muzea rekordů a kuriozit v Pelhřimově a některá další média.</p>
''' + gal(('pred-startem', 'Před startem'), ('start', 'Start z ruky'), ('pristani', 'Po přistání'), ('letadlo-celek', 'Letadlo v celku'), cols=4) + '''
<p>Počasí toho dne snad už horší být asi nemohlo. Silný nárazový vítr dával tušit, že první let bude i posledním. První pokus byl start rozjezdem po dráze. Tady se projevil naprosto nedostatečný výkon motoru, který ve spojení s větrem nedával prakticky možnost odstartovat. Proto se Karel rozhodl, že provede start z ruky. Vyčkal chvíle, kdy nebyl větší poryv větru, a hodil. A světe, div se. Letělo to. Pravda, na nějaké povely to moc nereagovalo, protože vzápětí po hodu zase funěl vítr ze všech stran, ale díky mistrovství pilota se nakonec přece jen podařilo let usměrnit a posléze i po 9,5 s trvajícím letu přistát do trávy.</p>
<p>Škody byly nepatrné a snadno opravitelné. Byl přeražen pouze jeden nosník trupu a jedna vzpěra u motoru. Ale jinak vše v pořádku.</p>
<p>Po zkušenostech s prvním letem jsme dospěli k názoru, že je naprosto nevyhnutelné osadit silnější motor. S tím je opět spojena úprava motorového lože a současně jeho předsunutí vpřed kvůli lepšímu vyvážení. Tím se ale dostáváme již do prací plánovaných a o nich budu zase psát, až se stanou skutečností.</p>
<div class="award">''' + fig('cert-let', 'Certifikát o vytvoření českého rekordu') + '''<p>Letu skleněného letadla byl vystaven <strong>certifikát o vytvoření českého rekordu</strong>.</p></div>''',

'vsehochut': '''
<h2>Skleněná pružina</h2>
<p>Video skleněné pružiny je ''' + ext('https://www.facebook.com/video.php?v=801285146577057', 'ke zhlédnutí na Facebooku') + '''.</p>
<h2>Pijící čáp</h2>
<p>Protože klasický tvar čápa s dlouhým krkem se vyrábí již od samého počátku, tak jsem se pokoušel dát mu trochu jiný tvar. Takže to již čápa moc nepřipomíná, spíš datla. Já mu důvěrně říkám „Kejvák“.</p>
''' + fig('kejvaci', 'Kejváci — pijící ptáčci ze skla', 'fig--wide') + yt('xisxZoYq5ms', 'Kejváci v akci'),
}

OSTATNI = f'''
<p class="lead">Máte-li zájem zhlédnout pár mých dalších výrobků, odkážu vás na můj {ext('https://www.fler.cz/sklozam', 'Flér')}.</p>
<p>Budete-li mít nějaké speciální požadavky, napište mi a já se pokusím spojit vaše představy a moje možnosti.</p>
<p class="btns"><a class="btn" href="https://www.fler.cz/sklozam" target="_blank" rel="noopener">Moje výrobky na Fléru</a> <a class="btn btn--ghost" href="mailto:sklozam@gmail.com">Napsat e-mail</a></p>
'''

TECHNICKE = '''
<p class="lead">V rámci možností mé dílny vám mohu nabídnout výrobu a opravu laboratorního a technického skla.</p>
<p>Dejte mi vědět, jaké jsou vaše požadavky, a pokusíme se je realizovat s mými možnostmi.</p>
<p class="btns"><a class="btn" href="mailto:sklozam@gmail.com?subject=Technick%C3%A9%20sklo">Napsat e-mail</a> <a class="btn btn--ghost" href="tel:+420608969213">+420 608 969 213</a></p>
'''

DIPLOMY = '<p class="lead">Certifikáty, diplomy a pamětní listy z výstav a setkání u nás i v zahraničí.</p>' + gal(
    ('cert-let', 'Let skleněného letadla — český rekord'),
    ('cert-lok', 'Skleněný parní stroj — český rekord'),
    ('sklenena-pruzina', 'Skleněná pružina — český rekord'),
    ('rr', 'Rekordman roku 2005'),
    ('diplom-sobotka', 'Originální výrobek v Sobotce'),
    ('hettstedt', 'Výstava v Hettstedtu'),
    ('hk2004', 'Nábřeží Paromilů 2004'),
    ('paromil-2004', 'Nábřeží Paromilů 2004'),
    ('paromil-2005', 'Nábřeží Paromilů 2005'),
    ('paromil-2006', 'Nábřeží Paromilů 2006'),
    ('paromil-2007', 'Nábřeží Paromilů 2007'),
    ('paromil-2008', 'Nábřeží Paromilů 2008'),
    ('paromil-2011', 'Nábřeží Paromilů 2011'),
    ('polsko', 'Předvádění řemesla v Polsku'),
    cols=4, cls='gal--docs')

SPRATELENE = f'''
<ul class="friends">
  <li><strong>Broušení skla do škol.</strong> Máte-li zájem si do školy pozvat špičkového brusiče skla, aby vašim dětem ukázal, jak se sklo brousí, a aby si to mohly také vyzkoušet, obraťte se na pana Petra Bílka.</li>
  <li><strong>Řemeslné akce.</strong> Hledáte-li přehledný seznam řemeslných akcí, navštivte {ext('http://www.webtrziste.cz', 'www.webtrziste.cz')}.</li>
</ul>
'''


# ---------- struktura webu ----------
# (cesta, položka v menu, titulek stránky, popis, obsah, rodič)
PAGES = [
    ('', 'Úvod', 'Michal Zahradník — sklář, skleněné modely', 'Stránky jednoho z nejstarších sklářských rodů v Čechách. Pohyblivé skleněné modely parních strojů, rodokmen od roku 1775 a přednášky o skle pro školy.', HOME, None),
    ('jak-to-zacalo', 'Mé sklářské začátky', 'Mé sklářské začátky', 'Jak to začalo: od skleněné loutky po ozubené kolo ze skla a diamantový brus za tři konzervy.', ZACATKY, None),
    ('rodokmen', 'Rodokmen', 'Rodokmen', 'Devět generací sklářského rodu Zahradníků od roku 1775.', RODOKMEN, None),
    ('akce-pro-skoly', 'Akce pro školy a školky', 'Akce pro školy a školky', 'Dvouhodinová přednáška o skle s ukázkami tvarování skla nad kahanem. Každé dítě si vyfoukne skleněnou kuličku.', SKOLY, None),
    ('akce-pro-skoly/reference-tabulka', 'Navštívené školy', 'Navštívené školy', 'Seznam škol a školek, kde proběhla přednáška o skle.', NAVSTIVENE, 'akce-pro-skoly'),
    ('akce-pro-skoly/planovaci-kalendar', 'Plánovací kalendář pro školy', 'Plánovací kalendář pro školy', 'Vyberte si volný termín přednášky o skle.', KALENDAR, None),
    ('remeslne-trhy', 'Řemeslné trhy', 'Řemeslné trhy', 'Pojízdná sklárna — předvádění foukání skla nad kahanem na řemeslných trzích.', TRHY, None),
    ('sklenene-modely', 'Skleněné modely', 'Skleněné modely', 'Pohyblivé modely ze skla: parní stroje, lokomotivy, auto, motory a letadlo.', MODELY_INTRO, None),
] + [(f'sklenene-modely/{s}', t, t, d, MODEL_BODY[s], 'sklenene-modely') for s, t, i, d in MODELS] + [
    ('ostatni-vyrobky', 'Ostatní výrobky', 'Ostatní výrobky', 'Další skleněné výrobky na Fléru a výroba na přání.', OSTATNI, None),
    ('technicke-sklo', 'Technické sklo', 'Technické sklo', 'Výroba a oprava laboratorního a technického skla.', TECHNICKE, None),
    ('diplomy-a-oceneni', 'Diplomy a ocenění', 'Diplomy a ocenění', 'Certifikáty českých rekordů, diplomy a pamětní listy.', DIPLOMY, None),
    ('spratelene-weby', 'Spřátelené weby', 'Spřátelené weby', 'Odkazy na přátele a řemeslné akce.', SPRATELENE, None),
]

SITEMAP_BODY = '<ul class="sitemap">' + ''.join(
    f'<li class="{"sub" if p[5] else ""}"><a href="~/{p[0] + "/" if p[0] else ""}">{p[1]}</a></li>' for p in PAGES) + '</ul>'
PAGES.append(('sitemap', None, 'Mapa stránek', 'Přehled všech stránek.', SITEMAP_BODY, None))

BYPATH = {p[0]: p for p in PAGES}


def menu_html(cur):
    section = cur.split('/')[0]
    out = ['<ul class="menu-list">']
    for path, label, _, _, _, parent in PAGES:
        if not label or parent:
            continue
        on = ' aria-current="page"' if path == cur else ''
        cls = ' class="in"' if path and path.split('/')[-1] == section and path != cur else ''
        out.append(f'<li{cls}><a href="~/{path + "/" if path else ""}"{on}>{label}</a>')
        kids = [p for p in PAGES if p[5] == path]
        if kids and section == path.split('/')[0] and path:
            out.append('<ul>')
            for k in kids:
                kon = ' aria-current="page"' if k[0] == cur else ''
                out.append(f'<li><a href="~/{k[0]}/"{kon}>{k[1]}</a></li>')
            out.append('</ul>')
        out.append('</li>')
    out.append('</ul>')
    return ''.join(out)


def crumbs(cur):
    if not cur:
        return ''
    parts, acc = [('', 'Úvod')], ''
    for seg in cur.split('/'):
        acc = f'{acc}/{seg}' if acc else seg
        p = BYPATH.get(acc)
        if p:
            parts.append((acc, p[1] or p[2]))
    items = [f'<a href="~/{a + "/" if a else ""}">{t}</a>' for a, t in parts[:-1]] + [f'<span aria-current="page">{parts[-1][1]}</span>']
    return '<nav class="crumbs" aria-label="Drobečková navigace">' + ' <i>›</i> '.join(items) + '</nav>'


def pager(cur):
    """Předchozí / další model pod stránkou modelu."""
    slugs = [m[0] for m in MODELS]
    s = cur.split('/')[-1]
    if not cur.startswith('sklenene-modely/') or s not in slugs:
        return ''
    i = slugs.index(s)
    prev = MODELS[i - 1] if i > 0 else None
    nxt = MODELS[i + 1] if i < len(MODELS) - 1 else None
    a = lambda m, cls, lab: f'<a class="{cls}" href="~/sklenene-modely/{m[0]}/"><small>{lab}</small>{m[1]}</a>' if m else '<span></span>'
    return f'<nav class="pager">{a(prev, "prev", "← Předchozí model")}{a(nxt, "next", "Další model →")}</nav>'


LAYOUT = '''<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{site}/assets/img/illustration.jpg">
<meta name="theme-color" content="#B9C2D8">
<link rel="icon" href="~/assets/favicon.svg?v={v_fav}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,400;0,600;1,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="~/assets/style.css?v={v_css}">
<script src="~/assets/main.js?v={v_js}" defer></script>
</head>
<body>
<a class="skip" href="#obsah">Přeskočit na obsah</a>
<div class="sheet">
  <header class="head">
    <div class="head-top">
      <div>
        <a class="name" href="~/">Michal Zahradník</a>
        <p class="motto">… z Boží vůle sklář…</p>
      </div>
      <p class="head-meta">Sklářský rod od roku 1775<br><span>osmá generace</span></p>
      <button class="menu-btn" aria-expanded="false" aria-controls="side">Menu</button>
    </div>
    <figure class="banner">
      <img src="~/assets/img/illustration.jpg" width="900" height="278" alt="Pět generací sklářů Zahradníků — 1869, 1896, 1924, 1927 a 1957">
    </figure>
  </header>

  <div class="main">
    <aside class="side" id="side">
      <nav class="menu" aria-label="Hlavní menu">{menu}</nav>
      <section class="contact" aria-labelledby="kontakt-h">
        <h2 id="kontakt-h">Kontakt</h2>
        <p><strong>Michal Zahradník — Sklozam</strong><br>Švecova 398/12<br>Praha 4, Chodov<br>149 00</p>
        <p class="contact-ic">IČ: 10133640</p>
        <p><a href="tel:+420608969213">+420 608 969 213</a><br><a href="mailto:sklozam@gmail.com">sklozam@gmail.com</a></p>
        <details class="map">
          <summary>Zobrazit mapu</summary>
          <iframe title="Mapa — Švecova 398/12, Praha 4" loading="lazy" data-src="https://maps.google.com/maps?q=50.0354482,14.5142903&z=15&output=embed" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </details>
      </section>
      <figure class="stamp">
        <img src="~/assets/img/turisticka-znamka.jpg" alt="Výroční turistická známka Muzea řemesel Letohrad, Řemeslnická sobota 10. 7. 2010" loading="lazy">
        <figcaption>Turistická známka — Muzeum řemesel Letohrad, 2010</figcaption>
      </figure>
    </aside>

    <main class="content" id="obsah">
      {crumbs}
      <h1>{h1}</h1>
      {body}
      {pager}
    </main>
  </div>

  <footer class="foot">
    <p>© 2026 Michal Zahradník — Sklozam · IČ 10133640</p>
    <p><a href="~/">Úvodní stránka</a> | <a href="~/sitemap/">Mapa stránek</a> | <a href="#" data-print>Tisk</a></p>
  </footer>
</div>

<dialog class="lb-box" id="lb" aria-label="Zvětšená fotografie">
  <button class="lb-x" data-close aria-label="Zavřít">×</button>
  <button class="lb-nav lb-prev" aria-label="Předchozí">‹</button>
  <figure><img src="" alt=""><figcaption></figcaption></figure>
  <button class="lb-nav lb-next" aria-label="Další">›</button>
</dialog>
</body>
</html>
'''


def build():
    v = dict(v_css=ver('assets/style.css'), v_js=ver('assets/main.js'), v_fav=ver('assets/favicon.svg'))
    for path, label, title, desc, body, parent in PAGES:
        depth = len(path.split('/')) if path else 0
        rel = '../' * depth or './'
        full_title = title if not path else f'{title} — Michal Zahradník, sklář'
        page = LAYOUT.format(
            title=html.escape(full_title), desc=html.escape(desc, quote=True), site=SITE,
            canon=f'{SITE}/{path + "/" if path else ""}', menu=menu_html(path), crumbs=crumbs(path),
            h1='Dobrý den,' if not path else title, body=body, pager=pager(path), **v)
        page = page.replace('~/', rel)
        out = os.path.join(ROOT, path, 'index.html')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(page)
    # 404 pro GitHub Pages
    nf = LAYOUT.format(title='Stránka nenalezena — Michal Zahradník, sklář', desc='', site=SITE, canon=SITE + '/',
                       menu=menu_html('404'), crumbs='', h1='Stránka nenalezena',
                       body='<p class="lead">Tahle stránka tu není. Možná se přestěhovala při úpravě webu.</p><p><a href="~/">Zpět na úvodní stránku</a> nebo zkuste <a href="~/sitemap/">mapu stránek</a>.</p>',
                       pager='', **v)
    with open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8') as f:
        f.write(nf.replace('~/', '/sklozam/'))
    print(f'{len(PAGES)} stránek, css {v["v_css"]}, js {v["v_js"]}')


if __name__ == '__main__':
    build()
