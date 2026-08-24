# -*- coding: utf-8 -*-
"""Rend UNE page autonome : le catalogue export bois canadien.

Meme mecanique que le repertoire droits humains et que la page eclairage :
tout tient dans un seul fichier, rien n'est recharge, et SANS JAVASCRIPT le
catalogue entier est deja dans le HTML. Le script filtre ce qui est deja la.

Trois axes ici au lieu de deux, parce que le brief le demande : la famille de
produit, l'application, et le NIVEAU DE TRANSFORMATION. Ce troisieme axe n'est
pas decoratif : l'acheteur de grumes et l'acheteur de lamelle-colle ne sont
pas la meme personne, ne paient pas la meme chose et ne demandent pas les
memes documents.
"""
import html, sys
import data as D
from traductions import EN

SORTIE = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
LANG = sys.argv[2] if len(sys.argv) > 2 else 'fr'
if LANG not in ('fr', 'en'):
    raise SystemExit('langue inconnue : %r (fr ou en)' % LANG)


def T(s):
    """Traduit une chaine, ou REFUSE de construire.

    Renvoyer le francais quand la traduction manque produirait une page
    anglaise a moitie francaise, et personne ne s'en apercevrait avant le
    client. On leve donc.
    """
    if LANG == 'fr':
        return s
    if s not in EN:
        raise SystemExit('TRADUCTION MANQUANTE :\n  %r' % s)
    return EN[s]


