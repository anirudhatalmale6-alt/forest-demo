# -*- coding: utf-8 -*-
"""Presse le catalogue export bois dans un vrai navigateur.

Ce qui compte sur une page d'export, dans cet ordre :

  1. AUCUNE CAPACITE, AUCUN VOLUME, AUCUN PRIX. Le brief demandait des
     capacites d'approvisionnement ; je n'en ai aucune de mesuree. Un volume
     annonce est la premiere chose qu'un acheteur fait verifier.
  2. AUCUNE CERTIFICATION PRESENTEE COMME DETENUE. Un referentiel est une case
     a remplir. Le test va plus loin : aucun sigle de referentiel n'apparait
     nulle part sur la page, donc aucun ne peut etre lu comme un label affiche.
  3. Le tableau des ports ne contient QUE des faits verifiables : nom,
     province, facade. Aucun chiffre — pas meme un tirant d'eau.
  4. Le catalogue entier est dans le HTML servi.
  5. Les trois axes se croisent et le compte suit ce qui est VISIBLE.
  6. Rien ne deborde, ni a droite ni a gauche, et la barre du haut reste sur
     la meme colonne que le reste de la page.

Usage :  python3 tests.py
"""
import os, re, sys
from playwright.sync_api import sync_playwright
import data as D

ICI = os.path.dirname(os.path.abspath(__file__))
# Un chemin en argument sert au CONTROLE NEGATIF : on presse une copie truquee
# de la page pour verifier que les tests savent encore echouer. Une suite qui
# n'a jamais echoue ne prouve rien.
CONTROLE = len(sys.argv) > 1
PAGE = os.path.abspath(sys.argv[1]) if CONTROLE else os.path.join(ICI, 'index.html')
if not os.path.exists(PAGE):
    PAGE = os.path.join(os.path.dirname(ICI), 'index.html')
if not os.path.exists(PAGE):
    raise SystemExit('index.html introuvable — lancer build.py d’abord')
URL = 'file://' + PAGE
ok = ko = 0


def t(nom, cond, detail=''):
    global ok, ko
    if cond:
        ok += 1; print('  OK    %s' % nom)
    else:
        ko += 1; print('  ECHEC %s   %s' % (nom, detail))


