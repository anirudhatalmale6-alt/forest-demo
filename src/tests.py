# -*- coding: utf-8 -*-
"""Presse le catalogue export bois dans un vrai navigateur, DANS LES DEUX LANGUES.

Ce qui compte sur une page d'export, dans cet ordre :

  1. AUCUNE CAPACITE, AUCUN VOLUME, AUCUN PRIX. Le brief demandait des
     capacites d'approvisionnement ; je n'en ai aucune de mesuree.
  2. AUCUNE CERTIFICATION PRESENTEE COMME DETENUE, et aucun sigle de
     referentiel nulle part.
  3. Le tableau des ports ne contient QUE des faits verifiables.
  4. LA PAGE ANGLAISE EST ENTIEREMENT ANGLAISE. Le test prend les 201 chaines
     francaises du jeu de donnees et exige qu'AUCUNE ne survive dans la page
     anglaise. Une page a moitie traduite est le defaut le plus courant et le
     plus invisible d'un site bilingue.
  5. Les trois axes se croisent et le compte suit ce qui est VISIBLE.
  6. Les deux bords, la colonne, le contraste — le rouge est la couleur ou
     l'on passe le plus facilement sous le seuil sans le voir.

Usage :
  python3 tests.py                      les deux langues
  python3 tests.py page-truquee.html    CONTROLE NEGATIF : doit echouer
"""
import os, re, sys
from playwright.sync_api import sync_playwright
import data as D
from traductions import EN

ICI = os.path.dirname(os.path.abspath(__file__))
CONTROLE = len(sys.argv) > 1
RACINE = ICI if os.path.exists(os.path.join(ICI, 'index.html')) \
    else os.path.dirname(ICI)

if CONTROLE:
    PAGES = [('fr', os.path.abspath(sys.argv[1]))]
else:
    PAGES = [('fr', os.path.join(RACINE, 'index.html')),
             ('en', os.path.join(RACINE, 'en', 'index.html'))]
for _, p in PAGES:
    if not os.path.exists(p):
        raise SystemExit('%s introuvable — lancer build.py d’abord' % p)

ok = ko = 0

# Les libelles qui dependent de la langue. Le test doit savoir ce qu'il
# cherche : chercher « volontairement » dans une page anglaise echouerait
# pour la mauvaise raison.
LIB = {
    'fr': {'aucune': 'Aucune', 'volontaire': 'volontairement',
           'delibere': 'délibéré', 'cat': 'catégorie'},
    'en': {'aucune': 'No category', 'volontaire': 'deliberately',
           'delibere': 'deliberate', 'cat': 'categor'},
}


def t(nom, cond, detail=''):
    global ok, ko
    if cond:
        ok += 1; print('  OK    %s' % nom)
    else:
        ko += 1; print('  ECHEC %s   %s' % (nom, detail))