# Le texte de la page elle-meme (hors donnees). Meme regle : les deux langues
# vivent cote a cote, une entree ne peut pas exister a moitie.
CHROME = {
    'nav_cat':    ('Catalogue', 'Catalogue'),
    'nav_ports':  ('Ports', 'Ports'),
    'nav_ref':    ('Référentiels', 'Standards'),
    'nav_mar':    ('Marchés', 'Markets'),
    'demo':       ('Maquette de démonstration', 'Demonstration mock-up'),
    'demo_suite': ('est un intitulé provisoire. Aucun volume, aucune capacité '
                   'et aucun prix ne figurent sur cette page.',
                   'is a provisional name. No volume, no capacity and no price '
                   'appears on this page.'),
    'h1':         ('Bois canadien et produits dérivés, pour les marchés '
                   'internationaux',
                   'Canadian wood and wood products, for international markets'),
    'chapo':      ('Un seul catalogue, de la grume au lamellé-collé. Bois '
                   'd’œuvre résineux et feuillus, panneaux, contreplaqué, OSB, '
                   'bois d’ingénierie, produits de bois massif, bois traité, '
                   'pâte, papier, carton et biomasse. Filtrez par famille, par '
                   'application et par niveau de transformation ; chaque '
                   'catégorie annonce les champs qu’un acheteur international '
                   'exigera avant de coter.',
                   'One catalogue, from the log to glued laminated timber. '
                   'Softwood and hardwood lumber, panels, plywood, OSB, '
                   'engineered wood, solid wood products, treated timber, pulp, '
                   'paper, board and biomass. Filter by family, by application '
                   'and by level of processing; every category states the '
                   'fields an international buyer will require before quoting.'),
    'kpi_cat':    ('catégories de produits', 'product categories'),
    'kpi_fam':    ('familles', 'families'),
    'kpi_app':    ('applications', 'applications'),
    'kpi_ch':     ('champs à renseigner', 'fields to complete'),
    'kpi_ports':  ('ports canadiens', 'Canadian ports'),
    'l_fam':      ('Famille de produit', 'Product family'),
    'l_app':      ('Application', 'Application'),
    'l_niv':      ('Niveau de transformation', 'Level of processing'),
    'l_q':        ('Recherche', 'Search'),
    'o_fam':      ('Toutes les familles', 'All families'),
    'o_app':      ('Toutes les applications', 'All applications'),
    'o_niv':      ('Tous les niveaux', 'All levels'),
    'ph_q':       ('érable, OSB, granulés, pâte…', 'maple, OSB, pellets, pulp…'),
    'raz':        ('Tout afficher', 'Show everything'),
    'cpt':        ('catégories', 'categories'),
    'cpt_1':      ('1 catégorie', '1 category'),
    'cpt_0':      ('Aucune catégorie ne correspond', 'No category matches'),
    'vide':       ('Aucune catégorie ne correspond à ces critères. Élargissez '
                   'la famille ou l’application.',
                   'No category matches these criteria. Widen the family or the '
                   'application.'),
    'champs':     ('Champs à renseigner avant cotation',
                   'Fields to complete before quoting'),
    'h_ports':    ('Ports d’expédition', 'Shipping ports'),
    'p_ports':    ('Les façades canadiennes ouvrent sur trois routes très '
                   'différentes : le Pacifique vers l’Asie, le Saint-Laurent et '
                   'l’Atlantique vers l’Europe et l’Afrique du Nord, les Grands '
                   'Lacs vers l’intérieur du continent. Le port de départ n’est '
                   'pas un détail logistique : il conditionne le délai, le coût '
                   'et parfois la faisabilité de la vente.',
                   'The Canadian seaboards open onto three very different '
                   'routes: the Pacific towards Asia, the St. Lawrence and the '
                   'Atlantic towards Europe and North Africa, the Great Lakes '
                   'towards the interior of the continent. The port of '
                   'departure is not a logistics detail: it drives the lead '
                   'time, the cost and sometimes the feasibility of the sale.'),
    'cap_ports':  ('Nom, province et façade maritime. Rien d’autre — aucun '
                   'tonnage, aucun tirant d’eau, aucune fréquence de départ, '
                   'aucun délai de transit.',
                   'Name, province and seaboard. Nothing else — no tonnage, no '
                   'draught, no sailing frequency, no transit time.'),
    'th_port':    ('Port', 'Port'),
    'th_prov':    ('Province', 'Province'),
    'th_fac':     ('Façade', 'Seaboard'),
    'h_ref':      ('Référentiels et documents à fournir',
                   'Standards and documents to provide'),
    'p_ref':      ('Ce sont des cases à remplir, pas des certificats affichés. '
                   'Aucun n’est présenté comme détenu : la page dit ce qu’un '
                   'acheteur demandera, pas ce que le vendeur possède.',
                   'These are boxes to fill in, not certificates on display. '
                   'None is presented as held: the page says what a buyer will '
                   'ask for, not what the seller owns.'),
    'h_mar':      ('Marchés d’exportation', 'Export markets'),
    'p_mar':      ('Les régions couvertes par la mise en relation. Aucune part '
                   'de marché, aucun volume, aucun classement : quel produit '
                   'part vers quelle destination dépend du carnet de commandes '
                   'réel, pas d’une page web.',
                   'The regions covered by the introduction service. No market '
                   'share, no volume, no ranking: which product goes to which '
                   'destination depends on the real order book, not on a web '
                   'page.'),
    'h_note':     ('Comment lire ce catalogue', 'How to read this catalogue'),
    'h_avert':    ('Ce que la page n’affiche pas, volontairement',
                   'What the page deliberately does not show'),
    'pied':       ('maquette de démonstration. Les champs listés sont des '
                   'informations à renseigner, pas des valeurs mesurées.',
                   'demonstration mock-up. The fields listed are information to '
                   'be completed, not measured values.'),
    'meta':       ('Catalogue export de la foresterie canadienne : bois d’œuvre '
                   'résineux, feuillus, panneaux, contreplaqué, OSB, bois '
                   'd’ingénierie, bois massif transformé, bois traité, pâte, '
                   'papier, carton et biomasse. Filtrable par famille, '
                   'application et niveau de transformation. Ports, '
                   'référentiels et marchés d’exportation.',
                   'Canadian forestry export catalogue: softwood lumber, '
                   'hardwoods, panels, plywood, OSB, engineered wood, '
                   'further-processed solid wood, treated timber, pulp, paper, '
                   'board and biomass. Filterable by family, application and '
                   'level of processing. Ports, standards and export markets.'),
}


def C(cle):
    return CHROME[cle][1 if LANG == 'en' else 0]