with sync_playwright() as pw:
    nav = pw.chromium.launch()

    # ---------------------------------------------------------------- 1
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

    # ---------------------------------------------------------------- 2
    print('\n2. Aucune capacite, aucun volume, aucun prix')
    INTERDITS = [
        ('un volume en metres cubes', r'[0-9][0-9\s.,]*\s?m(3|³)\b'),
        ('un tonnage', r'[0-9][0-9\s.,]*\s?(tonnes?|t/an|kg)\b'),
        ('une unite de bois d’oeuvre chiffree', r'[0-9][0-9\s.,]*\s?(MBF|MPMP|pmp)\b'),
        ('une capacite chiffree',
         r'\bcapacit[ée][^.]{0,30}\b[0-9]'),
        ('un prix', r'[0-9][0-9\s.,]*\s?(€|\$|EUR|USD|CAD)\b'),
        ('un delai ou une frequence',
         r'\b(d[ée]lai|transit|d[ée]part|livraison)[^.]{0,25}\b[0-9]+\s?(jours?|semaines?|mois)\b'),
        ('un conteneur par periode', r'[0-9]+\s?(EVP|TEU|conteneurs?)\b'),
        ('un pourcentage de part de marche', r'[0-9][0-9.,]*\s?%'),
    ]
    for nom, rx in INTERDITS:
        m = re.search(rx, corps, re.I)
        t('la page n’affiche jamais %s' % nom, m is None,
          repr(corps[max(0, m.start() - 40):m.end() + 20]) if m else '')

    # Le controle le plus important de la page : aucun sigle de referentiel,
    # nulle part. On ne peut pas lire comme un label affiche un sigle qui
    # n'existe pas dans le document.
    SIGLES = ['FSC', 'PEFC', 'SFI', 'NLGA', 'ALSC', 'AWPA', 'ISPM',
              'EUTR', 'EUDR', 'JAS', 'CSA Z']
    presents = [s for s in SIGLES if re.search(r'\b' + s, corps)]
    t('aucun sigle de referentiel n’apparait sur la page',
      not presents, str(presents))
    t('aucune certification n’est presentee comme detenue',
      not re.search(r'\b(nous sommes|notre bois est|produits?)\s+certifi', corps, re.I))
    t('la page dit elle-meme ce qu’elle n’affiche pas',
      'volontairement' in corps.lower() and 'délibéré' in corps.lower())
    t('aucun classement ni superlatif',
      not re.search(r'\b(top\s*\d|le meilleur|classement mondial|n°\s*1|leader)\b',
                    corps, re.I))

    # ---------------------------------------------------------------- 3
    print('\n3. Le tableau des ports ne contient que des faits verifiables')
    lignes = pg.eval_on_selector_all(
        'table.ports tbody tr', 'e=>e.map(r=>[...r.children].map(c=>c.textContent))')
    t('%d ports, un par ligne' % len(D.PORTS), len(lignes) == len(D.PORTS),
      str(len(lignes)))
    t('trois colonnes exactement, toutes remplies',
      all(len(r) == 3 and all(c.strip() for c in r) for r in lignes))
    attendus = [list(p) for p in D.PORTS]
    t('les lignes rendues sont celles de data.py',
      [[c.strip() for c in r] for r in lignes] == attendus,
      str([r for r in lignes if [c.strip() for c in r] not in attendus][:2]))
    tport = pg.eval_on_selector('table.ports', 'e=>e.innerText')
    t('aucun chiffre dans le tableau des ports',
      not re.search(r'[0-9]', tport),
      repr(re.findall(r'.{12}[0-9].{12}', tport)[:2]))

    # ---------------------------------------------------------------- 4
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

    # ---------------------------------------------------------------- 5
    print('\n5. Les trois axes filtrent, et le compte suit ce qui est visible')

    def visibles():
        return pg.evaluate("""() => [...document.querySelectorAll('.o')]
            .filter(e => e.getClientRects().length > 0).length""")

    for fcode, fnom in D.FAMILLES:
        pg.select_option('#f-fam', fcode); pg.wait_for_timeout(110)
        att = sum(1 for c in D.CATEGORIES if c[0] == fcode)
        t('famille « %s » : %d' % (fnom, att),
          visibles() == att, '%d vs %d' % (visibles(), att))
    pg.click('#raz'); pg.wait_for_timeout(120)

    for ncode, nnom in D.NIVEAUX:
        pg.select_option('#f-niv', ncode); pg.wait_for_timeout(110)
        att = sum(1 for c in D.CATEGORIES if c[1] == ncode)
        t('niveau « %s » : %d' % (nnom, att),
          visibles() == att, '%d vs %d' % (visibles(), att))
    pg.click('#raz'); pg.wait_for_timeout(120)

    for acode, anom in D.APPLICATIONS:
        pg.select_option('#f-app', acode); pg.wait_for_timeout(110)
        att = sum(1 for c in D.CATEGORIES if acode in c[3])
        t('application « %s » : %d' % (anom, att),
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
          (str(att) in aff) if att else ('Aucune' in aff), '%s / %d' % (aff, att))
        # Et ce qui est AFFICHE porte bien les trois criteres.
        mauvais = pg.evaluate("""([f,a,n]) => [...document.querySelectorAll('.o')]
            .filter(e => e.getClientRects().length > 0)
            .filter(e => e.dataset.fam !== f || e.dataset.niv !== n
                      || !(' '+e.dataset.app+' ').includes(' '+a+' '))
            .map(e => e.querySelector('h3').textContent)""", [f, a, n])
        t('  aucune carte hors criteres n’est affichee', not mauvais, str(mauvais[:2]))
    pg.click('#raz'); pg.wait_for_timeout(120)

    # ---------------------------------------------------------------- 6
    print('\n6. La recherche ignore les accents')
    pg.fill('#f-q', 'pate a dissoudre'); pg.wait_for_timeout(170)
    t('« pate a dissoudre » sans accent trouve « pâte à dissoudre »',
      visibles() == 1, str(visibles()))
    pg.fill('#f-q', 'phytosanitaire'); pg.wait_for_timeout(170)
    att = sum(1 for c in D.CATEGORIES if 'phyto' in c[5])
    t('un nom de champ est cherchable : %d resultats' % att,
      visibles() == att, '%d vs %d' % (visibles(), att))
    pg.fill('#f-q', 'zzzzzz'); pg.wait_for_timeout(170)
    t('une recherche sans resultat le dit', visibles() == 0 and
      pg.eval_on_selector('#vide', 'e=>e.getClientRects().length > 0'))
    pg.click('#raz'); pg.wait_for_timeout(120)

    # ---------------------------------------------------------------- 7
    print('\n7. Rendu : les deux bords et la colonne, a trois largeurs')
    JS_BORDS = """
    () => {
      const w = document.documentElement.clientWidth, out = [];
      document.querySelectorAll('body *').forEach(e => {
        if (e.hidden) return;
        const cs = getComputedStyle(e);
        if (cs.display === 'none' || cs.visibility === 'hidden') return;
        /* Un conteneur a defilement horizontal a le droit d'avoir un enfant
           plus large que lui : c'est le principe. On saute donc ce qui est
           dans un .tscroll, apres avoir verifie le .tscroll lui-meme. */
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
      const logo = b('.logo'), titre = b('.hero h1'),
            nav = b('.tbar nav a:last-child');
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

    # UN CONTROLE NEGATIF NE PRODUIT PAS DE CAPTURES. Sinon la derniere page
    # truquee ecrase les images livrables — et j'ai bien failli envoyer au
    # client une capture affichant « 12 000 tonnes par mois », c'est-a-dire
    # exactement ce que la page promet de ne jamais dire.
    if CONTROLE:
        nav.close()
        print('\n%d OK, %d ECHEC  (controle negatif : aucune capture ecrite)'
              % (ok, ko))
        sys.exit(0 if ko else 1)   # un controle negatif DOIT echouer

    pg.evaluate('() => window.scrollTo(0, 0)'); pg.wait_for_timeout(250)
    pg.screenshot(path='fo_1_haut.png')
    pg.select_option('#f-niv', 'valeur'); pg.wait_for_timeout(250)
    pg.eval_on_selector('.filtres', 'e=>e.scrollIntoView({block:"start"})')
    pg.wait_for_timeout(300)
    pg.screenshot(path='fo_2_valeur.png')
    pg.click('#raz'); pg.wait_for_timeout(150)
    pg.eval_on_selector('#ports', 'e=>e.scrollIntoView({block:"start"})')
    pg.wait_for_timeout(350)
    pg.screenshot(path='fo_3_ports.png')
    pg.set_viewport_size({'width': 390, 'height': 820})
    pg.evaluate('() => window.scrollTo(0, 0)'); pg.wait_for_timeout(350)
    pg.screenshot(path='fo_4_mobile.png')
    nav.close()

print('\n%d OK, %d ECHEC' % (ok, ko))
sys.exit(1 if ko else 0)