with sync_playwright() as pw:
    nav = pw.chromium.launch()

    for LANG, CHEMIN in PAGES:
        URL = 'file://' + CHEMIN
        L = LIB[LANG]
        print('\n' + '=' * 66)
        print('LANGUE : %s   (%s)' % (LANG.upper(), os.path.relpath(CHEMIN, RACINE)))
        print('=' * 66)

        # ------------------------------------------------------------ 1
        print('\n1. Sans JavaScript, le catalogue est entier')
        sansjs = nav.new_context(java_script_enabled=False)
        p0 = sansjs.new_page()
        p0.set_viewport_size({'width': 1280, 'height': 900})
        p0.goto(URL, wait_until='load')
        n0 = len(p0.query_selector_all('.o'))
        t('les %d categories sont dans le HTML servi' % len(D.CATEGORIES),
          n0 == len(D.CATEGORIES), '%d rendues' % n0)
        caches = p0.evaluate("""() => [...document.querySelectorAll('.o')]
            .filter(e => e.hidden || getComputedStyle(e).display === 'none').length""")
        t('aucune n’est masquee au chargement', caches == 0, str(caches))
        t('les ports, referentiels et marches sont en texte, sans script',
          len(p0.query_selector_all('table.ports tbody tr')) == len(D.PORTS)
          and len(p0.query_selector_all('.ref li')) == len(D.REFERENTIELS)
          and len(p0.query_selector_all('.mar li')) == len(D.MARCHES))
        sansjs.close()

        pg = nav.new_page()
        err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        pg.on('console', lambda m: err.append(m.text) if m.type == 'error' else None)
        pg.set_viewport_size({'width': 1280, 'height': 900})
        pg.goto(URL, wait_until='load')
        corps = pg.eval_on_selector('body', 'e=>e.innerText')

        # ------------------------------------------------------------ 2
        print('\n2. Aucune capacite, aucun volume, aucun prix')
        INTERDITS = [
            ('un volume en metres cubes', r'[0-9][0-9\s.,]*\s?m(3|³)\b'),
            ('un tonnage', r'[0-9][0-9\s.,]*\s?(tonnes?|t/an|kg)\b'),
            ('une unite de bois d’oeuvre chiffree',
             r'[0-9][0-9\s.,]*\s?(MBF|MPMP|pmp)\b'),
            ('une capacite chiffree', r'\bcapacit(y|[ée])[^.]{0,30}\b[0-9]'),
            ('un prix', r'[0-9][0-9\s.,]*\s?(€|\$|EUR|USD|CAD)\b'),
            ('un delai ou une frequence',
             r'\b(d[ée]lai|transit|d[ée]part|livraison|lead time|sailing)'
             r'[^.]{0,25}\b[0-9]+\s?(jours?|semaines?|mois|days?|weeks?|months?)\b'),
            ('un conteneur par periode', r'[0-9]+\s?(EVP|TEU|conteneurs?|containers?)\b'),
            ('un pourcentage de part de marche', r'[0-9][0-9.,]*\s?%'),
        ]
        for nom, rx in INTERDITS:
            m = re.search(rx, corps, re.I)
            t('la page n’affiche jamais %s' % nom, m is None,
              repr(corps[max(0, m.start() - 40):m.end() + 20]) if m else '')

        SIGLES = ['FSC', 'PEFC', 'SFI', 'NLGA', 'ALSC', 'AWPA', 'ISPM',
                  'EUTR', 'EUDR', 'JAS', 'CSA Z']
        presents = [s for s in SIGLES if re.search(r'\b' + s, corps)]
        t('aucun sigle de referentiel n’apparait sur la page',
          not presents, str(presents))
        t('aucune certification n’est presentee comme detenue',
          not re.search(r'\b(nous sommes|notre bois est|produits?)\s+certifi', corps, re.I)
          and not re.search(r'\b(we are|our timber is)\s+certified', corps, re.I))
        t('la page dit elle-meme ce qu’elle n’affiche pas',
          L['volontaire'] in corps.lower() and L['delibere'] in corps.lower())
        t('aucun classement ni superlatif',
          not re.search(r'\b(top\s*\d|le meilleur|the best|classement mondial'
                        r'|n°\s*1|leader)\b', corps, re.I))

        # ------------------------------------------------------------ 3
        print('\n3. Le tableau des ports ne contient que des faits verifiables')
        lignes = pg.eval_on_selector_all(
            'table.ports tbody tr',
            'e=>e.map(r=>[...r.children].map(c=>c.textContent))')
        t('%d ports, un par ligne' % len(D.PORTS), len(lignes) == len(D.PORTS),
          str(len(lignes)))
        t('trois colonnes exactement, toutes remplies',
          all(len(r) == 3 and all(c.strip() for c in r) for r in lignes))
        # Le NOM du port ne se traduit pas ; la province et la facade, si.
        noms_att = [p[0] for p in D.PORTS]
        t('les noms de ports rendus sont ceux de data.py',
          [r[0].strip() for r in lignes] == noms_att,
          str([r[0] for r in lignes][:3]))
        tport = pg.eval_on_selector('table.ports', 'e=>e.innerText')
        t('aucun chiffre dans le tableau des ports',
          not re.search(r'[0-9]', tport),
          repr(re.findall(r'.{12}[0-9].{12}', tport)[:2]))

        # ------------------------------------------------------------ 3bis
        if LANG == 'en':
            print('\n3bis. LA PAGE ANGLAISE EST ENTIEREMENT ANGLAISE')
            # Une elision francaise est un marqueur sans ambiguite. Il ne doit
            # pas en rester une seule.
            elisions = re.findall(r"\b[dlnqsjctm]’\w", corps)
            t('aucune elision francaise (d’, l’, qu’, n’…)',
              not elisions, str(sorted(set(elisions))[:6]))
            # Et le controle exact : chacune des chaines francaises du jeu de
            # donnees doit avoir disparu. Deux exceptions legitimes, et
            # seulement deux :
            #   - la traduction est identique au francais (« Ontario ») ;
            #   - la chaine est aussi un NOM DE PORT, qui est un nom propre et
            #     ne se traduit pas. « Québec » designe la province (traduite
            #     en « Quebec ») ET la ville portuaire (conservee telle
            #     quelle). Sans cette exception le test accuserait la page a
            #     tort — mais on ne desactive pas le controle pour autant, on
            #     nomme precisement ce qui a le droit de rester.
            noms_ports = {p[0] for p in D.PORTS}
            restes = [fr for fr, en in EN.items()
                      if fr != en and fr not in noms_ports and fr in corps]
            t('aucune des %d chaines francaises ne survit' % len(EN),
              not restes, str([r[:45] for r in restes[:4]]))
            mots = [w for w in (' est ', ' sont ', ' pour ', ' avec ', ' dans ',
                                ' aucune ', ' chaque ', ' très ')
                    if w in corps.lower()]
            t('aucun mot outil francais', not mots, str(mots))
        else:
            print('\n3bis. La page francaise est bien en francais')
            t('la page francaise contient des elisions francaises',
              len(re.findall(r"\b[dlnqsjctm]’\w", corps)) > 20)

        # ------------------------------------------------------------ 4
        print('\n4. Les compteurs sont derives des donnees')
        kpi = pg.eval_on_selector_all('.kpi b', 'e=>e.map(x=>x.textContent)')
        for i, (lab, att) in enumerate([
                ('categories', len(D.CATEGORIES)), ('familles', len(D.FAMILLES)),
                ('applications', len(D.APPLICATIONS)), ('champs', len(D.CHAMPS)),
                ('ports', len(D.PORTS))]):
            t('le bandeau annonce le vrai nombre de %s' % lab,
              kpi[i] == str(att), '%s vs %d' % (kpi[i], att))
        t('le compte de depart vaut le nombre reel',
          str(len(D.CATEGORIES)) in pg.eval_on_selector('#compte', 'e=>e.textContent'))
        t('chaque carte annonce sa grille de champs',
          len(pg.query_selector_all('.o .car b')) == len(D.CATEGORIES))

        # ------------------------------------------------------------ 5
        print('\n5. Les trois axes filtrent, et le compte suit ce qui est visible')

        def visibles():
            return pg.evaluate("""() => [...document.querySelectorAll('.o')]
                .filter(e => e.getClientRects().length > 0).length""")

        for fcode, fnom in D.FAMILLES:
            pg.select_option('#f-fam', fcode); pg.wait_for_timeout(100)
            att = sum(1 for c in D.CATEGORIES if c[0] == fcode)
            t('famille « %s » : %d' % (fcode, att),
              visibles() == att, '%d vs %d' % (visibles(), att))
        pg.click('#raz'); pg.wait_for_timeout(120)

        for ncode, nnom in D.NIVEAUX:
            pg.select_option('#f-niv', ncode); pg.wait_for_timeout(100)
            att = sum(1 for c in D.CATEGORIES if c[1] == ncode)
            t('niveau « %s » : %d' % (ncode, att),
              visibles() == att, '%d vs %d' % (visibles(), att))
        pg.click('#raz'); pg.wait_for_timeout(120)

        for acode, anom in D.APPLICATIONS:
            pg.select_option('#f-app', acode); pg.wait_for_timeout(100)
            att = sum(1 for c in D.CATEGORIES if acode in c[3])
            t('application « %s » : %d' % (acode, att),
              visibles() == att, '%d vs %d' % (visibles(), att))
        pg.click('#raz'); pg.wait_for_timeout(120)

        print('\n   ... et croises a trois')
        for f, a, n in (('resineux', 'residentiel', 'secondaire'),
                        ('biomasse', 'energie', 'valeur'),
                        ('panneaux', 'ameublement', 'secondaire'),
                        ('grumes', 'papeterie', 'primaire')):
            pg.click('#raz'); pg.wait_for_timeout(70)
            pg.select_option('#f-fam', f)
            pg.select_option('#f-app', a)
            pg.select_option('#f-niv', n); pg.wait_for_timeout(150)
            att = sum(1 for c in D.CATEGORIES
                      if c[0] == f and c[1] == n and a in c[3])
            aff = pg.eval_on_selector('#compte', 'e=>e.textContent')
            t('%s + %s + %s : %d' % (f, a, n, att),
              visibles() == att, '%d vs %d' % (visibles(), att))
            t('  le compte affiche correspond',
              (str(att) in aff) if att else (L['aucune'] in aff),
              '%s / %d' % (aff, att))
            mauvais = pg.evaluate("""([f,a,n]) => [...document.querySelectorAll('.o')]
                .filter(e => e.getClientRects().length > 0)
                .filter(e => e.dataset.fam !== f || e.dataset.niv !== n
                          || !(' '+e.dataset.app+' ').includes(' '+a+' '))
                .map(e => e.querySelector('h3').textContent)""", [f, a, n])
            t('  aucune carte hors criteres n’est affichee', not mauvais,
              str(mauvais[:2]))
        pg.click('#raz'); pg.wait_for_timeout(120)

        # ------------------------------------------------------------ 6
        print('\n6. La recherche ignore les accents')
        if LANG == 'fr':
            pg.fill('#f-q', 'pate a dissoudre'); pg.wait_for_timeout(170)
            t('« pate a dissoudre » sans accent trouve « pâte à dissoudre »',
              visibles() == 1, str(visibles()))
            pg.fill('#f-q', 'phytosanitaire'); pg.wait_for_timeout(170)
            att = sum(1 for c in D.CATEGORIES if 'phyto' in c[5])
        else:
            pg.fill('#f-q', 'dissolving pulp'); pg.wait_for_timeout(170)
            t('« dissolving pulp » trouve la bonne categorie',
              visibles() == 1, str(visibles()))
            pg.fill('#f-q', 'phytosanitary'); pg.wait_for_timeout(170)
            att = sum(1 for c in D.CATEGORIES if 'phyto' in c[5])
        t('un nom de champ est cherchable : %d resultats' % att,
          visibles() == att, '%d vs %d' % (visibles(), att))
        pg.fill('#f-q', 'zzzzzz'); pg.wait_for_timeout(170)
        t('une recherche sans resultat le dit', visibles() == 0 and
          pg.eval_on_selector('#vide', 'e=>e.getClientRects().length > 0'))
        pg.click('#raz'); pg.wait_for_timeout(120)

        # ------------------------------------------------------------ 7
        print('\n7. Le selecteur de langue')
        t('la langue du document est declaree',
          pg.eval_on_selector('html', 'e=>e.lang') == LANG,
          pg.eval_on_selector('html', 'e=>e.lang'))
        t('la langue courante est marquee active, l’autre est un lien',
          pg.eval_on_selector('.lg-on', 'e=>e.textContent') == LANG.upper()
          and pg.eval_on_selector('.lgs a.lg', 'e=>e.textContent')
          == ('EN' if LANG == 'fr' else 'FR'))
        cible = pg.eval_on_selector('.lgs a.lg', 'e=>e.getAttribute("href")')
        # Un selecteur de langue qui pointe dans le vide est le classique du
        # site bilingue. On resout le chemin sur le disque.
        vise = os.path.normpath(os.path.join(os.path.dirname(CHEMIN), cible,
                                             'index.html'))
        t('le lien vers l’autre langue mene a un fichier qui existe',
          os.path.exists(vise), '%s -> %s' % (cible, vise))

        # ------------------------------------------------------------ 8
        print('\n8. Rendu : les deux bords et la colonne, a trois largeurs')
        JS_BORDS = """
        () => {
          const w = document.documentElement.clientWidth, out = [];
          document.querySelectorAll('body *').forEach(e => {
            if (e.hidden) return;
            const cs = getComputedStyle(e);
            if (cs.display === 'none' || cs.visibility === 'hidden') return;
            if (e.closest('.tscroll') && !e.classList.contains('tscroll')) return;
            const r = e.getBoundingClientRect();
            if (r.width < 1 && r.height < 1) return;
            if (r.left < -1) out.push(['gauche', Math.round(r.left), e.className || e.tagName]);
            else if (r.right > w + 1) out.push(['droite', Math.round(r.right - w), e.className || e.tagName]);
          });
          return out.slice(0, 4);
        }"""
        JS_ALIGN = """
        () => {
          const b = s => { const e = document.querySelector(s);
            const r = e.getBoundingClientRect(); return [r.left, r.right]; };
          const logo = b('.logo'), titre = b('.hero h1'), nav = b('.lgs');
          return {gauche: Math.abs(logo[0] - titre[0]),
                  droite: Math.abs((document.documentElement.clientWidth - nav[1]) - titre[0])};
        }"""
        for w in (390, 768, 1280):
            pg.set_viewport_size({'width': w, 'height': 900})
            pg.wait_for_timeout(180)
            bords = pg.evaluate(JS_BORDS)
            t('aucun debordement a %d px, ni a gauche ni a droite' % w,
              not bords, str(bords))
            al = pg.evaluate(JS_ALIGN)
            t('  la barre du haut est alignee sur la colonne a %d px' % w,
              al['gauche'] <= 1 and al['droite'] <= 1, str(al))
        pg.set_viewport_size({'width': 1280, 'height': 900})
        pg.wait_for_timeout(150)

        JS_CONTRASTE = """
        () => {
          const lum = c => { const f = v => { v/=255; return v<=0.03928 ? v/12.92
            : Math.pow((v+0.055)/1.055, 2.4); };
            return 0.2126*f(c[0]) + 0.7152*f(c[1]) + 0.0722*f(c[2]); };
          const parse = s => { const m = s.match(/[\\d.]+/g); return m ? m.slice(0,3).map(Number) : null; };
          const alpha = s => { const m = s.match(/[\\d.]+/g); return m && m.length>3 ? parseFloat(m[3]) : 1; };
          const bg = el => { let e = el;
            while (e) { const c = getComputedStyle(e).backgroundColor;
              if (c && alpha(c) > 0.85) return parse(c); e = e.parentElement; }
            return [255,255,255]; };
          const bas = [];
          document.querySelectorAll('body *').forEach(el => {
            if (el.hidden) return;
            const txt = [...el.childNodes].filter(n => n.nodeType === 3)
              .map(n => n.textContent.trim()).join(' ').trim();
            if (!txt) return;
            const cs = getComputedStyle(el);
            if (cs.visibility === 'hidden' || cs.display === 'none') return;
            const r = el.getBoundingClientRect();
            if (r.width < 2 || r.height < 2) return;
            const fg = parse(cs.color), b = bg(el);
            if (!fg || !b) return;
            const l1 = lum(fg), l2 = lum(b);
            const ratio = (Math.max(l1,l2)+0.05) / (Math.min(l1,l2)+0.05);
            const px = parseFloat(cs.fontSize);
            const gros = px >= 24 || (px >= 18.66 && parseInt(cs.fontWeight,10) >= 700);
            if (ratio < (gros ? 3 : 4.5)) bas.push([txt.slice(0,36), ratio.toFixed(2), px]);
          });
          return bas;
        }"""
        bas = pg.evaluate(JS_CONTRASTE)
        t('contraste : 0 element sous le seuil', not bas, str(bas[:3]))
        t('aucune erreur JS', not err, str(err[:3]))

        if CONTROLE:
            continue

        pfx = 'fo_' if LANG == 'fr' else 'fo_en_'
        pg.evaluate('() => window.scrollTo(0, 0)'); pg.wait_for_timeout(250)
        pg.screenshot(path=os.path.join(RACINE, pfx + '1_haut.png'))
        pg.select_option('#f-niv', 'valeur'); pg.wait_for_timeout(250)
        pg.eval_on_selector('.filtres', 'e=>e.scrollIntoView({block:"start"})')
        pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(RACINE, pfx + '2_valeur.png'))
        pg.click('#raz'); pg.wait_for_timeout(150)
        pg.eval_on_selector('#ports', 'e=>e.scrollIntoView({block:"start"})')
        pg.wait_for_timeout(350)
        pg.screenshot(path=os.path.join(RACINE, pfx + '3_ports.png'))
        pg.set_viewport_size({'width': 390, 'height': 820})
        pg.evaluate('() => window.scrollTo(0, 0)'); pg.wait_for_timeout(350)
        pg.screenshot(path=os.path.join(RACINE, pfx + '4_mobile.png'))
        pg.close()

    nav.close()

if CONTROLE:
    print('\n%d OK, %d ECHEC  (controle negatif : aucune capture ecrite)'
          % (ok, ko))
    sys.exit(0 if ko else 1)   # un controle negatif DOIT echouer

print('\n%d OK, %d ECHEC' % (ok, ko))
sys.exit(1 if ko else 0)