def verifier():
    """Une faute de frappe dans un code de filtre ne casse rien a l'oeil :
    elle rend une carte introuvable pour toujours. On refuse de construire."""
    fam = {c for c, _ in D.FAMILLES}
    app = {c for c, _ in D.APPLICATIONS}
    niv = {c for c, _ in D.NIVEAUX}
    ch = {c for c, _ in D.CHAMPS}
    err = []
    for f, n, nom, apps, desc, champs in D.CATEGORIES:
        if f not in fam:
            err.append('%s : famille inconnue %r' % (nom, f))
        if n not in niv:
            err.append('%s : niveau inconnu %r' % (nom, n))
        if not apps:
            err.append('%s : aucune application' % nom)
        for a in apps:
            if a not in app:
                err.append('%s : application inconnue %r' % (nom, a))
        for k in champs:
            if k not in ch:
                err.append('%s : champ inconnu %r' % (nom, k))
        if len(set(apps)) != len(apps):
            err.append('%s : application en double' % nom)
        if len(set(champs)) != len(champs):
            err.append('%s : champ en double' % nom)
    noms = [c[2] for c in D.CATEGORIES]
    for n in set(noms):
        if noms.count(n) > 1:
            err.append('categorie en double : %s' % n)
    for c, nom in D.FAMILLES:
        if not any(x[0] == c for x in D.CATEGORIES):
            err.append('famille sans aucune categorie : %s' % nom)
    for c, nom in D.APPLICATIONS:
        if not any(c in x[3] for x in D.CATEGORIES):
            err.append('application jamais employee : %s' % nom)
    for c, nom in D.NIVEAUX:
        if not any(x[1] == c for x in D.CATEGORIES):
            err.append('niveau jamais employe : %s' % nom)
    for c, nom in D.CHAMPS:
        if not any(c in x[5] for x in D.CATEGORIES):
            err.append('champ jamais employe : %s' % nom)
    # Les ports sont des faits : trois colonnes, toujours remplies.
    for p in D.PORTS:
        if len(p) != 3 or not all(p):
            err.append('port incomplet : %r' % (p,))
    if err:
        raise SystemExit('DONNEES INVALIDES :\n  - ' + '\n  - '.join(err))


CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{--bg:__BG__;--c:__C__;--l:__L__;--e:__E__;--tx:__TX__;--mu:__MU__;
      --ac:__AC__;--acd:__ACD__}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--tx);
  font:16px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,
  "Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--ac)}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px}
h1,h2,h3{color:var(--e);line-height:1.16;letter-spacing:-.02em;margin:0 0 12px;font-weight:800}

.demo{background:var(--e);color:#e6dbd9;font-size:12.5px;padding:9px 16px;text-align:center}
.demo b{color:#ff9d9d}

/* L'accent doit SE VOIR : un filet rouge sous la barre, les compteurs en
   rouge, un liseré rouge en tête des cartes. Le vert très pâle de la première
   version ne se lisait comme une couleur sur aucun écran. */
header.top{background:var(--c);border-bottom:2px solid var(--ac);position:sticky;top:0;z-index:30}
.lgs{display:inline-flex;gap:2px;align-items:center;margin-left:4px}
.lg{font-size:12.5px;font-weight:800;letter-spacing:.06em;padding:4px 8px;
  border-radius:6px;text-decoration:none;border:1px solid var(--l);color:var(--mu)}
a.lg:hover{border-color:var(--ac);color:var(--acd)}
.lg-on{background:var(--ac);border-color:var(--ac);color:#fff}
/* padding-inline EXPLICITE. Le meme <div> porte « wrap » et « tbar » : un
   raccourci « padding:15px 0 » ici effacerait le padding horizontal de .wrap
   (meme specificite, declaree plus bas) et collerait le logo au bord de
   l'ecran. Rien ne deborderait, donc aucun test de debordement ne le verrait.
   C'est arrive sur trois pages avant d'etre trouve a la mesure. */
.tbar{display:flex;align-items:center;gap:20px;padding-block:15px;flex-wrap:wrap}
.logo{font-weight:800;font-size:15.5px;letter-spacing:.04em;color:var(--e)}
.tbar nav{margin-left:auto;display:flex;gap:18px;font-size:14.5px}
.tbar nav a{color:var(--mu);text-decoration:none}
.tbar nav a:hover{color:var(--ac)}

.hero{background:var(--c);border-bottom:1px solid var(--l);padding:44px 0 38px}
.hero h1{font-size:clamp(27px,4vw,42px);max-width:20ch}
.hero p{font-size:17.5px;color:var(--mu);max-width:68ch;margin:0 0 20px}
.kpi{display:flex;flex-wrap:wrap;gap:10px 34px;margin-top:22px}
.kpi div b{display:block;font-size:26px;font-weight:800;color:var(--ac);
  font-variant-numeric:tabular-nums;line-height:1.1}
.kpi div span{font-size:13px;color:var(--mu)}

main{padding:26px 0 60px}

.filtres{background:var(--c);border:1px solid var(--l);border-radius:12px;
  padding:16px;margin:0 0 18px;display:grid;grid-template-columns:repeat(4,1fr);gap:13px}
.f{display:flex;flex-direction:column;gap:6px;min-width:0}
.f label{font-size:12.5px;font-weight:700;color:var(--e);letter-spacing:.02em}
.f select,.f input{width:100%;min-width:0;font:inherit;font-size:15px;color:var(--e);
  background:#fff;border:1px solid var(--l);border-radius:8px;padding:10px 11px}
.f select:focus,.f input:focus{outline:2px solid var(--ac);outline-offset:1px}
.barre{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:0 0 14px}
.compte{font-size:16px;font-weight:700;color:var(--e)}
.raz{font:inherit;font-size:14px;cursor:pointer;background:transparent;color:var(--ac);
  border:1px solid var(--l);border-radius:8px;padding:7px 13px}
.raz:hover{border-color:var(--ac)}

.liste{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.o{background:var(--c);border:1px solid var(--l);border-top:3px solid var(--ac);
  border-radius:12px;padding:16px 18px 17px;
  display:flex;flex-direction:column;gap:9px;min-width:0}
.o[hidden]{display:none}
.o h3{font-size:16.5px;margin:0;line-height:1.3}
.o .ou{font-size:13px;color:var(--mu);margin:0;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.o .ou .fam{font-weight:600;color:var(--tx)}
.o p.d{font-size:14.5px;color:var(--tx);margin:0;flex:1 1 auto}

.nv{font-size:11px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;
  padding:3px 9px;border-radius:99px;white-space:nowrap;
  background:#eef2f0;color:#33544a;border:1px solid #d5e0da}
.nv-secondaire{background:#eaf1f7;color:#1d4463;border-color:#cfdeeb}
.nv-valeur{background:#f4eee6;color:#6b4715;border-color:#e6d8c4}

.tags{display:flex;flex-wrap:wrap;gap:5px;margin:0}
.tags span{font-size:11.5px;font-weight:600;padding:3px 9px;border-radius:99px;
  background:#eef1f0;color:#2c4239;border:1px solid #dae1de;white-space:nowrap}

.car{margin:0;border-top:1px dashed var(--l);padding-top:9px}
.car b{display:block;font-size:11px;font-weight:800;letter-spacing:.04em;
  text-transform:uppercase;color:var(--mu);margin:0 0 6px}
.car ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:5px}
.car li{font-size:11.5px;padding:3px 9px;border-radius:6px;background:#f5f7f6;
  color:var(--tx);border:1px solid var(--l);white-space:nowrap}

.vide{grid-column:1/-1;background:var(--c);border:1px dashed var(--l);border-radius:12px;
  padding:26px;color:var(--mu);margin:0}

/* Les trois blocs du bas : ports, referentiels, marches. Statiques, en texte,
   lisibles sans script — c'est ce que lira un moteur de recherche. */
.bloc{background:var(--c);border:1px solid var(--l);border-radius:12px;
  padding:20px 22px;margin:22px 0 0}
.bloc h2{font-size:19px;margin:0 0 6px}
.bloc > p{color:var(--mu);font-size:14.5px;margin:0 0 15px;max-width:74ch}

table.ports{border-collapse:collapse;width:100%;font-size:14.5px}
table.ports caption{text-align:left;font-size:12.5px;color:var(--mu);
  padding:0 0 8px;caption-side:top}
table.ports th,table.ports td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--l)}
table.ports th{font-size:12px;text-transform:uppercase;letter-spacing:.04em;
  color:var(--mu);font-weight:800}
table.ports tr:last-child td{border-bottom:0}
.tscroll{overflow-x:auto}

.ref{list-style:none;margin:0;padding:0;display:grid;
  grid-template-columns:repeat(2,1fr);gap:12px}
.ref li{border:1px solid var(--l);border-radius:10px;padding:13px 15px;background:#fafbfa}
.ref b{display:block;color:var(--e);font-size:14.5px;margin:0 0 4px}
.ref span{font-size:13.5px;color:var(--tx)}

.mar{display:flex;flex-wrap:wrap;gap:7px;margin:0;padding:0;list-style:none}
.mar li{font-size:13.5px;padding:5px 12px;border-radius:99px;background:#f2f5f3;
  border:1px solid var(--l);color:var(--tx)}

.note{background:var(--c);border:1px solid var(--l);border-left:4px solid var(--ac);
  border-radius:0 10px 10px 0;padding:15px 18px;margin:24px 0 0;font-size:14.5px;color:var(--tx)}
.note b{display:block;color:var(--e);margin-bottom:4px}
.avert{background:#fdf8ec;border:1px solid #e8d9b0;border-left:4px solid #8a6410;
  border-radius:0 10px 10px 0;padding:15px 18px;margin:14px 0 0;font-size:14px;color:#54400f}
.avert b{display:block;margin-bottom:4px}

footer{border-top:1px solid var(--l);background:var(--c);padding:22px 0 44px;
  color:var(--mu);font-size:13.5px}

@media (max-width:980px){
  .filtres{grid-template-columns:1fr 1fr}
  .liste{grid-template-columns:1fr}
  .ref{grid-template-columns:1fr}
}
/* Quatre liens plus le selecteur de langue ne tiennent pas sur une ligne de
   390 px : la barre debordait de 16 px a droite. Le menu passe sur sa propre
   ligne, TOUJOURS cale a droite — sinon le selecteur de langue quitte la
   colonne et le test d'alignement le voit. */
@media (max-width:760px){
  .tbar{gap:8px}
  .tbar nav{margin-left:0;width:100%;justify-content:flex-end;
    flex-wrap:wrap;gap:6px 14px;font-size:13.5px}
}
@media (max-width:560px){
  .filtres{grid-template-columns:1fr}
  .kpi{gap:10px 22px}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

JS = """
const $ = s => document.querySelector(s);

/* Sans les accents : « foresterie » doit trouver « Foresterie », et surtout
   « pate a dissoudre » doit trouver « pâte à dissoudre ». Personne ne tape les
   accents dans un champ de recherche. */
const plat = s => (s || '').toLowerCase()
  .normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');

function filtrer(){
  const fam = $('#f-fam').value, app = $('#f-app').value,
        niv = $('#f-niv').value, q = plat($('#f-q').value.trim());
  let n = 0;
  document.querySelectorAll('.o').forEach(el => {
    const d = el.dataset;
    let ok = true;
    if (fam && d.fam !== fam) ok = false;
    if (ok && niv && d.niv !== niv) ok = false;
    /* Une categorie porte PLUSIEURS applications : appartenance, pas egalite,
       avec des espaces autour pour ne pas trouver « exterieur » dans un autre
       code qui le contiendrait. */
    if (ok && app && !(' ' + d.app + ' ').includes(' ' + app + ' ')) ok = false;
    if (ok && q && !plat(d.rech).includes(q)) ok = false;
    el.hidden = !ok;
    if (ok) n++;
  });
  const c = $('#compte');
  c.textContent = n === 0 ? '__CPT0__'
    : n === 1 ? '__CPT1__' : n + ' __CPTN__';
  $('#vide').hidden = n !== 0;
}

['#f-fam', '#f-app', '#f-niv'].forEach(s => $(s).addEventListener('change', filtrer));
$('#f-q').addEventListener('input', filtrer);
$('#raz').addEventListener('click', () => {
  $('#f-fam').value = ''; $('#f-app').value = '';
  $('#f-niv').value = ''; $('#f-q').value = '';
  filtrer();
});
filtrer();
"""


def e(s):
    return html.escape(str(s), quote=True)


def options(paires, vide):
    o = ['<option value="">%s</option>' % e(vide)]
    for code, nom in paires:
        o.append('<option value="%s">%s</option>' % (e(code), e(nom)))
    return ''.join(o)


def carte(cat):
    fam, niv, nom, apps, desc, champs = cat
    lfam = dict(D.FAMILLES)
    lapp = dict(D.APPLICATIONS)
    lniv = dict(D.NIVEAUX)
    lch = dict(D.CHAMPS)

    tags = ''.join('<span>%s</span>' % e(T(lapp[a])) for a in apps)
    liste = ''.join('<li>%s</li>' % e(T(lch[k])) for k in champs)
    rech = ' '.join([T(nom), T(lfam[fam]), T(lniv[niv]), T(desc)]
                    + [T(lapp[a]) for a in apps] + [T(lch[k]) for k in champs])

    return (
      '<article class="o" data-fam="%s" data-niv="%s" data-app="%s" data-rech="%s">'
      '<p class="ou"><span class="nv nv-%s">%s</span>'
      '<span class="fam">%s</span></p>'
      '<h3>%s</h3>'
      '<p class="d">%s</p>'
      '<p class="tags">%s</p>'
      '<div class="car"><b>%s</b><ul>%s</ul></div>'
      '</article>'
      % (e(fam), e(niv), e(' '.join(apps)), e(rech),
         e(niv), e(T(lniv[niv])), e(T(lfam[fam])), e(T(nom)), e(T(desc)),
         tags, e(C('champs')), liste))


def ports():
    # Le NOM du port ne se traduit pas : « Trois-Rivières » s'appelle
    # Trois-Rivieres en anglais aussi. La province et la facade, si.
    lignes = ''.join(
        '<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (e(a), e(T(b)), e(T(c)))
        for a, b, c in D.PORTS)
    return ('<div class="tscroll"><table class="ports">'
            '<caption>%s</caption>'
            '<thead><tr><th>%s</th><th>%s</th>'
            '<th>%s</th></tr></thead><tbody>%s</tbody></table></div>'
            % (e(C('cap_ports')), e(C('th_port')), e(C('th_prov')),
               e(C('th_fac')), lignes))


def page():
    css = (CSS.replace('__BG__', D.FOND).replace('__C__', D.CARTE)
              .replace('__L__', D.LIGNE).replace('__E__', D.ENCRE)
              .replace('__TX__', D.TEXTE).replace('__MU__', D.MUET)
              .replace('__AC__', D.ACCENT).replace('__ACD__', D.ACCENT_D))

    js = (JS.replace('__CPT0__', C('cpt_0'))
            .replace('__CPT1__', C('cpt_1')).replace('__CPTN__', C('cpt')))

    cartes = '\n'.join(carte(c) for c in D.CATEGORIES)
    refs = ''.join('<li><b>%s</b><span>%s</span></li>' % (e(T(a)), e(T(b)))
                   for a, b in D.REFERENTIELS)
    mar = ''.join('<li>%s</li>' % e(T(m)) for m in D.MARCHES)

    # Le selecteur de langue. La page francaise est a la racine, l'anglaise
    # dans en/ : les chemins relatifs different donc selon la langue.
    if LANG == 'en':
        sel = ('<a class="lg" href="../">FR</a>'
               '<span class="lg lg-on">EN</span>')
        alt = ('<link rel="alternate" hreflang="fr" href="../">'
               '<link rel="alternate" hreflang="en" href="./">')
    else:
        sel = ('<span class="lg lg-on">FR</span>'
               '<a class="lg" href="en/">EN</a>')
        alt = ('<link rel="alternate" hreflang="fr" href="./">'
               '<link rel="alternate" hreflang="en" href="en/">')

    # Tous DERIVES. Aucun nombre ecrit a la main dans le HTML.
    n_cat, n_fam = len(D.CATEGORIES), len(D.FAMILLES)
    n_app, n_ch = len(D.APPLICATIONS), len(D.CHAMPS)
    n_ports = len(D.PORTS)

    return """<!doctype html>
<html lang="%(lang)s"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(m)s — %(t)s</title>
<meta name="description" content="%(meta)s">
<meta name="robots" content="noindex,nofollow">
%(alt)s
<style>%(css)s</style>
</head><body>

<div class="demo">%(demo)s &mdash; <b>%(m)s</b> %(demo2)s</div>

<header class="top"><div class="wrap tbar">
  <span class="logo">%(m)s</span>
  <nav>
    <a href="#catalogue">%(nav1)s</a>
    <a href="#ports">%(nav2)s</a>
    <a href="#referentiels">%(nav3)s</a>
    <a href="#marches">%(nav4)s</a>
    <span class="lgs">%(sel)s</span>
  </nav>
</div></header>

<section class="hero"><div class="wrap">
  <h1>%(h1)s</h1>
  <p>%(chapo)s</p>
  <div class="kpi">
    <div><b>%(n)d</b><span>%(k1)s</span></div>
    <div><b>%(nf)d</b><span>%(k2)s</span></div>
    <div><b>%(na)d</b><span>%(k3)s</span></div>
    <div><b>%(nc)d</b><span>%(k4)s</span></div>
    <div><b>%(np)d</b><span>%(k5)s</span></div>
  </div>
</div></section>

<main class="wrap">

  <div id="catalogue"></div>

  <div class="filtres">
    <div class="f"><label for="f-fam">%(lfam)s</label>
      <select id="f-fam">%(ofam)s</select></div>
    <div class="f"><label for="f-app">%(lapp)s</label>
      <select id="f-app">%(oapp)s</select></div>
    <div class="f"><label for="f-niv">%(lniv)s</label>
      <select id="f-niv">%(oniv)s</select></div>
    <div class="f"><label for="f-q">%(lq)s</label>
      <input id="f-q" type="search" placeholder="%(phq)s"></div>
  </div>

  <div class="barre">
    <span class="compte" id="compte">%(n)d %(cptn)s</span>
    <button class="raz" id="raz" type="button">%(raz)s</button>
  </div>

  <div class="liste">
%(cartes)s
    <p class="vide" id="vide" hidden>%(vide)s</p>
  </div>

  <section class="bloc" id="ports"><h2>%(hports)s</h2>
  <p>%(pports)s</p>
  %(ports)s</section>

  <section class="bloc" id="referentiels"><h2>%(href)s</h2>
  <p>%(pref)s</p>
  <ul class="ref">%(refs)s</ul></section>

  <section class="bloc" id="marches"><h2>%(hmar)s</h2>
  <p>%(pmar)s</p>
  <ul class="mar">%(mar)s</ul></section>

  <div class="note" id="methode"><b>%(hnote)s</b>
  %(note)s</div>

  <div class="avert"><b>%(havert)s</b>
  %(avert)s</div>

</main>

<footer><div class="wrap">%(m)s &mdash; %(pied)s</div></footer>

<script>%(js)s</script>
</body></html>""" % {
        'lang': LANG, 'alt': alt, 'sel': sel,
        'm': e(T(D.MARQUE)), 't': e(T(D.TITRE)), 'css': css, 'js': js,
        'meta': e(C('meta')), 'demo': e(C('demo')), 'demo2': e(C('demo_suite')),
        'nav1': e(C('nav_cat')), 'nav2': e(C('nav_ports')),
        'nav3': e(C('nav_ref')), 'nav4': e(C('nav_mar')),
        'h1': e(C('h1')), 'chapo': e(C('chapo')),
        'k1': e(C('kpi_cat')), 'k2': e(C('kpi_fam')), 'k3': e(C('kpi_app')),
        'k4': e(C('kpi_ch')), 'k5': e(C('kpi_ports')),
        'lfam': e(C('l_fam')), 'lapp': e(C('l_app')), 'lniv': e(C('l_niv')),
        'lq': e(C('l_q')), 'phq': e(C('ph_q')), 'raz': e(C('raz')),
        'cptn': e(C('cpt')), 'vide': e(C('vide')),
        'hports': e(C('h_ports')), 'pports': e(C('p_ports')),
        'href': e(C('h_ref')), 'pref': e(C('p_ref')),
        'hmar': e(C('h_mar')), 'pmar': e(C('p_mar')),
        'hnote': e(C('h_note')), 'havert': e(C('h_avert')),
        'pied': e(C('pied')),
        'n': n_cat, 'nf': n_fam, 'na': n_app, 'nc': n_ch, 'np': n_ports,
        'ofam': options([(c, T(n)) for c, n in D.FAMILLES], C('o_fam')),
        'oapp': options([(c, T(n)) for c, n in D.APPLICATIONS], C('o_app')),
        'oniv': options([(c, T(n)) for c, n in D.NIVEAUX], C('o_niv')),
        'cartes': cartes, 'ports': ports(), 'refs': refs, 'mar': mar,
        'note': e(T(D.NOTE)), 'avert': e(T(D.AVERTISSEMENT)),
    }


if __name__ == '__main__':
    verifier()
    with open(SORTIE, 'w', encoding='utf-8') as f:
        f.write(page())
    par_niv = {}
    for c in D.CATEGORIES:
        par_niv[c[1]] = par_niv.get(c[1], 0) + 1
    print('%d categories (%s), %d familles, %d applications, %d champs, %d ports -> %s'
          % (len(D.CATEGORIES),
             ', '.join('%s %d' % (k, v) for k, v in par_niv.items()),
             len(D.FAMILLES), len(D.APPLICATIONS), len(D.CHAMPS),
             len(D.PORTS), SORTIE))
